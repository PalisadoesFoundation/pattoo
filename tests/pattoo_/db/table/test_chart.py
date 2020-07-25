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
from pattoo.constants import DbRowChart
from pattoo.db.table import chart


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test_idx_exists(self):
        """Testing method or function named idx_exists."""
        # Add entry to database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure it exists
        idx_chart = chart.exists(chart_checksum)

        # Verify that the index exists
        result = chart.idx_exists(idx_chart)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method or function named exists."""
        # Create a translation
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))

        # Make sure it does not exist
        result = chart.exists(chart_checksum)
        self.assertFalse(bool(result))

        # Add database row
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure it exists
        result = chart.exists(chart_checksum)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method or function named insert_row."""
        # Add an entry to the database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure it exists
        idx_chart = chart.exists(chart_checksum)

        # Verify the index exists
        result = chart.idx_exists(idx_chart)
        self.assertTrue(result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
