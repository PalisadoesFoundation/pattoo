#!/usr/bin/env python3
"""CLI import testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse
import tempfile
import csv

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}cli'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from pattoo.cli.cli_import import (
    process, _process_key_translation, _process_agent_translation)
from pattoo_shared import log
from pattoo.db import db
from pattoo.cli.cli import _Import
from pattoo.db.table import language
from pattoo.db.models import PairXlate, AgentXlate

# Pattoo unittest imports
from setup._pattoo import db as db_cli
from tests.libraries.configuration import UnittestConfig
from tests.libraries import general


class TestCLIImport(unittest.TestCase):
    """Tests importing new agent and key translation from csv files"""

    # Parser Instantiation
    parser = argparse.ArgumentParser()

    # Determine whether should setup up test for travis-ci tool
    travis_ci = os.getenv('travis_ci')

    # Number of expected languages
    language_code = general.random_string()
    language_count = 2

    def populate_fn(
            self, expected, cmd_args, target_table, callback, _process):
        """Allows for creation of csv file to test importation of translations
        for the process functions of cli_import

        Args:
            expected: key-value pairs to be stored in temporary csv file
            cmd_args: command line arguments to be parsed to be passed to
            callback
            target_table: database table to be queried
            callback: specific translation process function from cli_import
            module
            _process: Boolean to indicate whether process is used to run either
            _process_key_translation or _process_agent_translation

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
            args = self.parser.parse_args(
                cmd_args + ['--filename', '{}'.format(fptr.name)])

            # Determine how to run callback based on value of process
            if _process is True:
                with self.assertRaises(SystemExit):
                    callback(args)
            else:
                callback(args)

        # Updating language to match table language table name
        expected['idx_language'] = expected['language']
        del expected['language']

        result = None
        # Retrives result using stored key translation
        with db.db_query(30002) as session:
            query = session.query(target_table)
            result = query.filter_by(
                translation=expected['translation'].encode()).first()

        # Asserting that each inserted element into target_table test tables
        # matches arguments passed to 'callback' function
        for key, value in expected.items():
            if key == 'idx_language':
                self.assertEqual(result.__dict__[key], self.language_count)
            elif target_table == AgentXlate and key == 'key':
                self.assertEqual(result.__dict__['agent_program'],
                                 value.encode())
            else:
                self.assertEqual(result.__dict__[key], value.encode())

        # Asserts created and modified columns were created.
        self.assertIsNotNone(result.ts_modified)
        self.assertIsNotNone(result.ts_created)

        return result

    def _process_log_test(self, callback):
        """Testing proper log message in _process_key_translation and
        _process_agent_translation

        Args:
            callback: Function to be tested for correct log outputs

        Return:
            None

        """
        # Testing for log message invalid filename is passed
        args = self.parser.parse_args([])
        args.filename = 'test_pattoo'
        expected_included_str = 'File {} does not exist'.format(args.filename)

        log_obj = log._GetLog()
        with self.assertLogs(log_obj.stdout(), level='CRITICAL') as cm_:
            with self.assertRaises(SystemExit):
                callback(args)
        self.assertIn(expected_included_str, cm_.output[0])

    @classmethod
    def setUpClass(cls):
        """Setup tables in pattoo_unittest database"""
        # Create the database for testing
        cls.database = db_cli.Database()
        cls.database.recreate()

        # Setting up arpser to be able to parse import cli commands
        subparser = cls.parser.add_subparsers(dest='action')
        _Import(subparser)

        # Creating test data in Language and PairXlateGroup tables
        language.insert_row(cls.language_code, general.random_string)

    @classmethod
    def tearDownClass(cls):
        """Cleanup."""

        # Recreate a fresh database so that other tests can run without error
        cls.database.recreate()

    def test_process(self):
        """Test import argument process function"""

        # Testing for invalid args.qualifier
        args = self.parser.parse_args([])
        args.qualifier = ''
        self.assertIsNone(process(args))

        ####################################################################
        #
        # Testing for proper key_translation execution
        #
        ####################################################################
        expected = {
            'language': self.language_code,
            'key': 'test_key',
            'translation': 'test_translation',
            'units': 'test_units'
        }
        cmd_args = ['import', 'key_translation', '--idx_pair_xlate_group', '1']
        result = self.populate_fn(expected, cmd_args, PairXlate, process, True)

        # Asserts that idx_pair_xlate_group group matches requested group value
        self.assertEqual(result.idx_pair_xlate_group, 1)

        ####################################################################
        #
        # Testing for proper agent_translation execution
        #
        ####################################################################
        expected = {
            'language': self.language_code,
            'key': 'test_key',
            'translation': 'test_translation'
        }
        cmd_args = ['import', 'agent_translation']
        self.populate_fn(expected, cmd_args, AgentXlate, process, True)

    def test__process_key_translation(self):
        """Tests process_key_translation"""

        # Valid Input Testing
        expected = {
            'language': self.language_code,
            'key': 'test_key_process_translation',
            'translation': 'test_key_translation',
            'units': 'test_key_units'
        }
        cmd_args = ['import', 'key_translation', '--idx_pair_xlate_group', '1']
        result = self.populate_fn(expected, cmd_args, PairXlate,
                                  _process_key_translation, False)

        # Asserts that idx_pair_xlate_group group matches requested group value
        self.assertEqual(result.idx_pair_xlate_group, 1)

        # Testing for log message invalid filename is passed
        self._process_log_test(_process_key_translation)

    def test__process_agent_translation(self):
        """Tests process_key_translation"""

        expected = {
            'language': self.language_code,
            'key': 'test_agent',
            'translation': 'test_agent_translation'
        }
        cmd_args = ['import', 'agent_translation']
        self.populate_fn(
            expected, cmd_args, AgentXlate, _process_agent_translation, False)

        # Testing for log message invalid filename is passed
        self._process_log_test(_process_agent_translation)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
