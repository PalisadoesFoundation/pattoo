#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
if EXEC_DIR.endswith('/pattoo-shared/tests/test_pattoo_shared') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo-shared/tests/test_pattoo_shared" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from tests.libraries.configuration import UnittestConfig

from pattoo_shared.constants import PATTOO_API_SITE_PREFIX
from pattoo.constants import PATTOO_API_WEB_PREFIX
from pattoo.constants import PATTOO_API_WEB_EXECUTABLE
from pattoo.constants import PATTOO_API_WEB_PROXY
from pattoo.constants import PATTOO_API_WEB_REST_PREFIX


class TestConstants(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_constants(self):
        """Testing constants."""
        # Test pattoo API constants
        self.assertEqual(
            PATTOO_API_WEB_PREFIX, '{}/web'.format(PATTOO_API_SITE_PREFIX))
        self.assertEqual(
            PATTOO_API_WEB_EXECUTABLE, 'pattoo-apid')
        self.assertEqual(
            PATTOO_API_WEB_PROXY,
            '{}-gunicorn'.format(PATTOO_API_WEB_EXECUTABLE))


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
