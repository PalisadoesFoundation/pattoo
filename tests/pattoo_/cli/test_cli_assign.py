#!/usr/bin/env python3
"""CLI Assign testing"""

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
from pattoo.cli.cli_assign import process, _process_agent
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.table import agent, pair_xlate_group, language
from pattoo.cli.cli import _Assign
from pattoo.db.models import Agent, PairXlateGroup, Language

# Pattoo unittest imports
from tests.bin.setup_db import create_tables, teardown_tables, DB_URI
from tests.libraries.configuration import UnittestConfig


class TestCLIAssign(unittest.TestCase):
    """Tests CLI assign module"""

    # Parser Instantiation
    parser = argparse.ArgumentParser()

    # Logger
    log_obj = log._GetLog()

    # Determine whether should setup up test for travis-ci tool
    travis_ci = os.getenv('travis_ci')

    def assign_fn(self, expected, cmd_args, target_table, callback, process):
        """

        Args:
            expected: testcase values
            cmd_args: command line arguments to be parsed to be passed to
            callback
            target_table: database table to be queried
            callback: specific cli_assign function to be ran
            process: Boolean to indicate whether process is used to run either

        Return:
            None

        """
        # Calling cmd_args using argparse method parse_args
        args = self.parser.parse_args(cmd_args)

        # Determine how to run callback based on value of process
        if process is True:
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
        _Assign(subparser)

        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [
                Agent.__table__,
                PairXlateGroup.__table__,
                Language.__table__
            ]

            # Returns engine object
            self.engine = create_tables(self.tables)

            # Creates test entries in Language and PairXlateGroup tables
            language.insert_row('en', 'English')
            pair_xlate_group.insert_row('test_pair_xlate_group_one')

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from database."""

        # Skips class teardown if using travis-ci
        if not self.travis_ci:
            teardown_tables(self.tables, self.engine)

    def test_process(self):
        """Tests assign argument process function."""

        # Testing for invalid args.qualifier
        args = self.parser.parse_args([])
        args.qualifier = ''
        self.assertIsNone(process(args))

        ####################################################################
        #
        # Testing for proper _process_agent execution
        #
        ####################################################################

        # Agent information
        agent_id = 'test_agent_id_one'
        agent_target = 'test_agent_target_one'
        agent_program = 'test_agent_program_one'

        # Inserting agent data and getting agent idx_agent value
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.idx_agent(agent_id, agent_target, agent_program)

        # Derfining expected data and command line entries to be passed to
        # process function
        expected = {
            'idx_agent': idx_agent,
            'idx_pair_xlate_group': '1'
        }
        cmd_args = [
            'assign', 'agent', '--idx_agent', str(idx_agent),
            '--idx_pair_xlate_group', expected['idx_pair_xlate_group']]

        self.assign_fn(expected, cmd_args, Agent, process, True)

    def test__process_agent(self):
        """Tests _process_agent"""

        # Agent information
        agent_id = 'test_process_agent_one'
        agent_target = 'test_process_agent_one'
        agent_program = 'test_process_agent_progam_one'

        # Inserting agent data and getting agent idx_agent value
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.idx_agent(agent_id, agent_target, agent_program)

        # Derfining expected data and command line entries to be passed to
        # process function
        expected = {
            'idx_agent': idx_agent,
            'idx_pair_xlate_group': '1'
        }
        cmd_args = [
            'assign', 'agent', '--idx_agent', str(idx_agent),
            '--idx_pair_xlate_group', expected['idx_pair_xlate_group']]

        self.assign_fn(expected, cmd_args, Agent, _process_agent, False)

        # Asserting that appropriate log message is ran if idx_pair_xlate_group
        # does not exist
        args = self.parser.parse_args([])
        args.idx_pair_xlate_group = ''
        expected_included_str = ('''\
idx_pair_xlate_group "{}" not found.'''.format(args.idx_pair_xlate_group))

        with self.assertLogs(self.log_obj.stdout(), level='INFO') as cm:
            print('Exception thrown testing test__process_agent: ')
            with self.assertRaises(SystemExit):
                _process_agent(args)
        self.assertIn(expected_included_str, cm.output[0])

        # Asserting that appropriate log message is ran if idx_agent does not
        # exist
        args = self.parser.parse_args([])
        args.idx_pair_xlate_group = '1'
        args.idx_agent = ''
        expected_included_str = ('''\
idx_agent "{}" not found.'''.format(args.idx_agent))

        with self.assertLogs(self.log_obj.stdout(), level='INFO') as cm:
            print('Exception thrown testing test__process_agent: ')
            with self.assertRaises(SystemExit):
                _process_agent(args)
        self.assertIn(expected_included_str, cm.output[0])


if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
