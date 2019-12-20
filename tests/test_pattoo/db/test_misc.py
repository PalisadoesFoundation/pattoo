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
            EXEC_DIR,
            os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/db') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/db" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import datapoint, glue, pair
from pattoo.db import misc
from pattoo.ingest import get
from pattoo.constants import ChecksumLookup
from pattoo.db.table import agent


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_checksums(self):
        """Testing method / function checksums."""
        # Initialize key variables
        expected = {}
        polling_interval = 1
        pattoo_agent_polled_target = 'panda_bear'
        pattoo_agent_program = 'koala_bear'
        pattoo_agent_hostname = 'grizzly_bear'

        # Insert an entry in the agent table
        agent_id = data.hashstring(str(random()))
        idx_agent = agent.idx_agent(
            agent_id, pattoo_agent_polled_target, pattoo_agent_program)

        # Populate database with key-value pairs
        for data_index in range(0, 10):
            time.sleep(0.1)

            # Add the checksum to the database
            checksum = data.hashstring(str(random()))
            datapoint.insert_row(
                checksum, DATA_FLOAT, polling_interval, idx_agent)
            idx_datapoint = datapoint.checksum_exists(checksum)

            # Define what we expect from the test function
            expected[checksum] = ChecksumLookup(
                idx_datapoint=idx_datapoint,
                polling_interval=polling_interval,
                last_timestamp=1)

            # Add key-pairs to the database
            record = PattooDBrecord(
                pattoo_checksum=checksum,
                pattoo_key='key',
                pattoo_agent_polling_interval=polling_interval,
                pattoo_agent_id=agent_id,
                pattoo_timestamp=int(time.time() * 1000),
                pattoo_data_type=DATA_FLOAT,
                pattoo_value=(data_index * 10),
                pattoo_agent_polled_target=pattoo_agent_polled_target,
                pattoo_agent_program=pattoo_agent_program,
                pattoo_agent_hostname=pattoo_agent_hostname,
                pattoo_metadata=[])
            pairs = get.key_value_pairs(record)
            pair.insert_rows(pairs)
            idx_pairs = pair.idx_pairs(pairs)

            # Create glue entry
            glue.insert_rows(idx_datapoint, idx_pairs)

        #######################################################################
        # This is added to verify that we only get a subset of results
        #######################################################################

        # Insert an entry in the agent table
        fake_agent_id = data.hashstring(str(random()))
        idx_agent = agent.idx_agent(
            fake_agent_id, pattoo_agent_polled_target, pattoo_agent_program)

        # Populate database with key-value pairs
        for data_index in range(0, 17):
            time.sleep(0.1)

            # Add the checksum to the database
            checksum = data.hashstring(str(random()))
            datapoint.insert_row(
                checksum, DATA_FLOAT, polling_interval, idx_agent)
            idx_datapoint = datapoint.checksum_exists(checksum)

            # Add key-pairs to the database
            record = PattooDBrecord(
                pattoo_checksum=checksum,
                pattoo_key='key',
                pattoo_agent_polling_interval=polling_interval,
                pattoo_agent_id=fake_agent_id,
                pattoo_timestamp=int(time.time() * 1000),
                pattoo_data_type=DATA_FLOAT,
                pattoo_value=(data_index * 10),
                pattoo_agent_polled_target=pattoo_agent_polled_target,
                pattoo_agent_program=pattoo_agent_program,
                pattoo_agent_hostname=pattoo_agent_hostname,
                pattoo_metadata=[])
            pairs = get.key_value_pairs(record)
            pair.insert_rows(pairs)
            idx_pairs = pair.idx_pairs(pairs)

            # Create glue entry
            glue.insert_rows(idx_datapoint, idx_pairs)

        # Test
        result = misc.agent_checksums(agent_id)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), len(expected))
        for key, value in result.items():
            self.assertEqual(
                value.idx_datapoint,
                expected[key].idx_datapoint)
            self.assertEqual(
                value.polling_interval,
                expected[key].polling_interval)
            self.assertEqual(
                value.last_timestamp,
                expected[key].last_timestamp)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
