#!/usr/bin/env python3
"""Test pattoo db script."""
from tests.libraries.configuration import UnittestConfig
import os
import unittest
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}setup_{0}_pattoo'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
    sys.path.append(os.path.join(ROOT_DIR, 'setup'))
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


class TestDb(unittest.TestCase):
    """Checks all functions for the Pattoo db script."""

    def test_insertions(self):
        """Testing method or function named "insertions"."""
        pass

    def test__insert_language(self):
        """Testing method or function named "_insert_language"."""
        pass

    def test__insert_pair_xlate_group(self):
        """Testing method or function named "_insert_pair_xlate_group"."""
        pass

    def test__insert_agent_xlate(self):
        """Testing method or function named "_insert_agent_xlate"."""
        pass

    def test__insert_user(self):
        """Testing method or function named "_insert_user"."""
        pass

    def test__insert_chart(self):
        """Testing method or function named "_insert_chart"."""
        pass

    def test__insert_favorite(self):
        """Testing method or function named "_insert_favorite"."""
        pass

    def test__mysql(self):
        """Testing method or function named "_mysql"."""
        pass

    def test_install(self):
        """Testing method or function named "install"."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
