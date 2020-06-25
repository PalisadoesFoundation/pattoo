#!/usr/bin/env/python3
"""Test pattoo configuration script."""

from tests.libraries.configuration import UnittestConfig
from unittest.mock import patch
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
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from setup._pattoo.configure import already_written, set_configdir
from setup._pattoo.configure import read_config, prompt, create_user
from setup._pattoo.configure import _mkdir, group_exists, user_exists
from setup._pattoo.configure import check_pattoo_server, check_pattoo_client


class TestConfigure(unittest.TestCase):
    """Checks all functions for the Pattoo config script."""

    def test__init__(self):
        """Unnittest to test the __init__ function."""
        pass

    def test_group_exists(self):
        """Unittest to test the group exists function."""
        # Test case for when the group does not exist
        with self.subTest():
            expected = False
            # Generating random string
            result = group_exists(str(os.urandom(5)))
            self.assertEqual(result, expected)
        with self.subTest():
            # Test case for when the group exists
            expected = True
            result = group_exists(os.getgid())

    def test_user_exists(self):
        """Unittest to test the user_exists function."""
        # Test case for when the user does not exist
        with self.subTest():
            expected = False
            result = user_exists(str(os.urandom(5)))
            self.assertEqual(result, expected)
        # Test case for when the user does exist
        with self.subTest():
            expected = True
            result = user_exists(os.getuid())
            self.assertEqual(result, expected)

    def test_check_pattoo_server(self):
        """Unittest to test the check_pattoo_server function."""
        pass

    def test_check_pattoo_client(self):
        """Unittest to test the check_pattoo_client function."""
        pass

    def test_pattoo_server_config(self):
        """Unittest to test the pattoo_server_config function."""
        pass

    def test_read_config(self):
        """Unittest to test the read_server_config function."""
        opt_directory = '{0}opt{0}pattoo'.format(os.sep)
        run_dir = (
            '/var/run/pattoo' if getpass.getuser() == 'root'else opt_directory)
        default_config = {
            'pattoo': {
                'language': 'en',
                'log_directory': (
                    '{1}{0}pattoo{0}log'.format(os.sep, opt_directory)),
                'log_level': 'debug',
                'cache_directory': (
                    '{1}{0}pattoo{0}cache'.format(os.sep, opt_directory)),
                'daemon_directory': (
                    '{1}{0}pattoo{0}daemon'.format(os.sep, opt_directory)),
                'system_daemon_directory': ('''\
                    /var/run/pattoo''' if getpass.getuser() == 'root' else (
                    '{1}{0}pattoo{0}daemon'.format(os.sep, run_dir)))
            },
            'pattoo_agent_api': {
                'ip_address': '127.0.0.1',
                'ip_bind_port': 20201
            },
            'pattoo_web_api': {
                'ip_address': '127.0.0.1',
                'ip_bind_port': 20202,
            }
        }
        expected = default_config
        # Create temporary directory using the temp file package
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "pattoo_temp_config.yaml")
            # Dumps default configuration to file in temp directory
            with open(file_path, 'w+') as temp_config:
                yaml.dump(expected, temp_config, default_flow_style=False)
            config = read_config(file_path, expected)
            result = config == expected
            self.assertEqual(result, True)

    def test_mkdir(self):
        """Unitttest to test the _mkdir function."""
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = os.path.join(temp_dir, 'test_dir')
            _mkdir(directory)
            expected = True
            result = os.path.isdir(directory)
            self.assertEqual(result, expected)

    @patch('builtins.input', return_value='')
    def test_prompt_default(self, mock_patch):
        """Unittest to test the prompt function with no data."""
        result = prompt('test', 't', 'test')
        expected = 'test'
        self.assertEqual(result, expected)

    @patch('builtins.input', return_value='somedata')
    def test_prompt_data(self, mock_patch):
        """Unittest to test the prompt function with data."""
        result = prompt('test', 't', 'testo')
        expected = 'somedata'
        self.assertEqual(result, expected)

    @patch('builtins.input', return_value='')
    def test_prompt_dir(self, mock_patch):
        """Unittest to test the prompt function with default values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = os.path.join(temp_dir, 'test_dir')
            prompt('test', 'test_directory', directory)
            result = os.path.isdir(directory)
            expected = True
            self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
