#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import os
import sys
import subprocess
import traceback
# from shared import _log, _run_script

EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))

prompt_value = False

def set_global_prompt(new_val):
    global prompt_value
    prompt_value = new_val


def install_missing(package):
    """Install missing pip3 packages."""
    # pip3 install to --target
    # or pip3 install --root
    # You want this to be installed in the home directory
    # Consider installing pattoo as the username pattoo
    pip_path = '.local{0}lib{0}python3.6{0}site-packages'.format(os.sep)
    directory = os.path.join(os.path.expanduser('~'), pip_path)
    _run_script('pip3 install --target {0} {1}'.format(directory, package))


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
    filepath = '{}{}pip_requirements.txt'.format(requirements_dir, os.sep)
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


def check_database():
    """Ensure database is installed correctly.

    Args:
        None

    Returns:
        True to represent the databaase being successfully configured

    """
    #  Check database
    print('??: Setting up database.')
    filepath = '{0}{1}_check_database.py'.format(ROOT_DIR, os.sep)
    _run_script(filepath)
    print('OK: Database setup complete.')
    return True


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
        if messages != [] and prompt_value:
            print(messages)
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

    # Check configuration
    check_config()

    # Check database
    check_database()

    # Install System Daemons
    install_systemd()

    # Print next steps
    next_steps()


if __name__ == '__main__':
    install(False)
