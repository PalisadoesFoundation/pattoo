#!/usr/bin/env python3
"""Test pattoo db script."""
from tests.libraries.configuration import UnittestConfig
import os
import getpass
import unittest
import sys
import tempfile
import yaml

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}test_setup'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


class TestDb(unittest.TestCase):
    """Checks all functions for the Pattoo db script."""

    def test__init__(self):
        """Unittest to test the __init__ function."""
        pass

    def test_insertions(self):
        """Unittest to test the insertions function."""
        pass

    def test_mysql(self):
        """Unittest to test the _mysql function."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
