from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from trend_app_protect.context import get_context
from trend_app_protect.logger import log
from trend_app_protect.patcher import monkeypatch


# Set name so plugin can be enabled and disabled.
NAME = "flask"
HOOKS_CALLED = [
    "redirect",
]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add our hooks into the flask library functions.
    """
    meta = {}

    try:
        import flask
    except ImportError:
        return None

    meta["version"] = flask.__version__

    # Install a hook to capture newly created wsgi apps and wrap them.
    hook_flask_app(run_hook, get_agent_func, timer)

    # Install a hook around the redirect method
    hook_flask_redirect(run_hook, timer)

    return meta


def hook_flask_app(run_hook, get_agent_func, timer):
    """
    Wrap the `Flask()` __init__ function so we can wrap each WSGI
    app as it is produced. This also creates the Agent if it hasn't been
    created yet.
    """
    import flask

    # If we don't have a `get_agent_func()` defined the app will be
    # wrapped elsewhere.
    if not get_agent_func:
        return

    # For new-style classes, special methods like __call__ are looked up
    # on the class directly, not the instance. This means it can't be
    # overridden normally. Instead, we have to override it on the class
    # to get it to check an instance method to allow us to override it
    # from the __init__ monkeypatch below.
    def trend_app_protect_call(self, *args, **kwargs):
        """
        Simply duplicate the behaviour of the original __call__ and proxy
        everything to the internal `wsgi_app` method. This stub will be
        wrapped by the Agent during the `__init__` monkeypatch below.
        """
        return self.wsgi_app(*args, **kwargs)
    flask.Flask._trend_app_protect_call = trend_app_protect_call

    @monkeypatch(flask.Flask, "__call__", timer=timer,
                 report_name="plugin.flask.app.__call__")
    def _call(orig, flask_self, *args, **kwargs):
        """
        We patch __call__ here because it is impossible to patch it on a
        per-instance basis. This mokeypatch on the class simply proxies
        through the stub `_trend_app_protect_call` defined above. Since the
        `_trend_app_protect_call` method is "normal", it can be overridden on
        the Flask instance during the __init__ monkeypatch below.
        """
        log.debug("Call to patched __call__(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })
        # Always call the trend_app_protect_call stub defined above. Since the
        # stub is not a special method, it can be overridden on the instance
        # below.
        return flask_self._trend_app_protect_call(*args, **kwargs)

    @monkeypatch(flask.Flask, "__init__", timer=timer,
                 report_name="plugin.flask.app.__init__")
    def _flask_init(orig, flask_self, *args, **kwargs):
        """
        Here we patch the `__call__` method (via the _trend_app_protect_call
        stub) of every new Flask app. This ensures that when the app object is
        used as a WSGI callable, we already have it wrapped.
        """
        log.debug("Call to patched __init__(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })
        # Get the WSGI app (__init__ always returns None)
        orig(flask_self, *args, **kwargs)

        # Get or create the TrendAppProtect Agent singleton
        agent = get_agent_func()

        # Wrap the Flask app __call__ method (via _trend_app_protect_call) with
        # Trend App Protect.
        flask_self._trend_app_protect_call = agent.wrap_wsgi_app(
            flask_self._trend_app_protect_call)


def hook_flask_redirect(run_hook, timer):
    """Listen for the redirect() to be called and all redirect"""
    import flask
    import werkzeug.utils

    # Flask imports the redirect method directly in to it's namespace, so
    # it's possible for it to be called from two locations
    for klass in (flask, werkzeug.utils):
        @monkeypatch(klass, "redirect", timer=timer,
                     report_name="plugin.flask.redirect")
        def _redirect(orig, location, *args, **kwargs):
            stack = get_context()
            run_hook("redirect", {
                "stack": stack,
                "location": location,
            })

            return orig(location, *args, **kwargs)
