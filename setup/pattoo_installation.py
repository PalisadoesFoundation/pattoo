#!/usr/bin/env python3

import argparse
import os
import sys
import getpass
from shared import _run_script, _log

EXEC_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
PIP_DIR = '/opt/pattoo/daemon/.python'
_EXPECTED = '{0}pattoo{0}setup'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.append(ROOT_DIR)
    sys.path.append(PIP_DIR)
    # Try catch block to automatically set the config dir if it isn't already
    # set
    try:
        os.environ['PATTOO_CONFIGDIR']
    except KeyError:
        os.environ['PATTOO_CONFIGDIR'] = '/etc/pattoo'
else:
    print('''\
This script is not installed in the "{}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)
  
# Importing installation related packages
from installation_lib.install import install
from installation_lib.install import check_pip3
from installation_lib.configure import configure_installation

# Setup pip directories
pip3_directory = '{0}opt{0}pattoo-daemon{0}.python'.format(os.sep)
sys.path.append(pip3_directory)


def running_venv():
    """
    Check if a venv is currently activated.

    Args:
        None

    Returns:
        True: If a virtual environment is currently activated
        False: If a virtual environment is not activated
    """
    with open('temp_venv_file.txt', 'r') as temp_file:
        line = temp_file.readline()
        if os.path.isdir(line):
            venv_val = True
        else:
            venv_val = False
    os.remove('temp_venv_file.txt')
    return venv_val


def prompt_args():
    """
    Get CLI arguments for enabling the verbose mode of the installation.

    Args:
        None

    Returns:
        NamedTuple of arugument values
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    return args


def installation_checks():
    """
    Validate conditions needed to start installation.

    Prevents installation if pattoo is not being run in a venv and if the
    script is not run as root

    Args:
        None

    Returns:
        True: If conditions for installation are satisfied
    """
    if getpass.getuser() != 'travis':
        if getpass.getuser() != 'root':
            _log('You are currently not running the script as root.\
Run as root to continue')
    return True


def install_pattoo():
    installation_checks()
    args = prompt_args()
    print(ROOT_DIR)
    configure_installation(args.prompt)
    install(args.prompt)


if __name__ == '__main__':
    install_pattoo()
