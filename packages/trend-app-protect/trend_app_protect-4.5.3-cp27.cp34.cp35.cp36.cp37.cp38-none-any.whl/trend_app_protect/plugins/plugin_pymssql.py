from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from trend_app_protect.plugins.dbapi2_helper import wrap_connect


# Name plugin so it can be enabled and disabled.
NAME = "sqli_pymssql"
HOOKS_CALLED = ["sql_execute"]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks to the pymssql library.
    """
    try:
        import pymssql
    except ImportError:
        return None

    meta = {
        "version": pymssql.__version__
    }

    def mogrify(_connection, _cursor, sql, params):
        return pymssql._mssql.substitute_params(sql, params)

    # wrap 'connect' function
    wrapped_connect = wrap_connect(run_hook, get_agent_func, pymssql.connect,
                                   "mssql", mogrify)

    # replace dbapi2 reference to connect
    pymssql.connect = wrapped_connect

    return meta
