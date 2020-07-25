#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}db{0}table'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo_shared import data
from tests.libraries.configuration import UnittestConfig
from pattoo.constants import DbRowUser
from pattoo.db.table import user

class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test_idx_exists(self):
        """Testing method or function named "idx_exists"."""
        # Add entry to database
        uname = data.hashstring(str(random()))
        passwrd = data.hashstring(str(random()))
        f_name = data.hashstring(str(random()))
        l_name = data.hashstring(str(random()))
        user.insert_row(
            DbRowUser(
                username=uname,
                password=passwrd,
                first_name=f_name,
                last_name=l_name,
                enabled=0
            )
        )

        # Make sure it exists
        idx_user = user.exists(uname)

        # Verify that the index exists
        result = user.idx_exists(idx_user)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method or function named "exists"."""
        # Create a translation
        uname = data.hashstring(str(random()))
        passwrd = data.hashstring(str(random()))
        f_name = data.hashstring(str(random()))
        l_name = data.hashstring(str(random()))

        # Make sure it does not exist
        result = user.exists(uname)
        self.assertFalse(bool(result))

        # Add database row
        user.insert_row(
            DbRowUser(
                username=uname,
                password=passwrd,
                first_name=f_name,
                last_name=l_name,
                enabled=0
            )
        )

        # Make sure it exists
        result = user.exists(uname)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method or function named "insert_row"."""
        # Add an entry to the database
        uname = data.hashstring(str(random()))
        passwrd = data.hashstring(str(random()))
        f_name = data.hashstring(str(random()))
        l_name = data.hashstring(str(random()))
        user.insert_row(
            DbRowUser(
                username=uname,
                password=passwrd,
                first_name=f_name,
                last_name=l_name,
                enabled=0
            )
        )

        # Make sure it exists
        idx_user = user.exists(uname)

        # Verify the index exists
        result = user.idx_exists(idx_user)
        self.assertTrue(result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
