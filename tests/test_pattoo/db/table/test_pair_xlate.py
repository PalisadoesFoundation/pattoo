#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random

# PIP3
import pandas as pd
from sqlalchemy import and_

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

    def test_pair_xlate_exists(self):
        """Testing method / function pair_xlate_exists."""
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
        units = data.hashstring(str(random()))
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        pair_xlate.insert_row(
            key, description, units, idx_language, idx_pair_xlate_group)

        # Test
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertTrue(result)

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
        units = data.hashstring(str(random()))
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        pair_xlate.insert_row(
            key, description, units, idx_language, idx_pair_xlate_group)

        # Test
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertTrue(result)

    def test_update_row(self):
        """Testing method / function update_row."""
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
        units = data.hashstring(str(random()))
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        pair_xlate.insert_row(
            key, description, units, idx_language, idx_pair_xlate_group)

        # Test existence
        result = pair_xlate.pair_xlate_exists(
            idx_pair_xlate_group, idx_language, key)
        self.assertTrue(result)

        # Test update
        new_description = data.hashstring(str(random()))
        pair_xlate.update_row(
            key, new_description, units, idx_language, idx_pair_xlate_group)

        with db.db_query(20071) as session:
            row = session.query(PairXlate).filter(and_(
                PairXlate.idx_pair_xlate_group == idx_pair_xlate_group,
                PairXlate.key == key.encode(),
                PairXlate.idx_language == idx_language)).one()
        self.assertEqual(row.description.decode(), new_description)

    def test_update(self):
        """Testing method / function update."""
        # Add a language and pair_xlate_group entry to the database
        code = data.hashstring(str(random()))
        _description = data.hashstring(str(random()))
        language.insert_row(code, _description)
        idx_language = language.exists(code)
        pair_xlate_group.insert_row(_description)
        idx_pair_xlate_group = pair_xlate_group.exists(_description)

        # Create data
        _data = []
        for key in range(0, 10):
            _data.append(
                [code, str(key), '_{}_'.format(key), '0{}0'.format(key)])
        _df0 = pd.DataFrame(_data, columns=[
            'language', 'key', 'description', 'units'])
        pair_xlate.update(_df0, idx_pair_xlate_group)

        # Update data
        _data = []
        for key in range(0, 10):
            _data.append(
                [code, str(key), '|{}|'.format(key), '1{}1'.format(key)])
        _df = pd.DataFrame(_data, columns=[
            'language', 'key', 'description', 'units'])
        pair_xlate.update(_df, idx_pair_xlate_group)

        # Test updated data
        for key in range(0, 10):
            with db.db_query(20125) as session:
                row = session.query(PairXlate).filter(and_(
                    PairXlate.idx_pair_xlate_group == idx_pair_xlate_group,
                    PairXlate.key == str(key).encode(),
                    PairXlate.idx_language == idx_language)).one()
            self.assertEqual(row.description.decode(), _df['description'][key])
            self.assertEqual(row.units.decode(), _df['units'][key])

        # Old descriptions should not exist
        for description in _df0['description']:
            with db.db_query(20126) as session:
                row = session.query(PairXlate).filter(and_(
                    PairXlate.idx_pair_xlate_group == idx_pair_xlate_group,
                    PairXlate.description == description.encode(),
                    PairXlate.idx_language == idx_language))
            self.assertEqual(row.count(), 0)

    def test_cli_show_dump(self):
        """Testing method / function cli_show_dump."""
        # Add an entry to the database
        description = data.hashstring(str(random()))
        pair_xlate_group.insert_row(description)

        # Make sure it exists
        idx_pair_xlate_group = pair_xlate_group.exists(description)

        result = pair_xlate.cli_show_dump()
        for item in result:
            if item.idx_pair_xlate_group == idx_pair_xlate_group:
                self.assertEqual(item.name, description)
                break


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
