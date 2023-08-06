from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from trend_app_protect.plugins.dbapi2_helper import wrap_connect


# Name plugin so it can be enabled and disabled.
NAME = "sqli_sqlite2"
HOOKS_CALLED = ["sql_execute"]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks to the pysqlite2 library.
    """
    try:
        import pysqlite2.dbapi2
    except ImportError:
        return None

    meta = {
        "version": pysqlite2.dbapi2.version,
        "sqlite_version": pysqlite2.dbapi2.sqlite_version,
    }

    def mogrify(_connection, cursor, sql, params):
        # sqlite3 doesn't contain a mogrify, but by default it uses
        # the qmark paramsytle, which at least is valid SQL
        if not cursor:
            return sql

        # Django wraps the cursor in a SQLiteCursorWrapper that uses
        # 'format' instead. At least it contains a convert
        klass = (str(cursor.__class__.__module__) + "."
                 + str(cursor.__class__.__name__))
        if klass == 'django.db.backends.sqlite3.base.SQLiteCursorWrapper':
            try:
                return cursor.convert_query(sql)
            except Exception:
                pass

        return sql

    # wrap 'pysqlite2.dbapi2.connect' function
    wrapped_connect = wrap_connect(run_hook, get_agent_func,
                                   pysqlite2.dbapi2.connect,
                                   "sqlite3", mogrify)

    # replace dbapi2 reference to connect
    pysqlite2.dbapi2.connect = wrapped_connect

    return meta
