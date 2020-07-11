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
from pattoo.cli.cli import _Import
from pattoo.db.models import BASE, PairXlate, AgentXlate, PairXlateGroup, Language

# Pattoo unittest imports
from tests.test_pattoo.cli.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig

class TestImport(unittest.TestCase):
    """Defines basic database setup and teardown methods"""

    travis_ci = os.getenv('travis_ci')

    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [PairXlate.__table__, AgentXlate.__table__, PairXlateGroup.__table__, Language.__table__]

            self.engine = create_tables(self.tables) # Returns engine object

            # Creating session object to make updates to tables in test database
            self.session = sessionmaker(bind=self.engine)()

            # Instantiation of test data in each table
            self.session.add(Language('fr'.encode(), 'French'.encode(), 1))
            self.session.add(PairXlateGroup('pair_1'.encode(), 1))

            self.language_count = self.session.query(Language).count()
            self.session.commit()
        else:
            # Creating session object to for making updates to test database for
            # tests
            self.session = sessionmaker(bind=create_engine(DB_URI))()

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""

        # Skips class teardown if using travis-ci
        if not self.travis_ci:
            print('tables teardown')
            print(self.tables, self.engine)
            teardown_tables(self.tables, self.engine)
        print('session closing')
        self.session.close()

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
        expected = {'language': 'fr', 'key': 'test_key', 'translation':'test_translation', 'units': 'test_units'}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv') as fptr:

            # Instantiation of csv writer object and fieldnames
            fieldnames = expected.keys()
            writer = csv.DictWriter(fptr, fieldnames=fieldnames)

            # Populating temporary csv file with key translation data
            writer.writeheader()
            writer.writerow(expected)
            fptr.seek(0)

            # Importing key_translation from temporary csv file
            args = parser.parse_args(['import', 'key_translation', '--idx_pair_xlate_group',
                              '1', '--filename', '{}'.format(fptr.name)])
            _process_key_translation(args)

        # Create new PairXlate object
        expected['idx_language'] = expected['language']
        del expected['language']

        # Retrives stored key translation made using '_process_key_translation'
        queried_result = self.session.query(PairXlate).filter_by(key =
                                                                 b'test_key').first()

        # Asserting that each inserted elment into PairXlate test tables matches
        # arguments passed to '_process_key_translation', as well asserts that a
        for key, value in expected.items():
            if key == 'idx_language':
                self.assertEqual(queried_result.__dict__[key],
                                 self.language_count)
            else:
                self.assertEqual(queried_result.__dict__[key], value.encode())

        # Asserts created and modified columns were created.
        self.assertIsNotNone(queried_result.ts_modified)
        self.assertIsNotNone(queried_result.ts_created)

        # Asserts that idx_pair_xlate_group group matches requested group value
        self.assertEqual(queried_result.idx_pair_xlate_group, 1)

        # Testing for proper agent_translation execution
        args.qualifier = 'agent_translation'

    def test__process_key_translation(self):
        pass

    def test_process_agent_translation(self):
        pass

if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
