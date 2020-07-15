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
from pattoo.cli.cli_set import (process, _process_language,
                                   _process_pair_xlate_group)
from pattoo.db import db
from pattoo.db.table import language, pair_xlate_group
from pattoo.cli.cli import _Set
from pattoo.db.models import BASE, PairXlateGroup, Language
from pattoo_shared import log

# Pattoo unittest imports
from tests.bin.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig


class TestSet(unittest.TestCase):
    """Tests CLI set module"""

    # Parser Instantiation
    parser = argparse.ArgumentParser()

    # Determine whether should setup up test for travis-ci tool
    travis_ci = os.getenv('travis_ci')

    def set_fn(self, name, expected, cmd_args, target_table, callback, process):
        """Testing proper setting/updating of entries into a given table
        associated with the _process_language and _process_pair_xlate_group
        operations

        Args:
            name: current_name of a given element within target_table
            expected: testcase values
            cmd_args: command line arguments to be parsed to be passed to
            callback
            target_table: database table to be queried
            callback: specific cli_set function to be ran
            process: Boolean to indicate whether process is used to run either
            _process_language or _process_pair_xlate_group

        Return:

        """
        # Instantiation of commandline arguments
        args = self.parser.parse_args(cmd_args)

        _ts_modified = None
        # Retrieves the current ts_modified before updates are made
        with db.db_query(31000) as session:
            query = session.query(target_table)
            queried_result = query.filter_by(name = name.encode()).first()
            _ts_modified = queried_result.ts_modified

        # Determine how to run callback based on value of process
        if process == True:
            with self.assertRaises(SystemExit):
                callback(args)
        else:
            callback(args)

        result = None
        # Retrieves updated result
        with db.db_query(31002) as session:
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

        # Asserts that result ts_modified time was updated
        self.assertGreaterEqual(result.ts_modified, _ts_modified)

    def remove_test_entry(self, name, target_table):
        """Removes a given test entry from a target table

        Args:
            name: Corresponding name of test entry in target_table
            target_table: Table to look for entry to be removed

        Return:
            None

        """
        with db.db_modify(31003) as session:
            query = session.query(target_table)
            entry = query.filter_by(name = name.encode()).first()
            session.delete(entry)
            session.commit()

    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        # Setting up parsing for cli_set module
        subparser = self.parser.add_subparsers(dest='action')
        _Set(subparser)

        # Logger
        self.log_obj = log._GetLog()

        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [PairXlateGroup.__table__, Language.__table__]

            # Returns engine object
            self.engine = create_tables(self.tables)

            # Creating session object to make updates to tables in test
            # database
            with db.db_modify(30005) as session:
                # Instantiation of test data in each table
                session.add(Language('en'.encode(), 'English'.encode(), 1))
                session.add(PairXlateGroup('Pattoo Default'.encode(), 1))

        self.idx_pair_xlate_group_count = 1
        # Getting number of entries in PairXlateGroup table
        with db.db_query(30004) as session:
            result = session.query(PairXlateGroup)
            self.idx_pair_xlate_group_count += result.count()

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""

        # Skips class teardown if using travis-ci
        if not self.travis_ci:
            teardown_tables(self.tables, self.engine)

    def test_process(self):
        """Test import argument process function"""

        # Testing for invalid args.qualifier
        args = self.parser.parse_args([])
        args.qualifier = ''
        self.assertIsNone(process(args))

        ####################################################################
        #
        # Testing for proper _process_language execution
        #
        ####################################################################
        current_name = 'Chinese'
        expected = {'code': 'fr', 'name': 'French'}
        cmd_args = ['set', 'language', '--code', expected['code'], '--name',
                    expected['name']]

        # Inserting test language entry into Language table
        language.insert_row(expected['code'], current_name)

        # Asserting that updates were made in Language table
        self.set_fn(current_name, expected, cmd_args, Language, process, True)

        ####################################################################
        #
        # Testing for proper _process_pair_xlate_group execution
        #
        ####################################################################
        current_name = 'TEST GROUP'
        expected = {'name': 'TEST GROUP NAME CHANGE', 'idx_pair_xlate_group':
                    self.idx_pair_xlate_group_count}
        cmd_args = ['set', 'key_translation_group', '--idx_pair_xlate_group',
                    str(expected['idx_pair_xlate_group']), '--name',
                     expected['name']]

        self.idx_pair_xlate_group_count += 1

        # Inserting test pair_xlate_group entry into PairXlateGroup table
        pair_xlate_group.insert_row(current_name)

        # Asserting that updates were made in the PairXlateGroup table
        self.set_fn(current_name, expected, cmd_args, PairXlateGroup, process,
                    True)

    def test__process_language(self):
        "Tests _process_language"
        current_name = 'Spanish'
        expected = {'code': 'cn', 'name': 'Chinese'}
        cmd_args = ['set', 'language', '--code', expected['code'], '--name',
                    expected['name']]

        # Inserting test language entry into Language table
        language.insert_row(expected['code'], current_name)

        # Asserting that updates were made in Language table
        self.set_fn(current_name, expected, cmd_args, Language,
                    _process_language, False)

        # Asserting that if a language is not found an appropirate log message
        # is shown
        args = self.parser.parse_args([])
        args.code = 'random_code'
        expected_included_str = 'Language code "{}" not found'.format(args.code)

        with self.assertLogs(self.log_obj.stdout(), level='INFO') as cm:
            print('Exception thrown testing test__process_language: ')
            with self.assertRaises(SystemExit):
                _process_language(args)
        self.assertIn(expected_included_str, cm.output[0])

    def test__process_pair_xlate_group(self):
        "Tests _process_pair_xlate_group"
        current_name = 'Process Xlate Test Entry'
        expected = {'name': 'Xlate Changed Entry', 'idx_pair_xlate_group':
                    self.idx_pair_xlate_group_count}
        cmd_args = ['set', 'key_translation_group', '--idx_pair_xlate_group',
                    str(expected['idx_pair_xlate_group']), '--name',
                     expected['name']]

        self.idx_pair_xlate_group_count += 1

        # Inserting test pair_xlate_group entry into PairXlateGroup table
        pair_xlate_group.insert_row(current_name)

        # Asserting that updates were made in the PairXlateGroup table
        self.set_fn(current_name, expected, cmd_args, PairXlateGroup,
                    _process_pair_xlate_group, False)

        def log_test(idx_pair_xlate_group, expected_included_str, args_name=''):
            """Asserts that given log message is shown given a particular error

            Args:
                idx_pair_xlate_group: Index number to be quiered

            Return:
                None

            """
            # Setting up args
            args = self.parser.parse_args([])
            args.idx_pair_xlate_group = idx_pair_xlate_group
            args.name = args_name

            with self.assertLogs(self.log_obj.stdout(), level='INFO') as cm:
                print('Exception thrown testing test__process_language: ')
                with self.assertRaises(SystemExit):
                    _process_pair_xlate_group(args)
            print(cm.output[0])
            print('')
            self.assertIn(expected_included_str, cm.output[0])

        # Testing for log message when translation group is not found
        mock_idx = self.idx_pair_xlate_group_count + 1
        expected = 'Translation group "{}" not found'.format(mock_idx)
        log_test(mock_idx, expected)

        # Testiing for log message when translation group already exists
        mock_idx = 1
        mock_name = 'Pattoo Default'
        expected= 'Translation group "{}" already exists'.format(mock_name)
        log_test(mock_idx, expected, mock_name)

        # Testiing for log message when translation group requested to bchanged
        # is the first element
        mock_idx = 1
        mock_name = 'test_name_change'
        expected = 'Cannot change Translation group "1".'
        log_test(mock_idx, expected, mock_name)


if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
