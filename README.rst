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
        g++ -DDEBUG  -O0 -g -std=c++17 -pthread -I ./include -lm -lstdc++ \
          -Wall -Wextra -Wno-strict-aliasing -Wpedantic \\
          -MMD -MP -MF -c src/tests.cpp -o build/./src/tests.cpp.o
     ''')

NOTES:

* I can see no good way to make pipes or redirection work.

.. code-block:: python

    import runs
    result = runs.check_output('echo "foo" > bar.txt')
    assert result == ['foo > bar.txt\n']  # :-/

*  Environment variables are not expanded

.. code-block:: python

    import runs
    result = runs.check_output('echo $FOO', env={'FOO': 'bah!'})
    assert result == ['$FOO\n']

One could make these substitutions work but it would be more reliable and less
work to use ``string.format`` or f-strings in Python.

The environment variables *are* visible in any binaries you call, and that's
the important thing.

API
===

``runs()``
~~~~~~~~~~

.. code-block:: python

  runs(
       *args,
       iterate=False,
       encoding='utf8',
       on_exception=None,
       echo=False,
       **kwargs,
  )

(`runs.py, 153-167 <https://github.com/rec/runs/blob/master/runs.py#L153-L167>`_)

Run each command with arguments. Return a list of ``subprocess.CompletedProcess`` instances.

See the help for ``subprocess.run`` for more information.

Arguments:
  commands:
    One string, which gets split into lines on line endings, or a list of
    strings.

  args:
    Positional arguments for ``subprocess.run`` (but prefer keyword
    arguments!)

  on_exception:
    If ``on_exception`` is ``False``, the default, exceptions from
    ``subprocess.run`` are raised as usual.

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
    Like the argument to ``subprocess.run``, except the default  is
    ``'utf8'``

  kwargs:
    Named arguments passed on to ``subprocess.run``

``runs.call()``
~~~~~~~~~~~~~~~

.. code-block:: python

  runs.call(
       commands,
       *args,
       iterate=False,
       encoding='utf8',
       on_exception=None,
       echo=False,
       **kwargs,
  )

(`runs.py, 153-167 <https://github.com/rec/runs/blob/master/runs.py#L153-L167>`_)

Run each command with arguments. Return a list of returncodes, one
for each command executed

See the help for ``subprocess.call`` for more information.

Arguments:
  commands:
    One string, which gets split into lines on line endings, or a list of
    strings.

  args:
    Positional arguments for ``subprocess.call`` (but prefer keyword
    arguments!)

  on_exception:
    If ``on_exception`` is ``False``, the default, exceptions from
    ``subprocess.call`` are raised as usual.

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
    Like the argument to ``subprocess.call``, except the default  is
    ``'utf8'``

  kwargs:
    Named arguments passed on to ``subprocess.call``

``runs.check_call()``
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  runs.check_call(
       commands,
       *args,
       iterate=False,
       encoding='utf8',
       on_exception=None,
       echo=False,
       **kwargs,
  )

(`runs.py, 153-167 <https://github.com/rec/runs/blob/master/runs.py#L153-L167>`_)

Run each command with arguments. If any command has a non-zero exit code,
raise a ``subprocess.CallProcessError``.

See the help for ``subprocess.check_call`` for more information.

Arguments:
  commands:
    One string, which gets split into lines on line endings, or a list of
    strings.

  args:
    Positional arguments for ``subprocess.check_call`` (but prefer keyword
    arguments!)

  on_exception:
    If ``on_exception`` is ``False``, the default, exceptions from
    ``subprocess.check_call`` are raised as usual.

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
    Like the argument to ``subprocess.check_call``, except the default  is
    ``'utf8'``

  kwargs:
    Named arguments passed on to ``subprocess.check_call``

``runs.check_output()``
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  runs.check_output(
       commands,
       *args,
       iterate=False,
       encoding='utf8',
       on_exception=None,
       echo=False,
       **kwargs,
  )

(`runs.py, 153-167 <https://github.com/rec/runs/blob/master/runs.py#L153-L167>`_)

Run each command with arguments. If a command has a non-zero exit code,
raise a ``subprocess.CallProcessError``.  Otherwise, return the results as a
list of strings.

See the help for ``subprocess.check_output`` for more information.

Arguments:
  commands:
    One string, which gets split into lines on line endings, or a list of
    strings.

  args:
    Positional arguments for ``subprocess.check_output`` (but prefer keyword
    arguments!)

  on_exception:
    If ``on_exception`` is ``False``, the default, exceptions from
    ``subprocess.check_output`` are raised as usual.

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
    Like the argument to ``subprocess.check_output``, except the default  is
    ``'utf8'``

  kwargs:
    Named arguments passed on to ``subprocess.check_output``

``runs.run()``
~~~~~~~~~~~~~~

.. code-block:: python

  runs.run(
       commands,
       *args,
       iterate=False,
       encoding='utf8',
       on_exception=None,
       echo=False,
       **kwargs,
  )

(`runs.py, 153-167 <https://github.com/rec/runs/blob/master/runs.py#L153-L167>`_)

Run each command with arguments. Return a list of ``subprocess.CompletedProcess`` instances.

See the help for ``subprocess.run`` for more information.

Arguments:
  commands:
    One string, which gets split into lines on line endings, or a list of
    strings.

  args:
    Positional arguments for ``subprocess.run`` (but prefer keyword
    arguments!)

  on_exception:
    If ``on_exception`` is ``False``, the default, exceptions from
    ``subprocess.run`` are raised as usual.

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
    Like the argument to ``subprocess.run``, except the default  is
    ``'utf8'``

  kwargs:
    Named arguments passed on to ``subprocess.run``

(automatically generated by `doks <https://github.com/rec/doks/>`_ on 2020-11-14T19:24:25.790753)
