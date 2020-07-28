#!/usr/bin/env python3
"""Script create a test user."""

from __future__ import print_function
from random import random
import os
import sys
import argparse

# Try to create a working PYTHONPATH
DEV_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(DEV_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}bin'.format(os.sep)
if DEV_DIR.endswith(_EXPECTED) is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# pattoo libraries
from pattoo_shared import data
from pattoo.db.table import user
from pattoo.constants import DbRowUser


def main():
    """Test all the pattoo modules with unittests.

    Args:
        None

    Returns:
        None

    """
    # Set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--username', '-u', help='Username to create',
        type=str, default='pattoo-test@palisadoes.org')
    args = parser.parse_args()

    # Determine whether user already exists
    username = args.username
    if bool(user.exists(username)) is False:
        row = DbRowUser(
            username=username,
            password=data.hashstring(str(random())),
            first_name='Pattoo: {}'.format(username),
            last_name='Test: {}'.format(username),
            enabled=True,
            )
        user.insert_row(row)


if __name__ == '__main__':

    # Do the unit test
    main()
