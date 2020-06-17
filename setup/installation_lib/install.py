#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import os
import sys
import subprocess
import traceback
import getpass
from pattoo_shared import files, configuration
from pattoo_shared import log


EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))

prompt_value = False


def set_global_prompt(new_val):
    """
    Set the value for the global prompt value.

    Args:
        new_val: A boolean value to enable or disable a verbose installation

    Returns:
        None
    """

    global prompt_value
    prompt_value = new_val


def install_missing(package):
    """
    Install missing pip3 packages.
    Args:
        package: The pip3 package to be installed
    Returns:
        True: if the package could be successfully installed
        False: if the package could not be installed
    """
    _run_script('pip3 install {0}'.format(package))
    return True


def check_pip3():
    """Ensure PIP3 packages are installed correctly.

    Args:
        None
    Returns:
        True if pip3 packages are installed successfully
    """
    # Initialize key variables
    lines = []
    requirements_dir = os.path.abspath(os.path.join(ROOT_DIR, os.pardir))
    # Read pip_requirements file
    filepath = '{}{}requirements.txt'.format(requirements_dir, os.sep)
    print('??: Checking pip3 packages')
    if os.path.isfile(filepath) is False:
        _log('Cannot find PIP3 requirements file {}'.format(filepath))
    with open(filepath, 'r') as _fp:
        line = _fp.readline()
        while line:
            # Strip line
            _line = line.strip()
            # Read line
            if True in [_line.startswith('#'), bool(_line) is False]:
                pass
            else:
                lines.append(_line)
            line = _fp.readline()

    # Try to import the modules listed in the file
    # Add conditional to check if verbose option is selected
    for line in lines:
        # Determine the package
        package = line.split('=', 1)[0]
        package = package.split('>', 1)[0]
        if prompt_value:
            print('??: Checking package {}'.format(package))
        command = 'pip3 show {}'.format(package)
        (returncode, _, _) = _run_script(command, die=False)
        if bool(returncode) is True:
            # If the pack
            install_missing(package)
            # Insert pip3 install function
        if prompt_value:
            print('OK: package {}'.format(line))
    print('OK: pip3 packages successfully installed')
    return True


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


def run_configuration_checks():
    """Setup pattoo.

    Args:
        None

    Returns:
        None

    """
    # Check configuration
    check_pattoo_server()
    check_pattoo_client()

def check_config():
    """Ensure configuration is correct.

    Args:
        None

    Returns:
        True to represet a sucessful configuration
    """
    # Print Status
    print('??: Checking configuration')
    # Make sure the PATTOO_CONFIGDIR environment variable is set

    if 'PATTOO_CONFIGDIR' not in os.environ:
        # Sets the default if the pattoo config dir is not in os.environ
        os.environ['PATTOO_CONFIGDIR'] = '{0}etc{0}pattoo'.format(os.sep)

    # Make sure the PATTOO_CONFIGDIR environment variable is set
    if os.path.isdir(os.environ['PATTOO_CONFIGDIR']) is False:
        log_message = ('''\
    Set your PATTOO_CONFIGDIR cannot be found. Set the variable to point to an\
    existing directory:

    $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

    Then run this command again.
    ''')
        _log(log_message)
        #  Check parameters in the configuration
    filepath = '{0}{1}_check_config.py'.format(ROOT_DIR, os.sep)
    run_configuration_checks()
    print('OK: Configuration check passed')
    return True


def install_systemd():
    """
    Automatically install system daemons.

    Args:
        None

    Returns:
        True for a successful of installation the system daemons
    """
    print('??: Attempting to install system daemons')
    systemd_dir = 'systemd{0}bin{0}install_systemd.py'.format(os.sep)
    filepath = os.path.join(ROOT_DIR, systemd_dir)
    config = os.environ['PATTOO_CONFIGDIR']
    _run_script('sudo {0} \
--config_dir {1} --username pattoo --group pattoo'.format(filepath, config))
    print('OK: System daemons successfully installed')


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
    if prompt_value:
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


def next_steps():
    """Print what needs to be done after successful installation.

    Args:
        None

    Returns:
        True: if system daemons are successfully run
    """
    message = ('''

Hooray successful installation! Panna Cotta Time!


Next Steps
==========

Enabling and running system daemons
''')
    print(message)
    if getpass.getuser() != 'travis':
    # Run system daemons
        print('??: Enabling system daemons')
        _run_script('sudo systemctl daemon-reload')
        _run_script('sudo systemctl enable pattoo_apid')
        _run_script('sudo systemctl enable pattoo_api_agentd')
        _run_script('sudo systemctl enable pattoo_ingesterd')
        print('OK: System daemons enabled')
        print('??: Starting system daemons')
        _run_script('sudo systemctl start pattoo_apid')
        _run_script('sudo systemctl start pattoo_api_agentd')
        _run_script('sudo systemctl start pattoo_ingesterd')
        print('OK: System daemons successfully started')
    return True


def install(prompt_value):
    """Driver for pattoo setup.

    Args:
        None

    Returns:
        None

    """
    # Check PIP3 packages

    set_global_prompt(prompt_value)

    check_pip3()
    from installation_lib.db import create_pattoo_db

    create_pattoo_db()
    # Check configuration
    check_config()

    # Install System Daemons
    install_systemd()

    # Print next steps
    next_steps()


if __name__ == '__main__':
    install(False)
