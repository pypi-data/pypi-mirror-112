from __future__ import (
    absolute_import,
    division,
    print_function,
)

import sys
from functools import partial

try:
    import contextvars
except ImportError:
    contextvars = None

try:
    import asyncio
except ImportError:
    asyncio = None

from trend_app_protect.compat import to_native_string
from trend_app_protect.context import get_context
from trend_app_protect.exceptions import TrendAppProtectOverrideResponse
from trend_app_protect.logger import log
from trend_app_protect.patcher import monkeypatch


NAME = "tornado"
HOOKS_CALLED = ["framework_input_params", "http_request_start",
                "http_request_body_chunk", "http_response_start", "redirect"]
PATCHED_AGENT = False


class TransactionLocal(object):
    """A modified version of StackContext to support transactions."""

    def __init__(self):
        self.transaction = None
        self.transaction_features_enabled = None
        self.transaction_properties = {}
        self.active = True

    def enter(self):
        pass

    def exit(self, type, value, traceback):
        pass

    def __enter__(self):
        from tornado.stack_context import _state

        self.old_contexts = _state.contexts
        self.new_contexts = (self.old_contexts[0] + (self,), self)
        _state.contexts = self.new_contexts

        return self

    def __exit__(self, type, value, traceback):
        from tornado.stack_context import (
            _state,
            StackContextInconsistentError,
        )

        final_contexts = _state.contexts
        _state.contexts = self.old_contexts

        if final_contexts is not self.new_contexts:
            raise StackContextInconsistentError(
                "stack_context inconsistency (may be caused by yield "
                'within a "with StackContext" block)'
            )

        # Break up a reference to itself to allow for faster GC on CPython.
        self.new_contexts = None

    def deactivate(self):
        self.active = False

    @classmethod
    def current(cls):
        from tornado.stack_context import _state

        for ctx in reversed(_state.contexts[0]):
            if isinstance(ctx, cls) and ctx.active:
                return ctx


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add our request hooks to Tornado apps using httpserver.
    """
    # TODO: set meta
    meta = {}

    try:
        import tornado
    except ImportError:
        log.debug("Tornado not found")
        return None
    else:
        log.debug("Tornado {} found".format(tornado.version))

    if tornado.version_info[0] > 5 and not contextvars:
        log.info("contextvars required for Tornado version {}".format(
            tornado.version))
        return None

    if sys.version_info[:2] < (3, 6):
        log.info("Unsupported Tornado/Python version {}".format(sys.version))
        return None

    hook_tornado_http1connection(run_hook, get_agent_func, timer)
    hook_tornado_web(run_hook, get_agent_func, timer)

    if asyncio:
        hook_asyncio(timer)

    return meta


def _hook_agent(get_agent_func):
    from ..agent import Agent

    if not get_agent_func:
        return
    agent = get_agent_func()

    if contextvars:
        local = Agent.ContextvarsLocal()
        log.debug("Tornado on Python using contextvars")
    else:
        def local(self):
            return TransactionLocal.current()
        log.debug("Tornado on Python using TransactionLocal")

    agent.local = local


def _block_request(request_handler, status, headers, body):
    import tornado.web
    if not isinstance(request_handler, tornado.web.RequestHandler):
        log.info("Attempting to block on non-RequestHandler")
        return

    if request_handler._headers_written:
        # TODO: what to do if we've written headers?
        log.info("Attempting to block request with written headers")
        return

    request_handler.clear()
    for header in headers:
        request_handler.set_header(
            to_native_string(header[0], "ascii"),
            to_native_string(header[1], "ISO-8859-1"),
        )

    if status is None:
        request_handler.set_status(403, "Forbidden")
    else:
        try:
            # TODO: reasons from wsgi?
            request_handler.set_status(int(status))
        except ValueError:
            request_handler.set_status(403, "Forbidden")

    request_handler.write(body)
    request_handler.finish()


def _override_http1connection(connection, exception):
    import tornado.httputil

    status, headers, body = exception.args
    headers = tornado.httputil.HTTPHeaders()
    for header in headers:
        headers.add(
            to_native_string(header[0], "ascii"),
            to_native_string(header[1], "ISO-8859-1"),
        )

    if status is None:
        start_line = tornado.httputil.ResponseStartLine(
            '',
            403,
            "Forbidden"
        )
    else:
        start_line = tornado.httputil.ResponseStartLine(
            '',
            int(status),
            tornado.httputil.responses.get(int(status), "Unknown")
        )

    connection.write_headers(start_line, headers, body)
    connection.finish()


def hook_tornado_http1connection(run_hook, get_agent_func, timer):

    import tornado
    import tornado.http1connection
    from tornado import httputil

    # TODO: undo _ProxyAdapter xheaders?
    if not get_agent_func:
        return

    # Define the class here in case of different Tornado versions
    class _TrendHTTPAdapter(httputil.HTTPMessageDelegate):
        def __init__(self, delegate, http_connection):
            self.delegate = delegate

            # TODO: always an http1connection?
            self.http_connection = http_connection

            # Header received sets up the handler, if it hasn't been
            # called then we shouldn't be calling things like finish
            self.headers_received_called = False

        def headers_received(self, start_line, headers):
            context = self.http_connection.context
            path, _sep, query_string = start_line.path.partition("?")

            server_name = None
            server_port = 0
            try:
                sockname = self.http_connection.stream.socket.getsockname()
                server_name = sockname[0]
                server_port = sockname[1]
            except Exception as exc:
                log.trace("Unable to collect server socket "
                          "info: {}".format(exc))

            # Multiple headers will only use the last one here:
            our_headers = {key.lower(): value
                           for (key, value) in headers.get_all()}
            request_meta = {
                "path": path,
                "method": start_line.method,
                # TODO: works with _proxy?
                "scheme": context.protocol,
                "socket_ip": context.address[0] if context.address else None,
                "socket_port": context.address[1] if context.address else None,
                "protocol": start_line.version,
                "query_string": query_string,
                "headers": our_headers,
                "server_name": server_name,
                "server_port": server_port,
            }
            try:
                run_hook("http_request_start", request_meta)
            except TrendAppProtectOverrideResponse as exc:
                _override_http1connection(self.http_connection, exc)
                return

            self.headers_received_called = True
            return self.delegate.headers_received(start_line, headers)

        def _trend_override(self, exc):
            status, headers, body = exc.args

            if self.headers_received_called:
                log.debug("Overriding through handler")
                # Try to override through the handler:

                delegate = self
                while not isinstance(delegate, tornado.web._HandlerDelegate):
                    delegate = delegate.delegate

                handler = None
                try:
                    # @tornado.web.stream_request_body
                    handler = delegate.handler
                except AttributeError:
                    # Non @tornado.web.stream_request_body
                    def override():
                        _override_http1connection(self.http_connection, exc)
                    self.finish = override
                else:
                    _block_request(handler, status, headers, body)
            else:
                log.debug("Overriding through connection")
                _override_http1connection(self.http_connection, exc)

        def data_received(self, chunk):
            try:
                run_hook("http_request_body_chunk", {
                    "chunk": chunk,
                })
            except TrendAppProtectOverrideResponse as exc:
                try:
                    self._trend_override(exc)
                except AttributeError:
                    self._trend_block_this = True
                    log.info("Unable to block Tornado request")
                return

            return self.delegate.data_received(chunk)

        def finish(self):
            if self.headers_received_called:
                return self.delegate.finish()

        def on_connection_close(self):
            if self.headers_received_called:
                return self.delegate.on_connection_close()

    if tornado.version_info[0] > 5:
        from .plugin_tornado_async import hook_tornado_http1connection_async
        hook_tornado_http1connection_async(get_agent_func, _TrendHTTPAdapter)
    else:
        hook_tornado_http1connection_gen(get_agent_func, _TrendHTTPAdapter)


def hook_tornado_http1connection_gen(get_agent_func, http_adapter):
    import tornado.http1connection
    from tornado import gen

    agent = get_agent_func()

    @gen.coroutine
    def _read_message_context(orig, self, delegate):
        # NB: this code must be run after already setting
        # the context. The agent will attempt to access
        # the local context to store the transaction.

        agent.start_transaction()
        log.trace("Tornado transaction start: {}".format(
            agent.get_transaction_uuid()))

        try:
            ret = yield orig(self, http_adapter(delegate, self))
            raise gen.Return(ret)
        finally:
            agent.finish_transaction()

    # Because the transaction is finished by the end of this function
    # we're unable to pass a timer
    @monkeypatch(
        tornado.http1connection.HTTP1Connection,
        "_read_message",
        report_name="plugin.tornado._read_message",
    )
    @gen.coroutine
    def _read_message(orig, self, delegate):
        if self.is_client:
            ret = yield orig(self, delegate)
            raise gen.Return(ret)

        global PATCHED_AGENT
        if not PATCHED_AGENT:
            PATCHED_AGENT = True
            _hook_agent(get_agent_func)

        if contextvars:
            ctx = contextvars.copy_context()
            # Force a new context here so that the request-local
            # data is cleared when we leave it.
            ret = yield ctx.run(
                partial(_read_message_context, orig, self, delegate))
            raise gen.Return(ret)

        else:
            from tornado.stack_context import run_with_stack_context
            ctx = TransactionLocal()
            ret = yield run_with_stack_context(
                ctx, partial(_read_message_context, orig, self, delegate))
            raise gen.Return(ret)


def hook_tornado_web(run_hook, get_agent_func, timer):
    import tornado.web

    @monkeypatch(
        tornado.web.RequestHandler,
        "flush",
        timer=timer,
        report_name="plugin.tornado.web.flush",
    )
    def _flush(orig, self, *args, **kwargs):
        if not self._headers_written:
            headers = [[k, v] for k, v in self._headers.items()]
            response_meta = {
                "status": self._status_code,
                "status_string": self._reason,
                "headers": headers,
            }
            run_hook("http_response_start", response_meta)
            agent = get_agent_func()
            if agent:
                self.add_header(str(agent.get_transaction_uuid_header()),
                                str(agent.get_transaction_uuid()))

        return orig(self, *args, **kwargs)

    @monkeypatch(
        tornado.web.RequestHandler,
        "redirect",
        timer=timer,
        report_name="plugin.tornado.web.redirect",
    )
    def _redirect(orig, self, url, *args, **kwargs):
        if not self._headers_written:
            try:
                run_hook("redirect", {"stack": get_context(), "location": url})
            except TrendAppProtectOverrideResponse as exc:
                status, headers, body = exc.args
                _block_request(self, status, headers, body)
                return

        return orig(self, url, *args, **kwargs)

    @monkeypatch(
        tornado.web.RequestHandler,
        "_handle_request_exception",
        timer=timer,
        report_name="plugin.tornado.web.execute_exception",
    )
    def _handle_request_exception(orig, self, e):
        if not isinstance(e, TrendAppProtectOverrideResponse):
            return orig(self, e)

        status, headers, body = e.args
        _block_request(self, status, headers, body)
        return

    for method in ["get_argument", "get_arguments", "get_query_argument",
                   "get_query_arguments"]:
        @monkeypatch(
            tornado.web.RequestHandler,
            method,
            timer=timer,
            report_name="plugin.tornado.web.{}".format(method),
        )
        def _get_arg(orig, self, *args, **kwargs):
            try:
                self.request._trend_input_done
            except AttributeError:
                self.request._trend_input_done = True
            else:
                return orig(self, *args, **kwargs)

            run_hook("framework_input_params", {
                "params": self.request.query_arguments
            })
            return orig(self, *args, **kwargs)

    if tornado.version_info[0] > 5:
        from .plugin_tornado_async import hook_tornado_web_async
        hook_tornado_web_async(timer)
    else:
        hook_tornado_web_gen(timer)


def hook_tornado_web_gen(timer):
    import tornado.web
    from tornado import gen

    def _execute_handle_exception(self, type, exc, traceback):
        if type is TrendAppProtectOverrideResponse:
            status, headers, body = exc.args
            _block_request(self, status, headers, body)

            # See web.py _execute finally:
            self.result = None
            if (self._prepared_future is not None
                    and not self._prepared_future.done()):
                self._prepared_future.set_result(None)

            return True  # Indicate we handled this exception

    @monkeypatch(
        tornado.web.RequestHandler,
        "_execute",
        timer=timer,
        report_name="plugin.tornado.web.execute",
    )
    @gen.coroutine
    def _execute(orig, self, *args, **kwargs):
        # Wrap but handle what is normally done in the exception
        # handler at the end of execute

        from tornado import stack_context
        from functools import partial
        if contextvars:
            try:
                result = yield orig(self, *args, **kwargs)
                raise gen.Return(result)
            except TrendAppProtectOverrideResponse as exc:
                status, headers, body = exc.args
                _block_request(self, status, headers, body)
            raise gen.Return()
        else:
            try:
                ctx = stack_context.ExceptionStackContext(
                    partial(_execute_handle_exception, self))
                result = yield stack_context.run_with_stack_context(
                    ctx, partial(orig, self, *args, **kwargs))
                raise gen.Return(result)
            except TrendAppProtectOverrideResponse as exc:
                status, headers, body = exc.args
                _block_request(self, status, headers, body)
            raise gen.Return()


def hook_asyncio(timer):
    import asyncio.events

    # Not calling the exception handler here results in our exception not
    # showing up, but it still seems to be in the future.
    @monkeypatch(
        asyncio.events.Handle,
        "_run",
        timer=timer,
        report_name="plugin.tornado.asyncio.run",
    )
    def _run(orig, self, *args, **kwargs):
        try:
            return orig(self, *args, **kwargs)
        except TrendAppProtectOverrideResponse:
            # eat our exception, it's still on the future
            pass
