from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


from traceback import format_exc

from trend_app_protect.logger import log
from trend_app_protect.patcher import monkeypatch
from trend_app_protect.plugins.dbapi2_helper import (
    ConnectionWrapper,
    CursorWrapper,
    wrap_connect,
)

# Name plugin so it can be enabled and disabled.
NAME = "sqli_psycopg2"
HOOKS_CALLED = ["sql_execute"]


def hook_json(timer):
    import psycopg2._json

    def call_unwraped(orig, args, kwargs):
        conn_or_curs = None
        try:
            conn_or_curs = args[0]
        except IndexError:
            pass
        else:
            args = args[1:]

        try:
            conn_or_curs = kwargs['conn_or_curs']
        except KeyError:
            pass
        else:
            del kwargs['conn_or_curs']

        while isinstance(conn_or_curs, (ConnectionWrapper, CursorWrapper)):
            if isinstance(conn_or_curs, ConnectionWrapper):
                conn_or_curs = conn_or_curs._conn
            elif isinstance(conn_or_curs, CursorWrapper):
                conn_or_curs = conn_or_curs._cursor

        return orig(conn_or_curs, *args, **kwargs)

    if psycopg2._json.register_json:
        @monkeypatch(psycopg2._json, "register_json", timer=timer,
                     report_name="plugin.psycopg2.register_json")
        def _register_json(orig, *args, **kwargs):
            call_unwraped(orig, args, kwargs)

    if psycopg2._json.register_default_json:
        @monkeypatch(psycopg2._json, "register_default_json", timer=timer,
                     report_name="plugin.psycopg2.register_default_json")
        def _register_default_json(orig, *args, **kwargs):
            call_unwraped(orig, args, kwargs)

    if psycopg2._json.register_default_jsonb:
        @monkeypatch(psycopg2._json, "register_default_jsonb", timer=timer,
                     report_name="plugin.psycopg2.register_default_jsonb")
        def _register_default_jsonb(orig, *args, **kwargs):
            call_unwraped(orig, args, kwargs)


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks to psycopg2.
    """
    try:
        import psycopg2
    except ImportError:
        return None

    meta = {
        "version": psycopg2.__version__,
        "apilevel": psycopg2.apilevel,
        "threadsafety": psycopg2.threadsafety,
        "paramstyle": psycopg2.paramstyle,
    }

    def mogrify(_connection, cursor, sql, params):
        # psycopg2 supports db calls only on the cursor
        try:
            return cursor.mogrify(sql, params)
        except Exception:
            log.debug("psycopg2.mogrify unable to mogrify: %s", format_exc())
            return sql

    # Wrap original connect function.
    wrapped_connect = wrap_connect(run_hook, get_agent_func, psycopg2.connect,
                                   "postgres", mogrify)

    # replace all references to connect
    psycopg2.connect = wrapped_connect

    # Psycopg2 has additional extensions. Some extensions take a connection as
    # a parameter. This connection parameter must be a real psycopg2
    # connection, not our wrapper. Here, we hook those functions to unwrap.
    import psycopg2.extensions

    orig_register_type = psycopg2.extensions.register_type

    def register_type_wrapper(type_class, conn=None):
        while isinstance(conn, ConnectionWrapper):
            # If we're passed one of our wrappers, unwrap it
            conn = conn._conn
        return orig_register_type(type_class, conn)

    psycopg2.extensions.register_type = register_type_wrapper

    # Hook json type registering, it needs a true connection or cursor
    try:
        import psycopg2._json
    except ImportError:
        pass
    else:
        hook_json(timer)

    return meta
