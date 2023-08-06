from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from trend_app_protect.context import get_context
from trend_app_protect.patcher import monkeypatch


# Name plugin so it can be enabled and disabled.
NAME = "sqli_mysqldb"
HOOKS_CALLED = ["sql_execute"]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks to the MySQLdb.
    """
    try:
        import MySQLdb.cursors
    except ImportError:
        return None

    # The `pymysql` driver can emulate MySQLdb. If we detect it, don't patch
    # it again here
    if hasattr(MySQLdb, "install_as_MySQLdb"):
        return None

    meta = {
        "version": MySQLdb.__version__,
        "version_info": ".".join(map(str, MySQLdb.version_info)),
        "client_version": MySQLdb.get_client_info(),
    }

    if hasattr(MySQLdb.cursors.BaseCursor, "_do_query"):
        target = "_do_query"
    else:
        # mysqlclient >= 1.3.14 renames this to just `_query`.
        # Check `_do_query` first though because `_query` exists
        # in older versions.
        target = "_query"

    @monkeypatch(MySQLdb.cursors.BaseCursor, target, timer=timer,
                 report_name="plugin.mysqldb.cursors.BaseCursor.query")
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
