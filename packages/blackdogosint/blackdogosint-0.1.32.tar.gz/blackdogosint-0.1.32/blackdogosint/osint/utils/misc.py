# -*- coding: utf-8 -*-
import errno
import os


def read(path, count=-1, skip=0):
    r"""read(path, count=-1, skip=0) -> str
    Open file, return content.
    Examples:
        >>> read('/proc/self/exe')[:4]
        b'\x7fELF'
    """
    path = os.path.expanduser(os.path.expandvars(path))
    with open(path, 'rb') as fd:
        if skip:
            fd.seek(skip)
        return fd.read(count)


def mkdir_p(path):
    """Emulates the behavior of ``mkdir -p``."""

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise


def write(path, data=b'', create_dir=False, mode='w'):
    """Create new file or truncate existing to zero length and write data."""
    path = os.path.expanduser(os.path.expandvars(path))
    if create_dir:
        path = os.path.realpath(path)
        mkdir_p(os.path.dirname(path))
    if mode == 'w' and isinstance(data, bytes):
        mode += 'b'
    with open(path, mode) as f:
        f.write(data)
