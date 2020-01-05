#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import json
import socket
from random import random, uniform

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR, os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/ingest') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/ingest" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import converter, files, data, times
from pattoo_shared.variables import (
    DataPoint, TargetDataPoints, AgentPolledData)
from pattoo_shared.constants import DATA_INT
from pattoo.configuration import ConfigIngester as Config
from pattoo.constants import PATTOO_API_AGENT_NAME, PATTOO_INGESTER_NAME
from pattoo.db.table import datapoint
from pattoo.ingest.files import Cache
from pattoo.ingest import files as files_test

from tests.libraries.configuration import UnittestConfig


class TestCache(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_records(self):
        """Testing method / function records."""
        # Initialize key variables
        pattoo_values = create_cache()

        # Read data from directory
        cache = Cache()
        all_records = cache.records()

        # Test
        self.assertEqual(len(all_records), 1)
        self.assertEqual(len(all_records[0]), 1)
        result = all_records[0][0]
        self.assertEqual(
            result.pattoo_key,
            pattoo_values['pattoo_key'])
        self.assertEqual(
            result.pattoo_data_type,
            99)
        self.assertEqual(
            result.pattoo_value,
            pattoo_values['pattoo_value'])
        self.assertEqual(
            result.pattoo_agent_polled_target,
            pattoo_values['pattoo_agent_polled_target'])
        self.assertEqual(
            result.pattoo_agent_program,
            pattoo_values['pattoo_agent_program'])
        self.assertEqual(
            result.pattoo_agent_hostname,
            pattoo_values['pattoo_agent_hostname'])
        self.assertEqual(
            result.pattoo_agent_polling_interval,
            '20000')
        self.assertEqual(
            result.pattoo_metadata,
            [])
        self.assertEqual(
            result.pattoo_agent_id,
            pattoo_values['pattoo_agent_id'])

        # Purge cache to make sure there are no extraneous files
        cache.purge()

    def test_purge(self):
        """Testing method / function purge."""
        # Initialize key variables
        config = Config()
        cache_directory = config.agent_cache_directory(PATTOO_API_AGENT_NAME)

        # Initialize key variables
        _ = create_cache()

        # Test
        result = files.read_json_files(cache_directory)
        self.assertTrue(bool(result))

        # Test - Purge
        cache = Cache()
        cache.purge()

        # Test
        result = files.read_json_files(cache_directory, die=False)
        self.assertFalse(bool(result))

    def test_ingest(self):
        """Testing method / function ingest."""
        # Initialize key variables
        polling_interval = 20
        _pi = polling_interval * 1000

        _ = create_cache()

        # Read data from directory
        cache = Cache()
        all_records = cache.records()

        # Test
        self.assertEqual(len(all_records), 1)
        self.assertEqual(len(all_records[0]), 1)
        pdbr = all_records[0][0]

        # Datapoint should not exist before ingest
        checksum = pdbr.pattoo_checksum
        timestamp = pdbr.pattoo_timestamp
        value = pdbr.pattoo_value
        self.assertFalse(datapoint.checksum_exists(checksum))

        # Ingest
        cache.ingest()

        # Test (checksum should exist)
        idx_datapoint = datapoint.checksum_exists(checksum)
        self.assertTrue(bool(idx_datapoint))

        # Test (Single data entry should exist)
        obj = datapoint.DataPoint(idx_datapoint)
        result = obj.data(timestamp, timestamp)
        self.assertEqual(len(result), 1)
        key_pair = result[0]
        self.assertEqual(
            key_pair['timestamp'], times.normalized_timestamp(_pi, timestamp))
        self.assertEqual(key_pair['value'], value)


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_process_cache(self):
        """Testing method / function process_cache."""
        # Initialize key variables
        polling_interval = 20
        _pi = polling_interval * 1000

        _ = create_cache()

        # Read data from directory
        cache = Cache()
        all_records = cache.records()

        # Test
        self.assertEqual(len(all_records), 1)
        self.assertEqual(len(all_records[0]), 1)
        pdbr = all_records[0][0]

        # Datapoint should not exist before ingest
        checksum = pdbr.pattoo_checksum
        timestamp = pdbr.pattoo_timestamp
        value = pdbr.pattoo_value
        self.assertFalse(datapoint.checksum_exists(checksum))

        # Ingest using process_cache
        result = files_test.process_cache(fileage=0)
        self.assertTrue(result)

        # Test (checksum should exist)
        idx_datapoint = datapoint.checksum_exists(checksum)
        self.assertTrue(bool(idx_datapoint))

        # Test (Single data entry should exist)
        obj = datapoint.DataPoint(idx_datapoint)
        result = obj.data(timestamp, timestamp)
        self.assertEqual(len(result), 1)
        key_pair = result[0]
        self.assertEqual(
            key_pair['timestamp'], times.normalized_timestamp(_pi, timestamp))
        self.assertEqual(key_pair['value'], value)

    def test__lock(self):
        """Testing method / function _lock."""
        # Initialize key variables
        config = Config()
        lockfile = files.lock_file(PATTOO_INGESTER_NAME, config)

        # Test
        self.assertFalse(os.path.isfile(lockfile))
        result = files_test._lock()
        self.assertTrue(os.path.isfile(lockfile))
        self.assertTrue(result)

        # Should fail
        result = files_test._lock()
        self.assertFalse(result)

        # Remove and test again
        result = files_test._lock(delete=True)
        self.assertTrue(result)
        self.assertFalse(os.path.isfile(lockfile))
        result = files_test._lock()
        self.assertTrue(result)
        self.assertTrue(os.path.isfile(lockfile))

        # Delete again to revert to known working state
        result = files_test._lock(delete=True)
        self.assertTrue(result)


def create_cache():
    """Testing method / function records."""
    # Initialize key variables
    config = Config()
    polling_interval = 20
    cache_directory = config.agent_cache_directory(PATTOO_API_AGENT_NAME)
    result = {
        'pattoo_agent_program': data.hashstring(str(random())),
        'pattoo_agent_polled_target': socket.getfqdn(),
        'pattoo_key': data.hashstring(str(random())),
        'pattoo_value': round(uniform(1, 100), 5),
        'pattoo_agent_hostname': socket.getfqdn()
    }

    # We want to make sure we get a different AgentID each time
    filename = files.agent_id_file(
        result['pattoo_agent_program'],
        result['pattoo_agent_hostname'],
        config)
    if os.path.isfile(filename) is True:
        os.remove(filename)
    result['pattoo_agent_id'] = files.get_agent_id(
        result['pattoo_agent_program'],
        result['pattoo_agent_hostname'],
        config)

    # Setup AgentPolledData
    apd = AgentPolledData(result['pattoo_agent_program'], polling_interval)

    # Initialize TargetDataPoints
    ddv = TargetDataPoints(result['pattoo_agent_hostname'])

    # Setup DataPoint
    data_type = DATA_INT
    variable = DataPoint(
        result['pattoo_key'], result['pattoo_value'], data_type=data_type)

    # Add data to TargetDataPoints
    ddv.add(variable)

    # Write data to cache
    apd.add(ddv)
    cache_dict = converter.posting_data_points(
        converter.agentdata_to_post(apd))
    cache_file = '{}{}cache_test.json'.format(cache_directory, os.sep)
    with open(cache_file, 'w') as _fp:
        json.dump(cache_dict, _fp)

    return result


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
