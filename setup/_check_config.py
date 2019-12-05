#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import sys
import os


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
if EXEC_DIR.endswith('/pattoo/setup') is True:
    sys.path.append(ROOT_DIR)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)


# Pattoo imports
from pattoo_shared import files
from pattoo_shared import log


def check():
    """Ensure PIP3 packages are installed correctly.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    config_directory = os.environ['PATTOO_CONFIGDIR']

    # Print Status
    print('??: Checking configuration parameters.')

    # Check config
    config = files.read_yaml_files(config_directory)

    # Check main keys
    keys = ['main', 'db', 'pattoo-api-agentd']
    for key in keys:
        if key not in config:
            log_message = ('''\
Section "{}" not found in configuration file in directory {}. Please fix.\
'''.format(key, config_directory))
            log.log2die_safe(21000, log_message)

    # Check secondary keys
    secondaries = [
        'log_level', 'log_directory', 'cache_directory',
        'daemon_directory', 'polling_interval']
    secondary_key_check(config, 'main', secondaries)
    secondaries = [
        'db_pool_size', 'db_max_overflow', 'db_hostname', 'db_username',
        'db_password', 'db_name']
    secondary_key_check(config, 'db', secondaries)
    secondaries = ['api_listen_address', 'api_ip_bind_port']
    secondary_key_check(config, 'pattoo-api-agentd', secondaries)

    # Print Status
    print('OK: Configuration paramter check passed.')


def secondary_key_check(config, primary, secondaries):
    """Check secondary keys.

    Args:
        config: Configuration dict
        primary: Primary key
        secondaries: List of secondary keys

    Returns:
        None

    """
    # Check keys
    for key in secondaries:
        if key not in config[primary]:
            log_message = ('''\
Configuration file's "{}" section does not have a "{}" sub-section. \
Please fix.'''.format(primary, key))
            log.log2die_safe(21001, log_message)


def main():
    """Setup pattoo.

    Args:
        None

    Returns:
        None

    """
    # Check configuration
    check()


if __name__ == '__main__':
    # Run setup
    main()
