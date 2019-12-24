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
from pattoo.configuration import ConfigPattoo, ConfigAgent, ConfigIngester


class TestConfiguration(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    config = ConfigPattoo()

    def test___init__(self):
        """Testing method init."""
        # Test
        pass

    def test_db_pool_size(self):
        """Testing method db_pool_size."""
        # Initialize key values
        expected = 10

        # Test
        result = self.config.db_pool_size()
        self.assertEqual(result, expected)

    def test_db_max_overflow(self):
        """Testing method db_max_overflow."""
        # Initialize key values
        expected = 20

        # Test
        result = self.config.db_max_overflow()
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
        expected = 'travis'

        # Test
        result = self.config.db_username()
        self.assertEqual(result, expected)

    def test_db_password(self):
        """Testing method db_password."""
        # Initialize key values
        if 'PATTOO_TRAVIS' in os.environ:
            expected = ''
        else:
            expected = 'K2nJ8kFdthEbuwXE'

        # Test
        result = self.config.db_password()
        self.assertEqual(result, expected)

    def test_db_name(self):
        """Testing method db_name."""
        # Initialize key values
        expected = 'pattoo_unittest'

        # Test
        result = self.config.db_name()
        self.assertEqual(result, expected)


class TestConfigAgent(unittest.TestCase):
    """Checks all ConfigAgent methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################
    config = ConfigAgent()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_ip_listen_address(self):
        """Testing function ip_listen_address."""
        # Initialize key values
        expected = '127.0.0.2'

        # Test
        result = self.config.ip_listen_address()
        self.assertEqual(result, expected)

    def test_ip_bind_port(self):
        """Testing function ip_bind_port."""
        # Initialize key values
        expected = 40201

        # Test
        result = self.config.ip_bind_port()
        self.assertEqual(result, expected)


class TestConfigAgent(unittest.TestCase):
    """Checks all ConfigIngester methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################
    config = ConfigIngester()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_ingester_interval(self):
        """Testing function ingester_interval."""
        # Initialize key values
        expected = 45

        # Test
        result = self.config.ingester_interval()
        self.assertEqual(result, expected)

    def test_multiprocessing(self):
        """Testing function multiprocessing."""
        # Initialize key values
        expected = True

        # Test
        result = self.config.multiprocessing()
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
