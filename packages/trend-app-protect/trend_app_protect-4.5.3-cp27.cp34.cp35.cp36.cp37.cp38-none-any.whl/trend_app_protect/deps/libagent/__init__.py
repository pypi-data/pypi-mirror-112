from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import platform
import sys
from os import environ, path

from cffi import FFI

ffi = FFI()
lib = None

# Python 2/3 compatibility
#
# These match six, but are included here so that it can be included
# without dependencies.
_PY3 = sys.version_info[0] == 3

if _PY3:
    _text_type = str
    _binary_type = bytes
else:
    _text_type = unicode  # noqa: F821 - Exists in PY2
    _binary_type = str


def _ensure_binary(s, encoding='utf-8', errors='strict'):
    if isinstance(s, _text_type):
        return s.encode(encoding, errors)
    elif isinstance(s, _binary_type):
        return s
    else:
        raise TypeError("not expecting type '%s'" % type(s))


# Some macros in the libagent include files can't be parsed by cffi. We've
# placed markers around those sections to ignore.
INCLUDE_IGNORE_MARKER_START = "/** (python ignore start) **/\n"
INCLUDE_IGNORE_MARKER_END = "/** (python ignore end) **/\n"


def load_lib(lib_path=None, include_path=None):
    """Load the dynamic libagent library for the current platform"""
    global lib

    if lib is not None:
        # Can only be loaded once
        return

    if lib_path is None:
        lib_path = environ['LIBAGENT_PATH']
    if include_path is None:
        include_path = lib_path

    platform = str(sys.platform).lower()

    if 'linux' in platform:
        if path.isfile('/etc/alpine-release'):
            lib_filename = "libagent-x86_64-Linux-musl.so"
        else:
            lib_filename = "libagent-x86_64-Linux-gnu.so"
    elif 'darwin' in platform:
        lib_filename = "libagent-x86_64-Darwin.dylib"
    elif 'win32' in platform:
        lib_filename = "libagent-x86_64-Windows.dll"
    else:
        raise AgentException("Platform {0} not supported by agent",
                             sys.platform)

    lib = ffi.dlopen(path.join(lib_path, lib_filename))

    raw_open = open
    if hasattr(raw_open, "_trend_app_protect_original"):
        raw_open = raw_open._trend_app_protect_original

    with raw_open(path.join(include_path, "agent.h")) as f:
        include = []
        ignore = False
        for line in f.readlines():
            if line == INCLUDE_IGNORE_MARKER_START:
                ignore = True
            elif line == INCLUDE_IGNORE_MARKER_END:
                ignore = False
            if not ignore:
                include.append(line)
        ffi.cdef("".join(include))


class AgentException(Exception):
    """Exception thrown when an unexpected agent error happens."""

    pass


class LogLevel:
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5


class Type:
    NIL = 0
    BOOLEAN = 1
    NUMBER = 2
    STRING = 3
    TABLE = 4
    FUNCTION = 5


class Agent(object):
    def __init__(self, version, config=None, deployment_type=None):
        """
        Create a new agent. Several agents can co-exist, each with their own
        config and transactions.

        `version`:
            Provides the `agent_version` to the backend, and must be the
            version of the host language agent, NOT the version of libagent.
        `config`:
            Must be a dict holding the configuration of the agent.
            The values must strings. They will be parsed to the proper type
            internally (see libagent/src/config/parse.rs).
            See libagent/src/config/defaults.rs for the full list of
            configurations and their default values.

        If the agent is disabled (config.agent_enabled = false) a mock agent is
        returned. A mock agent will silently ignore all calls bellow but
        libagent_log*. However, libagent_start_transaction will return NULL.
        You are responsible for handling this special case.

        If the operation fails, the error is logged to config.log_file, and a
        mock agent is returned.
        """
        if config is None:
            config = {}
        config_ptr = lib.libagent_new_config()
        for k, v in config.items():
            if v is None:
                v = ""
            else:
                v = str(v)
            lib.libagent_set_config(config_ptr, _ensure_binary(k),
                                    _ensure_binary(v))

        self._ptr = lib.libagent_new_agent(
            b"agent-python", _ensure_binary(version), config_ptr)

        self.report("language", "Python", "%d.%d.%d" % sys.version_info[:3])
        self.report("runtime", platform.python_implementation(),
                    "%d.%d.%d" % sys.version_info[:3])

        if not deployment_type:
            deployment_type = "python-wheel-%s" % version

        self.report("agent_deployment_type", deployment_type, None)

    def __del__(self):
        lib.libagent_close_agent(self._ptr)

    @property
    def enabled(self):
        return bool(lib.libagent_is_enabled(self._ptr))

    @property
    def version(self):
        return _to_native_string(_dropped_string(lib.libagent_version()))

    @property
    def debug_mode(self):
        return bool(lib.libagent_is_debug_mode(self._ptr))

    def is_log_enabled(self, level):
        return bool(lib.libagent_is_log_enabled(self._ptr, level))

    def is_plugin_enabled(self, plugin):
        return bool(
            lib.libagent_is_plugin_enabled(self._ptr, _ensure_binary(plugin)))

    def log(self, level, target, message, file=None, line=0):
        lib.libagent_log(self._ptr,
                         _ensure_binary(target),
                         _ensure_nullable_binary(file),
                         line,
                         level,
                         _ensure_binary(message))

    def send_message(self, type, payload, version=None, mimetype=None,
                     encoding=None):
        if not isinstance(payload, _binary_type):
            raise TypeError("payload must be bytes")
        ret = lib.libagent_send_message(self._ptr,
                                        _ensure_binary(type),
                                        _ensure_nullable_binary(version),
                                        _ensure_nullable_binary(mimetype),
                                        _ensure_nullable_binary(encoding),
                                        payload,
                                        len(payload))
        if not ret:
            raise AgentException("Failed to send message. Check logs.")

    def report(self, report_type, name, version=None):
        """
        Schedule a bit of environment information to be reported to the
        back-end.

        `type`: One of "runtime" or "language".
        `name`: is required.
        `version`: can be None.
        """
        lib.libagent_report(
            self._ptr,
            _ensure_binary(report_type),
            _ensure_binary(name),
            _ensure_nullable_binary(version))

    def report_plugin(self, name, hooks=None, status=None, version=None):
        """
        Schedule a plugin status to be reported to the back-end.

        `name`: is required and must be unique to report a new plugin or else,
        it will perform an update on the information from the previous call.
        `hooks`: is a comma-separated list or hooks provided by the plugin,
        or None to leave unchanged from previous call.
        `status`: is one of: "pending", "loaded", "failed", "disabled",
        or None to leave unchanged from previous call.
        `version`: can be None to leave unchanged from previous call.

        Typically, on startup, you'd register each plugins with:

            agent.report_plugin("my_plugin", "hook1, hook2", "pending", None);

        Then, when the plugin is loaded:

            agent.report_plugin("my_plugin", None, "loaded", "1.0.0");

        """
        if isinstance(hooks, (list, tuple, set)):
            hooks = ",".join(hooks)

        lib.libagent_report_plugin(
            self._ptr,
            _ensure_binary(name),
            _ensure_nullable_binary(hooks),
            _ensure_nullable_binary(status),
            _ensure_nullable_binary(version))

    def start_transaction(self, transaction_id=None):
        ptr = lib.libagent_start_transaction(
            self._ptr, _ensure_nullable_binary(transaction_id))

        if ptr == ffi.NULL:
            raise AgentException("Can't start a transaction, "
                                 "agent is disabled")

        return Transaction(self, ptr)


class Transaction(object):
    """
    Represents a transaction in the agent, created from
    `agent.start_transaction(...)`. It holds all the information
    collected by the Lua hook handlers and can be sent to the back-end.

    WARNING: A transaction is NOT thread-safe. It should be stored in
    a thread-local variable and should NOT be shared between threads.
    """

    def __init__(self, agent, ptr):
        self._agent = agent
        self._ptr = ptr

    def __del__(self):
        self.finish()

    def finish(self):
        if self._ptr is None:
            return
        lib.libagent_finish_transaction(self._ptr)
        self._ptr = None

    def _check_finished(self):
        if self._ptr is None:
            raise AgentException("transaction has been finished")

    @property
    def uuid(self):
        self._check_finished()
        return _to_native_string(_dropped_string(
            lib.libagent_transaction_uuid(self._ptr)))

    def run_hook(self, plugin, hook, meta=None):
        """
        Run the specified hook (from plugin). meta must be a dict or Table.

        On success, a Table is returned. Otherwise, an empty dict is returned
        and the error is logged.
        """
        self._check_finished()

        if meta is None:
            meta_ptr = ffi.NULL
        elif isinstance(meta, Table):
            meta_ptr = meta._ptr
        elif isinstance(meta, dict):
            meta = self.new_table(meta)
            meta_ptr = meta._ptr
        else:
            raise TypeError("meta must be None, a dict or libagent.Table")

        result = lib.libagent_run_hook(self._ptr, _ensure_binary(plugin),
                                       _ensure_binary(hook), meta_ptr)

        if result == ffi.NULL:
            return {}
        return Table(self, result)

    def has_hook(self, hook):
        self._check_finished()
        return bool(lib.libagent_has_hook(self._ptr, _ensure_binary(hook)))

    def hook_ran(self, hook):
        self._check_finished()
        return bool(lib.libagent_hook_ran(self._ptr, _ensure_binary(hook)))

    def new_array(self, size=0):
        self._check_finished()
        ptr = _not_null(lib.libagent_create_array(self._ptr, size))
        return Table(self, ptr)

    def new_map(self, size=0):
        self._check_finished()
        ptr = _not_null(lib.libagent_create_map(self._ptr, size))
        return Table(self, ptr)

    def new_table(self, value):
        """Converts a Python collection to a Lua Table."""
        self._check_finished()
        if isinstance(value, dict):
            table = self.new_map(len(value))
            for k, v in value.items():
                table[k] = v
        elif isinstance(value, (list, tuple, set)):
            table = self.new_array(len(value))
            for i, v in enumerate(value):
                table[i] = v
        else:
            raise TypeError("Can't convert %s to a table" % type(value))
        return table

    def timer(self, name, report_type="plugin"):
        """
        Returns a Timer to be used in a `with` block. The execution of
        the block will be timed and reported to the backend.

        Only plugin hook code should be timed. Hook execution is
        already timed internally.

        The timings will be reported to the channel after the
        transaction finishes, and will be logged if the log_timings
        config is set.


            with transaction.timer("my-timer-name") as timer:
                ...
                timer.stop() # Pause the timer
                ...
                timer.start() # Resume the timer
                ...
        """
        self._check_finished()
        return Timer(self, name, report_type)


class Timer(object):
    def __init__(self, transaction, name, report_type):
        self._transaction = transaction
        self.name = name
        self.report_type = report_type

    def __enter__(self):
        self._ptr = lib.libagent_new_timer(
            self._transaction._ptr,
            _ensure_binary(self.report_type),
            _ensure_binary(self.name))
        return self

    def __exit__(self, type, value, traceback):
        if self._ptr is not ffi.NULL:
            lib.libagent_finish_timer(self._ptr, self._transaction._ptr)

    def start(self):
        if self._ptr is not ffi.NULL:
            lib.libagent_start_timer(self._ptr)

    def stop(self):
        if self._ptr is not ffi.NULL:
            lib.libagent_stop_timer(self._ptr)


class Table(object):
    """
    A table can represent an array or a map.
    They are used for passing arguments and as the return value when running
    hooks (see `run_hook`).

    They are internally represented as a Lua table.
    """

    def __init__(self, transaction, ptr):
        self._transaction = transaction
        self._ptr = ptr

    def __del__(self):
        lib.libagent_drop_table(self._ptr)

    def __len__(self):
        return lib.libagent_len(self._ptr)

    def __contains__(self, item):
        return self[item] is not None

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._get_index(key)
        else:
            return self.get(key)

    def lua_type(self, key):
        if isinstance(key, int):
            libagent_type = lib.libagent_geti_type(self._ptr, key)
        else:
            libagent_type = lib.libagent_get_type(
                self._ptr, _ensure_binary(key))
        if libagent_type == Type.NIL:
            return "nil"
        if libagent_type == Type.BOOLEAN:
            return "boolean"
        if libagent_type == Type.NUMBER:
            return "number"
        if libagent_type == Type.STRING:
            return "string"
        if libagent_type == Type.TABLE:
            return "table"
        raise TypeError("Unsupported type: %d" % libagent_type)

    def _get_index(self, index):
        # Adjust index to be 1-based for Lua tables
        index = index + 1

        libagent_type = lib.libagent_geti_type(self._ptr, index)
        if libagent_type == Type.NIL:
            return None
        if libagent_type == Type.BOOLEAN:
            return bool(lib.libagent_geti_boolean(self._ptr, index))
        if libagent_type == Type.NUMBER:
            return lib.libagent_geti_number(self._ptr, index)
        if libagent_type == Type.STRING:
            len_ptr = ffi.new("size_t *", 0)
            ptr = lib.libagent_geti_bytes(self._ptr, index, len_ptr)
            return _dropped_string(ptr, len_ptr[0])
        if libagent_type == Type.TABLE:
            return Table(self._transaction,
                         lib.libagent_geti_table(self._ptr, index))
        raise TypeError("Unsupported type: %d" % libagent_type)

    def get(self, key, default=None):
        key = _ensure_binary(key)

        libagent_type = lib.libagent_get_type(self._ptr, key)
        if libagent_type == Type.NIL:
            return default
        if libagent_type == Type.BOOLEAN:
            return bool(lib.libagent_get_boolean(self._ptr, key))
        if libagent_type == Type.NUMBER:
            return lib.libagent_get_number(self._ptr, key)
        if libagent_type == Type.STRING:
            len_ptr = ffi.new("size_t *", 0)
            ptr = lib.libagent_get_bytes(self._ptr, key, len_ptr)
            return _dropped_string(ptr, len_ptr[0])
        if libagent_type == Type.TABLE:
            return Table(self._transaction,
                         lib.libagent_get_table(self._ptr, key))
        raise TypeError("Unsupported type: %d" % libagent_type)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            return self._set_index(key, value)
        else:
            return self._set_key(key, value)

    def _set_index(self, index, value):
        # Adjust index to be 1-based for Lua tables
        index = index + 1

        if value is None:
            lib.libagent_seti_nil(self._ptr, index)
        elif isinstance(value, bool):
            lib.libagent_seti_boolean(self._ptr, index, value)
        elif isinstance(value, (int, float)):
            lib.libagent_seti_number(self._ptr, index, value)
        elif isinstance(value, _text_type):
            value = _ensure_binary(value)
            lib.libagent_seti_string(self._ptr, index, value, len(value))
        elif isinstance(value, _binary_type):
            lib.libagent_seti_string(self._ptr, index, value, len(value))
        elif isinstance(value, Table):
            lib.libagent_seti_table(self._ptr, index, value._ptr)
        elif isinstance(value, (dict, list, tuple, set)):
            table = self._transaction.new_table(value)
            lib.libagent_seti_table(self._ptr, index, table._ptr)
        else:
            raise TypeError("Unsupported type: %s" % type(value))

    def _set_key(self, key, value):
        key = _ensure_binary(key)

        if value is None:
            lib.libagent_set_nil(self._ptr, key)
        elif isinstance(value, bool):
            lib.libagent_set_boolean(self._ptr, key, value)
        elif isinstance(value, (int, float)):
            lib.libagent_set_number(self._ptr, key, value)
        elif isinstance(value, _text_type):
            value = _ensure_binary(value)
            lib.libagent_set_string(self._ptr, key, value, len(value))
        elif isinstance(value, _binary_type):
            lib.libagent_set_string(self._ptr, key, value, len(value))
        elif isinstance(value, Table):
            lib.libagent_set_table(self._ptr, key, value._ptr)
        elif isinstance(value, (dict, list, tuple, set)):
            table = self._transaction.new_table(value)
            lib.libagent_set_table(self._ptr, key, table._ptr)
        else:
            raise TypeError("Unsupported type: %s" % type(value))

    def __delitem__(self, key):
        self[key] = None

    def insert(self, index, value):
        raise NotImplementedError()

    def __iter__(self):
        for i in range(0, len(self)):
            yield self[i]

    def __str__(self):
        return _to_native_string(
            _dropped_string(lib.libagent_debug(self._ptr)))

    def __repr__(self):
        return "Table(%s)" % str(self)


# Utility functions

def _dropped_string(ffi_ptr, length=None):
    """
    If a function in libAgent returns a string or bytes, the caller must drop
    the string using libagent_drop_string(). This function handles the
    conversion to a python string and calling libagent_drop_string().
    """
    # Convert a char* to a Python string or bytes
    if length is None:
        pystring = ffi.string(ffi_ptr)
    else:
        # Got the length. So unpack as bytes.
        pystring = ffi.unpack(ffi_ptr, length)
    # Now drop the C string
    lib.libagent_drop_string(ffi_ptr)
    return pystring


def _ensure_nullable_binary(arg):
    """Convert None to NULL and some to binary"""
    if arg is None:
        return ffi.NULL
    else:
        return _ensure_binary(arg)


def _not_null(ret):
    """Make sure ret is not NULL"""
    if ret is ffi.NULL:
        raise AgentException("Agent returned a NULL value. Check the logs.")
    return ret


def _to_native_string(value, encoding="utf-8"):
    """Convert bytes from Lua to "Native" strings.
    In Python 3 these are 'str' and not 'bytes'.
    In Python 2 these are 'str' and not 'unicode'
    """
    assert isinstance(value, bytes), repr(value)
    return str(value.decode(encoding))
