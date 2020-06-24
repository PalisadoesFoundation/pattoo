
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
    sys.path.append(os.path.join(ROOT_DIR, 'setup'))
    # Try catch block to automatically set the config dir if it isn't already
    # set
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from setup._pattoo.packages import install_pip3, install_missing
from tests.libraries.configuration import UnittestConfig


class Test_Install(unittest.TestCase):
    """Checks all functions for the Pattoo install script."""

    def test__init__(self):
        """Unnittest to test the __init__ function."""
        pass

    def test_install_missing(self):
        """Unittest to test the install_missing function."""
        expected = True
        with tempfile.TemporaryDirectory() as temp_dir:
            result = install_missing('numpy', temp_dir, False)
            sys.path.append(temp_dir)
            self.assertEqual(result, expected)

    def test_install_missing_fail(self):
        """Test case that would cause the install_missing function to fail."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(SystemExit) as cm:
                install_missing('this does not exist', temp_dir, False)
            self.assertEqual(cm.exception.code, 2)

    def test_check_pip3(self):
        """Unittest to test the check_pip3 function."""
        expected = True
        result = install_pip3(False, ROOT_DIR)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
