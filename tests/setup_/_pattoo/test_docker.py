#!/usr/bin/env python3
"""Tests for the docker script."""

import os
import unittest
import sys
import tempfile
import yaml

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

from tests.libraries.configuration import UnittestConfig
from setup._pattoo import docker


class Test_Docker(unittest.TestCase):
    """Checks all functions for the Pattoo docker script."""

    @classmethod
    def setUpClass(cls):
        """Declare class attributes for Unittesting."""
        cls.temp_dir = tempfile.mkdtemp()
        cls.agentd_dict = {
            'pattoo_api_agentd': {
                'ip_listen_address': '0.0.0.0',
                'ip_bind_port': 20201,
            }
        }
        cls.test_yaml = os.path.join(cls.temp_dir, 'test.yaml')

    def test_get_ports(self):
        """Testing method or function named "get_ports"."""
        # Initialize key variables
        test_yaml = os.path.join(self.temp_dir, 'test.yaml')
        with open(test_yaml, 'w+') as config:
            # Test with empty file
            with self.subTest():
                result = docker.get_ports(test_yaml)
                self.assertEqual(result, [])

            # Write config
            yaml.dump(self.agentd_dict, config, default_flow_style=False)

        # Retrieve ports from yaml file
        result = docker.get_ports(self.test_yaml)
        self.assertEqual(result, [20201])

    def test_expose_ports(self):
        """Testing method or function named "expose_ports"."""
        # Initialize key variables
        docker_file = os.path.join(self.temp_dir, 'Dockerfile')
        config_file = os.path.join(self.temp_dir, 'config.yaml')

        with open(config_file, 'w+') as config:
            # Write config
            yaml.dump(self.agentd_dict, config, default_flow_style=False)

        with open(docker_file, 'w+') as f_handle:
            f_handle.write('# Expose ports\n')

        docker.expose_ports(config_file, docker_file)
        with open(docker_file, 'r+') as f_handle:
            lines = f_handle.readlines()
            expose_line = 'EXPOSE 20201\n'
            result = expose_line in lines
            self.assertTrue(result)   


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
