"""Utility module."""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import errno
import os
import re


def mkdir_p(path):
    """Ensure a directory exists."""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise


class DummyContext(object):
    """No-op context manager."""

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


# Regex for a valid RFC 8141 URN
# https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s06.html
# https://tools.ietf.org/html/rfc8141#section-2
# https://tools.ietf.org/html/rfc3986#section-3.3
RE_VALID_URN = re.compile(
    r"urn:[a-z0-9][a-z0-9-]{0,31}:[a-z0-9()+,\-.:=@;$_!*'%/?#]+$", re.I
)


def is_valid_urn(urn):
    return RE_VALID_URN.match(urn)
