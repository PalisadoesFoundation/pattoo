#!/usr/bin/env/python3
"""Test pattoo configuration script."""

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

from setup.configure.configure import already_written, set_configdir
from setup.configure.configure import read_config
from setup.configure.configure import _mkdir, _log


class Test_Configure(unittest.TestCase):
    """Checks all functions for the Pattoo config script."""

    def test__init__(self):
        """Unnittest to test the __init__ function."""
        pass

    def test_set_configuration_directory(self):
        """Unittest to test the set_configdir function ."""
        expected = True
        results = []
        config_path = '/opt/pattoo/config'
        env_variable = 'export PATTOO_CONFIGDIR={}'.format(config_path)
        file_path = os.path.join(os.path.join(
            os.path.expanduser('~')), '.bash_profile')
        set_configdir(file_path)
        with open(file_path, 'r') as file:
            for line in file:
                if line == env_variable:
                    results.append(True)
        results.append(os.environ['PATTOO_CONFIGDIR']) == config_path
        result = all(results)
        self.assertEqual(result, expected)

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
            result = read_config(file_path, expected)
            result == expected
            self.assertEqual(result == expected, True)

    def test_already_written(self):
        """Unittest to test the already_written function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, 'test_file.txt')
            line = 'export PATTOO_CONFIGDIR=/opt/Calico/config'
            with open(file_path, 'w') as file:
                file.write(line)
            expected = True
            result = already_written(file_path, line)
            self.assertEqual(expected, result)

    def test_mkdir(self):
        """Unitttest to test the _mkdir function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = os.path.join(temp_dir, 'test_dir')
            _mkdir(directory)
            expected = True
            result = os.path.isdir(directory)
            self.assertEqual(expected, result)

    def test_log(self):
        """Unittest to test the _log function."""
        with self.assertRaises(SystemExit) as cm:
            _log("Test Error Message")
        self.assertEqual(cm.exception.code, 3)

    def test_promt(self):
        """Unittest to test the prompt function."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
