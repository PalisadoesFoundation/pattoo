#!/usr/bin/env python3
"""Test pattoo db script."""
import os
import unittest
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}setup_{0}_pattoo'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
    sys.path.append(os.path.join(ROOT_DIR, 'setup'))
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)
from tests.libraries.configuration import UnittestConfig
from pattoo.db import URL
from pattoo.db.models import BASE
from pattoo.db.table import (
   language, pair_xlate_group, pair_xlate, agent_xlate, user, chart, favorite)
from pattoo.constants import DbRowUser, DbRowChart, DbRowFavorite
from setup._pattoo.db import _insert_chart, _insert_favorite, _insert_language
from setup._pattoo.db import _insert_agent_xlate, _insert_user, insertions
from setup._pattoo.db import _insert_pair_xlate_group, install, _mysql


class TestDb(unittest.TestCase):
    """Checks all functions for the Pattoo db script."""

    def test__insert_language(self):
        """Testing method or function named "_insert_language"."""
        _insert_language()
        result = language.idx_exists(1)
        self.assertTrue(result)

    def test__insert_pair_xlate_group(self):
        """Testing method or function named "_insert_pair_xlate_group"."""
        _insert_pair_xlate_group()
        names = ['OPC UA Agents', 'IfMIB Agents', 'Linux Agents', ]
        result = []
        # Loop through names and checks if they're inserted into the table
        for name in names:
            result.append(pair_xlate_group.exists(name))
        self.assertTrue(all(result))

    def test__insert_agent_xlate(self):
        """Testing method or function named "_insert_agent_xlate"."""
        _insert_agent_xlate()

        # Make sure agent translation exists
        result = agent_xlate.agent_xlate_exists(
            1, 'pattoo_agent_linux_autonomousd'
        )
        self.assertTrue(result)

    def test__insert_user(self):
        """Testing method or function named "_insert_user"."""
        _insert_user()
        # Make sure user exists
        idx_user = user.exists('pattoo')
        self.assertEqual(idx_user, 1)

        # Check if index exists
        result = user.idx_exists(1)
        self.assertTrue(result)

    def test__insert_chart(self):
        """Testing method or function named "_insert_chart"."""
        _insert_chart()
        chart_checksum = 'pattoo'

        # Make sure that chart exists
        idx_chart = chart.exists(chart_checksum)
        self.assertTrue(bool(idx_chart))

        # Verify that index exists
        result = chart.idx_exists(idx_chart)
        self.assertTrue(result)

    def test__insert_favorite(self):
        """Testing method or function named "_insert_favorite"."""
        _insert_favorite()
        result = favorite.idx_exists(1)
        self.assertTrue(result)

if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
