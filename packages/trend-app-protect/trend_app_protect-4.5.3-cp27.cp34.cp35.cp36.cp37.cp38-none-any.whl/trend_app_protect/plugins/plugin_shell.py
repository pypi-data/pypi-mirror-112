from __future__ import (
    print_function
)

import os
import subprocess
import sys
try:
    import popen2
    PATCH_POPEN2 = True
except ImportError:
    PATCH_POPEN2 = False
from functools import partial

from trend_app_protect.compat import string_types
from trend_app_protect.context import get_context
from trend_app_protect.logger import log
from trend_app_protect.patcher import monkeypatch


# Set plugin name so it can be enabled and disabled.
NAME = "rce"
HOOKS_CALLED = ["exec"]


def add_hooks(run_hook, get_agent_func=None, timer=None):
    """
    Add hooks for shell commands.
    """
    meta = {
        "version": ".".join(map(str, sys.version_info[:3])),  # Py version
    }

    hook_os_popen(run_hook, timer)
    hook_os_system(run_hook, timer)
    hook_subprocess_Popen(run_hook, timer)
    if PATCH_POPEN2:
        hook_popen2(run_hook)
#    hook_popen3_init(run_hook)
#    hook_popen4_init(run_hook)

    return meta


def hook_os_popen(run_hook, timer):
    """
    Add our hook into os.popen
    """
    # Replace the original 'os.popen'
    @monkeypatch(os, 'popen', timer=timer,
                 report_name="plugin.python.shell.os_popen")
    def _our_os_popen(orig_os_popen, *args, **kwargs):
        log.debug("os.popen(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })
        stack = get_context()
        run_hook("exec", {
            "method": "os.popen",
            "args": args[:1],  # just send command
            "stack": stack,
            "cwd": os.getcwd(),
            "is_shell": True,
        })
        return orig_os_popen(*args, **kwargs)


def hook_os_system(run_hook, timer):
    """
    Add our hook into os.system
    """
    # Replace the original 'os.system'
    @monkeypatch(os, 'system', timer=timer,
                 report_name="plugin.python.shell.os_system")
    def _our_os_system(orig_os_system, *args, **kwargs):
        log.debug("os.system(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })
        stack = get_context()
        run_hook("exec", {
            "method": "os.system",
            "args": args[:1],  # just send command
            "stack": stack,
            "cwd": os.getcwd(),
            "is_shell": True,
        })
        return orig_os_system(*args, **kwargs)


def hook_subprocess_Popen(run_hook, timer):  # noqa: N802: # capital
    """
    Add our hook into subprocess.Popen
    """
    # Replace the original
    @monkeypatch(subprocess.Popen, "_execute_child", timer=timer,
                 report_name="plugin.python.shell.subprocess_execute_child")
    def _our_execute_child(orig_execute_child, *args, **kwargs):
        log.debug("subprocess.Popen._execute_child(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
        })
        # argument ten is Shell. Only run the hook if it's true
        # and the command will be interpreted by a shell
        is_shell = args[10] or kwargs.get('shell')

        stack = get_context()
        command_args = args[1]
        if isinstance(command_args, string_types):
            command_args = (command_args,)
        run_hook("exec", {
            "method": "subprocess.Popen._execute_child",
            "args": command_args,
            "stack": stack,
            "cwd": os.getcwd(),
            "is_shell": is_shell,
        })
        return orig_execute_child(*args, **kwargs)


def hook_popen2(run_hook):
    def popen_patch_init(method, orig_init, *args, **kwargs):
        log.debug("%(method)s(%(args)s, %(kwargs)s)", {
            "method": method,
            "args": args,
            "kwargs": kwargs,
        })
        # argument one is cmd. It's run via a shell if it's a string
        # no shell otherwise.
        command_args = args[1]
        is_shell = False
        if isinstance(command_args, string_types):
            command_args = (command_args,)
            is_shell = True
        stack = get_context()
        run_hook("exec", {
            "method": method,
            # drop the first argument which is Popen3() self
            "args": args[1:2],  # just send command
            "stack": stack,
            "cwd": os.getcwd(),
            "is_shell": is_shell,
        })
        return orig_init(*args, **kwargs)

    monkeypatch(popen2.Popen3, "__init__")(
        partial(popen_patch_init, 'popen2.Popen3.__init__',)
    )
    monkeypatch(popen2.Popen4, "__init__")(
        partial(popen_patch_init, 'popen2.Popen4.__init__',)
    )
