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
sys.path.append(ROOT_DIR)
prompt_value = False


def set_global_prompt(new_val):
    """Set the value for the global prompt value.

    Args:
        new_val: A boolean value to enable or disable a verbose installation

    Returns:
        None
    """

    global prompt_value
    prompt_value = new_val


def install_missing(package):
    """Install missing pip3 packages.

    Args:
        package: The pip3 package to be installed

    Returns:
        True: if the package could be successfully installed
        False: if the package could not be installed

    """
    pip_dir = '/opt/pattoo/daemon/.python'
    # Automatically installs missing pip3 packages
    if getpass.getuser() != 'travis':
        _run_script('pip3 install {0} -t {1}'.format(package, pip_dir))
    else:
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


def install_systemd():
    """
    Automatically install system daemons.

    Args:
        None

    Returns:
        True for a successful of installation the system daemons
    """
    print('??: Attempting to install system daemons')
    systemd_dir = 'systemd{0}bin{0}systemd.py'.format(os.sep)
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
    # Change prompt value to verbose
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

Setting up database tables
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

    create_pattoo_db_tables()
    # Check configuration
    check_config()

    # Install System Daemons
    install_systemd()

    # Print next steps
    next_steps()

