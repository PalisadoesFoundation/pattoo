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

from pattoo_shared.times import normalized_timestamp
from pattoo import uri
from pattoo.configuration import ConfigIngester


class TestBasicFunctiions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_chart_timestamp_args(self):
        """Testing function chart_timestamp_args."""
        # Test nuisance cases
        config = ConfigIngester()
        _pi = config.polling_interval()

        # Other cases
        values = ['foo', None]
        for value in values:
            now = normalized_timestamp(_pi, int(time.time() * 1000))
            result = uri.chart_timestamp_args(value)
            self.assertEqual(result + 604800000, now)

        values = [-1, -6011, 1, 6011]
        for value in values:
            now = normalized_timestamp(_pi, int(time.time() * 1000))
            result = uri.chart_timestamp_args(value)
            self.assertEqual(result + (abs(value) * 1000), now)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
