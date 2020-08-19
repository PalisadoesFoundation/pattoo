#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random, randint
import crypt

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
from pattoo.db.models import User
from pattoo.db import db


def _random_user():
    """Create a random user in the database.

    Args:
        value: New value to apply

    Returns:
        result: DbRowUser object

    """
    result = DbRowUser(
        username=data.hashstring(str(random())),
        password=data.hashstring(str(random())),
        first_name=data.hashstring(str(random())),
        last_name=data.hashstring(str(random())),
        user_type=1,
        change_password=1,
        enabled=0
    )
    return result


def _insert_random_user():
    """Insert a random user in the database.

    Args:
        value: New value to apply

    Returns:
        result: DbRowUser object

    """
    result = _random_user()
    user.insert_row(result)
    return result


class TestUser(unittest.TestCase):
    """Checks all functions and methods."""

    # Add an entry to the database
    expected = _random_user()
    user.insert_row(expected)
    result = user.User(expected.username)

    def test___init__(self):
        """Testing function __init__."""
        # Try bad username
        test = user.User(data.hashstring(str(random())))
        self.assertIsNone(test.first_name)
        self.assertIsNone(test.last_name)
        self.assertIsNone(test.user_type)
        self.assertIsNone(test.change_password)
        self.assertIsNone(test.enabled)
        self.assertFalse(test.exists)

        # Test all the attributes
        self.assertEqual(
            self.result.first_name, self.expected.first_name)
        self.assertEqual(
            self.result.last_name, self.expected.last_name)
        self.assertEqual(
            self.result.user_type, self.expected.user_type)
        self.assertEqual(
            self.result.change_password,
            bool(self.expected.change_password))
        self.assertEqual(
            self.result.enabled,
            bool(self.expected.enabled))

    def test_valid_password(self):
        """Testing function valid_password."""
        # Test with a valid password
        result = self.result.valid_password(self.expected.password)
        self.assertTrue(result)

        # Test with an invalid password
        result = self.result.valid_password(data.hashstring(str(random())))
        self.assertFalse(result)


class TestModify(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        # Try bad username
        with self.assertRaises(SystemExit):
            user.Modify(data.hashstring(str(random())))

    def test_first_name(self):
        """Testing function first_name."""
        # Test existing attribute
        user_ = _insert_random_user()
        modify = user.Modify(user_.username)

        # Test modification
        new = data.hashstring(str(random()))
        modify.first_name(new)
        result = user.User(user_.username)
        self.assertEqual(result.first_name, new)

    def test_last_name(self):
        """Testing function last_name."""
        # Test existing attribute
        user_ = _insert_random_user()
        modify = user.Modify(user_.username)

        # Test modification
        new = data.hashstring(str(random()))
        modify.last_name(new)
        result = user.User(user_.username)
        self.assertEqual(result.last_name, new)

    def test_password(self):
        """Testing function password."""
        # Test existing attribute
        user_ = _insert_random_user()
        modify = user.Modify(user_.username)

        # Test modification
        new = data.hashstring(str(random()))
        modify.password(new)
        result = user.User(user_.username)
        self.assertTrue(result.valid_password(new))

    def test_user_type(self):
        """Testing function user_type."""
        # Test existing attribute
        user_ = _insert_random_user()
        modify = user.Modify(user_.username)

        # Test modification
        new = randint(0, 99)
        modify.user_type(new)
        result = user.User(user_.username)
        self.assertEqual(result.user_type, new)

    def test_change_password(self):
        """Testing function change_password."""
        # Test existing attribute
        user_ = _insert_random_user()
        modify = user.Modify(user_.username)

        # Test modification
        new = bool(randint(0, 1))
        modify.change_password(new)
        result = user.User(user_.username)
        self.assertEqual(result.change_password, new)

    def test_enabled(self):
        """Testing function enabled."""
        # Test existing attribute
        user_ = _insert_random_user()
        modify = user.Modify(user_.username)

        # Test modification
        new = bool(randint(0, 1))
        modify.enabled(new)
        result = user.User(user_.username)
        self.assertEqual(result.enabled, new)


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
                user_type=1,
                change_password=1,
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
                user_type=1,
                change_password=0,
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
        password = data.hashstring(str(random()))
        expected = DbRowUser(
            username=uname,
            password=password,
            first_name=data.hashstring(str(random())),
            last_name=data.hashstring(str(random())),
            user_type=1,
            change_password=1,
            enabled=0
        )
        user.insert_row(expected)

        # Make sure it exists
        idx_user = user.exists(uname)

        # Verify the index exists
        result = user.idx_exists(idx_user)
        self.assertTrue(result)

        # Verify that all the parameters match
        with db.db_query(20091) as session:
            row = session.query(
                User).filter(User.username == uname.encode()).one()

        self.assertEqual(expected.username, row.username.decode())
        self.assertEqual(expected.first_name, row.first_name.decode())
        self.assertEqual(expected.last_name, row.last_name.decode())
        self.assertEqual(expected.user_type, row.user_type)
        self.assertEqual(expected.change_password, row.change_password)
        self.assertEqual(expected.enabled, row.enabled)

        # Test password
        salt = row.password.decode().split('$')[2]
        password_hash = crypt.crypt(password, '$6${}'.format(salt))
        self.assertEqual(row.password.decode(), password_hash)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
