#!/usr/bin/env python3
"""CLI create testing"""

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
from pattoo.cli.cli import _Parser

class Test__Parser(unittest.TestCase):
    """Checks that the overridden error function from
    argparse.ArgumentParser() works properly
    """

    def test_error(self):
        """Testing _Parser error function"""
        help_message = 'test_help_messsage'
        additional_message = 'another_test_help_message'
        test_parser = _Parser(description=help_message,
                              formatter_class=argparse.RawDescriptionHelpFormatter)

        # Getting expected help message
        help_output = ''
        with patch('sys.stdout', new = StringIO()) as print_help_output:
            test_parser.print_help()
            help_output = print_help_output.getvalue()
        expected = ('\nERROR: {}\n\n' + help_output).format(additional_message)

        with patch('sys.stderr', new = StringIO()) as test_output:
            with self.assertRaises(SystemExit):
                test_parser.error(additional_message)
            self.assertEqual(test_output.getvalue(), expected)

if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()

