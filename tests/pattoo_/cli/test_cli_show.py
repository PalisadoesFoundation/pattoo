#!/usr/bin/env python3
"""CLI import testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse
from unittest.mock import patch
from io import StringIO

# SQLALCHMEY imports
from sqlalchemy import create_engine

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
from pattoo.cli.cli_show import (process, _process_agent, _process_language,
                                 _process_pair_xlate_group,
                                 _process_pair_xlate, _process_agent_xlate,
                                 _printer)
from pattoo.cli.cli import _Show
from pattoo.db import db
from pattoo.db.table import (agent, language, pair_xlate, pair_xlate_group,
                             agent_xlate)
from pattoo.db.models import (Agent, AgentXlate, Language, PairXlate,
                              PairXlateGroup)
from setup._pattoo import db as setup_database

# Pattoo unittest imports
from tests.bin.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig

# class TestCLIShow(unittest.TestCase):
    # """Tests CLI show module"""

    # # Parser Instantiation
    # parser = argparse.ArgumentParser()

    # # Binding engine
    # engine = create_engine(DB_URI)

    # # Determine whether should setup up test for travis-ci tool
    # travis_ci = os.getenv('travis_ci')

    # def show_fn(self, table_module, callback, process=False, cmd_args=None):
        # """

        # Args:
            # table_module: module that has a cli_show_dump method
            # callback: specific cli_show function to be ran
            # cmd_args

        # Return:
            # None

        # """
        # # Instantiate expected and callback_output
        # expected, callback_output = '', ''

        # # Parsing arguments
        # args = self.parser.parse_args(cmd_args)

        # # Gets callback stdout output
        # with patch('sys.stdout', new = StringIO()) as output:
            # if callback.__name__ in ['_process_pair_xlate', 'process']:
                # if callback.__name__ == 'process':
                    # with self.assertRaises(SystemExit):
                        # callback(args)
                # else:
                    # callback(args)
            # else:
                # callback()
            # callback_output = output.getvalue()

        # # Generating expected stdout output
        # if (callback.__name__ == '_process_pair_xlate' or table_module ==
            # pair_xlate):
            # data = table_module.cli_show_dump(args.idx_pair_xlate_group)
        # else:
            # data = table_module.cli_show_dump()

        # Gets expected stoud output using _printer
        # with patch('sys.stdout', new = StringIO()) as output:
            # _printer(data)
            # expected = output.getvalue()

        # self.assertEqual(callback_output, expected)

    # @classmethod
    # def setUpClass(self):
        # """Setup tables in pattoo_unittest database"""

        # # Setting up arpser to be able to parse import cli commands
        # subparser = self.parser.add_subparsers(dest='action')
        # _Show(subparser)

        # # Creates new database tables for test cli_show module
        # self.tables = [Agent.__table__, AgentXlate.__table__,
                       # Language.__table__, PairXlate.__table__,
                       # PairXlateGroup.__table__]
        # create_tables(self.tables)

        # # Test Insertions
        # setup_database._insert_language()
        # setup_database._insert_pair_xlate_group()
        # setup_database._insert_agent_xlate()

        # agent.insert_row('agent_id', 'agent_test_target', 'agent_program')
        # pair_xlate.insert_row('xlate_key', 'xlate_translation', 'xlate_units',
                              # 1, 1)

    # @classmethod
    # def tearDownClass(self):
        # """End session and drop all test tables from pattoo_unittest database"""

        # # Skips class teardown if using travis-ci
        # if not self.travis_ci:
            # teardown_tables(self.engine)

    # def test_process(self):
        # """Tests show process function"""

        # # Testing for invalid args.qualifier
        # args = self.parser.parse_args([])
        # args.qualifier = ''
        # self.assertIsNone(process(args))

        # test_vars = [('agent', agent), ('language', language),
                 # ('key_translation_group', pair_xlate_group),
                 # ('key_translation', pair_xlate), ('agent_translation',
                                                   # agent_xlate)]

        # for arg, fn in test_vars:
            # if arg == 'key_translation':
                # cmd_args = ['show', arg, '--idx_pair_xlate_group', '1']
                # self.show_fn(fn, process, True, cmd_args)
            # self.show_fn(fn, process, True, ['show', arg])


    # def test__process_agent(self):
        # """Tests _process_agent"""
        # self.show_fn(agent, _process_agent)

    # def test__process_language(self):
        # """Tests _process_agent"""
        # self.show_fn(language, _process_language)

    # def test__process_pair_xlate_group(self):
        # """Tests _process_agent"""
        # self.show_fn(pair_xlate_group, _process_pair_xlate_group)

    # def test__process_pair_xlate(self):
        # """Tests _process_agent"""
        # cmd_args = ['show', 'key_translation']
        # self.show_fn(pair_xlate, _process_pair_xlate, cmd_args=cmd_args)

        # cmd_args = ['show', 'key_translation', '--idx_pair_xlate_group', '1']
        # self.show_fn(pair_xlate, _process_pair_xlate, cmd_args=cmd_args)

    # def test__process_agent_xlate(self):
        # """Tests _process_agent"""
        # self.show_fn(agent_xlate, _process_agent_xlate)


# if __name__ == "__main__":
    # # Make sure the environment is OK to run unittests
    # config = UnittestConfig()
    # config.create()

    # # Do the unit test
    # unittest.main()
