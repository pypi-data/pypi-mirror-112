from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from hashlib import sha1

from trend_app_protect.compat import to_bytes
from trend_app_protect.context import get_context
from trend_app_protect.logger import log
from trend_app_protect.patcher import monkeypatch


# Set name so plugin can be enabled and disabled.
NAME = "django"

HOOKS_CALLED = [
    "framework_input_params",
    "redirect",
]


def sha1hash(value):
    """
    Return the sha1 hash of the provided value, or None if `value` is None.
    """
    if value is None:
        return None
    return sha1(to_bytes(value, encoding="utf8")).hexdigest()


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add our hooks into the django library functions.
    """
    try:
        import django
        import django.conf
    except ImportError:
        return None

    # Install a hook to capture newly created wsgi apps and wrap them.
    hook_get_wsgi_application(run_hook, get_agent_func, timer)

    # Install hooks to capture the input params
    hook_get_params(run_hook, timer)
    hook_post_params(run_hook, timer)

    # This installs the hooks around the response to watch for
    # redirects.
    hook_get_response(run_hook, timer)

    meta = {
        "version": django.get_version(),
    }

    return meta


def hook_get_wsgi_application(run_hook, get_agent_func, timer):
    """
    Wrap the `get_wsgi_application()` function so we can wrap each WSGI
    app as it is produced. This also creates the Agent if it hasn't been
    created yet.
    """
    import django.core.wsgi

    # If we don't have a `get_agent_func()` defined the app will be
    # wrapped elsewhere.
    if get_agent_func:
        @monkeypatch(django.core.wsgi, "get_wsgi_application", timer=timer,
                     report_name="plugin.django.get_wsgi_application")
        def _get_wsgi_application(orig, *args, **kwargs):
            # Get the WSGI app
            app = orig(*args, **kwargs)
            # Get or create the TrendAppProtect Agent singleton
            agent = get_agent_func()
            # Wrap the WSGI app object with TrendAppProtect.
            app = agent.wrap_wsgi_app(app)
            return app


def hook_get_params(run_hook, timer):
    """
    Wrap the request.GET cached property.
    """
    from django.core.handlers.wsgi import WSGIRequest
    from django.utils.functional import cached_property

    if isinstance(WSGIRequest.GET, cached_property):
        class WrappedProperty(object):
            """A proxy for django's version of a cached property. This is
            similar but not the same as the werkzeug utility code that
            does the same. For one the Django wrapper extends `object`
            instead of `property`. For another this is uses a non-data
            descriptor which will then be overridden by the value
            in the instances __dict__.

            This class also handles the QueryDict type used by Django.
            """
            def __init__(self, orig):
                self.__doc__ = getattr(orig, "__doc__", None)
                self.__trend_app_protect_orig = orig

            def __get__(self, instance, type=None):
                if instance is None:
                    return self

                value = self.__trend_app_protect_orig.__get__(instance, type)
                if hasattr(value, 'lists'):
                    run_hook("framework_input_params", {
                        "params": dict(value.lists()),
                    })
                elif isinstance(value, dict):
                    run_hook("framework_input_params", {
                        "params": value,
                    })
                return value

        WSGIRequest.GET = WrappedProperty(WSGIRequest.GET)
    else:
        raise Exception("Django's WSGI request.GET is not "
                        "a cached property ({0})".format(
                            type(WSGIRequest.GET)))


def hook_post_params(run_hook, timer):
    """
    Wrap the _load_post_and_files call that is used to load the post params.
    """
    from django.http.request import HttpRequest

    @monkeypatch(HttpRequest, "_load_post_and_files", timer=timer,
                 report_name="plugin.django._load_post_and_files")
    def _load_post_and_files(orig, self, *args, **kwargs):
        try:
            return orig(self, *args, **kwargs)
        finally:
            # Check if there is _post data (and not just files)
            if hasattr(self, '_post'):
                if hasattr(self._post, 'lists'):
                    value = dict(self._post.lists())
                else:
                    value = self._post
                if isinstance(value, dict):
                    run_hook("framework_input_params", {
                        "params": value,
                    })


def hook_get_response(run_hook, timer):
    """
    Hook the Django get_response to watch for redirects.
    """
    from django.core.handlers.base import BaseHandler
    from django.http.response import HttpResponseRedirectBase

    @monkeypatch(
        HttpResponseRedirectBase, "__init__", timer=timer,
        report_name="plugin.django.new_redirect")  # noqa: N807
    def __init__(orig, self, url, *args, **kwargs):
        result = orig(self, url, *args, **kwargs)

        self._trend_app_protect_stack = get_context()
        return result

    @monkeypatch(BaseHandler, "get_response", timer=timer,
                 report_name="plugin.django.get_response")
    def _get_response(orig, self, *args, **kwargs):
        log.debug("BaseHandler.get_response")

        response = orig(self, *args, **kwargs)
        if isinstance(response, HttpResponseRedirectBase):
            stack = response._trend_app_protect_stack
            run_hook("redirect", {
                "stack": stack,

                # Versions > 1.6 add a property, response.url, but it's
                # missing from older versions
                "location": response['location'],
            })

        return response
