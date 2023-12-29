import unittest
from pathlib import Path
from unittest import mock

import tdir

import runs


def assert_called(mock, *args, **kwds):
    mock.assert_any_call(*args, encoding='utf8', **kwds)


@mock.patch('runs.subprocess.run', autospec=True)
class TestRunsMock(unittest.TestCase):
    def test_simple1(self, run):
        results = runs('hello world', always_list=True)
        assert len(results) == 1

        assert_called(run, ['hello', 'world'])

    def test_simple2(self, run):
        results = runs('hello world')
        assert len(results) == 0

        assert_called(run, ['hello', 'world'])

    def test_shell1(self, run):
        results = runs('hello world', shell=True, always_list=True)
        assert len(results) == 1

        assert_called(run, 'hello world', shell=True)

    def test_shell2(self, run):
        results = runs('hello world', shell=True)
        assert len(results) == 0

        assert_called(run, 'hello world', shell=True)

    def test_iterate(self, run):
        results = runs('hello world', iterate=True)
        run.assert_not_called()

        results = list(results)
        assert len(results) == 1
        assert len(run.mock_calls) == 1

        assert_called(run, ['hello', 'world'])

    def test_longer(self, run):
        lines = """
           line one   # with a comment
           line "two # not comment"
        """
        results = runs(lines, shell=True)
        assert len(results) == 2

        assert_called(run, 'line one', shell=True)
        assert_called(run, "line 'two # not comment'", shell=True)

    def test_continuation(self, run):
        lines = """
           line \\
           one # a comment
           line "two # not comment"
        """
        results = runs(lines, shell=True)
        assert len(results) == 2
        assert_called(run, 'line one', shell=True)
        assert_called(run, "line 'two # not comment'", shell=True)

    def test_continuation_error(self, run):
        lines = """
           line one   # with a comment\\
           line "two # not comment"
        """
        with self.assertRaises(ValueError) as m:
            runs(lines)
        err = ('Comments cannot contain a line continuation',)
        assert m.exception.args == err


class TestRunsActual(unittest.TestCase):
    def test_echo(self):
        results = runs.check_output('echo "a test"')
        assert results == 'a test\n'

    def test_many(self):
        lines = """
           echo "BEGIN"  # line one
           ls -a -1
           echo "END"
        """
        begin, ls, end = runs.check_output(lines)
        assert begin == 'BEGIN\n'
        assert end == 'END\n'
        diff = DIR.difference(ls.splitlines())
        print(*diff)
        assert not diff

    @tdir
    def test_shell(self):
        r = runs.check_output('echo BEGIN > foo.txt', shell=True)
        assert len(r) == 16
        p = Path('foo.txt')
        assert not p.exists()
        assert r == 'BEGIN > foo.txt\n'


DIR = {
    '.',
    '..',
    '.git',
    '.gitignore',
    '.travis.yml',
    'CHANGELOG',
    'LICENSE',
    'README.rst',
    'pyproject.toml',
    'runs',
    'test_runs.py',
    'tox.ini',
}
