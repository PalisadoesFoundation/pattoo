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

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/db/table') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/db/table" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import pair_xlate, language, pair_xlate_group
from pattoo.db.models import PairXlate
from pattoo.db import db


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################
    def test_key_description(self):
        """Testing method / function key_description."""
        pass

    def test_key_descriptions(self):
        """Testing method / function key_descriptions."""
        pass

    def test_pair_xlate_exists(self):
        """Testing method / function pair_xlate_exists."""
        pass

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Add a language and pair_xlate_group entry to the database
        code = data.hashstring(str(random()))
        _description = data.hashstring(str(random()))
        language.insert_row(code, _description)
        idx_language = language.exists(code)
        pair_xlate_group.insert_row(_description)
        idx_pair_xlate_group = pair_xlate_group.exists(_description)

        # Make sure row does not exist
        description = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        pair_xlate.insert_row(
            key, description, idx_language, idx_pair_xlate_group)

        # Test
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertTrue(result)

    def test_update_row(self):
        """Testing method / function update_row."""
        pass

    def test_update(self):
        """Testing method / function update."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
