#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}test_pattoo{0}db{0}table'.format(os.sep)
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
from pattoo.db.table import pair


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_pair_exists(self):
        """Testing method / function pair_exists."""
        # Initialize key variables
        key = data.hashstring(str(random()))
        value = data.hashstring(str(random()))
        result = pair.pair_exists(key, value)
        self.assertFalse(result)

        # Create entry and check
        pair.insert_rows((key, value))
        result = pair.pair_exists(key, value)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_insert_rows(self):
        """Testing method / function insert_rows."""
        # Initialize key variables
        key = data.hashstring(str(random()))
        value = data.hashstring(str(random()))
        result = pair.pair_exists(key, value)
        self.assertFalse(result)

        # Create entry and check
        pair.insert_rows((key, value))
        result = pair.pair_exists(key, value)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_idx_pairs(self):
        """Testing method / function idx_pairs."""
        # Initialize key variables
        keypairs = []
        idx_pairs = []
        for _ in range(0, 10):
            time.sleep(0.05)
            key = data.hashstring(str(random()))
            value = data.hashstring(str(random()))
            keypairs.append((key, value))

        # Insert values in tables
        pair.insert_rows(keypairs)

        # Test
        for key, value in keypairs:
            idx_pairs.append(pair.pair_exists(key, value))

        result = pair.idx_pairs(keypairs)
        self.assertEqual(len(result), len(idx_pairs))
        for idx_pair in idx_pairs:
            self.assertTrue(idx_pair in result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
