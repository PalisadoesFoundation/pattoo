#!/usr/bin/env python3
"""Script to test all the pattoo unittests.

1)  This script runs each unittest script in the test directory.

2)  The only scripts run in the module are those whose names
    start with 'test_'

3)  All unittest scripts must be able to successfully run independently
    of all others.

"""

from __future__ import print_function
import locale
import os
import sys
import subprocess
import argparse

# Try to create a working PYTHONPATH
DEV_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(DEV_DIR, os.pardir)), os.pardir))
if DEV_DIR.endswith('/pattoo/tests/bin') is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/bin" directory. \
Please fix.''')
    sys.exit(2)

# pattoo libraries
from pattoo_shared import errors
from pattoo_shared import files
from tests.libraries.configuration import UnittestConfig


def main():
    """Test all the pattoo modules with unittests.

    Args:
        None

    Returns:
        None

    """
    # Set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', help='', action='store_true')
    args = parser.parse_args()

    # Determine unittest directory
    root_dir = ROOT_DIR
    test_dir = '{}/tests'.format(root_dir)

    # Create database tables if necessary
    command = '{}/setup/install.py'.format(root_dir)
    run_script(command)

    # Run the test
    command = 'python3 -m unittest discover --start {}'.format(test_dir)
    if args.verbose is True:
        command = '{} --verbose'.format(command)
    run_script(command)

    # Check error codes
    command = '{}/tests/bin/error_code_report.py'.format(root_dir)
    run_script(command)

    # Print
    message = ('\nHooray - All Done OK!\n')
    print(message)


def run_script(cli_string):
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

    # Run update_targets script
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


if __name__ == '__main__':
    # Test the configuration variables
    UnittestConfig().create()

    # Do the unit test
    main()
