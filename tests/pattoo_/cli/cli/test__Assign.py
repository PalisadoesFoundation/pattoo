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
from pattoo.cli.cli import _Assign


class Test__Assign(unittest.TestCase):
    """Testing CLI _Assign argparse class"""

    # Creating instance of _Assign class
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='action')
    _assign = _Assign(subparser)

    def test__init__(self):
        """Testing _Assign __init__"""

        # Checking that _Assign contains agent in choices dictionary with a
        # value containing an ArgumentParser instance to indicate that the
        # _Assign agent method was ran
        choices = self._assign.__dict__['subparsers'].choices

        self.assertIn('agent', choices)
        self.assertIsInstance(choices['agent'], argparse.ArgumentParser)

    def test_agent(self):
        """Testing _Assign agent method"""

        # Checking that proper argparse.Namespace is made when passing cli
        # arguments to assign an agent
        args = self.parser.parse_args(['assign', 'agent', '--idx_agent', '1',
                                       '--idx_pair_xlate_group', '1'])
        expected = argparse.Namespace(action='assign', idx_agent=1,
                                      idx_pair_xlate_group=1, qualifier='agent')
        self.assertEqual(args, expected)

if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
