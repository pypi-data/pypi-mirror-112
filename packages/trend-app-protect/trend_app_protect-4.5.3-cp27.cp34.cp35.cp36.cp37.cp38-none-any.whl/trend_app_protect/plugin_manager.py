from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import trend_app_protect.plugins.plugin_django
import trend_app_protect.plugins.plugin_fileio
import trend_app_protect.plugins.plugin_flask
import trend_app_protect.plugins.plugin_mysqldb
import trend_app_protect.plugins.plugin_psycopg2
import trend_app_protect.plugins.plugin_pymssql
import trend_app_protect.plugins.plugin_pymysql
import trend_app_protect.plugins.plugin_pyramid
import trend_app_protect.plugins.plugin_pysqlite2
import trend_app_protect.plugins.plugin_shell
import trend_app_protect.plugins.plugin_sqlite3
import trend_app_protect.plugins.plugin_tornado
import trend_app_protect.plugins.plugin_werkzeug
from trend_app_protect.deps.libagent import Table
from trend_app_protect.logger import log
from trend_app_protect.plugins import DISABLED, FAILED, LOADED, PENDING


class PluginManager(object):
    """Manages all plugins."""
    def __init__(self, agent):
        self.patched = False
        self.agent = agent

    def is_plugin_enabled(self, plugin):
        return self.agent.is_plugin_enabled(plugin)

    @property
    def debug_mode(self):
        return self.agent.debug_mode

    def timer(self, report_name=None, exclude_from=None):
        return self.agent.timer(report_name, exclude_from)

    def set_plugin_status(self, name, status=None, meta=None):
        self.agent.plugin_status(name, status, meta)

    def patch(self):
        """Actually run all the plugins to monkeypatch the code."""
        if self.patched:
            return
        self.patched = True

        # The order here is significant.
        # Patch low-level calls first
        self.register(trend_app_protect.plugins.plugin_fileio)
        self.register(trend_app_protect.plugins.plugin_shell)
        # Patch database drivers next since they are used by frameworks.
        self.register(trend_app_protect.plugins.plugin_sqlite3)
        self.register(trend_app_protect.plugins.plugin_pysqlite2)
        self.register(trend_app_protect.plugins.plugin_mysqldb)
        self.register(trend_app_protect.plugins.plugin_psycopg2)
        self.register(trend_app_protect.plugins.plugin_pymssql)
        self.register(trend_app_protect.plugins.plugin_pymysql)
        # Patch web frameworks next.
        self.register(trend_app_protect.plugins.plugin_django)
        self.register(trend_app_protect.plugins.plugin_flask)
        self.register(trend_app_protect.plugins.plugin_tornado)
        self.register(trend_app_protect.plugins.plugin_werkzeug)
        self.register(trend_app_protect.plugins.plugin_pyramid)

    def register(self, plugin_module):
        """
        Call the module to do the monkeypatching and give it a `run_hook`
        function to be used by the patched methods.
        """
        plugin_module_name = plugin_module.__name__
        meta = {
            "hooks": plugin_module.HOOKS_CALLED
        }

        # Only add plugins that are currently enabled.
        if not self.is_plugin_enabled(plugin_module.NAME):
            self.set_plugin_status(plugin_module.NAME, DISABLED, meta)
            return

        def run_hook(hook, meta):
            """
            Closure to add the name to the run_hook call.
            """
            return self._run_hook(plugin_module_name, hook, meta)

        # For backward compat in plugin code
        def get_agent(create_if_required=None):
            return self.agent

        # Actually do the monkeypatching
        try:
            # For hooks that don't immediately hook everything provide
            # a callback for them to update the status when they
            # consider themselves loaded.
            if getattr(plugin_module, "LATE_HOOK", False):
                self.set_plugin_status(plugin_module.NAME, PENDING, meta)
                # The plugin might set a status while running, so we set
                # pending first, then simply update the meta afterwards.
                meta.update(
                    plugin_module.add_hooks(run_hook,
                                            self.set_plugin_status,
                                            get_agent_func=get_agent,
                                            timer=self.timer) or {})
                self.set_plugin_status(plugin_module.NAME, meta=meta)
            else:
                meta.update(
                    plugin_module.add_hooks(run_hook,
                                            get_agent_func=get_agent,
                                            timer=self.timer) or {})
                if "version" in meta:
                    self.set_plugin_status(plugin_module.NAME, LOADED, meta)
        except:  # noqa: E722 # bare except
            if self.debug_mode:
                raise
            self.set_plugin_status(plugin_module.NAME, FAILED, meta)

    def _run_hook(self, plugin_name, hook, meta):
        """
        Receives all hook calls from the monkeypatched code.

        This function also enforces the guarantee that the `run_hook` function
        passed to plugins will always return a dict or table.
        """
        result = self.agent.run_hook(plugin_name, hook, meta)
        if not isinstance(result, dict) and not isinstance(result, Table):
            log.warning("Code for hook `%(hook)s` returned non-dict result.", {
                "hook": hook,
            })
            return {}
        return result
