#!/usr/bin/env python3
"""CLI import testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse
import tempfile
import csv

# SQLALCHMEY Imports
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
    # elsewhere on the system using PIP. This could corrupt test_data results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo.cli.cli_import import (process, _process_key_translation,
                                   _process_agent_translation)
from pattoo.cli.cli import _Import
from pattoo.db.models import PairXlate, AgentXlate, PairXlateGroup, Language
from tests.test_pattoo.cli.setup_db import create_tables, teardown_tables

class TestImport(unittest.TestCase):
    """Defines basic database setup and teardown methods"""

    key_test_data = 'key_translation_test_data.csv'
    agent_test_data = 'agent_translation_test_data.csv'

    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        # Create test tables for Import test
        self.tables = [PairXlate.__table__, AgentXlate.__table__, PairXlateGroup.__table__, Language.__table__]

        self.engine = create_tables(self.tables) # Returns engine object

        # Creating session object to make updates to tables in test database
        self.session = sessionmaker(bind=self.engine)()

        # Instantiation of test data in each table
        self.session.add(Language('en'.encode(), 'English'.encode(), 1))
        self.session.add(PairXlateGroup('pair_1'.encode(), 1))
        self.session.commit()

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""
        self.session.close()
        teardown_tables(self.tables, self.engine)

    def test_process(self):
        """Test import argument process function"""

        # Setting up args parseer
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest='action')
        _Import(subparser)
        args = parser.parse_args([])

        # Testing for invalid args.qualifier
        args.qualifier = ''
        self.assertIsNone(process(args))

        ####################################################################
        #
        # Testing for proper key_translation execution
        #
        ####################################################################
        test_data = {'language': 'en', 'key': 'test_key', 'translation':'test_translation', 'units': 'test_units'}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv') as fptr:

            # Instantiation of csv writer object and fieldnames
            fieldnames = test_data.keys()
            writer = csv.DictWriter(fptr, fieldnames=fieldnames)

            # Populating temporary csv file with key translation data
            writer.writeheader()
            writer.writerow(test_data)
            fptr.seek(0)

            # Importing key_translation from temporary csv file
            args = parser.parse_args(['import', 'key_translation', '--idx_pair_xlate_group',
                              '1', '--filename', '{}'.format(fptr.name)])
            _process_key_translation(args)

        # Create new PairXlate object
        test_data['idx_language'] = test_data['language']
        del test_data['language']
        expected = PairXlate(1, **test_data)

        # Querying test database for stored results from _process_key_translation
        queried_result = self.session.query(PairXlate).first()
        print(queried_result)

        # Testing for proper agent_translation execution
        args.qualifier = 'agent_translation'

    def test__process_key_translation(self):
        pass

    def test_process_agent_translation(self):
        pass
