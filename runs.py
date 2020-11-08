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
        for c in _split(cmd, kwargs.get('shell')):
            function = getattr(subprocess, name)
            try:
                result = function(c, *args, **kwargs)
            except Exception:
                if not on_exception:
                    raise
                elif callable(on_exception):
                    on_exception(c)
            else:
                yield result

    return wrapped


call = _wrap('call')
check_call = _wrap('check_call')
check_output = _wrap('check_output')
run = _wrap('run')

runs = xmod(run, __name__)


def _split(lines, shell):
    lines = (i.strip() for i in lines.splitlines())
    lines = (i for i in lines if i)
    if shell:
        return lines

    return (shlex.split(i) for i in lines)
