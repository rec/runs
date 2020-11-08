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


def _run(name, cmd, *args, on_exception=None, echo=False, **kwargs):
    echo = echo or (lambda *a: None)
    if echo is True:
        echo = '$'
    if isinstance(echo, str):
        echo = functools.partial(print, echo)

    assert callable(echo)

    function = getattr(subprocess, name)
    shell = kwargs.get('shell')

    for line in cmd.splitlines():
        echo(line)
        cmd = shlex.split(line, comments=True)

        if cmd:
            if shell:
                cmd = ' '.join(shlex.quote(c) for c in cmd)

            try:
                result = function(cmd, *args, **kwargs)

            except Exception:
                if not on_exception:
                    raise
                if on_exception is not True:
                    on_exception(cmd)

            else:
                yield result


def _wrap(name):
    @functools.wraps(getattr(subprocess, name))
    def wrapped(cmd, *args, iterate=False, **kwargs):
        it = _run(name, cmd, *args, **kwargs)
        if iterate:
            return it
        return list(it)

    return wrapped


call = _wrap('call')
check_call = _wrap('check_call')
check_output = _wrap('check_output')
run = _wrap('run')

xmod(run, __name__)
