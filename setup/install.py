#!/usr/bin/env python3
"""Install pattoo."""

# Main python libraries
import sys
import os
import getpass
import locale
import subprocess

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _BIN_DIRECTORY.endswith('/pattoo/bin') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Pattoo libraries
from pattoo_shared import log


class _PythonSetupPackages(object):
    """Class to setup Python."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self._username = getpass.getuser()
        valid = True
        major = 3
        minor = 5
        major_installed = sys.version_info[0]
        minor_installed = sys.version_info[1]

        # Exit if python version is too low
        if major_installed < major:
            valid = False
        elif major_installed == major and minor_installed < minor:
            valid = False
        if valid is False:
            log_message = (
                'Required python version must be >= {}.{}. '
                'Python version {}.{} installed'
                ''.format(major, minor, major_installed, minor_installed))
            log.log2die_safe(21027, log_message)

    def run(self):
        """Install PIP3 packages.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = self._username

        # Don't attempt to install packages if running in the Travis CI
        # environment
        if 'TRAVIS' in os.environ and 'CI' in os.environ:
            return

        # Determine whether PIP3 exists
        print('Installing required pip3 packages from requirements.txt file.')
        requirements_file = (
            '{}/pip_requirements.txt'.format(_ROOT_DIRECTORY))

        if username == 'root':
            script_name = ('''\
pip3 install --upgrade --requirement {}'''.format(requirements_file))
        else:
            script_name = ('''\
pip3 install --user --upgrade --requirement {}'''.format(requirements_file))
        _run_script(script_name)

        # Status message
        print('pip3 packages installation complete.')


def _run_script(cli_string):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    encoding = locale.getdefaultlocale()[1]
    pattoo_returncode = ('----- pattoo Return Code '
                         '----------------------------------------')
    pattoo_stdoutdata = ('----- pattoo Test Output '
                         '----------------------------------------')
    pattoo_stderrdata = ('----- pattoo Test Error '
                         '-----------------------------------------')

    # Say what we are doing
    string2print = '\nRunning Command: {}'.format(cli_string)
    print(string2print)

    # Run update_devices script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    process = subprocess.Popen(
        do_command_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdoutdata, stderrdata = process.communicate()
    returncode = process.returncode

    # Crash if the return code is not 0
    if returncode != 0:
        # Print the Return Code header
        string2print = '\n{}'.format(pattoo_returncode)
        print(string2print)

        # Print the Return Code
        string2print = '\n{}'.format(returncode)
        print(string2print)

        # Print the STDOUT header
        string2print = '\n{}\n'.format(pattoo_stdoutdata)
        print(string2print)

        # Print the STDOUT
        for line in stdoutdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # Print the STDERR header
        string2print = '\n{}\n'.format(pattoo_stderrdata)
        print(string2print)

        # Print the STDERR
        for line in stderrdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # All done
        sys.exit(2)


def run():
    """Setup infoset-ng.

    Args:
        None

    Returns:
        None

    """
    # Determine whether version of python is valid
    _PythonSetupPackages().run()


if __name__ == '__main__':
    # Run setup
    run()
