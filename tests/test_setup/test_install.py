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

from setup.install import check_pip3, check_database, check_config
from setup.install import _log


class Test_Install(unittest.TestCase):
    """Checks all functions for the Pattoo install script."""

    def test__init__(self):
        """Unnittest to test the __init__ function."""
        pass

    def test_install_missing(self):
        """Unittest to test the install_missing function."""
        pass

    def test_check_database(self):
        """Unittest to test the check_database function."""
        expected = True
        result = check_database()
        self.assertEqual(result, expected)

    def test_check_config(self):
        """Unittest to test the check_config function."""
        expected = True
        result = check_config()
        self.assertEqual(result, expected)

    def test_check_pip3(self):
        """Unittest to test the check_pip3 function."""
        expected = True
        result = check_pip3()
        self.assertEqual(result, expected)

    def test_log(self):
        """Unittest to test the _log function."""
        with self.assertRaises(SystemExit) as cm:
            _log("Test Error Message")
        self.assertEqual(cm.exception.code, 3)
