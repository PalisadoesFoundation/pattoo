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
from pattoo.db.table import agent_xlate, language
from pattoo.db.models import AgentXlate
from pattoo.db import db


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_agent_xlate_exists(self):
        """Testing method / function agent_xlate_exists."""
        # Add a language entry to the database
        code = data.hashstring(str(random()))
        _translation = data.hashstring(str(random()))
        language.insert_row(code, _translation)
        idx_language = language.exists(code)

        # Make sure row does not exist
        translation = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        result = agent_xlate.agent_xlate_exists(idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        agent_xlate.insert_row(key, translation, idx_language)

        # Test
        result = agent_xlate.agent_xlate_exists(idx_language, key)
        self.assertTrue(result)

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Add a language entry to the database
        code = data.hashstring(str(random()))
        _translation = data.hashstring(str(random()))
        language.insert_row(code, _translation)
        idx_language = language.exists(code)

        # Make sure row does not exist
        translation = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        result = agent_xlate.agent_xlate_exists(idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        agent_xlate.insert_row(key, translation, idx_language)

        # Test
        result = agent_xlate.agent_xlate_exists(idx_language, key)
        self.assertTrue(result)

    def test_update_row(self):
        """Testing method / function update_row."""
        # Add a language entry to the database
        code = data.hashstring(str(random()))
        _translation = data.hashstring(str(random()))
        language.insert_row(code, _translation)
        idx_language = language.exists(code)

        # Make sure row does not exist
        translation = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        result = agent_xlate.agent_xlate_exists(idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        agent_xlate.insert_row(key, translation, idx_language)

        # Test existence
        result = agent_xlate.agent_xlate_exists(idx_language, key)
        self.assertTrue(result)

        # Test update
        new_translation = data.hashstring(str(random()))
        agent_xlate.update_row(key, new_translation, idx_language)

        with db.db_query(20134) as session:
            row = session.query(AgentXlate).filter(and_(
                AgentXlate.agent_program == key.encode(),
                AgentXlate.idx_language == idx_language)).one()
        self.assertEqual(row.translation.decode(), new_translation)

    def test_update(self):
        """Testing method / function update."""
        # Add a language entry to the database
        code = data.hashstring(str(random()))
        _translation = data.hashstring(str(random()))
        language.insert_row(code, _translation)
        idx_language = language.exists(code)

        # Create data
        _data = []
        for key in range(0, 10):
            _data.append([code, str(key), '_{}_'.format(key)])
        _df0 = pd.DataFrame(_data, columns=['language', 'key', 'translation'])
        agent_xlate.update(_df0)

        # Update data
        _data = []
        for key in range(0, 10):
            _data.append([code, str(key), '|{}|'.format(key)])
        _df = pd.DataFrame(_data, columns=['language', 'key', 'translation'])
        agent_xlate.update(_df)

        # Test updated data
        for key in range(0, 10):
            with db.db_query(20135) as session:
                row = session.query(AgentXlate).filter(and_(
                    AgentXlate.agent_program == str(key).encode(),
                    AgentXlate.idx_language == idx_language)).one()
            self.assertEqual(row.translation.decode(), _df['translation'][key])

        # Old translations should not exist
        for translation in _df0['translation']:
            with db.db_query(20136) as session:
                row = session.query(AgentXlate).filter(and_(
                    AgentXlate.translation == translation.encode(),
                    AgentXlate.idx_language == idx_language))
            self.assertEqual(row.count(), 0)

    def test_cli_show_dump(self):
        """Testing method / function cli_show_dump."""
        # Add an entry to the database
        # Add a language entry to the database
        code = data.hashstring(str(random()))
        _translation = data.hashstring(str(random()))
        language.insert_row(code, _translation)
        idx_language = language.exists(code)

        # Make sure row does not exist
        translation = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        result = agent_xlate.agent_xlate_exists(idx_language, key)
        self.assertFalse(result)

        # Add an entry to the database
        agent_xlate.insert_row(key, translation, idx_language)

        result = agent_xlate.cli_show_dump()
        for item in result:
            if item.agent_program == key:
                self.assertEqual(item.translation, translation)
                break


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
