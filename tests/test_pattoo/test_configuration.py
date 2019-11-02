#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo" directory. Please fix.''')
    sys.exit(2)

from tests.libraries.configuration import UnittestConfig
from pattoo import configuration


class TestConfiguration(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    config = configuration.Config()

    def test___init__(self):
        """Testing method init."""
        # Test
        pass

    def test_sqlalchemy_pool_size(self):
        """Testing method sqlalchemy_pool_size."""
        # Initialize key values
        expected = 10

        # Test
        result = self.config.sqlalchemy_pool_size()
        self.assertEqual(result, expected)

    def test_sqlalchemy_max_overflow(self):
        """Testing method sqlalchemy_max_overflow."""
        # Initialize key values
        expected = 20

        # Test
        result = self.config.sqlalchemy_max_overflow()
        self.assertEqual(result, expected)

    def test_db_hostname(self):
        """Testing method db_hostname."""
        # Initialize key values
        expected = 'localhost'

        # Test
        result = self.config.db_hostname()
        self.assertEqual(result, expected)

    def test_db_username(self):
        """Testing method db_username."""
        # Initialize key values
        expected = 'pattoo_username'

        # Test
        result = self.config.db_username()
        self.assertEqual(result, expected)

    def test_db_password(self):
        """Testing method db_password."""
        # Initialize key values
        expected = 'pattoo_password'

        # Test
        result = self.config.db_password()
        self.assertEqual(result, expected)

    def test_db_name(self):
        """Testing method db_name."""
        # Initialize key values
        expected = 'pattoo_db'

        # Test
        result = self.config.db_name()
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
