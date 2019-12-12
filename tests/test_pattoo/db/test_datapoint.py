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
            EXEC_DIR,
            os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/db') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/db" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from pattoo_shared.constants import DATA_FLOAT
from tests.libraries.configuration import UnittestConfig
from pattoo.db import datapoint


class TestBasicFunctioins(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_checksum_exists(self):
        """Testing method / function checksum_exists."""
        # Initialize key variables
        result = datapoint.checksum_exists(-1)
        polling_interval = 1
        self.assertFalse(result)

        # Create entry and check
        _checksum = data.hashstring(str(random()))
        result = datapoint.checksum_exists(_checksum)
        self.assertFalse(result)
        datapoint.insert_row(_checksum, DATA_FLOAT, polling_interval)
        result = datapoint.checksum_exists(_checksum)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Initialize key variables
        result = datapoint.checksum_exists(-1)
        polling_interval = 1
        self.assertFalse(result)

        # Create entry and check
        checksum = data.hashstring(str(random()))
        result = datapoint.checksum_exists(checksum)
        self.assertFalse(result)
        datapoint.insert_row(checksum, DATA_FLOAT, polling_interval)
        result = datapoint.checksum_exists(checksum)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
