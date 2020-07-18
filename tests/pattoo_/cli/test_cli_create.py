#!/usr/bin/env python3
"""CLI create testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse

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
from pattoo.cli.cli_create import (process, _process_language,
                                   _process_pair_xlate_group)
from pattoo_shared import log
from pattoo.db import db
from pattoo.cli.cli import _Create
from pattoo.db.models import PairXlateGroup, Language
from pattoo.db.table import language, pair_xlate_group

# Pattoo unittest imports
from tests.bin.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig


class TestCLIImport(unittest.TestCase):
    """Tests importing new agent and key translation from csv files"""

    # Parser Instantiation
    parser = argparse.ArgumentParser()

    # Logger
    log_obj = log._GetLog()

    # Determine whether should setup up test for travis-ci tool
    travis_ci = os.getenv('travis_ci')

    def create_fn(self, expected, cmd_args, target_table, callback, process):
        """Creates either new key_translation_group or language entries

        Args:
            expected: testcase values
            cmd_args: command line arguments to be parsed to be passed to
            callback
            target_table: database table to be queried
            callback: specific cli_create function to be ran
            process: Boolean to indicate whether process is used to run either

        Return:
            None

        """
        # Instantiation of commandline arguments
        args = self.parser.parse_args(cmd_args)

        # Determine how to run callback based on value of process
        if process == True:
            with self.assertRaises(SystemExit):
                callback(args)
        else:
            callback(args)

        result = None
        # Retrieves updated result
        with db.db_query(33000) as session:
            query = session.query(target_table)
            result = query.filter_by(name = expected['name'].encode()).first()

        # Asserts that changes made usin the 'callback' function was reflected
        # in target_table
        for key, value in expected.items():
            result_value = result.__dict__[key]
            if type(result_value) == int:
                self.assertEqual(result_value, int(value))
            else:
                self.assertEqual(result_value, value.encode())

    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        # Setting up arpser to be able to parse import cli commands
        subparser = self.parser.add_subparsers(dest='action')
        _Create(subparser)

        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [PairXlateGroup.__table__, Language.__table__]

            # Returns engine object
            self.engine = create_tables(self.tables)

            # Inserting default entries
            language.insert_row('en', 'English')
            pair_xlate_group.insert_row('pair_1')

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""

        # Skips class teardown if using travis-ci
        if not self.travis_ci:
            teardown_tables(self.tables, self.engine)

    def test_process(self):
        """Test create argument process function"""

        # Testing for invalid args.qualifier
        args = self.parser.parse_args([])
        args.qualifier = ''
        self.assertIsNone(process(args))

        ####################################################################
        #
        # Testing for proper _process_language execution
        #
        ####################################################################

        # Defining table and expected entries into Language table
        code = 'fr'
        name = 'French'

        expected = {'code': code, 'name': name,}
        cmd_args = ['create', 'language', '--code', code, '--name', name]

        self.create_fn(expected, cmd_args, Language, process, True)

        ####################################################################
        #
        # Testing for proper _process_pair_xlate_group execution
        #
        ####################################################################

        # Defining table and expected entries into PairXlateGroup table
        name = 'pair_2'

        expected = {'name': name}
        cmd_args = ['create', 'key_translation_group', '--name', name]

        self.create_fn(expected, cmd_args, PairXlateGroup, process, True)

    def test__process_language(self):
        """Test _process_language"""

        # Defining table and expected entries into Language table
        code = 'cn'
        name = 'Chinese'

        expected = {'code': code, 'name': name,}
        cmd_args = ['create', 'language', '--code', code, '--name', name]

        self.create_fn(expected, cmd_args, Language, _process_language, False)

        # Asserting that appropriate log message is ran if language already
        # exists
        args = self.parser.parse_args([])
        args.code = code
        expected_included_str = ('''\
Language code "{}" already exists.'''.format(args.code))

        with self.assertLogs(self.log_obj.stdout(), level='INFO') as cm:
            print('Exception thrown testing test__process_language: ')
            with self.assertRaises(SystemExit):
                _process_language(args)
        print(cm.output[0])
        print('')
        self.assertIn(expected_included_str, cm.output[0])

    def test_process_pair_xlate_group(self):
        """Tests process_pair_xlate_group"""

        # Defining table and expected entries into PairXlateGroup table
        name = 'pair_group_test'

        expected = {'name': name}
        cmd_args = ['create', 'key_translation_group', '--name', name]

        self.create_fn(expected, cmd_args, PairXlateGroup,
                       _process_pair_xlate_group, False)

        # Asserting that appropriate log message is ran if pair_xlate_group
        # already exists
        args = self.parser.parse_args([])
        args.name = name
        expected_included_str = ('''\
Agent group name "{}" already exists.'''.format(args.name))

        with self.assertLogs(self.log_obj.stdout(), level='INFO') as cm:
            print('Exception thrown testing test__process_pair_xlate_group: ')
            with self.assertRaises(SystemExit):
                _process_pair_xlate_group(args)
        print(cm.output[0])
        print('')
        self.assertIn(expected_included_str, cm.output[0])

if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
