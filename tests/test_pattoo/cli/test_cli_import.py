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
from sqlalchemy import create_engine

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

# Pattoo imports
from pattoo.cli.cli_import import (process, _process_key_translation,
                                   _process_agent_translation)
from pattoo.db import db
from pattoo.cli.cli import _Import
from pattoo.db.models import BASE, PairXlate, AgentXlate, PairXlateGroup, Language

# Pattoo unittest imports
from tests.test_pattoo.cli.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig


class TestImport(unittest.TestCase):
    """Defines basic database setup and teardown methods"""

    travis_ci = os.getenv('travis_ci')

    def populate_fn(self, expected, cmd_args, target_table, parser, callback):
        """Allows for creation of csv file to test importation of translations for
        the process functions of cli_import

        Args:
            expected: key-value pairs to be stored in temporary csv file
            cmd_args: command line arguments to be parsed to be passed to callback
            target_table: database table to be queried
            parser: used to parse command line arguments
            callback: specific translation process function from cli_import module

        Return:
            queried_result: Result obtain from querying 'target_table'

        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv') as fptr:

            # Instantiation of csv writer object and fieldnames
            fieldnames = expected.keys()
            writer = csv.DictWriter(fptr, fieldnames=fieldnames)

            # Populating temporary csv file with key translation data
            writer.writeheader()
            writer.writerow(expected)
            fptr.seek(0)

            # Importing key_translation from temporary csv file
            args = parser.parse_args(cmd_args + ['--filename',
                                                 '{}'.format(fptr.name)])
            callback(args)

        # Updating language to match table language table name
        expected['idx_language'] = expected['language']
        del expected['language']

        result = None
        # Retrives stored key translation made using '_process_key_translation'
        with db.db_query(30002) as session:
            result = session.query(target_table).filter_by(translation = b'test_translation').first()

        # Asserting that each inserted element into PairXlate test tables matches
        # arguments passed to '_process_key_translation', as well asserts that a
        for key, value in expected.items():
            if key == 'idx_language':
                self.assertEqual(result.__dict__[key], self.language_count)
            elif target_table == AgentXlate and key == 'key':
                self.assertEqual(result.__dict__['agent_program'], value.encode())
            else:
                self.assertEqual(result.__dict__[key], value.encode())

        # Asserts created and modified columns were created.
        self.assertIsNotNone(result.ts_modified)
        self.assertIsNotNone(result.ts_created)

        return result

    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [PairXlate.__table__, AgentXlate.__table__, PairXlateGroup.__table__, Language.__table__]

            self.engine = create_tables(self.tables) # Returns engine object

            self.language_count = 1
            # Creating session object to make updates to tables in test database
            with db.db_modify(30001) as session:
                # Instantiation of test data in each table
                session.add(Language('en'.encode(), 'English'.encode(), 1))
                session.add(PairXlateGroup('pair_1'.encode(), 1))

                self.language_count = session.query(Language).count()
                session.commit()

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""

        # Skips class teardown if using travis-ci
        if not self.travis_ci:
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
        expected = {'language': 'en', 'key': 'test_key', 'translation':'test_translation', 'units': 'test_units'}
        cmd_args = ['import', 'key_translation', '--idx_pair_xlate_group', '1']
        result = self.populate_fn(expected, cmd_args, PairXlate, parser, _process_key_translation)

        # Asserts that idx_pair_xlate_group group matches requested group value
        self.assertEqual(result.idx_pair_xlate_group, 1)

        ####################################################################
        #
        # Testing for proper agent_translation execution
        #
        ####################################################################
        expected = {'language': 'en', 'key': 'test_key', 'translation': 'test_translation'}
        cmd_args = ['import', 'agent_translation']
        self.populate_fn(expected, cmd_args, AgentXlate, parser,
                         _process_agent_translation)

if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
