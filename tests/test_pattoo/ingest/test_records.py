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
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}test_pattoo{0}ingest'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo_shared import data as lib_data
from pattoo_shared import times
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import pair, datapoint
from pattoo.ingest import get
from pattoo.ingest import records as ingest_data


class TestExceptionWrapper(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_re_raise(self):
        """Testing method / function re_raise."""
        pass


class TestRecords(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_multiprocess_pairs(self):
        """Testing method / function multiprocess_pairs."""
        # Initialize key variables
        items = make_records()
        records = items['records']

        # Key-value pair should not exist
        for record in records:
            key = record.pattoo_key
            value = record.pattoo_value
            result = pair.pair_exists(key, value)
            self.assertFalse(result)

        # Insert pairs as necessary
        process = ingest_data.Records([records])
        process.multiprocess_pairs()

        # Key-value pair should exist
        for record in records:
            key = record.pattoo_key
            value = record.pattoo_value
            result = pair.pair_exists(key, value)
            self.assertFalse(result)

    def test_multiprocess_data(self):
        """Testing method / function multiprocess_data."""
        # Initialize key variables
        items = make_records()
        timestamps = items['timestamps']
        records = items['records']
        expected = items['expected']
        checksum = items['checksum']

        # Entry should not exist
        result = datapoint.checksum_exists(checksum)
        self.assertFalse(result)

        # Test
        process = ingest_data.Records([records])
        process.multiprocess_pairs()
        process.multiprocess_data()

        # Get data from database
        idx_datapoint = datapoint.checksum_exists(checksum)
        _dp = datapoint.DataPoint(idx_datapoint)
        ts_start = min(timestamps)
        ts_stop = max(timestamps)
        results = _dp.data(ts_start, ts_stop)

        # Test
        for index, result in enumerate(results):
            self.assertEqual(result['value'], expected[index]['value'])
            self.assertEqual(result['timestamp'], expected[index]['timestamp'])

    def test_singleprocess_pairs(self):
        """Testing method / function singleprocess_pairs."""
        # Initialize key variables
        items = make_records()
        records = items['records']

        # Key-value pair should not exist
        for record in records:
            key = record.pattoo_key
            value = record.pattoo_value
            result = pair.pair_exists(key, value)
            self.assertFalse(result)

        # Insert pairs as necessary
        process = ingest_data.Records([records])
        process.singleprocess_pairs()

        # Key-value pair should exist
        for record in records:
            key = record.pattoo_key
            value = record.pattoo_value
            result = pair.pair_exists(key, value)
            self.assertFalse(result)

    def test_singleprocess_data(self):
        """Testing method / function singleprocess_data."""
        # Initialize key variables
        items = make_records()
        timestamps = items['timestamps']
        records = items['records']
        expected = items['expected']
        checksum = items['checksum']

        # Entry should not exist
        result = datapoint.checksum_exists(checksum)
        self.assertFalse(result)

        # Test
        process = ingest_data.Records([records])
        process.singleprocess_pairs()
        process.singleprocess_data()

        # Get data from database
        idx_datapoint = datapoint.checksum_exists(checksum)
        _dp = datapoint.DataPoint(idx_datapoint)
        ts_start = min(timestamps)
        ts_stop = max(timestamps)
        results = _dp.data(ts_start, ts_stop)

        # Test
        for index, result in enumerate(results):
            self.assertEqual(result['value'], expected[index]['value'])
            self.assertEqual(result['timestamp'], expected[index]['timestamp'])

    def test_ingest(self):
        """Testing method / function ingest."""
        # Initialize key variables
        items = make_records()
        timestamps = items['timestamps']
        records = items['records']
        expected = items['expected']
        checksum = items['checksum']

        # Entry should not exist
        result = datapoint.checksum_exists(checksum)
        self.assertFalse(result)

        # Test
        process = ingest_data.Records([records])
        process.ingest()

        # Get data from database
        idx_datapoint = datapoint.checksum_exists(checksum)
        _dp = datapoint.DataPoint(idx_datapoint)
        ts_start = min(timestamps)
        ts_stop = max(timestamps)
        results = _dp.data(ts_start, ts_stop)

        # Test
        for index, result in enumerate(results):
            self.assertEqual(result['value'], expected[index]['value'])
            self.assertEqual(result['timestamp'], expected[index]['timestamp'])


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test__process_kvps_exception(self):
        """Testing method / function _process_kvps_exception."""
        # Tested by TestProcess class unittests in this file
        pass

    def test__process_data_exception(self):
        """Testing method / function _process_data_exception."""
        # Tested by TestProcess class unittests in this file
        pass

    def test__multiprocess_pairs(self):
        """Testing method / function _multiprocess_pairs."""
        # Tested by TestProcess class unittests in this file
        pass

    def test__multiprocess_data(self):
        """Testing method / function _multiprocess_data."""
        # Tested by TestProcess class unittests in this file
        pass

    def test_process_db_records(self):
        """Testing method / function process_db_records."""
        # Initialize key variables
        items = make_records()
        timestamps = items['timestamps']
        records = items['records']
        expected = items['expected']
        checksum = items['checksum']

        # Entry should not exist
        result = datapoint.checksum_exists(checksum)
        self.assertFalse(result)

        # Create key-pair values in the database
        kvps = get.key_value_pairs(records)
        pair.insert_rows(kvps)

        # Insert
        ingest_data.process_db_records(records)

        # Get data from database
        idx_datapoint = datapoint.checksum_exists(checksum)
        _dp = datapoint.DataPoint(idx_datapoint)
        ts_start = min(timestamps)
        ts_stop = max(timestamps)
        results = _dp.data(ts_start, ts_stop)

        # Test
        for index, result in enumerate(results):
            self.assertEqual(result['value'], expected[index]['value'])
            self.assertEqual(result['timestamp'], expected[index]['timestamp'])


def make_records():
    """Testing method / function process_db_records."""
    # Initialize key variables
    checksum = lib_data.hashstring(str(random()))
    agent_id = lib_data.hashstring(str(random()))
    data_type = DATA_FLOAT
    _pi = 10 * 1000
    pattoo_key = lib_data.hashstring(str(random()))
    _timestamp = times.normalized_timestamp(
        _pi, int(time.time() * 1000))
    expected = []
    timestamps = []
    records = []
    result = {}

    # Create a list of PattooDBrecord objects
    for pattoo_value in range(0, 5):
        timestamp = _timestamp + (pattoo_value * _pi)
        expected.append({'timestamp': timestamp, 'value': pattoo_value})
        timestamps.append(timestamp)
        record = PattooDBrecord(
            pattoo_checksum=checksum,
            pattoo_key=pattoo_key,
            pattoo_agent_id=agent_id,
            pattoo_agent_polling_interval=_pi,
            pattoo_timestamp=timestamp,
            pattoo_data_type=data_type,
            pattoo_value=pattoo_value,
            pattoo_agent_polled_target='pattoo_agent_polled_target',
            pattoo_agent_program='pattoo_agent_program',
            pattoo_agent_hostname='pattoo_agent_hostname',
            pattoo_metadata=[]
        )
        records.append(record)

    result['records'] = records
    result['expected'] = expected
    result['timestamps'] = timestamps
    result['checksum'] = checksum
    return result


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
