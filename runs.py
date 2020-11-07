"""
🏃 Run one or more commands 🏃
------------------------------------------------------------------
"""

import functools
import shlex
import subprocess as sp
import xmod

__all__ = 'call', 'check_call', 'check_output', 'run', 'runs'
__version__ = '0.2.0'


def _wrap(f):
    @functools.wraps(f)
    def wrapped(cmd, *args, **kwargs):
        assert isinstance(cmd, str)

        lines = (c.strip() for c in cmd.splitlines())
        lines = (c for c in lines if c)
        if not kwargs.get('shell'):
            lines = (shlex.strip(c) for c in lines)

        for c in lines:
            yield f(c, *args, **kwargs)

    return wrapped


call = _wrap(sp.call)

check_call = _wrap(sp.check_call)

check_output = _wrap(sp.check_output)

run = _wrap(sp.run)

runs = xmod(run)
