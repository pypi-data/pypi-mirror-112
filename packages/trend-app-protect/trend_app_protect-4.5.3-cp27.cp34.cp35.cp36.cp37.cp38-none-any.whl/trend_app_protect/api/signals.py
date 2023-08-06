from trend_app_protect.singleton import run_hook
from trend_app_protect.util import is_valid_urn


FAILED_LOGIN = "urn:trend-ap:failed-login"


def send_failed_login(username):
    """
    Signal a failed login attempt to the trend app protect agent.
    """
    send_signal(FAILED_LOGIN, username=username)


def send_signal(urn, **metadata):
    """
    Send a signal to the trend app protect agent.
    """
    # TODO move URN validation to libagent when we are ready to roll
    # out custom signals in all agents
    if not is_valid_urn(urn):
        raise ValueError("Invalid URN {}".format(urn))

    run_hook(urn, metadata)
