#!/usr/bin/env/python3
"""Test pattoo installation shared script"""


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

from tests.libraries.configuration import UnittestConfig
from setup._pattoo import shared


class Test_Shared(unittest.TestCase):
    """Checks all functions for the Pattoo config script."""

    def test_log(self):
        """Unittest to test the _log function."""
        with self.assertRaises(SystemExit) as cm_:
            shared.log("Test Error Message")
        self.assertEqual(cm_.exception.code, 3)

    def test_run_script(self):
        """Unittest to test the _run_script function."""
        # Test case where the script should fail and exit with 2
        with self.subTest():
            with self.assertRaises(SystemExit) as cm_:
                shared.run_script("this will exit with 2")
            self.assertEqual(cm_.exception.code, 2)

        # Test case where the script should print "this works" to the console
        with self.subTest():
            expected = 0
            result = shared.run_script("echo this works")[0]
            self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
