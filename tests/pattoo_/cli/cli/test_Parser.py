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
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}cli{0}cli'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo unittest imports
from tests.libraries.configuration import UnittestConfig
from pattoo.cli.cli import Parser
from pattoo.cli.cli import _Parser


class Test_Parser(unittest.TestCase):
    """Testing CLI Parser class"""

    # Standard help message
    additional_help = 'additional help test message'

    def compare_parser(self, parser):
        """Compares attributes of a parser to ensure of correct values

        Args:
            parser: _Parser instance

        Return:
            None

        """
        expected = {'prog': '', 'usage': None, 'description': self.additional_help,
                    'formatter_class': argparse.RawTextHelpFormatter,
                    'conflict_handler': 'error', 'add_help': True}

        for key, value in expected.items():
            self.assertEqual(parser.__dict__[key], value)

    def args_test_template(self, cmd_args, expected_namespace):
        """Executes unittest template for each CLI subparser that can be
        returned from running Parser args.

        Args:
            cmd_args: commandline arguments to be passed to parser
            expected_namespace: namespace that should be generated as return
            value from Parser.

        Return:
            None

        """

        # Test Parse Instance
        test_parse = Parser(self.additional_help)

        # Setting up commandline arguments for Parser
        sys.argv = [''] + cmd_args

        # Calling test_parse getting Namespace and Parser as results
        result_args, result_parser = test_parse.args()

        # Asserting equality for Namespace and Parser
        self.assertEqual(result_args, expected_namespace)
        self.compare_parser(result_parser)

    def test__init__(self):
        """Testing Parser __init__ method"""

        # Checking that the '_help' attribute is set properly on every new
        # Parser instance
        parser = Parser(self.additional_help)
        self.assertEqual(parser._help, self.additional_help)

        # Testing if no parameters passed to Parser '__init__' method
        no_args_parser = Parser()
        expected = ''
        self.assertEqual(no_args_parser._help, expected)

    def test_args(self):
        """Testing Parser __init__ method"""

        ####################################################################
        #
        # Testing Parser with _Show arguments
        #
        ####################################################################

        # _Show agent
        cmd_args = ['show', 'agent']
        namespace = argparse.Namespace(action='show', qualifier='agent')
        self.args_test_template(cmd_args, namespace)

        # _Show key_translation_group
        cmd_args = ['show', 'key_translation_group', '--idx_pair_xlate_group',
                    '1']
        namespace = argparse.Namespace(action='show', idx_pair_xlate_group=1,
                                       qualifier='key_translation_group')
        self.args_test_template(cmd_args, namespace)

        # _Show key_translation
        cmd_args = ['show', 'key_translation']
        namespace = argparse.Namespace(action='show', idx_pair_xlate_group=None,
                                       qualifier='key_translation')
        self.args_test_template(cmd_args, namespace)

        # _Show language
        cmd_args = ['show', 'language']
        namespace = argparse.Namespace(action='show', qualifier='language')
        self.args_test_template(cmd_args, namespace)

        # _Show agent_translation
        cmd_args = ['show', 'agent_translation']
        namespace = argparse.Namespace(action='show',
                                     qualifier='agent_translation')
        self.args_test_template(cmd_args, namespace)

        ####################################################################
        #
        # Testing Parser with _Create arguments
        #
        ####################################################################

        # _Create language
        cmd_args = ['create', 'language', '--code', 'code', '--name', 'name']
        namespace = argparse.Namespace(action='create', code='code',
                                       name='name', qualifier='language')
        self.args_test_template(cmd_args, namespace)

        # _Create key_translation_group
        cmd_args = ['create', 'key_translation_group', '--name', 'name']
        namespace = argparse.Namespace(action='create', name='name',
                                       qualifier='key_translation_group')
        self.args_test_template(cmd_args, namespace)

        ####################################################################
        #
        # Testing Parser with _Set arguments
        #
        ####################################################################

        # _Set language
        cmd_args = ['set', 'language', '--code', 'code', '--name', 'name']
        namespace = argparse.Namespace(action='set', code='code',
                                       name='name', qualifier='language')
        self.args_test_template(cmd_args, namespace)

        # _Set key_translation_group
        cmd_args = ['set', 'key_translation_group', '--idx_pair_xlate_group',
                    '1', '--name', 'name']
        namespace = argparse.Namespace(action='set', idx_pair_xlate_group=1,
                                       name='name',
                                       qualifier='key_translation_group')
        self.args_test_template(cmd_args, namespace)

        ####################################################################
        #
        # Testing Parser with _Import arguments
        #
        ####################################################################

        # _Import key_translation
        cmd_args = ['import', 'key_translation', '--filename', 'filename',
                    '--idx_pair_xlate_group', '1']
        namespace = argparse.Namespace(action='import', filename='filename',
                                       idx_pair_xlate_group=1,
                                       qualifier='key_translation')
        self.args_test_template(cmd_args, namespace)

        # _Import agent_translation
        cmd_args = ['import', 'agent_translation', '--filename', 'filename']
        namespace = argparse.Namespace(action='import', filename='filename',
                                       qualifier='agent_translation')
        self.args_test_template(cmd_args, namespace)

        ####################################################################
        #
        # Testing Parser with _Assign arguments
        #
        ####################################################################

        # _Assign agent
        cmd_args = ['assign', 'agent', '--idx_agent', '1',
                    '--idx_pair_xlate_group', '1']
        namespace = argparse.Namespace(action='assign', idx_agent=1,
                                       idx_pair_xlate_group=1,
                                       qualifier='agent')
        self.args_test_template(cmd_args, namespace)


if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
