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
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from tests.libraries.configuration import UnittestConfig

from pattoo_shared.constants import PATTOO_API_SITE_PREFIX
from pattoo.constants import PATTOO_API_WEB_NAME
from pattoo.constants import PATTOO_API_WEB_PROXY
from pattoo.constants import PATTOO_API_AGENT_NAME
from pattoo.constants import PATTOO_API_AGENT_PROXY
from pattoo.constants import PATTOO_INGESTERD_NAME
from pattoo.constants import PATTOO_INGESTER_NAME
from pattoo.constants import PATTOO_INGESTER_SCRIPT


class TestConstants(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_constants(self):
        """Testing constants."""
        # Test pattoo API constants
        self.assertEqual(
            PATTOO_API_WEB_NAME, 'pattoo_apid')
        self.assertEqual(
            PATTOO_API_WEB_PROXY,
            '{}-gunicorn'.format(PATTOO_API_WEB_NAME))
        self.assertEqual(
            PATTOO_API_AGENT_NAME, 'pattoo_api_agentd')
        self.assertEqual(
            PATTOO_API_AGENT_PROXY,
            '{}-gunicorn'.format(PATTOO_API_AGENT_NAME))
        self.assertEqual(
            PATTOO_INGESTERD_NAME, 'pattoo_ingesterd')
        self.assertEqual(
            PATTOO_INGESTER_NAME, 'pattoo_ingester')
        self.assertEqual(
            PATTOO_INGESTER_SCRIPT, 'pattoo_ingester.py')


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
