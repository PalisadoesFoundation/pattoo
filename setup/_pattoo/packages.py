"""Install pip3 packages."""

# Main python libraries
import os
import sys
import subprocess
import traceback
import getpass
import shutil

from _pattoo import shared


def install_missing(package, pip_dir, verbose):
    """Automatically Install missing pip3 packages.

    Args:
        package: The pip3 package to be installed
        pip_dir: The directory the packages should be installed to

    Returns:
        True: if the package could be successfully installed

    """
    # Installs to the directory specified as pip_dir if the user is not travis
    if getpass.getuser() != 'travis':
        _run_script('pip3 install {0} -t {1}'.format(package, pip_dir),
                     verbose)
    else:
        _run_script('pip3 install {0}'.format(package), verbose)
    return True


def get_pip3_dir(prompt_value):
    """Get directory to install pip3 packages.

    Args:
        prompt_value: A boolean value that allows for the pip3 dir to be
                      Manually set

    Returns:
        pip_dir: The directory where the pip3 packages will be installed

    """
    # Default pip3 directory
    pip_dir = '/opt/pattoo-daemon/.python'
    if prompt_value is True:

        # Prompts for input until a valid directory is entered
        pip_dir = input('Enter the directory for the pip3 packages: ')
        while not os.path.isdir(pip_dir):
            pip_dir = input('Enter the directory for the pip3 packages: ')

    # Return pip3 directory
    return pip_dir


def check_pip3(prompt_value, requirements_dir, pip3_dir):
    """Ensure PIP3 packages are installed correctly.

    Args:
        prompt_value: A boolean value to toggle the script's verbose mode and
                      enable the pip3 directory to be manually set.
        requirements_dir: The directory that the requirements.txt file is
                          located in.

    Returns:
        True if pip3 packages are installed successfully

    """
    # Initialize key variables
    lines = []

    # Appends pip3 dir to python path
    sys.path.append(pip3_dir)

    # Read pip_requirements file
    filepath = '{}{}requirements.txt'.format(requirements_dir, os.sep)
    print('??: Checking pip3 packages')
    if os.path.isfile(filepath) is False:
        shared._log('Cannot find PIP3 requirements file {}'.format(filepath))

    # Opens requirements.txt file for reading
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
    for line in lines:

        # Determine the package
        package = line.split('=', 1)[0]
        package = package.split('>', 1)[0]

        # If prompt_value is true, the package being checked is shown
        if prompt_value:
            print('??: Checking package {}'.format(package))
        command = 'pip3 show {}'.format(package)
        (returncode, _, _) = _run_script(command, prompt_value, die=False)
        if bool(returncode) is True:

            # Installs missing pip3 package
            install_missing(package, pip3_dir, prompt_value)

        # If the prompt_value is True, the package will be shown
        if prompt_value:
            print('OK: package {}'.format(line))

        # Set ownership of python packages to pattoo user
        if getpass.getuser() != 'travis' and getpass.getuser() == 'root':
            _run_script('chown -R pattoo:pattoo {}'.format(pip3_dir),
                        prompt_value)
    print('OK: pip3 packages successfully installed')
    return True


def install_pip3(prompt_value, requirements_dir):
    """Install pip3 packages.

     Args:
        prompt_value: A boolean value to toggle the script's verbose mode and
                      enable the pip3 directory to be manually set.
        requirements_dir: The directory that the requirements.txt file is
                          located in.

    Returns:
        True if pip3 packages are installed successfully
    """

    # Retrieve directory to install packages
    pip3_dir = get_pip3_dir(prompt_value)
    # Checks for and installs missing packages
    check_pip3(prompt_value, requirements_dir, pip3_dir)


def _run_script(cli_string, verbose, die=True):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        cli_string: String of command to run
        verbose: A boolean value to toggle the script's verbose mode
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
    if verbose:
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