"""
🏃 runs: subprocess with the sharp edges removed 🏃
-------------------------------------------------------

``subprocess`` is essential but:

* You can only run one command, not a sequence of them

* Commands to subprocess must be either a sequence of strings or a string,
  depending on whether shell=True or not

* Results are returned by default as binary strings

``runs`` lets you run a block of text as a sequence of subprocess calls It
provides nearly drop-in replacements for four key functions from
``subprocess``: ``call()``, ``check_call()``, ``check_output()``, and ``run()``
- the big change is that each returns a list of values and not a single value.

The ``runs`` functions also allow comments and line continuations, optional
logging and error handling, and lazy evaluation.


EXAMPLES:

.. code-block:: python

    # Calling runs() on a block of text is like typing
    # the commands from the keyboard: the results go to stdout and stderr./

    import runs
    runs('ls')
    runs.run('ls')  # Same as the previous line

    # runs.check_output() returns a list: one string result for each command

    results = check_output('''
        echo  line   one  # Here's line one.
        echo   'line "  two  "'  # and two!
    ''')
    assert results == ['line one', 'line "  two  "']

    # Line continuations work too
    runs('''
        ls -cail

        # One command that takes many lines.
        g++ -DDEBUG  -O0 -g -std=c++17 -pthread -I ./include -lm -lstdc++ \\
          -Wall -Wextra -Wno-strict-aliasing -Wpedantic \\\\
          -MMD -MP -MF -c src/tests.cpp -o build/./src/tests.cpp.o
     ''')

NOTES:

* I can see no good way to make pipes or redirection work.

.. code-block:: python

    import runs
    result = runs.check_output('echo "foo" > bar.txt')
    assert result == ['foo > bar.txt\\n']  # :-/

*  Environment variables are not expanded

.. code-block:: python

    import runs
    result = runs.check_output('echo $FOO', env={'FOO': 'bah!'})
    assert result == ['$FOO\\n']

One could make these substitutions work but it would be more reliable and less
work to use ``string.format`` or f-strings in Python.

The environment variables *are* visible in any binaries you call, and that's
the important thing.
"""

import functools
import shlex
import subprocess
import sys
import xmod

__version__ = '1.1.0'
__all__ = 'call', 'check_call', 'check_output', 'run', 'split_commands'


def _run(name, commands, *args, on_exception=None, echo=False, **kwargs):
    if echo is True:
        echo = '$'

    if echo == '':
        echo = print

    if echo and not callable(echo):
        echo = functools.partial(print, echo)

    if on_exception is True:
        on_exception = lambda *x: None  # noqa: E731

    if not callable(on_exception):
        on_exception = functools.partial(print, on_exception, file=sys.stderr)

    function = getattr(subprocess, name)
    shell = kwargs.get('shell')

    for line in split_commands(commands, echo):
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


def split_commands(lines, echo=None):
    waiting = []

    def emit():
        parts = ''.join(waiting).strip()
        waiting.clear()
        if parts:
            yield parts

    if isinstance(lines, str):
        lines = lines.splitlines()

    for line in lines:
        echo and echo(line)

        if line.endswith('\\'):
            no_comments = ' '.join(shlex.split(line[:-1], comments=True))
            if line.count('#') > no_comments.count('#'):
                raise ValueError('Comments cannot contain a line continuation')

            waiting.append(line[:-1])

        else:
            waiting.append(line)
            yield from emit()

    yield from emit()


def _wrap(name, summary):
    def wrapped(
        commands,
        *args,
        iterate=False,
        encoding='utf8',
        on_exception=None,
        echo=False,
        **kwargs,
    ):
        kwargs.update(echo=echo, encoding=encoding, on_exception=on_exception)
        it = _run(name, commands, *args, **kwargs)
        if iterate:
            return it
        return list(it)

    wrapped.__name__ = name
    wrapped.__doc__ = _ARGS.format(function=name, summary=summary)

    return wrapped


_ARGS = """
{summary}
See the help for ``subprocess.{function}()`` for more information.

Arguments:
  commands:
    One string, which gets split into lines on line endings, or a list of
    strings.

  args:
    Positional arguments for ``subprocess.{function}()`` (but prefer keyword
    arguments!)

  on_exception:
    If ``on_exception`` is ``False``, the default, exceptions from
    ``subprocess.{function}()`` are raised as usual.

    If ``on_exception`` is True, they are ignored.

    If ``on_exception`` is a callable, the line that caused the exception is
    passed to it.

    If ``on_exception`` is a string, the line causing the exception
    is printed, prefixed with that string.

  echo:
    If ``echo`` is ``False``, the default, then commands are silently executed.
    If ``echo`` is ``True``, commands are printed prefixed with ``$``
    If ``echo`` is a string, commands are printed prefixed with that string
    If ``echo`` is callable, then each command is passed to it.

  iterate:
    If ``iterate`` is ``False``, the default, then a list of results is
    returned.

    Otherwise an iterator of results which is returned, allowing for lazy
    evaluation.

  encoding:
    Like the argument to ``subprocess.{function}()``, except the default  is
    ``'utf8'``

  kwargs:
    Named arguments passed on to ``subprocess.{function}()``
"""

call = _wrap(
    'call',
    """
Run each command with arguments. Return a list of returncodes, one
for each command executed
""",
)

check_call = _wrap(
    'check_call',
    """
Run each command with arguments. If any command has a non-zero exit code,
raise a ``subprocess.CallProcessError``.
""",
)

check_output = _wrap(
    'check_output',
    """
Run each command with arguments. If a command has a non-zero exit code,
raise a ``subprocess.CallProcessError``.  Otherwise, return the results as a
list of strings.
""",
)

run = _wrap(
    'run',
    """
Run each command with arguments. Return a list of \
``subprocess.CompletedProcess`` instances.
""",
)

xmod(run, __name__, mutable=True)
