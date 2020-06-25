#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import sys
import os
import shutil
import subprocess
import traceback
import grp
import pwd
from pathlib import Path
import getpass
try:
    import yaml
except:
    print('Install the Python3 "pyyaml" package, then run this script again')
    sys.exit(2)
# Pattoo libraries
from pattoo_shared import files, configuration
from pattoo_shared import log
from _pattoo import shared


def _run_script(cli_string, die=True):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        cli_string: String of command to run
        die: Exit with error if True

    Returns:
        (returncode, stdoutdata, stderrdata):
            Execution code, STDOUT output and STDERR output.

    """
    # Initialize key variables
    messages = []
    stdoutdata = ''.encode()
    stderrdata = ''.encode()
    returncode = 1

    # Say what we are doing
    print('Running Command: "{}"'.format(cli_string))

    # Run update_targets script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    try:
        process = subprocess.Popen(
            do_command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()
        returncode = process.returncode
    except:
        (exc_type, exc_value, exc_traceback) = sys.exc_info()
        messages.append('''\
Bug: Exception Type:{}, Exception Instance: {}, Stack Trace Object: {}]\
    '''.format(exc_type, exc_value, exc_traceback))
        messages.append(traceback.format_exc())

    # Crash if the return code is not 0
    if bool(returncode) is True:
        # Print the Return Code header
        messages.append(
            'Return code:{}'.format(returncode)
        )

        # Print the STDOUT
        for line in stdoutdata.decode().split('\n'):
            messages.append(
                'STDOUT: {}'.format(line)
            )

        # Print the STDERR
        for line in stderrdata.decode().split('\n'):
            messages.append(
                'STDERR: {}'.format(line)
            )

        # Log message
        print("messages: {})".format(messages))
        if messages != []:
            for log_message in messages:
                print(log_message)

            if bool(die) is True:
                # All done
                sys.exit(2)

    # Return
    return (returncode, stdoutdata, stderrdata)


def pattoo_config(config_directory, prompt_value):
    """Create pattoo.yaml file.

    Args:
        config_directory: Configuration directory

    Returns:
        None
    """
    # Initialize key variables
    filepath = '{}{}pattoo.yaml'.format(config_directory, os.sep)
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

    # Say what we are doing
    print('\nConfiguring {} file.\n'.format(filepath))

    # Get configuration

    config = read_config(filepath, default_config)
    for section, item in sorted(config.items()):
        for key, value in sorted(item.items()):
            if prompt_value:
                new_value = prompt(section, key, value)
                config[section][key] = new_value
    # Check validity of directories
    for key, value in sorted(config['pattoo'].items()):
        if 'directory' in key:
            if os.sep not in value:
                shared._log('''\
Provide full directory path for "{}" in section "pattoo: {}". \
Please try again.\
'''.format(value, key))

            # Attempt to create directory
            full_directory = os.path.expanduser(value)
            if os.path.isdir(full_directory) is False:
                _mkdir(full_directory)
                initialize_ownership(key, full_directory)

    # Write file
    with open(filepath, 'w') as f_handle:
        yaml.dump(config, f_handle, default_flow_style=False)


def create_user():
    """Create pattoo user and pattoo group.

    Args:
        None

    Returns:
        None
    """
    # If the group pattoo does not exist, it gets created
    if not group_exists('pattoo'):
        print('\nCreating pattoo group')
        _run_script('groupadd pattoo')
    # If the user pattoo does not exist, it gets created
    if not user_exists('pattoo'):
        print('\nCreating pattoo user')
        _run_script('useradd -d /nonexistent -s /bin/false -g pattoo pattoo')


def group_exists(group_name):
    """Check if the group already exists.

    Args:
        group_name: The name of the group

    Returns
        True if the group exists and False if it does not
    """
    try:
        # Gets group name
        grp.getgrnam(group_name)
        return True
    except KeyError:
        return False


def user_exists(user_name):
    """Check if the user already exists.

    Args:
        user_name: The name of the user

    Returns
        True if the user exists and False if it does not
    """
    try:
        # Gets user name
        pwd.getpwnam(user_name)
        return True
    except KeyError:
        return False


def initialize_ownership(dir_name, dir_path):
    """Change the ownership of the directories to the pattoo user and group.

    Args:
        dir_name: The name of the directory
        dir_path: The path to the directory

    Returns:
        None
    """
    print('\nSetting ownership of the {} directory to pattoo'.format(dir_name))
    if getpass.getuser() != 'travis':
        # Set ownership of file specified at dir_path
        shutil.chown(dir_path, 'pattoo', 'pattoo')


def pattoo_server_config(config_directory, prompt_value):
    """
    Create pattoo_server.yaml file.

    Args:
        config_directory: Configuration directory

    Returns:
        None
    """
    # Initialize key variables
    filepath = '{}{}pattoo_server.yaml'.format(config_directory, os.sep)
    default_config = {
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
        },
        'pattoo_ingesterd': {
            'ingester_interval': 3600,
            'batch_size': 500
        }
    }

    # Say what we are doing
    print('\nConfiguring {} file.\n'.format(filepath))

    # Get configuration
    config = read_config(filepath, default_config)
    if prompt_value:
        for section, item in sorted(config.items()):
            for key, value in sorted(item.items()):
                new_value = prompt(section, key, value)
                config[section][key] = new_value
    else:
        print('Using default values')
    # Write file
    with open(filepath, 'w') as f_handle:
        yaml.dump(config, f_handle, default_flow_style=False)


def read_config(filepath, default_config):
    """Read configuration file and replace default values.

    Args:
        filepath: Name of configuration file
        default_config: Default configuration dict

    Returns:
        config: Dict of configuration
    """
    # Convert config to yaml
    default_config_string = yaml.dump(default_config)

    # Read config
    if os.path.isfile(filepath) is True:
        with open(filepath, 'r') as f_handle:
            yaml_string = (
                '{}\n{}'.format(default_config_string, f_handle.read()))
            config = yaml.safe_load(yaml_string)
    else:
        config = default_config
    return config


def prompt(section, key, default_value):
    """Log messages and exit abnormally.

    Args:
        key: Configuration key
        default_value: Default value for key

    Returns:
        result: Desired value from user
    """
    # Get input from user
    result = input('''Enter "{}: {}" value (Hit <enter> for: "{}"): \
'''.format(section, key, default_value))
    if bool(result) is False:
        result = default_value

        # Try to create necessary directories
        if 'directory' in key:
            try:
                os.makedirs(result, mode=0o750, exist_ok=True)
            except:
                shared._log('''\
Cannot create directory {} in configuration file. Check parent directory \
permissions and typos'''.format(result))

    return result


def _mkdir(directory):
    """Recursively creates directory and its parents.

    Args:
        directory: Directory to create

    Returns:
        None
    """
    # Check if directory already exists
    if os.path.isdir(directory) is False:
        try:
            Path(directory).mkdir(parents=True, mode=0o750, exist_ok=True)
        except OSError:
            shared._log('''Cannot create directory {}. Please try again.\
'''.format(directory))


def check_pattoo_server():
    """Ensure server configuration exists.

    Args:
        None

    Returns:
        True: If the server had been configured correctly

    """
    # Print Status
    print('??: Checking server configuration parameters.')

    # Checks server config
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
    return True


def check_pattoo_client():
    """Ensure client configuration exists.

    Args:
        None

    Returns:
        True: if the client has been configured correctly

    """
    # Print Status
    print('??: Checking client configuration parameters.')

    # Checks client config
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
    return True


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


def configure_installation(prompt_value):
    """Start configuration process.

    Args:
        prompt_value: A boolean value to toggle the script's verbose mode

    Returns:
        None
    """
    # Initialize key variables
    if os.environ.get('PATTOO_CONFIGDIR') is None:
        os.environ['PATTOO_CONFIGDIR'] = '{0}etc{0}pattoo'.format(os.sep)
    config_directory = os.environ.get('PATTOO_CONFIGDIR')

    # Make sure the PATTOO_CONFIGDIR environment variable is set
    if bool(config_directory) is False:
        log_message = ('''\
Set your PATTOO_CONFIGDIR to point to your configuration directory like this:

$ export PATTOO_CONFIGDIR=/path/to/configuration/directory

Then run this command again.
''')
        shared._log(log_message)

    # Prompt for configuration directory
    print('\nPattoo configuration utility.')
    # Create the pattoo user and group
    if getpass.getuser() != 'travis':
        create_user()
    # Attempt to create configuration directory
    _mkdir(config_directory)

    # Create configuration
    pattoo_config(config_directory, prompt_value)
    pattoo_server_config(config_directory, prompt_value)

    # Checking configuration
    check_pattoo_server()
    check_pattoo_client()

    # All done
    output = '''
Successfully created configuration files:

    {0}{1}pattoo.yaml
    {0}{1}pattoo_server.yaml

Next Steps
==========

Checking pip3 packages
'''.format(config_directory, os.sep)
    print(output)
