#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
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

from tests.libraries.configuration import UnittestConfig
from pattoo.configuration import ConfigAPId, ConfigAgentAPId, ConfigIngester


class TestConfiguration(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    config = ConfigAPId()

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

    def test_daemon_directory(self):
        """Test pattoo_shared.Config inherited method daemon_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.daemon_directory()

    def test_log_directory(self):
        """Test pattoo_shared.Config inherited method log_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.log_directory()

    def test_log_file(self):
        """Test pattoo_shared.Config inherited method log_file."""
        # Initialize key values
        expected = '{1}{0}pattoo.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file()
        self.assertEqual(result, expected)

    def test_log_file_api(self):
        """Test pattoo_shared.Config inherited method log_file_api."""
        # Initialize key values
        expected = '{1}{0}pattoo-api.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_api()
        self.assertEqual(result, expected)

    def test_log_level(self):
        """Test pattoo_shared.Config inherited method log_level."""
        # Initialize key values
        expected = 'debug'

        # Test
        result = self.config.log_level()
        self.assertEqual(result, expected)

    def test_log_file_daemon(self):
        """Test pattoo_shared.Config inherited method log_file_daemon."""
        # Initialize key values
        expected = '{1}{0}pattoo-daemon.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_daemon()
        self.assertEqual(result, expected)

    def test_cache_directory(self):
        """Test pattoo_shared.Config inherited method cache_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.cache_directory()

    def test_agent_cache_directory(self):
        """Test pattoo_shared.Config inherited method agent_cache_directory."""
        # Initialize key values
        agent_id = 123
        expected = '{1}{0}{2}'.format(
            os.sep, self.config.cache_directory(), agent_id)

        # Test
        result = self.config.agent_cache_directory(agent_id)
        self.assertEqual(result, expected)


class TestConfigAgentAPId(unittest.TestCase):
    """Checks all ConfigAgentAPId methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################
    config = ConfigAgentAPId()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_ip_listen_address(self):
        """Testing function ip_listen_address."""
        # Initialize key values
        expected = '127.0.0.1'

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

    def test_daemon_directory(self):
        """Test pattoo_shared.Config inherited method daemon_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.daemon_directory()

    def test_log_directory(self):
        """Test pattoo_shared.Config inherited method log_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.log_directory()

    def test_log_file(self):
        """Test pattoo_shared.Config inherited method log_file."""
        # Initialize key values
        expected = '{1}{0}pattoo.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file()
        self.assertEqual(result, expected)

    def test_log_file_api(self):
        """Test pattoo_shared.Config inherited method log_file_api."""
        # Initialize key values
        expected = '{1}{0}pattoo-api.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_api()
        self.assertEqual(result, expected)

    def test_log_level(self):
        """Test pattoo_shared.Config inherited method log_level."""
        # Initialize key values
        expected = 'debug'

        # Test
        result = self.config.log_level()
        self.assertEqual(result, expected)

    def test_log_file_daemon(self):
        """Test pattoo_shared.Config inherited method log_file_daemon."""
        # Initialize key values
        expected = '{1}{0}pattoo-daemon.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_daemon()
        self.assertEqual(result, expected)

    def test_cache_directory(self):
        """Test pattoo_shared.Config inherited method cache_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.cache_directory()

    def test_agent_cache_directory(self):
        """Test pattoo_shared.Config inherited method agent_cache_directory."""
        # Initialize key values
        agent_id = 123
        expected = '{1}{0}{2}'.format(
            os.sep, self.config.cache_directory(), agent_id)

        # Test
        result = self.config.agent_cache_directory(agent_id)
        self.assertEqual(result, expected)

    def test_api_email_address(self):
        """Test api email address retrieval"""
        # Test from yaml file
        result = self.config.api_email_address()
        expected = 'test_api@example.org'

        self.assertEqual(result, expected)


class TestConfigIngester(unittest.TestCase):
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

    def test_batch_size(self):
        """Testing function batch_size."""
        # Initialize key values
        expected = 1503

        # Test
        result = self.config.batch_size()
        self.assertEqual(result, expected)

    def test_daemon_directory(self):
        """Test pattoo_shared.Config inherited method daemon_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.daemon_directory()

    def test_log_directory(self):
        """Test pattoo_shared.Config inherited method log_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.log_directory()

    def test_log_file(self):
        """Test pattoo_shared.Config inherited method log_file."""
        # Initialize key values
        expected = '{1}{0}pattoo.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file()
        self.assertEqual(result, expected)

    def test_log_file_api(self):
        """Test pattoo_shared.Config inherited method log_file_api."""
        # Initialize key values
        expected = '{1}{0}pattoo-api.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_api()
        self.assertEqual(result, expected)

    def test_log_level(self):
        """Test pattoo_shared.Config inherited method log_level."""
        # Initialize key values
        expected = 'debug'

        # Test
        result = self.config.log_level()
        self.assertEqual(result, expected)

    def test_log_file_daemon(self):
        """Test pattoo_shared.Config inherited method log_file_daemon."""
        # Initialize key values
        expected = '{1}{0}pattoo-daemon.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_daemon()
        self.assertEqual(result, expected)

    def test_cache_directory(self):
        """Test pattoo_shared.Config inherited method cache_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.cache_directory()

    def test_agent_cache_directory(self):
        """Test pattoo_shared.Config inherited method agent_cache_directory."""
        # Initialize key values
        agent_id = 123
        expected = '{1}{0}{2}'.format(
            os.sep, self.config.cache_directory(), agent_id)

        # Test
        result = self.config.agent_cache_directory(agent_id)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
