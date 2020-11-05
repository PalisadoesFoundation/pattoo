#!/usr/bin/env python3
"""Test pattoo installation shared script"""

import os
import unittest
import sys
import tempfile
import yaml
import distro
from random import random

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
from pattoo_shared import data
from pattoo_shared.installation.systemd import _filepaths, copy_service_files, symlink_dir
from pattoo_shared.installation.systemd import _get_runtime_directory, _check_symlinks
from pattoo_shared.installation.systemd import update_environment_strings


class Test_Systemd(unittest.TestCase):
    """Checks all functions and methods."""

    def test__filepaths(self):
        """Testing method or function named "_filepaths"."""
        # Initialize temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, 'test_file.txt')

            # Create file
            with open(file_path, 'w+') as test_file:
                test_file.write('this is a test')
            expected = [file_path]
            result = _filepaths(temp_dir)
            self.assertEqual(expected, result)

    def test_copy_service_files(self):
        """Testing method or function named "copy_service_files"."""
        # Initialize key variables
        service_directory = '{1}/{0}systemd/system'.format('setup/', ROOT_DIR)
        files = os.listdir(service_directory)

        # Open agentd service file for reading
        with open(os.path.join(service_directory, files[0]), 'r') as agentd:
            pattoo_api_agentd = agentd.readlines()

        # Open ingesterd service file for reading
        with open(os.path.join(service_directory, files[1]), 'r') as ingesterd:
            pattoo_ingesterd = ingesterd.readlines()

        # Open apid service file for reading
        with open(os.path.join(service_directory, files[2]), 'r') as apid:
            pattoo_apid = apid.readlines()

        # Put all service file contents into a list
        expected_contents = sorted([
                pattoo_api_agentd, pattoo_ingesterd, pattoo_apid])

        # Initialize temporary directory to copy service files
        with tempfile.TemporaryDirectory() as temp_dir:

            # Initialize as set to ensure equality
            expected = set([
                os.path.join(temp_dir, 'pattoo_api_agentd.service'),
                os.path.join(temp_dir, 'pattoo_apid.service'),
                os.path.join(temp_dir, 'pattoo_ingesterd.service')
            ])

            copied_service_files = copy_service_files(
                                                temp_dir, service_directory)

            # Ensure service files are copied to directory
            result = set(copied_service_files)
            self.assertEqual(result, expected)

            # Ensure file contents are preserved
            with open(os.path.join(
                    service_directory,
                    copied_service_files[0]), 'r') as agentd:
                temp_api_agentd = agentd.readlines()

            with open(os.path.join(
                    service_directory,
                    copied_service_files[1]), 'r') as ingesterd:
                temp_ingesterd = ingesterd.readlines()

            with open(os.path.join(
                    service_directory,
                    copied_service_files[2]), 'r') as apid:
                temp_apid = apid.readlines()

            actual_contents = sorted(
                [temp_api_agentd, temp_ingesterd, temp_apid])

            # Ensure contents are equal
            self.assertEqual(expected_contents, actual_contents)

    def test__symlink_dir(self):
        """Testing method or function named "_symlink_dir"."""
        # Initialise key variables
        linux_distro = distro.linux_distribution()[0].lower()
        etc_dir = '/etc/systemd/system/multi-user.target.wants'

        if linux_distro == 'ubuntu':
            expected = '/lib/systemd/system'
        else:
            # Expected directory for CentOS
            expected = '/usr/lib/systemd/system'

        # Test directory without symlinks
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(SystemExit) as cm_:
                symlink_dir(temp_dir)
            self.assertEqual(cm_.exception.code, 3)

        # Test directory with expected symlinks
        result = symlink_dir(etc_dir)
        self.assertEqual(result, expected)

    def test__update_environment_strings(self):
        """Testing method or function named "_update_environment_strings"."""
        # Initialize key variables
        config_dir = os.environ.get('PATTOO_CONFIGDIR')
        service_directory = '{1}/{0}systemd/system'.format('setup/', ROOT_DIR)
        log_directory = tempfile.mkdtemp()
        cache_directory = tempfile.mkdtemp()
        daemon_directory = tempfile.mkdtemp()

        default_config = {
            'pattoo': {
                'language': 'en',
                'log_directory': (
                    log_directory),
                'log_level': 'debug',
                'cache_directory': (
                    cache_directory),
                'daemon_directory': (
                    daemon_directory),
                'system_daemon_directory': '/var/run/pattoo'
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

        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize key variables
            config_dir = os.path.join(temp_dir, 'pattoo-config')

            # If the config dir doesn't exist it gets created
            if os.path.isdir(config_dir) is False:
                os.mkdir(config_dir)

            # Dump config to pattoo.yaml
            with open(os.path.join(
                    config_dir, 'pattoo.yaml'), 'w+') as config:
                yaml.dump(default_config, config, default_flow_style=False)

            # Initialize as set to ensure equality
            expected = set([
                'pattoo-config',
                'pattoo_api_agentd.service',
                'pattoo_apid.service',
                'pattoo_ingesterd.service'
            ])

            # Place service files into temp dir
            destination_filepaths = copy_service_files(
                temp_dir, service_directory)
            update_environment_strings(
                filepaths=destination_filepaths,
                install_dir=ROOT_DIR,
                config_dir=config_dir,
                username='pattoo',
                group='pattoo'
            )

            # Ensure files are copied into temp directory
            copied_files = os.listdir(temp_dir)
            result = set(copied_files)
            self.assertEqual(result, expected)

    def test__get_runtime_directory_default(self):
        """Testing method or function named "_get_runtime_directory"."""
        # Initialize key variables
        default_config = {
            'pattoo': {
                'language': 'en',
                'log_directory': (
                    '/var/log/pattoo'),
                'log_level': 'debug',
                'cache_directory': (
                    '/opt/pattoo-cache'),
                'daemon_directory': (
                    '/opt/pattoo-daemon'),
                'system_daemon_directory': '/var/run/pattoo'
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

        expected = ('/var/run/pattoo', 'pattoo')

        # Retrieve runtime directory from temp directory
        with tempfile.TemporaryDirectory() as temp_dir:

            # Test with default system daemon directory
            with open(os.path.join(temp_dir, 'pattoo.yaml'), 'w+') as config:
                yaml.dump(default_config, config, default_flow_style=False)
                result = _get_runtime_directory(temp_dir)
            self.assertEqual(expected, result)

    def test__get_runtime_undefined_file(self):
        """Testing method or function named "_get_runtime_directory"."""
        with self.assertRaises(SystemExit) as cm_:
            # Generate random directory name
            _get_runtime_directory(data.hashstring(str(random())))
        self.assertEqual(cm_.exception.code, 3)

    def test__get_runtime_directory_no_systemd(self):
        """Testing method or function named "_get_runtime_directory"."""
        # Initialize key variables
        fake_config = {
            'pattoo': {
                    'language': 'en',
                    'log_directory': (
                        '/var/log/pattoo'),
                    'log_level': 'debug',
                    'cache_directory': (
                        '/opt/pattoo-cache'),
                    'daemon_directory': (
                        '/opt/pattoo-daemon')
                }
            }

        # Retrieve runtime directory from temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(os.path.join(temp_dir, 'pattoo.yaml'), 'w+') as config:
                yaml.dump(fake_config, config, default_flow_style=False)

            # Test without system daemon directory
            with self.assertRaises(SystemExit) as cm_:
                _get_runtime_directory(temp_dir)
            self.assertEqual(cm_.exception.code, 3)

    def test___check_symlinks(self):
        """Testing method or function named "_get_runtime_directory"."""
        # Initialize key variables
        daemons = [
            'pattoo_apid',
            'pattoo_api_agentd',
            'pattoo_ingesterd'
            ]
        result = []

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create target directory
            target_dir = os.path.join(temp_dir, 'test_symlink')
            os.mkdir(target_dir)

            # Check for symlinks and sudo access
            with self.assertRaises(SystemExit) as cm_:
                _check_symlinks(temp_dir, daemons)
            self.assertEqual(cm_.exception.code, 2)

        self.assertTrue(all(result))


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
