from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


# Hold singleton copies of key objects for this app
_global_agent = None


def wrap_wsgi_app(app):
    """
    Helper function to create the global Agent instance, and use it to
    wrap the supplied WSGI app callable.
    """
    agent = get_agent()
    if agent.enabled:
        return agent.wrap_wsgi_app(app)
    else:
        # If agent is not enabled, just return the original app
        return app


def run_hook(hook_name, meta):
    """
    Helper function to get reference to the global agent and call
    `run_hook`.
    """
    agent = get_agent()
    return agent.run_hook("api", hook_name, meta)


def get_agent(create_if_required=True, deployment_type=None):
    """
    Shortcut function for accessing a singleton agent.
    """
    # Import inside function to avoid circular import.
    from trend_app_protect import agent
    global _global_agent

    if not _global_agent and create_if_required:
        _global_agent = agent.Agent(deployment_type=deployment_type)
        _global_agent.start()
    return _global_agent


def start():
    """
    Manual function to create an agent and start it up. Returns
    a reference to the agent so it can be used in a call to
    `agent.wrap_wsgi_app(original_app)`.

    This is only required for frameworks where we don't automatically wrap
    the produced wsgi app. In most cases you should just
    `import trend_app_protect.start` at the top of your application entry file.
    """
    return get_agent()


def do_setup():
    """
    For backward compatibility. Use start() instead.
    """
    start()
