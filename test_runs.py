from unittest import mock
import runs
import unittest


@mock.patch('runs.subprocess.run', autospec=True)
class TestRuns(unittest.TestCase):
    def test_simple(self, run):
        results = list(runs('hello world'))
        run.assert_called_once_with(['hello', 'world'])
        assert len(results) == 1

    def test_shell(self, run):
        results = list(runs('hello world', shell=True))
        run.assert_called_once_with('hello world', shell=True)
        assert len(results) == 1
