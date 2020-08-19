#!/usr/bin/env/python3
"""Test pattoo configuration script."""

from unittest.mock import patch
import os
import getpass
import grp
import unittest
import sys
import tempfile
import yaml
import secrets

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

from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from tests.libraries.configuration import UnittestConfig
from setup._pattoo.configure import read_config, prompt, create_user
from setup._pattoo.configure import pattoo_server_config, pattoo_config
from setup._pattoo.configure import _mkdir, group_exists, user_exists
from setup._pattoo.configure import check_pattoo_server, check_pattoo_client


class TestConfigure(unittest.TestCase):
    """Checks all functions for the Pattoo config script."""

    def test__init__(self):
        """Unittest to test the __init__ function."""
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
            # Creating grp.struct object
            grp_struct = grp.getgrgid(os.getgid())
            result = group_exists(grp_struct.gr_name)
            self.assertEqual(result, expected)

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
            result = user_exists(getpass.getuser())
            self.assertEqual(result, expected)

    def test_pattoo_server_config(self):
        """Unittest to test the pattoo_server_config function."""
        # Initialize key variables
        expected = {
            'pattoo_db': {
                'db_pool_size': 10,
                'db_max_overflow': 20,
                'db_hostname': 'localhost',
                'db_username': 'pattoo',
                'db_password': 'password',
                'db_name': 'pattoo'
            },
            'pattoo_api_agentd': {
                'ip_listen_address': '0.0.0.0',
                'ip_bind_port': 20201,
            },
            'pattoo_apid': {
                'ip_listen_address': '0.0.0.0',
                'ip_bind_port': 20202,
                'jwt_secret_key': 'test_text',
                'acesss_token_exp': '15_m',
                'refresh_token_exp': '1_D'
            },
            'pattoo_ingesterd': {
                'ingester_interval': 3600,
                'batch_size': 500,
                'graceful_timeout': 10
            }
        }

        # Initialize temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "pattoo_server.yaml")
            # Create config file
            pattoo_server_config(temp_dir, False)

            # Extract pattoo_server config
            result = read_config(file_path, None)

            # Changing jwt_secret_key to match in both expected and result
            # configs
            jwt_secret_key = secrets.token_urlsafe(MAX_KEYPAIR_LENGTH)
            expected['pattoo_apid']['jwt_secret_key'] = jwt_secret_key
            result['pattoo_apid']['jwt_secret_key'] = jwt_secret_key

            # Asserting that result and expected are the same
            self.assertEqual(result, expected)

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
