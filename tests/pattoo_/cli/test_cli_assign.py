#!/usr/bin/env python3
"""CLI Assign testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse
from unittest.mock import patch
from io import StringIO

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
from pattoo.cli.cli_import import (process, _process_key_translation,
                                   _process_agent_translation)
from pattoo_shared import log
from pattoo.db import db
from patoo.db.table import agent, pair_xlate_group
from pattoo.cli.cli import _Assign
from pattoo.db.models import (BASE, PairXlate, AgentXlate, PairXlateGroup,
                              Language)

# Pattoo unittest imports
from tests.bin.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig


class TestCLIAssign(unittest.TestCase):
    """Tests CLI assign module"""

    # Parser Instantiation
    parser = argparse.ArgumentParser()

    # Determine whether should setup up test for travis-ci tool
    travis_ci = os.getenv('travis_ci')

    def assign_fn(self, expected, cmd_args, target_table, callback, process):
        """

        Args:
            expected: testcase values
            cmd_args: command line arguments to be parsed to be passed to
            target_table: database table to be queried
            callback: specific cli_assign function to be ran
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

    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        # Setting up arpser to be able to parse import cli commands
        subparser = self.parser.add_subparsers(dest='action')
        _Assign(subparser)

        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [AgentXlate.__table__, PairXlateGroup.__table__]

            # Returns engine object
            self.engine = create_tables(self.tables)

            # Creating Agent and PairXlateGroup table entries
            agent.insert_row('test_agent_id_one', 'test_agent_target_one',
                             'test_agent_program_one')
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

        ####################################################################
        #
        # Testing for proper _process_agent execution
        #
        ####################################################################
        expected = {'language': 'en', 'key': 'test_key',
                    'translation':'test_translation', 'units': 'test_units'}
        cmd_args = ['assign', 'agent', '--idx_agent', idx_agent,
                    '--idx_pair_xlate_group', '1']
        result = self.populate_fn(expected, cmd_args, PairXlate, process, True)

    def test__process_agent(self):
        """Tests _process_agent"""
        pass


if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
