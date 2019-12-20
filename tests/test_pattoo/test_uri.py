#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys
import time

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
if EXEC_DIR.endswith('/pattoo/tests/test_pattoo') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from tests.libraries.configuration import UnittestConfig

from pattoo import uri


class TestBasicFunctiions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_chart_timestamp_args(self):
        """Testing function chart_timestamp_args."""
        # Test nuisance cases
        (ts_start, ts_stop) = uri.chart_timestamp_args('foo')
        self.assertEqual(ts_start + 604800000, ts_stop)

        # Other cases
        values = [None, -1, -6011, 1, 6011]
        for value in values:
            (ts_start, ts_stop) = uri.chart_timestamp_args(value)
            self.assertEqual(ts_stop > ts_start, True)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
