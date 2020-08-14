#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys
import time
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from tests.libraries.configuration import UnittestConfig

from pattoo_shared.times import normalized_timestamp
from pattoo_shared.constants import DATA_FLOAT
from pattoo_shared import data
from pattoo import uri
from pattoo.configuration import ConfigIngester
from pattoo.db.table import agent, datapoint


class TestBasicFunctiions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_chart_timestamp_args(self):
        """Testing function chart_timestamp_args."""
        # Create a new Agent entry
        _pi = 1000
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Create entry and check
        checksum = data.hashstring(str(random()))
        result = datapoint.checksum_exists(checksum)
        self.assertFalse(result)
        datapoint.insert_row(checksum, DATA_FLOAT, _pi, idx_agent)
        idx_datapoint = datapoint.checksum_exists(checksum)

        # Test
        values = [False, None]
        for value in values:
            now = normalized_timestamp(_pi, int(time.time() * 1000))
            result = uri.chart_timestamp_args(idx_datapoint, value)
            self.assertEqual(result + 604800000, now)

        values = [-1, -6011, 1, 6011]
        for value in values:
            now = normalized_timestamp(_pi, int(time.time() * 1000))
            result = uri.chart_timestamp_args(idx_datapoint, value)
            self.assertEqual(result + (abs(value) * 1000), now)

        values = ['foo', [None]]
        for value in values:
            now = normalized_timestamp(_pi, int(time.time() * 1000))
            result = uri.chart_timestamp_args(idx_datapoint, value)
            self.assertEqual(result + 604800000, now)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
