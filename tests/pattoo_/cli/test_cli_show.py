#!/usr/bin/env python3
"""CLI import testing"""

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
from pattoo.cli.cli_show import (_process, _process_agent, _process_language,
                                 _pr_process_pair_xlate_group,
                                 _process_pair_xlate, _process_agent_xlate,
                                 _printer)
from pattoo.db import db
from pattoo.cli.cli import _Show
from pattoo.db.models import (PairXlate, AgentXlate, PairXlateGroup, Language,
                              Agent)

# Pattoo unittest imports
from tests.bin.setup_db import (create_tables, teardown_tables, DB_URI)


class TestCLIShow(unittest.TestCase):
    """Tests CLI show module"""

    # Parser Instantiation
    parser = argparse.ArgumentParser()

    # Logger
    log_obj = log._GetLog()

    # Determine whether should setup up test for travis-ci tool
    travis_ci = os.getenv('travis_ci')

    def show_fn(self, expected, cmd_args, target_table, callback, process):
        """

        Args:
            expected: testcase values
            cmd_args: command line arguments to be parsed to be passed to
            callback
            target_table: database table to be queried
            callback: specific cli_show function to be ran
            process: Boolean to indicate whether process is used to run either

        Return:
            None

        """
        # Calling cmd_args using argparse method parse_args
        args = self.parser.parse_args(cmd_args)

        # Determine how to run callback based on value of process
        if process == True:
            with self.assertRaises(SystemExit):
                callback(args)
        else:
            callback(args)

        result = None
        # Retrieves updated result
        with db.db_query(32000) as session:
            query = session.query(target_table)
            result = query.filter_by(idx_agent = expected['idx_agent']).first()

        # Asserts that changes made using the 'callback' function was reflected
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
        _(subparser)

        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [AgentXlate.__table__, PairXlate.__table__,
                           Agent.__table__, PairXlateGroup.__table__,
                           Language.__table__]

            # Returns engine object
            self.engine = create_tables(self.tables)

            # Creates test entries in Language and PairXlateGroup tables
            language.insert_row('en', 'English')
            pair_xlate_group.insert_row('test_pair_xlate_group_one')

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""

        # Skips class teardown if using travis-ci
        if not self.travis_ci:
            teardown_tables(self.tables, self.engine)

    def test_process(self):
        """Tests assign argument process function"""

        # Testing for invalid args.qualifier
        args = self.parser.parse_args([])
        args.qualifier = ''
        self.assertIsNone(process(args))
