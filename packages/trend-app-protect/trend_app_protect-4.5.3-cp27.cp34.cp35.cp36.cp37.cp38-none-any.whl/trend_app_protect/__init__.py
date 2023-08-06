from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

# Import functions to be exposed at the `trend_app_protect.*` level
from trend_app_protect.singleton import (  # noqa: F401 # Ignore unused imports
    do_setup,
    start,  # Deprecated, use `do_setup` and `wrap_wsgi_app` instead.
    wrap_wsgi_app,
)

# Get package version
from ._version import get_versions  # noqa: E402 # allow import after del
__version__ = get_versions()['version']
del get_versions


__agent_name__ = "agent-python"
__vm_version__ = "2.2.0"
