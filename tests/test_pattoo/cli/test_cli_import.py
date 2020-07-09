#!/usr/bin/env python3
"""CLI import testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse

# SQLALCHMEY Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}test_pattoo{0}cli'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo Imports
from pattoo.cli.cli_import import process, _process_key_translation, _process_agent_translation
from pattoo.db.models import BASE, PairXlate, AgentXlate, PairXlateGroup, Language

class TestImport(unittest.TestCase):
    """Defines basic database setup and teardown methods"""


    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        # Creating engine to interface with test database
        # Creating session object to make updates to tables in test database
        self.engine = create_engine('mysql://:@localhost/pattoo_unittest')
        self.session = sessionmaker(bind=self.engine)()

        # Create test tables for Import test
        self.tables = [PairXlate.__table__, AgentXlate.__table__, PairXlateGroup.__table__, Language.__table__]
        BASE.metadata.create_all(self.engine, tables=self.tables)

        # Instantiation of test data in each table
        self.session.add(Language('en'.encode(), 'English'.encode(), 1))
        self.session.add(PairXlateGroup('pair_1'.encode(), 1))
        self.session.commit()

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""
        self.session.close()
        BASE.metadata.drop_all(self.engine, tables=self.tables)

    def test_process(self):
        """Test import argument process function"""

        # Setting up args parseer
        parser = argparse.ArgumentParser()
        args = parser.parse_args(['--qualifier', ''])

        # Testing for invalid args.qualifier
        self.assertIsNone(process(args))

        # Testing for proper key_translation execution
        args.qualifier = 'key_translation'

        # Testing for proper agent_translation execution
        args.qualifier = 'agent_translation'

    def test__process_key_translation(self):
        pass

    def test_process_agent_translation(self):
        pass
