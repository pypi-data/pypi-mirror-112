from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Iterator
from functools import wraps
from itertools import tee

from trend_app_protect.compat import get_iteritems, to_unicode
from trend_app_protect.context import get_context
from trend_app_protect.logger import log


def get_db_context_meta(get_agent_func):
    stack = get_context()

    return {
        "stack": stack,
    }


def wrap_connect(run_hook, get_agent_func, original_connect, dialect,
                 mogrify_func=None):
    """
    Function to wrap a normal dbapi `connect` functions.
    """
    @wraps(original_connect)
    def connect_wrapper(*args, **kwargs):
        log.debug("dbapi2.connect(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })

        # Convert some class parameters to class names.
        hook_kwargs = dict(kwargs)
        for key in ["factory", "connection_factory", "cursorclass"]:
            if key in hook_kwargs:
                hook_kwargs[key] = hook_kwargs[key].__name__

        # Remove some parameters that don't serialize
        for key in ["conv"]:
            if key in hook_kwargs:
                # Can't encode it, so just remove it for now
                del hook_kwargs[key]

        conn = original_connect(*args, **kwargs)

        return ConnectionWrapper(run_hook, get_agent_func, conn, dialect,
                                 mogrify_func)
    return connect_wrapper


class ConnectionWrapper(object):
    """
    Internal wrapper for a dbapi2 Connection object.

    Note, we're not using inheritance here. If one method uses another,
    we don't want multiple hooks. For instance, if execute() internally
    calls cursor(), we don't want to see both hooks.
    """
    def __init__(self, run_hook, get_agent_func, real_connection, dialect,
                 mogrify_func=None):
        self._run_hook = run_hook
        self._get_agent_func = get_agent_func
        self._conn = real_connection
        self._dialect = dialect
        self._mogrify_func = mogrify_func

    def __getattr__(self, name):
        """
        If we don't specifically override a method here, pass through
        to the the wrapped Connection.
        """
        # If a non-dbapi2 function is called
        if name in ["execute", "executemany"]:
            # And it is present in the real connection
            if hasattr(self._conn, name):
                # Call our wrapped version instead
                return getattr(self, "_" + name)

        return getattr(self._conn, name)

    def __setattr__(self, name, value):
        if name in ['_dialect',
                    '_run_hook',
                    '_get_agent_func',
                    '_conn',
                    '_mogrify_func']:
            object.__setattr__(self, name, value)
        else:
            setattr(self._conn, name, value)

    def __delattr__(self, item):
        if item in ['_dialect',
                    '_run_hook',
                    '_get_agent_func',
                    '_conn',
                    '_mogrify_func']:
            object.__delattr__(self, item)
        else:
            delattr(self._conn, item)

    def cursor(self, *args, **kwargs):
        log.debug("Connection.cursor(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })

        # Convert some class parameters to class names.
        hook_kwargs = dict(kwargs)
        for key in ["factory", "cursor_factory", "cursorclass"]:
            if key in hook_kwargs:
                hook_kwargs[key] = hook_kwargs[key].__name__

        new_cursor = self._conn.cursor(*args, **kwargs)
        return CursorWrapper(self, self._run_hook, self._get_agent_func,
                             new_cursor, self._dialect, self._mogrify_func)

    def _execute(self, sql, params=None):
        # This is only used by sqlite3 pysqlite2, which doesn't have mogrify
        params, params_dict = params_to_dict(params)
        log.debug("Connection._execute(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params,
        })

        meta = {
            "db_dialect": self._dialect,
            "sql": sql,
            "params": params_dict,
        }
        meta.update(get_db_context_meta(self._get_agent_func))
        self._run_hook("sql_execute", meta)

        # Some versions of psycopg2 are picky about the value of the default
        # params argument. To avoid any issues, don't pass through params=None.
        if params is None:
            return self._conn.execute(sql)
        else:
            return self._conn.execute(sql, params)

    def _executemany(self, sql, params_list):
        # This is only used by sqlite2 pysqliet, which doesn't have mogrify
        params_list, params_dicts = params_list_to_dicts(params_list)
        log.debug("Connection._executemany(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params_list,
        })

        context_meta = get_db_context_meta(self._get_agent_func)
        for params_dict in params_dicts:
            meta = {
                "db_dialect": self._dialect,
                "sql": sql,
                "params": params_dict,
            }
            meta.update(context_meta)
            self._run_hook("sql_execute", meta)

        return self._conn.executemany(sql, params_list)


class CursorWrapper(object):
    """
    Internal wrapper for a dbapi2 Cursor object.

    Note, we're not using inheritance here. If one method uses another,
    we don't want multiple hooks. For instance, if executemany()
    internally calls execute(), we don't want to see both hooks.
    """
    def __init__(self, connection_wrapper, run_hook, get_agent_func,
                 real_cursor, dialect, mogrify_func=None):
        # Cursor objects require a reference to their connection. We want that
        # reference to point to our wrapped connection.
        self.connection = connection_wrapper

        self._run_hook = run_hook
        self._get_agent_func = get_agent_func
        self._cursor = real_cursor
        self._dialect = dialect
        self._mogrify_func = mogrify_func

    def __getattr__(self, name):
        """
        If we don't specifically override a method here, pass through
        to the the wrapped Cursor.
        """
        return getattr(self._cursor, name)

    def __setattr__(self, name, value):
        if name in ['connection',
                    '_dialect',
                    '_run_hook',
                    '_get_agent_func',
                    '_cursor',
                    '_mogrify_func']:
            object.__setattr__(self, name, value)
        else:
            setattr(self._cursor, name, value)

    def __delattr__(self, item):
        if item in ['connection',
                    '_dialect',
                    '_run_hook',
                    '_get_agent_func',
                    '_cursor',
                    '_mogrify_func']:
            object.__delattr__(self, item)
        else:
            delattr(self._cursor, item)

    def __iter__(self):
        """
        Implement the cursor iteration protocol by passing to the underlying
        real cursor.
        """
        for result in self._cursor:
            yield result

    def execute(self, sql, params=None):
        if self._mogrify_func:
            conv_sql = self._mogrify_func(None, self._cursor, sql, params)
        else:
            conv_sql = sql

        params, params_dict = params_to_dict(params)
        log.debug("Cursor.execute(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params,
        })

        meta = {
            "db_dialect": self._dialect,
            "sql": conv_sql,
            "params": {},
        }
        meta.update(get_db_context_meta(self._get_agent_func))
        self._run_hook("sql_execute", meta)

        # Some versions of psycopg2 are picky about the value of the default
        # params argument. To avoid any issues, don't pass through params=None.
        if params is None:
            return self._cursor.execute(sql)
        else:
            return self._cursor.execute(sql, params)

    def executemany(self, sql, params_list):
        params_list, params_dicts = params_list_to_dicts(params_list)
        log.debug("Cursor.executemany(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params_list,
        })

        context_meta = get_db_context_meta(self._get_agent_func)
        for params_dict in params_dicts:
            if self._mogrify_func:
                conv_sql = self._mogrify_func(None, self._cursor, sql,
                                              params_dict)
            else:
                conv_sql = sql

            meta = {
                "db_dialect": self._dialect,
                "sql": conv_sql,
                "params": {},
            }
            meta.update(context_meta)
            self._run_hook("sql_execute", meta)
        return self._cursor.executemany(sql, params_list)


def _decode_param(string):
    """
    Convert 1 parameter value to a string so it can be processed
    by Lua.
    """
    try:
        return string.__unicode__()
    except AttributeError:
        pass

    try:
        return string.__str__()
    except (AttributeError, UnicodeEncodeError):
        pass

    return string


def params_to_dict(params):
    """
    Converts a params list to a dict w/ indexes as names.

    Eg.:

        ['a', 'b'] => {'0': 'a', '1': 'b'}

    Returns a tuple of the original params, in case it was a iterator,
    and a params dict.
    """
    if params is None:
        params_dict = {}

    elif isinstance(params, dict):
        params_dict = dict((key, _decode_param(value))
                           for (key, value) in get_iteritems(params)())

    else:
        # An iterator can only be consumed once, so never consume from
        # params directly and use tee to consume from a copy instead.
        if isinstance(params, Iterator):
            params_dup, params = tee(params)
        else:
            params_dup = params

        params_dict = dict((to_unicode(i), _decode_param(param))
                           for i, param in enumerate(params_dup))

    return params, params_dict


def params_list_to_dicts(params_list):
    """
    Convert a list of params list to a list of dicts w/ indexes as names.

    Returns a tuple of the original list of params, in case some of them
    were iterators, and a list of params dicts.
    """
    params_dicts = []
    new_params_list = []

    for params in params_list:
        params, params_dict = params_to_dict(params)
        new_params_list.append(params)
        params_dicts.append(params_dict)

    return new_params_list, params_dicts
