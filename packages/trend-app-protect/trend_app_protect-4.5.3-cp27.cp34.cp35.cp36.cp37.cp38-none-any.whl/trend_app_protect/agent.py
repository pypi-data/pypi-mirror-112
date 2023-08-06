from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import datetime
import threading
from collections import defaultdict
from os import path

from trend_app_protect import wsgi
from trend_app_protect.config import Config
from trend_app_protect.deps import libagent
from trend_app_protect.exceptions import TrendAppProtectOverrideResponse
from trend_app_protect.logger import log
from trend_app_protect.plugin_manager import PluginManager
from trend_app_protect.util import DummyContext

from . import __version__


DEFAULT_TRANSACTION_UUID_HEADER = "x-transaction-uuid"

_ROOT = path.dirname(path.realpath(__file__))
libagent.load_lib(path.join(_ROOT, "deps", "libagent"))


def collect_libraries():
    """
    Collect information about the packages installed. This is static data that
    should not change during one run.
    """
    try:
        from pkg_resources import working_set
        libraries = [{"name": x.project_name, "version": x.version}
                     for x in working_set]
    except (ImportError, AttributeError):
        libraries = None
    return libraries


class AgentTransactionStoreContext():
    def __init__(self, store, key, value):
        try:
            self.original_value = store[key]
            self.existed = True
        except KeyError:
            self.existed = False
        self.store = store
        self.key = key

        store[key] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.existed:
            self.store[self.key] = self.original_value
        else:
            try:
                del self.store[self.key]
            except KeyError:
                log.warning(
                    "Transaction Store attempted to delete missing key %s",
                    self.key)


class Agent(object):
    """
    Manages all aspects of TrendAppProtect on a target webserver. There should
    only be a single instance of this class for each webserver process.
    """

    class ContextvarsLocal(object):
        """
        Use Python 3.7+ contextvars for storing per-transaction data.
        """
        def __init__(self):
            import contextvars

            self._transaction = contextvars.ContextVar(
                'transaction', default=None)

            self._transaction_features_enabled = contextvars.ContextVar(
                'transaction_features_enable', default=None)

            self._transaction_properties = contextvars.ContextVar(
                'transaction_properties', default=None)

        def __getattr__(self, key):
            try:
                return getattr(self, "_" + key).get()
            except LookupError:
                raise AttributeError()  # from exc when Py3

        def __setattr__(self, key, value):
            if key.startswith('_'):
                object.__setattr__(self, key, value)
            else:
                getattr(self, "_" + key).set(value)

        def __delattr__(self, key):
            getattr(self, "_" + key).set(None)

    # There should only be one of these, just like the agents:
    class ThreadLocal(object):
        """
        Use threading.local to store variables that need to be per-transaction.
        """
        def __init__(self):
            # Create thread-local storage for maintaining the active
            # transaction_uuid. This is to be used in version of Python
            # before 3.7. Using thread-local alone does not allow us to
            # support fully multi-threaded async servers because it does
            # now allow proper tracking of requests on those servers.
            self._local_data = threading.local()
            self._local_data.transaction = None
            self._local_data.transaction_features_enabled = None
            self._local_data.transaction_properties = {}

        # Proxy attributes to the tread local ones
        def __getattr__(self, key):
            return getattr(self._local, key)

        def __setattr__(self, key, value):
            if key in ['_local', '_local_data']:
                object.__setattr__(self, key, value)
            else:
                setattr(self._local, key, value)

        def __delattr__(self, key):
            # we only track one level of threadlocal, this could have a stack
            if key in ['_local', '_local_data']:
                object.__delattr__(self, key)  # should  never be called
            else:
                delattr(self._local, key)

        @property
        def _local(self):
            """Return a thread local datastore."""
            # Check for a change in the type of `treading.local`. Gevent might
            # change this if `monkey.patch_thread` is called after the agent
            # has already started.
            local_type = type(threading.local())
            if not isinstance(self._local_data, local_type):
                if self._local_data.transaction:
                    log.warning("threading.local was changed from %(old)s to "
                                "%(new)s during a transaction, returning "
                                "existing local", {
                                    "old": type(self._local_data),
                                    "new": local_type,
                                })
                else:
                    log.debug("threading.local type changed. "
                              "Was %(old)s, now %(new)s", {
                                  "old": type(self._local_data),
                                  "new": local_type,
                              })
                    self._local_data = threading.local()
                    self._local_data.transaction = None
                    self._local_data.transaction_features_enabled = None
                    self._local_data.transaction_properties = {}
            return self._local_data

    def __init__(self, config=None, plugin_manager=None, deployment_type=None):
        if config is None:
            config = Config()
        if plugin_manager is None:
            plugin_manager = PluginManager(self)

        self.sent_libraries = False

        self._config = config
        self.plugin_manager = plugin_manager

        self.local = self.ThreadLocal()

        # The name of the header to add to each response with the
        # transaction_uuid.
        self._transaction_uuid_header = self._config.get(
            "transaction_uuid_header", DEFAULT_TRANSACTION_UUID_HEADER,
            datatype=str)

        # Track the hook timings for each transaction
        self._transaction_timings = defaultdict(dict)

        self._agent = libagent.Agent(
            __version__, self._config, deployment_type)

        # Switch to the real logger now that libagent is loaded.
        log.switch(self._agent.is_log_enabled, self._agent.log)

    @property
    def enabled(self):
        """
        Check if the Agent is enabled or not.
        """
        return self._agent.enabled

    @property
    def debug_mode(self):
        return self._agent.debug_mode

    def get_transaction_uuid_header(self):
        return self._transaction_uuid_header

    def start(self):  # noqa: F811 # start reused
        """Start the agent."""
        if self.enabled:
            self.plugin_manager.patch()

    def wrap_wsgi_app(self, app):
        """
        Wrap a WSGI app with the Agent. If agent is disabled, just return
        the original app.
        """
        # Don't wrap again if we've already wrapped once.
        if isinstance(app, wsgi.WsgiWrapper):
            log.warning("The WSGI app callable has already been wrapped by "
                        "Trend Application Protection. Trend Application "
                        "Protection will operate normally, but you can "
                        "remove the explicit call to `agent.wrap_wsgi_app()`. "
                        "Please contact support for more information.")
            return app

        if self.enabled:
            # wsgi isn't a true plugin, but it's status is needed for the
            # backend.
            #
            # TODO: It might make sense for wsgi to become a plugin after the
            # py3k and libagent changes. For now hard-code the hooks/status
            self.plugin_status("wsgi", "loaded", {"hooks": wsgi.HOOKS_CALLED})
            return wsgi.WsgiWrapper(self, app, self._transaction_uuid_header)
        else:
            # If we're not enabled then there's no libagent to send
            # status updates.
            return app

    def timestamp(self):
        """
        Create a timestamp string. Append a 'Z' so it's clear that all
        timestamps are UTC.
        """
        return datetime.datetime.utcnow().isoformat() + "Z"

    def start_transaction(self):
        # Generate new ID
        if self.get_transaction() is not None:
            raise Exception(
                "New transaction starting before previous transaction "
                "(uuid=%s) complete." % self.local.transaction.uuid)

        # Create a new property store
        try:
            if self.local.transaction_properties:
                log.warning("New transaction with existing properties, "
                            "clearing")
        except AttributeError:
            pass  # No transaction_properties is expected
        self.local.transaction_properties = {}

        # Clear any existing enabled features
        self.local.transaction_features_enabled = None

        self.local.transaction = self._agent.start_transaction()

        # If this is this first transaction - call lib_loaded hook
        if not self.sent_libraries:
            self.local.transaction.run_hook(
                "agent", "lib_loaded", {"libraries": collect_libraries()})
            self.sent_libraries = True

        return self.local.transaction

    def finish_transaction(self, transaction=None):
        # If transaction_uuid is not provided, try to find it
        if transaction is None:
            transaction = self.get_transaction()
        transaction.finish()

        # Done with this transaction_uuid, clear it to help detect failures
        self.clear_transaction()

    def clear_transaction(self):
        self.local.transaction = None
        self.local.transaction_features_enabled = None
        self.local.transaction_properties = {}

    def run_hook(self, plugin, hook, meta, transaction=None):
        """
        Send the hook data into the Engine. If the Engine is not enabled,
        do nothing.
        """
        # If the Agent is not enabled, return an empty `dict` and no-op
        if not self.enabled:
            return {}

        # If transaction is not provided, try to find it
        if transaction is None:
            transaction = self.get_transaction()
        if transaction is None:
            # Hooks can use `skip_if` to avoid calling `run_hook` when
            # the feature is disabled (which includes when there's no
            # transaction), but in cases where the patch is lightweight
            # it's probably easier to just call and return here.
            log.debug("run_hook with no transaction: %s %s %s",
                      plugin, hook, meta)
            return {}

        result = transaction.run_hook(plugin, hook, meta)
        log.debug("Result from hook: %(result)r", {
            "result": result,
        })

        # Check if response should be overridden
        if result.get("override_status") or result.get("override_body"):
            raise TrendAppProtectOverrideResponse(
                int(result.get("override_status", 200)),
                [list(x) for x in result.get("override_headers", [])],
                result.get("override_body", ""),
            )

        return result

    def plugin_status(self, name, status=None, meta=None):
        """Add the status message to the environment."""
        if meta is None:
            meta = {}

        self._agent.report_plugin(name,
                                  hooks=meta.get("hooks"),
                                  status=status,
                                  version=meta.get("version"))

    def timer(self, report_name=None, exclude_from=None):
        transaction = self.get_transaction()
        if transaction:
            if not report_name:
                raise ValueError("`report_name` can't be %r" % (report_name,))
            category, name = report_name.split(".", 1)
            return transaction.timer(name, report_type=category)
        return DummyContext()

    def get_transaction(self):
        """
        Find the current transaction from thread-local storage. This is
        primarily to support gevent-based servers. We don't support fully
        threaded servers yet.
        This will require some work to make it safe for use in async code
        like tornado or twisted.
        """
        try:
            ret = self.local.transaction
            return ret
        except AttributeError:
            return None

    def get_transaction_uuid(self):
        transaction = self.get_transaction()
        return transaction.uuid if transaction else None

    def property_set(self, key, value):
        return AgentTransactionStoreContext(
            self.local.transaction_properties, key, value)

    def property_get(self, key, default=None):
        return self.local.transaction_properties.get(key, default)

    def is_plugin_enabled(self, plugin):
        return self._agent.is_plugin_enabled(plugin)

    def is_feature_enabled(self, feature_name):
        # If the agent is disabled, no features are enabled
        if not self.enabled:
            return False

        # If there's no active transaction, no features are enabled
        if self.get_transaction() is None:
            return False

        # TODO use features_enabled hook here
        return True
