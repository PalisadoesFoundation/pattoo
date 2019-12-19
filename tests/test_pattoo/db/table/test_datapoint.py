#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
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
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import datapoint, agent


class TestBasicFunctioins(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_idx_datapoint(self):
        """Testing method / function idx_datapoint."""
        # Initialize key variables
        checksum = data.hashstring(str(random()))
        pattoo_db_record = PattooDBrecord(
            pattoo_checksum=checksum,
            pattoo_metadata=[('key', 'value')],
            pattoo_data_type=32,
            pattoo_key='polar_bear',
            pattoo_value=0.0,
            pattoo_timestamp=1575789070108,
            pattoo_agent_polled_target='panda_bear',
            pattoo_agent_program='koala_bear',
            pattoo_agent_hostname='grizzly_bear',
            pattoo_agent_id='red_stripe_beer',
            pattoo_agent_polling_interval=10000)

        # Checksum should not exist
        self.assertFalse(datapoint.checksum_exists(checksum))

        # Test creation
        result = datapoint.idx_datapoint(pattoo_db_record)
        expected = datapoint.checksum_exists(checksum)
        self.assertEqual(result, expected)

        # Test after creation
        result = datapoint.idx_datapoint(pattoo_db_record)
        expected = datapoint.checksum_exists(checksum)
        self.assertEqual(result, expected)

    def test_checksum_exists(self):
        """Testing method / function checksum_exists."""
        # Initialize key variables
        result = datapoint.checksum_exists(-1)
        polling_interval = 1
        self.assertFalse(result)

        # Create a new Agent entry
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Create entry and check
        _checksum = data.hashstring(str(random()))
        result = datapoint.checksum_exists(_checksum)
        self.assertFalse(result)
        datapoint.insert_row(
            _checksum, DATA_FLOAT, polling_interval, idx_agent)
        result = datapoint.checksum_exists(_checksum)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Initialize key variables
        result = datapoint.checksum_exists(-1)
        polling_interval = 1
        self.assertFalse(result)

        # Create a new Agent entry
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Create entry and check
        checksum = data.hashstring(str(random()))
        result = datapoint.checksum_exists(checksum)
        self.assertFalse(result)
        datapoint.insert_row(checksum, DATA_FLOAT, polling_interval, idx_agent)
        result = datapoint.checksum_exists(checksum)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
