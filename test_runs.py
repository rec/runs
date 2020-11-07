# from unittest import mock
# import tdir

import runs
import unittest

FILENAME = 'a_file.txt'


# @mock.patch('runs.subprocess.call', autospec=True)
class TestRuns(unittest.TestCase):
    #   @tdir(FILENAME)
    def test_existing(self):
        assert runs
