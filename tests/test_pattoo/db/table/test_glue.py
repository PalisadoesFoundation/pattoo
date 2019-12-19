#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/db/table') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/db/table" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from pattoo_shared.constants import DATA_FLOAT
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import glue, pair, datapoint, agent


class TestBasicFunctioins(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_glue_exists(self):
        """Testing method / function glue_exists."""
        # Initialize key variables
        polling_interval = 1
        checksum = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        value = data.hashstring(str(random()))

        # Create a new Agent entry
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Insert values in tables
        pair.insert_rows((key, value))
        idx_pair = pair.pair_exists(key, value)
        datapoint.insert_row(checksum, DATA_FLOAT, polling_interval, idx_agent)
        idx_datapoint = datapoint.checksum_exists(checksum)

        # Create entry and check
        result = glue.glue_exists(idx_datapoint, idx_pair)
        self.assertFalse(result)
        glue.insert_rows(idx_datapoint, idx_pair)
        result = glue.glue_exists(idx_datapoint, idx_pair)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_insert_rows(self):
        """Testing method / function insert_rows."""
        # Initialize key variables
        polling_interval = 1
        checksum = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        value = data.hashstring(str(random()))

        # Create a new Agent entry
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Insert values in tables
        pair.insert_rows((key, value))
        idx_pair = pair.pair_exists(key, value)
        datapoint.insert_row(checksum, DATA_FLOAT, polling_interval, idx_agent)
        idx_datapoint = datapoint.checksum_exists(checksum)

        # Create entry and check
        result = glue.glue_exists(idx_datapoint, idx_pair)
        self.assertFalse(result)
        glue.insert_rows(idx_datapoint, idx_pair)
        result = glue.glue_exists(idx_datapoint, idx_pair)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_idx_pairs(self):
        """Testing method / function idx_pairs."""
        # Initialize key variables
        checksum = data.hashstring(str(random()))
        polling_interval = 1
        keypairs = []
        idx_pairs = []
        for _ in range(0, 10):
            time.sleep(0.05)
            key = data.hashstring(str(random()))
            value = data.hashstring(str(random()))
            keypairs.append((key, value))

        # Create a new Agent entry
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Insert values in tables
        pair.insert_rows(keypairs)
        datapoint.insert_row(checksum, DATA_FLOAT, polling_interval, idx_agent)
        idx_datapoint = datapoint.checksum_exists(checksum)

        # Test
        for key, value in keypairs:
            idx_pairs.append(pair.pair_exists(key, value))
        glue.insert_rows(idx_datapoint, idx_pairs)

        result = glue.idx_pairs(idx_datapoint)
        self.assertEqual(len(result), len(idx_pairs))
        for idx_pair in idx_pairs:
            self.assertTrue(idx_pair in result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
