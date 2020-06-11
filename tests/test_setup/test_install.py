
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
from setup.installation_lib.install import _log, check_config
from setup.installation_lib.install import check_pip3
from tests.libraries.configuration import UnittestConfig
#from setup.install import _log


class Test_Install(unittest.TestCase):
    """Checks all functions for the Pattoo install script."""

    def test__init__(self):
        """Unnittest to test the __init__ function."""
        pass

    def test_install_missing(self):
        """Unittest to test the install_missing function."""
        
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


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    print(os.environ['PATTOO_CONFIGDIR'])
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
