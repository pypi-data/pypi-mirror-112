from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import pkg_resources

from trend_app_protect.patcher import monkeypatch


# Set name so plugin can be enabled and disabled.
NAME = "pyramid"
HOOKS_CALLED = []


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks to pyramid.
    """
    try:
        import pyramid  # noqa: F401 # unused
    except ImportError:
        return None

    try:
        version = pkg_resources.get_distribution("pyramid").version
    except pkg_resources.DistributionNotFound:
        version = None

    meta = {
        "version": version

    }

    # The handle_request hooks imports pyramid.config which imports a ton of
    # other modules. If other patches are needed patch this last.
    add_handle_request_hook(run_hook, get_agent_func, timer)

    return meta


def add_handle_request_hook(run_hook, get_agent_func, timer):
    """
    Add a hook as early as possible in the Pyramid request flow to extract
    the user_id making the request. This is required because normally the
    user is not loaded unless the app-code actually requests it.
    """
    import pyramid.config

    # Wrap `pyramid.config.Configurator.make_wsgi_app` to get access to
    # the wsgi `app` object.
    @monkeypatch(pyramid.config.Configurator, "make_wsgi_app", timer=timer,
                 report_name="plugin.pyramid.app.make_wsgi_app")
    def _make_wsgi_app(orig, *args, **kwargs):
        app = orig(*args, **kwargs)

        # Wrap the WSGI app object with trend_app_protect.
        # If we don't have a `get_agent_func()` defined the app will be
        # wrapped elsewhere.
        if get_agent_func:
            # Get or create the trend_app_protect Agent singleton
            agent = get_agent_func()
            # Do the wrapping
            app = agent.wrap_wsgi_app(app)
        return app
