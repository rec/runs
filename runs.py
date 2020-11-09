"""
🏃 runs: subprocess with the sharp edges removed 🏃
-------------------------------------------------------

``subprocess`` is both essential and annoying:

* Sometimes ('commands', 'are', 'like', 'this')
*


"""

import functools
import shlex
import subprocess
import sys
import xmod

__version__ = '0.3.0'
__all__ = 'call', 'check_call', 'check_output', 'run'


def _run(name, cmd, *args, on_exception=None, echo=False, **kwargs):
    if echo is True:
        echo = '$'

    if not callable(echo):
        echo = functools.partial(print, echo)

    if on_exception is True:
        on_exception = '!'

    if not callable(on_exception):
        on_exception = functools.partial(print, on_exception, file=sys.stderr)

    function = getattr(subprocess, name)
    shell = kwargs.get('shell')

    for line in _lines(cmd, echo):
        cmd = shlex.split(line, comments=True)
        if shell:
            cmd = ' '.join(shlex.quote(c) for c in cmd)

        try:
            result = function(cmd, *args, **kwargs)

        except Exception:
            if not on_exception:
                raise
            on_exception(line)

        else:
            yield result


def _lines(cmd, echo):
    waiting = []

    def emit():
        parts = ''.join(waiting).strip()
        waiting.clear()
        if parts:
            yield parts

    for line in cmd.splitlines():
        echo(line)

        if line.endswith('\\'):
            no_comments = ' '.join(shlex.split(line[:-1], comments=True))
            if line.count('#') > no_comments.count('#'):
                raise ValueError('Comments cannot contain a line continuation')

            waiting.append(line[:-1])

        else:
            waiting.append(line)
            yield from emit()

    yield from emit()


def _wrap(name):
    @functools.wraps(getattr(subprocess, name))
    def wrapped(cmd, *args, iterate=False, encoding='utf8', **kwargs):
        it = _run(name, cmd, *args, encoding=encoding, **kwargs)
        if iterate:
            return it
        return list(it)

    return wrapped


call = _wrap('call')
check_call = _wrap('check_call')
check_output = _wrap('check_output')
run = _wrap('run')

xmod(run, __name__)
