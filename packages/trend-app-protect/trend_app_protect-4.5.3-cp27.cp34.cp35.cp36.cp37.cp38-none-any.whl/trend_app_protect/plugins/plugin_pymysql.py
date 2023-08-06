from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from trend_app_protect.context import get_context
from trend_app_protect.patcher import monkeypatch


# Name plugin so it can be enabled and disabled.
NAME = "sqli_pymysql"
HOOKS_CALLED = ["sql_execute"]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks to the PyMySQL driver.
    """
    try:
        import pymysql
    except ImportError:
        return None

    meta = {
        "version": pymysql.__version__,
    }

    method = "query"
    if pymysql.VERSION[:2] < (0, 3):
        method = "_query"

    @monkeypatch(pymysql.connections.Connection, method, timer=timer,
                 report_name="plugin.pymysql.connections.Connection.query")
    def _query(orig, self, sql, *args, **kwargs):
        stack = get_context()
        run_hook("sql_execute", {
            "stack": stack,
            "db_dialect": "mysql",
            "sql": sql,
            "params": {},
        })
        return orig(self, sql, *args, **kwargs)

    return meta
