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
from pattoo.db.table import pair_xlate_group
from pattoo.db.models import PairXlateGroup, Language
from pattoo.db import db


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_idx_exists(self):
        """Testing method / function idx_exists."""
        # Add an entry to the database
        name = data.hashstring(str(random()))
        pair_xlate_group.insert_row(name)

        # Make sure it exists
        idx_pair_xlate_group = pair_xlate_group.exists(name)

        # Verify the index exists
        result = pair_xlate_group.idx_exists(idx_pair_xlate_group)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method / function exists."""
        # Create a name
        name = data.hashstring(str(random()))

        # Make sure it does not exist
        result = pair_xlate_group.exists(name)
        self.assertFalse(bool(result))

        # Add an entry to the database
        pair_xlate_group.insert_row(name)

        # Make sure it exists
        result = pair_xlate_group.exists(name)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Add an entry to the database
        name = data.hashstring(str(random()))
        pair_xlate_group.insert_row(name)

        # Make sure it exists
        idx_pair_xlate_group = pair_xlate_group.exists(name)

        # Verify the index exists
        result = pair_xlate_group.idx_exists(idx_pair_xlate_group)
        self.assertTrue(result)

    def test_update_name(self):
        """Testing method / function update_name."""
        # Add an entry to the database
        name = data.hashstring(str(random()))

        # Make sure it does not exist
        result = pair_xlate_group.exists(name)
        self.assertFalse(bool(result))

        # Add row to database
        pair_xlate_group.insert_row(name)

        # Make sure it exists
        idx = pair_xlate_group.exists(name)

        # Get current name
        with db.db_query(20093) as session:
            result = session.query(PairXlateGroup.name).filter(
                PairXlateGroup.idx_pair_xlate_group == idx).one()

        # Test
        self.assertEqual(name, result.name.decode())

        # Update the name
        new_name = data.hashstring(str(random()))
        pair_xlate_group.update_name(idx, new_name)

        # Get current name
        with db.db_query(20094) as session:
            result = session.query(PairXlateGroup.name).filter(
                PairXlateGroup.idx_pair_xlate_group == idx).one()

        # Test
        self.assertEqual(new_name, result.name.decode())

    def test_cli_show_dump(self):
        """Testing method / function cli_show_dump."""
        # Add an entry to the database
        name = data.hashstring(str(random()))
        pair_xlate_group.insert_row(name)

        # Make sure it exists
        idx_pair_xlate_group = pair_xlate_group.exists(name)

        result = pair_xlate_group.cli_show_dump()
        for item in result:
            if item.idx_pair_xlate_group == idx_pair_xlate_group:
                self.assertEqual(
                    item.translation_group_name, name)
                break


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
