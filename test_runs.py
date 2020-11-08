from unittest import mock
import runs
import unittest


def assert_called(mock, *args, **kwds):
    mock.assert_any_call(*args, encoding='utf8', **kwds)


@mock.patch('runs.subprocess.run', autospec=True)
class TestRunsMock(unittest.TestCase):
    def test_simple(self, run):
        results = runs('hello world')
        assert len(results) == 1

        assert_called(run, ['hello', 'world'])

    def test_shell(self, run):
        results = runs('hello world', shell=True)
        assert len(results) == 1

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


class TestRunsActual(unittest.TestCase):
    def test_echo(self):
        results = runs.check_output('echo "a test"')
        assert results == ['a test\n']

    def test_many(self):
        lines = """
           echo "BEGIN"  # line one
           ls -a -1
           echo "END"
        """
        begin, ls, end = runs.check_output(lines)
        assert begin == 'BEGIN\n'
        assert end == 'END\n'
        assert DIR.issubset(ls.splitlines())


DIR = {
    '.',
    '..',
    '.coveragerc',
    '.git',
    '.gitignore',
    '.travis.yml',
    'CHANGELOG',
    'LICENSE',
    'README.rst',
    'pyproject.toml',
    'requirements.txt',
    'runs.py',
    'setup.cfg',
    'setup.py',
    'test_requirements.txt',
    'test_runs.py',
    'tox.ini',
}
