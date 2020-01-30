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
from pattoo_shared import files, configuration
from pattoo_shared import log


def check_pattoo_server():
    """Ensure server configuration exists.

    Args:
        None

    Returns:
        None

    """
    # Print Status
    print('??: Checking server configuration parameters.')

    ###########################################################################
    # Check server config
    ###########################################################################
    config_file = configuration.agent_config_filename('pattoo_server')
    config = files.read_yaml_file(config_file)

    # Check main keys
    keys = [
        'pattoo_db', 'pattoo_api_agentd', 'pattoo_apid', 'pattoo_ingesterd']
    for key in keys:
        if key not in config:
            log_message = ('''\
Section "{}" not found in {} configuration file. Please fix.\
'''.format(key, config_file))
            log.log2die_safe(20141, log_message)

    # Check secondary keys for 'pattoo_db'
    secondaries = [
        'db_pool_size', 'db_max_overflow', 'db_hostname', 'db_username',
        'db_password', 'db_name']
    secondary_key_check(config, 'pattoo_db', secondaries)

    # Check secondary keys for 'pattoo_api_agentd'
    secondaries = ['ip_listen_address', 'ip_bind_port']
    secondary_key_check(config, 'pattoo_api_agentd', secondaries)

    # Check secondary keys for 'pattoo_apid'
    secondaries = ['ip_listen_address', 'ip_bind_port']
    secondary_key_check(config, 'pattoo_apid', secondaries)

    # Print Status
    print('OK: Server configuration parameter check passed.')


def check_pattoo_client():
    """Ensure client configuration exists.

    Args:
        None

    Returns:
        None

    """
    # Print Status
    print('??: Checking client configuration parameters.')

    ###########################################################################
    # Check client config
    ###########################################################################
    config_file = configuration.agent_config_filename('pattoo')
    config = files.read_yaml_file(config_file)

    # Check main keys
    keys = ['pattoo']
    for key in keys:
        if key not in config:
            log_message = ('''\
Section "{}" not found in {} configuration file. Please fix.\
'''.format(key, config_file))
            log.log2die_safe(20090, log_message)

    # Check secondary keys for 'pattoo'
    secondaries = [
        'log_level', 'log_directory', 'cache_directory', 'daemon_directory']
    secondary_key_check(config, 'pattoo', secondaries)

    # Print Status
    print('OK: Client configuration parameter check passed.')


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
            log.log2die_safe(20091, log_message)


def main():
    """Setup pattoo.

    Args:
        None

    Returns:
        None

    """
    # Check configuration
    check_pattoo_server()
    check_pattoo_client()


if __name__ == '__main__':
    # Run setup
    main()
