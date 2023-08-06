"""
azure_function implements the API to integrate the agent with Azure Functions.

Azure Functions only support Python 3.6+.

Azure Functions have bindings defined in function.json. They can have
input and output parameters and/or a return value. The parameter names and
types are configurable. Therefore we need to inspect the function
to determine which argument (if any) contains the HttpRequest input,
and if the function is expected to return an HttpResponse.

In theory, with inspection, we can support generation of different response
types and blanking of out parameters, depending on what is expected.
"""

import functools

from azure.functions import HttpRequest, HttpResponse

from trend_app_protect import __version__
from trend_app_protect.compat import to_native_string
from trend_app_protect.exceptions import (
    TrendAppProtectBlocked,
    TrendAppProtectOverrideResponse,
)
from trend_app_protect.singleton import get_agent


def identify_deployment_type():
    return "azure-function-python-wheel-{}".format(__version__)


def protect_function(func):
    agent = get_agent(deployment_type=identify_deployment_type())

    @functools.wraps(func)
    def wrapped(**kwargs):
        if not agent.enabled:
            return func(**kwargs)

        http_request, context = _parse_kwargs(kwargs)
        returns_http = http_request is not None
        try:
            transaction = agent.start_transaction()
            agent.run_hook(
                __name__,
                "urn:trend-ap:azure-function-start",
                {
                    "request": http_request,
                    "context": context,
                },
                transaction=transaction,
            )
            return func(**kwargs)

        except TrendAppProtectOverrideResponse as exc:
            # If the function is configured to return an HttpResponse,
            # generate one.
            if returns_http:
                code, headers, body = exc.args
                headers = {to_native_string(header[0], "ascii"):
                           to_native_string(header[1], "ISO-8859-1")
                           for header in headers}
                return HttpResponse(
                    body, headers=headers, status_code=code
                )
            # Otherwise just re-raise to block the execution.
            # Re-raise as something that doesn't derive from BaseException
            # since that crashes the runtime and causes a client timeout.
            raise TrendAppProtectBlocked(*exc.args)
        finally:
            agent.finish_transaction(transaction)

    return wrapped


def _parse_kwargs(kwargs):
    http_request = None
    context = _context_to_dict(kwargs.get('context'))
    for val in kwargs.values():
        if isinstance(val, HttpRequest):
            http_request = _request_to_dict(val)
    return http_request, context


def _request_to_dict(req):
    if not req:
        return {}
    return {
        "method": req.method,
        "url": req.url,
        "headers": dict(req.headers),
        "params": dict(req.params),
        "route_params": dict(req.route_params),
        "body": req.get_body(),
    }


def _context_to_dict(ctx):
    if not ctx:
        return {}
    return {
        "function_name": ctx.function_name,
        "function_directory": ctx.function_directory,
        "invocation_id": ctx.invocation_id,
    }
