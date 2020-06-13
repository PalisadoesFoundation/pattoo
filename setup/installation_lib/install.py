#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import os
import sys
import subprocess
import traceback
import getpass

from shared import _log, _run_script

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
        None
    """
    _run_script('pip3 install {0} --user'.format(package))


def check_pip3():
    """Ensure PIP3 packages are installed correctly.

    Args:
        The file path for the requirements document
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
    _run_script(filepath)
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



def next_steps():
    """Print what needs to be done after successful installation.

    Args:
        None

    Returns:
        None

    """
    # Don't display this
    # Just run it
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
