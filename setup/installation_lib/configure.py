#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import sys
import os
import shutil
import subprocess
import traceback
from pathlib import Path
# from shared import _log, _run_script
import getpass
try:
    import yaml
except:
    print('Install the Python3 "pyyaml" package, then run this script again')
    sys.exit(2)


def already_written(file_path, env_export):
    """
    Check if the CONFIG_DIR had already been exported.

    Args:
        file_path: The path to bash_profile
        env_export: The line being exported to bash_profile

    Returns:
        True: if the line that exports the PATTOO CONFIGDIR is already in
        bash profile
        False: if the line that exports the PATTOO CONFIGDIR had not been
        written to bash profile
    """
    with open(file_path, 'r') as file:
        for line in file:
            if line == env_export:
                return True
        return False


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


def _log(message):
    """Log messages and exit abnormally.

    Args:
        message: Message to print

    Returns:
        None

    """
    # exit
    print('\nPATTOO Error: {}'.format(message))
    sys.exit(3)


def set_configdir(filepath):
    """
    Automatically sets the configuration directory.

    Args:
        The file path for bash_profile

    Returns:
        None
    """
    config_path = '{0}etc{0}pattoo'.format(os.sep)
    env_export = 'export PATTOO_CONFIGDIR={}'.format(config_path)
    with open(filepath, 'a') as file:
        if not (already_written(filepath, env_export)):
            file.write(env_export)
    os.environ['PATTOO_CONFIGDIR'] = config_path


def get_configdir():
    """
    Retrieve the configuration directory.

    Args:
        None

    Returns:
        The file path for the configuration directory
    """
    return os.environ['PATTOO_CONFIGDIR']


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

    # Directories that will be excluded from prompt
    directories = [
        'system_daemon_directory', 'log_directory', 'cache_directory',
        'system_daemon_directory']
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
                _log('''\
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
    """
    Create pattoo user and pattoo group.

    Args:
        None

    Returns:
        None
    """
    print('\nCreating pattoo group')
    _run_script('groupadd pattoo')
    print('\nCreating pattoo user')
    _run_script('useradd -d /nonexistent -s /bin/false -g pattoo pattoo')


def initialize_ownership(dir_name, dir_path):
    """
    Changes the ownership of the directories to the pattoo user and group.

    Args:
        dir_name: The name of the directory
        dir_path: The path to the directory
    Returns:
        None
    """
    print('\nSetting ownership of the {} directory to pattoo'.format(dir_name))
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
                _log('''\
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
    if os.path.isdir(directory) is False:
        try:
            Path(directory).mkdir(parents=True, mode=0o750, exist_ok=True)
        except OSError:
            _log('''Cannot create directory {}. Please try again.\
'''.format(directory))


def configure_installation(prompt_value):
    """Start configuration process.

    Args:
        prompt_value: A boolean value to toggle the script's verbose mode

    Returns:
        None

    """
    # Initialize key variables
    if os.environ.get('PATTOO_CONFIGDIR') is None:
        path = os.path.join(os.path.join(os.path.expanduser('~')),
                            '.bash_profile')
        set_configdir(path)
    config_directory = os.environ.get('PATTOO_CONFIGDIR')

    # Make sure the PATTOO_CONFIGDIR environment variable is set
    if bool(config_directory) is False:
        log_message = ('''\
Set your PATTOO_CONFIGDIR to point to your configuration directory like this:

$ export PATTOO_CONFIGDIR=/path/to/configuration/directory

Then run this command again.
''')
        _log(log_message)

    # Prompt for configuration directory
    print('\nPattoo configuration utility.')
    # Create the pattoo user and group
    create_user()
    # Attempt to create configuration directory
    _mkdir(config_directory)

    # Create configuration
    pattoo_config(config_directory, prompt_value)
    pattoo_server_config(config_directory, prompt_value)

    # All done
    output = '''
Successfully created configuration files:

    {0}{1}pattoo.yaml
    {0}{1}pattoo_server.yaml

Next Steps
==========

Running Installation Script
'''.format(config_directory, os.sep)
    print(output)
    #if prompt_value:
        #print(output)

    
