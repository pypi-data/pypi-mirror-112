from __future__ import (
    absolute_import,
    division,
    print_function,
)

# No unicode_literals because wsgi expects ascii strings

import logging
import sys
from threading import local

from trend_app_protect.compat import to_bytes, to_native_string
from trend_app_protect.context import get_stack
from trend_app_protect.exceptions import TrendAppProtectOverrideResponse
from trend_app_protect.logger import log

HOOKS_CALLED = ["http_request_start", "exception", "http_response_start",
                "http_response_body_chunk", "http_request_body_chunk"]


HTTP_STATUS_CODES = {
    200: "200 OK",
    201: "201 Created",
    202: "202 Accepted",
    204: "204 No Content",

    301: "301 Moved Permanently",
    302: "302 Found",
    303: "303 See Other",
    304: "304 Not Modified",
    307: "307 Temporary Redirect",

    400: "400 Bad Request",
    401: "401 Unauthorized",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",

    500: "500 Internal Server Error",
}


class WsgiWrapper(object):
    """
    Accepts new requests and hands off to a new WsgiTransaction object to
    handle.

    The WsgiTransaction object takes care of calling Agent.finish_transaction()
    on completion.
    """

    def __init__(self, agent, app, transaction_uuid_header):
        self._agent = agent
        self._app = app
        self._transaction_uuid_header = transaction_uuid_header
        self._local = local()
        self._local.wsgi_transaction = None
        self._warned_about_unclosed_iter = False

    def __call__(self, environ, start_response):
        """
        Register new request with Agent then create a WsgiTransaction object
        to handle it.
        """
        # If we're in debug logging, grab some extra data about the call stack
        # here to help identify what web server we're running under
        if log.isEnabledFor(logging.DEBUG):
            stack = "\n".join([
                "    %s:%d:%s" % frame for frame in get_stack()
            ])
            log.debug("WsgiWrapper.__call__ stack:\n%s", stack)

        # Ensure the `wsgi_response` thread local is present
        if not hasattr(self._local, "wsgi_transaction"):
            self._local.wsgi_transaction = None

        # If the previous WsgiTransaction is safe to close, but hasn't been
        # closed, close it here. This should not happen for well-behaved WSGI
        # servers, but we handle the case here in case we're running under a
        # server that doesn't comply to the spec.
        if (
            self._local.wsgi_transaction
            and not self._local.wsgi_transaction.closed
        ):
            if self._local.wsgi_transaction.safe_to_close:
                if not self._warned_about_unclosed_iter:
                    log.warning("WsgiResponse iterator was not closed by "
                                "server for request '%s'. Forcing close now.",
                                self._local.wsgi_transaction._transaction.uuid)
                    self._warned_about_unclosed_iter = True
                self._local.wsgi_transaction.close()
            else:
                # If the iterator was not fully consumed, and was not closed
                # always log a warning.
                log.warning("WsgiResponse iterator was not fully consumed and "
                            "was not closed for request '%s'.",
                            self._local.wsgi_transaction._transaction.uuid)

        # If a transaction is already in progress for this thread, don't start
        # a new one.
        if self._agent.get_transaction_uuid() is not None:
            # Just call original app directly.
            log.debug("Transaction '%s' already in progress, calling sub-app",
                      self._agent.get_transaction_uuid())
            return self._app(environ, start_response)

        transaction = self._agent.start_transaction()

        self._local.wsgi_transaction = WsgiTransaction(
            self._agent, self._app, transaction, self._transaction_uuid_header)

        return self._local.wsgi_transaction.handle_request(
            environ, start_response)


class WsgiTransaction(object):
    def __init__(self, agent, app, transaction, transaction_uuid_header):
        self._agent = agent
        self._app = app
        self._transaction = transaction
        self._transaction_uuid_header = transaction_uuid_header

        self._orig_start_response = None
        self._start_response_called = False
        self._wrapped_input = None
        self._output_gen = None
        self._inspect_response = False
        self._buffer_response = False
        # This is set to True when the response iteration is complete
        self.safe_to_close = False
        self.closed = False

    def handle_request(self, environ, start_response):
        # Keep a reference to the original start_response
        self._orig_start_response = start_response

        # Extract request meta
        request_metadata = self._extract_request_meta(environ)

        # Guard call to original app
        try:
            # Report to engine
            hook_result = self._agent.run_hook(
                "wsgi",
                "http_request_start",
                request_metadata,
                transaction=self._transaction)

            inspect_body = hook_result.get("inspect_body", True)

            # If the agent wants to see the request body, add our wrapper.
            if inspect_body:
                # Wrap the wsgi input object
                content_length = environ.get('CONTENT_LENGTH')

                self.wrapped_input = WsgiInputWrapper(
                    self._transaction, self._agent, environ["wsgi.input"],
                    content_length)
                environ["wsgi.input"] = self.wrapped_input

            # Call into original app
            self._output_gen = self._app(environ, self._wrapped_start_response)

            # If we're in debug logging, grab some extra data about the result
            # type here to help identify what how it should be handled.
            if log.isEnabledFor(logging.DEBUG):
                import inspect
                output_file = None
                debug_error = None
                try:
                    target = self._output_gen
                    if hasattr(target, "__class__"):
                        target = target.__class__
                    output_file = inspect.getfile(target)
                except Exception as exc:
                    debug_error = str(exc)

                log.debug(
                    "WsgiWrapper.handle_request output_gen: "
                    "type:'%s' has-close:'%s' file:'%s' error:'%s'",
                    type(self._output_gen), hasattr(self._output_gen, "close"),
                    output_file, debug_error)

        except TrendAppProtectOverrideResponse as exc:
            # Block this request
            status, headers, body = exc.args

            # Headers from Lua can come back as:
            # [["header", "value"], ]
            headers = [(to_native_string(h, 'ascii'),
                       to_native_string(v, 'ISO-8859-1')) for
                       (h, v) in headers]
            self._block_request(status, headers, body)

        except Exception as exc:
            # Report error to engine
            self._agent.run_hook(
                "wsgi", "exception", {
                    "source": "WsgiWrapper.__call__",
                    "exception": str(exc),
                }, transaction=self._transaction)
            # This request is over
            self.close()
            # Re-raise to framework so it can clean up
            raise

        # This object also implements the iterator protocol
        return self

    def _wrapped_start_response(self, status, headers, exc_info=None):
        if self._transaction_uuid_header:
            headers.append(
                (str(self._transaction_uuid_header),
                 str(self._transaction.uuid))
            )

        # `status` is a string like "404 NOT FOUND" but Lua expects a number.
        status_code = int(status[:3])

        # We can't pass actual exceptions into Lua, so stringify if present
        if exc_info:
            exc_info_str = "%s %s" % (exc_info[0].__name__, exc_info[1])
        else:
            exc_info_str = None

        hook_response = self._agent.run_hook(
            "wsgi", "http_response_start", {
                "status": status_code,
                "status_string": status,
                "headers": headers,
                "exc_info": exc_info_str,
            }, transaction=self._transaction)

        # Check if response body should be inspected
        self._inspect_response = hook_response.get("inspect_body", False)
        # Default to no buffering
        self._buffer_response = (
            self._inspect_response
            and hook_response.get("buffer_body", False)
        )

        # If new headers are provided, use those instead
        if "headers" in hook_response:
            headers = hook_response["headers"]

        # Guard call to original start_response
        try:
            # PEP3333 requires that start_response takes an optional exc_info
            # but in Django tests the mock version only takes two:
            if exc_info:
                result = self._orig_start_response(status, headers, exc_info)
            else:
                result = self._orig_start_response(status, headers)
            self._start_response_called = True
        except Exception as exc:
            # Report error to engine
            self._agent.run_hook(
                "wsgi", "exception", {
                    "source": "start_response",
                    "exception": str(exc),
                }, transaction=self._transaction)
            # Re-raise to framework so it can clean up
            raise

        return result

    def _extract_request_meta(self, environ):
        request_metadata = {}
        request_metadata["protocol"] = environ.get("SERVER_PROTOCOL")
        request_metadata["scheme"] = environ.get("wsgi.url_scheme")
        request_metadata["uri"] = environ.get("REQUEST_URI")
        request_metadata["query_string"] = environ.get("QUERY_STRING")
        request_metadata["method"] = environ.get("REQUEST_METHOD")
        request_metadata["path"] = environ.get("PATH_INFO")
        request_metadata["socket_ip"] = environ.get("REMOTE_ADDR")
        try:
            request_metadata["socket_port"] = int(environ.get("REMOTE_PORT"))
        except (ValueError, TypeError):
            request_metadata["socket_port"] = 0
        request_metadata["server_name"] = environ.get("SERVER_NAME")
        try:
            request_metadata["server_port"] = int(environ.get("SERVER_PORT"))
        except ValueError:
            request_metadata["server_port"] = 0

        # Extract HTTP Headers
        headers = {}
        request_metadata["headers"] = headers
        for k, v in environ.items():
            # All headers start with HTTP_
            if k.startswith("HTTP_"):
                # Reformat as lowercase, dash separated
                header = k[5:].lower().replace('_', '-')
                headers[header] = v

        # Add in content headers
        if "content-type" not in headers:
            headers["content-type"] = environ.get("CONTENT_TYPE")
        if "content-length" not in headers:
            headers["content-length"] = environ.get("CONTENT_LENGTH")

        return request_metadata

    def _block_request(self, status, headers, body):
        """
        Block an http request by returning a Forbidden response.

        status = str
        headers = [(str, str),]
        body = bytes
        """
        # TODO Make this look pretty
        if status is None:
            status = "403 Forbidden"

        # status may be provided as an integer. If so, convert to the
        # equivalent string status.
        if isinstance(status, int):
            status = HTTP_STATUS_CODES.get(status, str(status))

        if headers is None:
            headers = []

        for header in headers:
            if header[0].lower() == "content-type":
                break
        else:
            headers.append(("Content-Type", "text/plain"))

        body = to_bytes(body, encoding="utf8")

        if self._transaction_uuid_header:
            headers.append(
                (str(self._transaction_uuid_header),
                 str(self._transaction.uuid))
            )

        if self._start_response_called:
            # start_response has already been called. In order to cancel the
            # response now we need to call start_response with exc_info set.
            exc_info = sys.exc_info()
        else:
            self._start_response_called = True
            exc_info = None

        # `status` is a string like "404 NOT FOUND" but Lua expects a number.
        status_code = int(status[:3])

        # We can't pass actual exceptions into Lua, so stringify if present
        if exc_info:
            exc_info_str = "%s %s" % (exc_info[0].__name__, exc_info[1])
        else:
            exc_info_str = None

        # Manually send the response start hook
        self._agent.run_hook(
            "wsgi", "http_response_start", {
                "status": status_code,
                "status_string": status,
                "headers": headers,
                "exc_info": exc_info_str,
            }, transaction=self._transaction)

        if exc_info:
            self._orig_start_response(status, headers, exc_info)
        else:
            self._orig_start_response(status, headers)
        self._output_gen = iter([body])

    @property
    def __class__(self):
        return self._output_gen.__class__

    def __bytes__(self):
        return bytes(self._output_gen)

    def __str__(self):
        return str(self._output_gen)

    def __getattr__(self, attr):
        return getattr(self._output_gen, attr)

    def __iter__(self):
        log.debug("WSGI starting response iterator")
        # Guard call to original output iterator
        try:
            buff = []
            # We have to start iterating before testing self._inspect_response
            # because start_response() might not be called until iteration
            # begins.
            for chunk in self._output_gen:
                if not self._inspect_response:
                    yield chunk
                elif self._buffer_response:
                    buff.append(chunk)
                    yield b""
                else:
                    # Report the outgoing chunk to the engine
                    self._agent.run_hook(
                        "wsgi", "http_response_body_chunk", {
                            "chunk": chunk,
                            "buffered": False,
                        }, transaction=self._transaction)

                    yield chunk
            if self._inspect_response and self._buffer_response:
                body = b""
                if buff:
                    body = type(buff[0])().join(buff)

                # Report the buffered body to the engine
                self._agent.run_hook(
                    "wsgi", "http_response_body_chunk", {
                        "chunk": body,
                        "buffered": True,
                    }, transaction=self._transaction)
                yield body

        except TrendAppProtectOverrideResponse as exc:
            # Kill current iterator
            # TODO Should we finish iterating through it first?
            self._output_gen.close()

            # Block request (this call will replace the closed
            # self._output_gen)
            status, headers, body = exc.args
            self._block_request(status, headers, body)
            for chunk in self._output_gen:
                yield chunk

        except Exception as exc:
            # Report error to engine
            self._agent.run_hook(
                "wsgi", "exception", {
                    "source": "WsgiWrapper.__next__",
                    "exception": str(exc),
                }, transaction=self._transaction)
            # Re-raise to framework so it can clean up
            raise
        finally:
            self.safe_to_close = True
            log.debug("WSGI response iterator complete")

    def close(self):
        log.debug("WSGI response close() called")
        if not self.safe_to_close:
            log.warning("Server is calling close() on transaction '%s' "
                        "before iteration complete.", self._transaction.uuid)

        # Guard call to original iterator close
        try:
            # If original generator has 'close' method, we need to call it
            if hasattr(self._output_gen, "close"):
                self._output_gen.close()
        except Exception as exc:
            # Report error to engine
            self._agent.run_hook(
                "wsgi", "exception", {
                    "source": "WsgiWrapper.close",
                    "exception": str(exc),
                }, transaction=self._transaction)
            # Re-raise to framework so it can clean up
            raise
        finally:
            # Report end to engine
            self._agent.finish_transaction(transaction=self._transaction)
            # Reset for next request
            self._transaction = None
            self._output_gen = None
            self._orig_start_response = None
            self._start_response_called = False
            self.closed = True


class WsgiInputWrapper(object):
    """
    Wraps a WSGI input stream. Reports chunks of the request body to
    the engine as they are read by the wrapped application.
    """
    def __init__(self, transaction, agent, original_input, content_length):
        self._transaction = transaction
        self._agent = agent
        self._input = original_input
        self._done_reported = False
        if content_length:
            self._content_left = int(content_length)
        else:
            self._content_left = None

    def report_chunk(self, chunk):
        if self._agent and chunk:
            self._agent.run_hook(
                "wsgi", "http_request_body_chunk", {
                    "chunk": chunk,
                }, transaction=self._transaction)

    def report_done(self):
        if self._agent and not self._done_reported:
            self._agent.run_hook("wsgi", "http_request_body_done", {},
                                 transaction=self._transaction)
            self._done_reported = True

    def _data_read(self, read, requested=None):
        if self._done_reported:
            return

        done = False
        if read == 0:
            done = True

        if self._content_left is not None:
            self._content_left -= read
            if self._content_left <= 0:
                self._content_left = 0
                done = True

        if requested and read < requested:
            done = True

        if done:
            self.report_done()

    def read(self, *args, **kwargs):
        """
        Reads a specified number of bytes from input. size defaults to None
        which reads the entire input.
        """
        requested_size = None
        try:
            requested_size = args[0]
        except IndexError:
            try:
                requested_size = kwargs["size"]
            except KeyError:
                try:
                    requested_size = kwargs["length"]
                except KeyError:
                    pass

        chunk = self._input.read(*args, **kwargs)
        self.report_chunk(chunk)

        if requested_size is None:
            self.report_done()
        else:
            self._data_read(len(chunk), requested_size)

        return chunk

    def readline(self, *args, **kwargs):
        requested_size = None
        try:
            requested_size = args[0]
        except IndexError:
            try:
                requested_size = kwargs["size"]
            except KeyError:
                pass

        chunk = self._input.readline(*args, **kwargs)
        self.report_chunk(chunk)
        self._data_read(len(chunk), requested_size)

        return chunk

    def readlines(self, *args, **kwargs):
        lines = self._input.readlines(*args, **kwargs)
        if self._agent:
            chunk = b""
            if lines:
                chunk = type(lines[0])().join(lines)
            self.report_chunk(chunk)
            self._data_read(len(chunk))
        return lines

    def __iter__(self):
        for chunk in self._input:
            self.report_chunk(chunk)
            yield chunk
            self._data_read(len(chunk))
        self.report_done()
