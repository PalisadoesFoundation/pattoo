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
from pattoo.db.table import language
from pattoo.db.models import Language
from pattoo.db import db



class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_idx_exists(self):
        """Testing method / function idx_exists."""
        # Add an entry to the database
        code = data.hashstring(str(random()))
        name = data.hashstring(str(random()))
        language.insert_row(code, name)

        # Make sure it exists
        idx_language = language.exists(code)

        # Verify the index exists
        result = language.idx_exists(idx_language)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method / function exists."""
        # Add an entry to the database
        code = data.hashstring(str(random()))
        name = data.hashstring(str(random()))
        language.insert_row(code, name)

        # Make sure it exists
        result = language.exists(code)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Add an entry to the database
        code = data.hashstring(str(random()))
        name = data.hashstring(str(random()))
        language.insert_row(code, name)

        # Make sure it exists
        idx_language = language.exists(code)

        # Verify the index exists
        result = language.idx_exists(idx_language)
        self.assertTrue(result)

    def test_update_name(self):
        """Testing method / function update_name."""
        # Add an entry to the database
        code = data.hashstring(str(random()))
        name = data.hashstring(str(random()))
        language.insert_row(code, name)

        # Get current name
        with db.db_query(20003) as session:
            result = session.query(Language.name).filter(
                Language.code == code.encode()).one()

        # Test
        self.assertEqual(name, result.name.decode())

        # Update the name
        new_name = data.hashstring(str(random()))
        language.update_name(code, new_name)

        # Get current name
        with db.db_query(20045) as session:
            result = session.query(Language.name).filter(
                Language.code == code.encode()).one()

        # Test
        self.assertEqual(new_name, result.name.decode())

    def test_cli_show_dump(self):
        """Testing method / function cli_show_dump."""
        # Add an entry to the database
        code = data.hashstring(str(random()))
        name = data.hashstring(str(random()))
        language.insert_row(code, name)

        # Make sure it exists
        idx_language = language.exists(code)

        result = language.cli_show_dump()
        for item in result:
            if item.idx_language == idx_language:
                self.assertEqual(item.name, name)
                self.assertEqual(item.code, code)
                break


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
