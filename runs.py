"""
🏃 Run one or more commands 🏃
------------------------------------------------------------------
"""

import functools
import shlex
import subprocess
import xmod

__version__ = '0.2.0'
__all__ = 'call', 'check_call', 'check_output', 'run'


def _wrap(name):
    @functools.wraps(getattr(subprocess, name))
    def wrapped(cmd, *args, on_exception=None, **kwargs):
        lines = (c.strip() for c in cmd.splitlines())
        lines = (c for c in lines if c)
        if not kwargs.get('shell'):
            lines = (shlex.split(c) for c in lines)

        for c in lines:
            function = getattr(subprocess, name)
            try:
                result = function(c, *args, **kwargs)
            except Exception:
                if not on_exception:
                    raise
                if callable(on_exception):
                    on_exception(c)
            else:
                yield result

    return wrapped


call = _wrap('call')
check_call = _wrap('check_call')
check_output = _wrap('check_output')
run = _wrap('run')

runs = xmod(run, __name__)
