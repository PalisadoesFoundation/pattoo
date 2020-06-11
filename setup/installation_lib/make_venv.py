#!/usr/bin/python3

import os 
import sys

EXEC_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
_EXPECTED = '{0}pattoo{0}setup{0}installation_lib'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.append(ROOT_DIR)
else:
    print('''\
This script is not installed in the "{}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from shared import _run_script


def make_venv(venv_name):
    """
    Create venv for pattoo installation.

    Args:
        venv_name: The name of the virtual environment

    Returns:
        None
    """
    venv_dir = os.path.join(os.path.expanduser('~'), venv_name)
    venv_activate = '{0}{1}bin{1}activate'.format(venv_dir, os.sep)
    print('??: Create virtual environment')
    _run_script('python3 -m venv {0}'.format(venv_dir))
    print('OK: Virtual environment created')
    print('??: Activate virtual environment')
    os.system('/bin/bash --rcfile {}'.format(venv_activate))

if __name__ == '__main__':
    make_venv('test-pattoo')