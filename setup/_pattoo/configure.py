"""Install pattoo."""

# Main python libraries
import sys
import os
import secrets
import shutil
import grp
import pwd
from pathlib import Path
import getpass
try:
    import yaml
except:
    print('Install the Python3 \'pyyaml\' package, then run this script again')
    sys.exit(2)

# Pattoo libraries
from pattoo_shared import files, configuration
from pattoo_shared import log
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from _pattoo import shared


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
    print('Configuring {} file.'.format(filepath))

    # Get configuration
    config = read_config(filepath, default_config)
    forced_directories = ['system_daemon_directory', 'daemon_directory']
    for section, item in sorted(config.items()):
        for key, value in sorted(item.items()):
            if key in forced_directories:
                continue
            if prompt_value:
                new_value = prompt(section, key, value)
                config[section][key] = new_value

    # Check validity of directories
    for key, value in sorted(config['pattoo'].items()):
        if 'directory' in key:
            if os.sep not in value:
                shared.log('''\
Provide full directory path for "{}" in section "pattoo: {}". \
Please try again.\
'''.format(value, key))

            # Attempt to create directory
            full_directory = os.path.expanduser(value)
            if os.path.isdir(full_directory) is False:
                _mkdir(full_directory)
                initialize_ownership(key, full_directory)

            # Ensure correct ownership of /var/run/pattoo
            if full_directory == '{0}var{0}run{0}pattoo'.format(os.sep):
                _chown(full_directory)

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
        print('Creating pattoo group')
        shared.run_script('groupadd pattoo')
    # If the user pattoo does not exist, it gets created
    if not user_exists('pattoo'):
        print('Creating pattoo user')
        shared.run_script(
            'useradd -d /nonexistent -s /bin/false -g pattoo pattoo')


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


def initialize_ownership(config_directory_parameter, dir_path):
    """Change the ownership of the directories to the pattoo user and group.

    Args:
        config_directory_parameter: The name of the directory
        dir_path: The path to the directory

    Returns:
        None
    """
    print('Setting ownership of the {} directory to pattoo'.format(
        config_directory_parameter))
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
            'JWT_SECRET_KEY': secrets.token_urlsafe(MAX_KEYPAIR_LENGTH)
        },
        'pattoo_ingesterd': {
            'ingester_interval': 3600,
            'batch_size': 500,
            'graceful_timeout': 10
        }
    }

    # Say what we are doing
    print('Configuring {} file.'.format(filepath))

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
                shared.log('''\
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
            shared.log('''Cannot create directory {}. Please try again.\
'''.format(directory))


def _chown(directory):
    """Recursively change the ownership of files in a directory.

    The directory must have the string '/pattoo/' in it

    Args:
        directory: Directory to create

    Returns:
        None

    """
    # Initialize key variables
    username = 'pattoo'
    group = 'pattoo'

    # Change ownership
    if '{}pattoo'.format(os.sep) in directory:
        # Change the parent directory
        shutil.chown(directory, user=username, group=group)

        # Recursively change the sub-directories and files
        for root, dirs, files_ in os.walk(directory):
            for dir_ in dirs:
                shutil.chown(
                    os.path.join(root, dir_), user=username, group=group)
            for file_ in files_:
                shutil.chown(
                    os.path.join(root, file_), user=username, group=group)


def check_pattoo_server():
    """Ensure server configuration exists.

    Args:
        None

    Returns:
        True: If the server had been configured correctly

    """
    # Print Status
    print('Checking server configuration parameters.')

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
    return True


def check_pattoo_client():
    """Ensure client configuration exists.

    Args:
        None

    Returns:
        True: if the client has been configured correctly

    """
    # Print Status
    print('Checking client configuration parameters.')

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


def install(prompt_value):
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

    # Create the pattoo user and group
    username = getpass.getuser()
    if username != 'travis':
        create_user()
    # Attempt to create configuration directory
    _mkdir(config_directory)

    # Attempt to change the ownership of the configuration directory
    if username != 'travis':
        _chown(config_directory)

    # Create configuration
    pattoo_config(config_directory, prompt_value)
    pattoo_server_config(config_directory, prompt_value)

    # Checking configuration
    check_pattoo_server()
    check_pattoo_client()

    # All done
    output = '''\
Successfully created configuration files:
    {0}{1}pattoo.yaml
    {0}{1}pattoo_server.yaml\
'''.format(config_directory, os.sep)
    print(output)
