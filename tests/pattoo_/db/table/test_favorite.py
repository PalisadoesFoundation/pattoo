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
from pattoo.db.table import user, chart, favorite
from pattoo.constants import DbRowUser, DbRowChart, DbRowFavorite


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""


    def test_idx_exists(self):
        """Testing method or function named "idx_exists"."""
        # Add user entry to database
        uname = data.hashstring(str(random()))
        passwrd = data.hashstring(str(random()))
        salt_ = data.hashstring(str(random()))
        f_name = data.hashstring(str(random()))
        l_name = data.hashstring(str(random()))
        user.insert_row(
            DbRowUser(
                username=uname,
                password=passwrd.encode(),
                salt=salt_.encode(),
                first_name=f_name,
                last_name=l_name,
<<<<<<< HEAD
                enabled=0,
                is_admin=0
=======
                role=1,
                password_expired=1,
                enabled=0
>>>>>>> 97d6587a82da5548550c1cee9bc4d351004e9cd7
            )
        )

        # Make sure user entry exists
        idx_user = user.exists(uname)
        self.assertTrue(bool(idx_user))

        # Add chart entry to database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure chart entry exists
        idx_chart = chart.exists(chart_checksum)
        self.assertTrue(bool(idx_chart))

        # Add favorite to database
        favorite.insert_row(
            DbRowFavorite(
                idx_chart=idx_chart,
                idx_user=idx_user,
                order=0,
                enabled=0
            )
        )

        # Make sure the favorite exists
        idx_favorite = favorite.exists(idx_chart, idx_user)

        # Verify that the index exists
        result = favorite.idx_exists(idx_favorite)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method or function named "exists"."""
        # Add user entry to database
        uname = data.hashstring(str(random()))
        passwrd = data.hashstring(str(random()))
        salt_ = data.hashstring(str(random()))
        f_name = data.hashstring(str(random()))
        l_name = data.hashstring(str(random()))
        user.insert_row(
            DbRowUser(
                username=uname,
                password=passwrd.encode(),
                salt=salt_.encode(),
                first_name=f_name,
                role=0,
                password_expired=1,
                last_name=l_name,
                enabled=0,
                is_admin=0
            )
        )
        # Make sure user entry exists
        idx_user = user.exists(uname)

        # Add chart entry to database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure chart entry exists
        idx_chart = chart.exists(chart_checksum)

        # Make sure favorite does not exist
        result = favorite.exists(idx_chart, idx_user)
        self.assertFalse(bool(result))

        # Add favorite to database
        favorite.insert_row(
            DbRowFavorite(
                idx_chart=idx_chart,
                idx_user=idx_user,
                order=0,
                enabled=0
            )
        )

        # Make sure favorite exists
        result = favorite.exists(idx_chart, idx_user)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method or function named "insert_row"."""
        # Add user entry to database
        uname = data.hashstring(str(random()))
        passwrd = data.hashstring(str(random()))
        salt_ = data.hashstring(str(random()))
        f_name = data.hashstring(str(random()))
        l_name = data.hashstring(str(random()))
        user.insert_row(
            DbRowUser(
                username=uname,
                password=passwrd.encode(),
                salt=salt_.encode(),
                first_name=f_name,
                last_name=l_name,
<<<<<<< HEAD
                enabled=0,
                is_admin=0
=======
                role=0,
                password_expired=1,
                enabled=0
>>>>>>> 97d6587a82da5548550c1cee9bc4d351004e9cd7
            )
        )

        # Make sure user entry exists
        idx_user = user.exists(uname)

        # Add chart entry to database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure chart entry exists
        idx_chart = chart.exists(chart_checksum)

        # Add favorite to database
        favorite.insert_row(
            DbRowFavorite(
                idx_chart=idx_chart,
                idx_user=idx_user,
                order=0,
                enabled=0
            )
        )

        # Make sure the favorite exists
        idx_favorite = favorite.exists(idx_chart, idx_user)

        # Verify that the index exists
        result = favorite.idx_exists(idx_favorite)
        self.assertTrue(result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
