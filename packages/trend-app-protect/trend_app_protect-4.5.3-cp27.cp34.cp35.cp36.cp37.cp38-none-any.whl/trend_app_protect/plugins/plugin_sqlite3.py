from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from trend_app_protect.plugins.dbapi2_helper import wrap_connect


# Name plugin so it can be enabled and disabled.
NAME = "sqli_sqlite3"
HOOKS_CALLED = ["sql_execute"]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks to the sqlite3 library.
    """
    try:
        # Some frameworks (notably Django) use the sqlite3.dbapi2 module
        # directly. Others use sqlite3 directly. To cover both cases we
        # have a single wrapper function which we patch onto both references.
        import sqlite3.dbapi2
    except ImportError:
        return None

    meta = {
        "version": sqlite3.dbapi2.version,
        "sqlite_version": sqlite3.dbapi2.sqlite_version,
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

    # wrap 'sqlite3.dbapi2.connect' function
    wrapped_connect = wrap_connect(run_hook, get_agent_func,
                                   sqlite3.dbapi2.connect, "sqlite3",
                                   mogrify)

    # replace dbapi2 reference to connect
    sqlite3.dbapi2.connect = wrapped_connect
    # replace sqlite3 reference to connect
    sqlite3.connect = wrapped_connect

    return meta
