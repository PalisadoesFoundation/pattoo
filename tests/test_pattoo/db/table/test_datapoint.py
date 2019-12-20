#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random
import time

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

from pattoo_shared import data, times
from pattoo_shared.constants import PattooDBrecord
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from pattoo.db.table import datapoint, agent
from pattoo.db.table import data as lib_data
from pattoo.db.table.datapoint import DataPoint
from pattoo.db.models import DataPoint as _DataPoint
from pattoo.db import db
from pattoo.constants import IDXTimestampValue

from tests.libraries.configuration import UnittestConfig


class TestBasicFunctions(unittest.TestCase):
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

    def test__counters(self):
        """Testing method / function _counters."""
        # Create a counter-like dict
        increment = 2
        inputs = {}
        for item in range(0, 20, increment):
            inputs[item] = item

        result = datapoint._counters(inputs, 1, 1)
        self.assertEqual(len(inputs) - 1, len(result))
        for item in result:
            self.assertTrue(item['timestamp'] in inputs)
            self.assertEqual(item['value'], increment * 1000)

    def test__response(self):
        """Testing method / function _response."""
        # Initialize variables
        inputs = {
            1: 1 * 3,
            2: 2 * 3,
            3: 3 * 3,
            4: 4 * 3
        }
        result = datapoint._response(inputs)
        self.assertEqual(len(inputs), len(result))
        for item in result:
            timestamp = item['timestamp']
            self.assertEqual(item['value'], inputs[timestamp])


class TestDataPoint(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing method / function __init__."""
        # Tested by other methods
        pass

    def test_enabled(self):
        """Testing method / function enabled."""
        # Create a new row in the database and test
        idx_datapoint = _idx_datapoint()
        obj = DataPoint(idx_datapoint)

        # Get the result
        with db.db_query(20105) as session:
            result = session.query(_DataPoint.enabled).filter(
                _DataPoint.idx_datapoint == idx_datapoint).one()
        self.assertEqual(result.enabled, obj.enabled())

    def test_idx_agent(self):
        """Testing method / function idx_agent."""
        # Create a new row in the database and test
        idx_datapoint = _idx_datapoint()
        obj = DataPoint(idx_datapoint)

        # Get the result
        with db.db_query(20104) as session:
            result = session.query(_DataPoint.idx_agent).filter(
                _DataPoint.idx_datapoint == idx_datapoint).one()
        self.assertEqual(result.idx_agent, obj.idx_agent())

    def test_checksum(self):
        """Testing method / function checksum."""
        # Create a new row in the database and test
        idx_datapoint = _idx_datapoint()
        obj = DataPoint(idx_datapoint)

        # Get the result
        with db.db_query(20103) as session:
            result = session.query(_DataPoint.checksum).filter(
                _DataPoint.idx_datapoint == idx_datapoint).one()
        self.assertEqual(result.checksum.decode(), obj.checksum())

    def test_data_type(self):
        """Testing method / function data_type."""
        # Create a new row in the database and test
        idx_datapoint = _idx_datapoint()
        obj = DataPoint(idx_datapoint)

        # Get the result
        with db.db_query(20102) as session:
            result = session.query(_DataPoint.data_type).filter(
                _DataPoint.idx_datapoint == idx_datapoint).one()
        self.assertEqual(result.data_type, obj.data_type())

    def test_exists(self):
        """Testing method / function exists."""
        # Create a new row in the database and test
        idx_datapoint = _idx_datapoint()
        obj = DataPoint(idx_datapoint)
        self.assertTrue(obj.exists())

    def test_last_timestamp(self):
        """Testing method / function last_timestamp."""
        # Create a new row in the database and test
        idx_datapoint = _idx_datapoint()
        obj = DataPoint(idx_datapoint)

        # Get the result
        with db.db_query(20101) as session:
            result = session.query(_DataPoint.last_timestamp).filter(
                _DataPoint.idx_datapoint == idx_datapoint).one()
        self.assertEqual(result.last_timestamp, obj.last_timestamp())

    def test_polling_interval(self):
        """Testing method / function polling_interval."""
        # Create a new row in the database and test
        idx_datapoint = _idx_datapoint()
        obj = DataPoint(idx_datapoint)

        # Get the result
        with db.db_query(20106) as session:
            result = session.query(_DataPoint.polling_interval).filter(
                _DataPoint.idx_datapoint == idx_datapoint).one()
        self.assertEqual(result.polling_interval, obj.polling_interval())

    def test_data(self):
        """Testing method / function data."""
        self.maxDiff = None

        # Initialize key variables
        _data = []
        expected = []
        checksum = data.hashstring(str(random()))
        pattoo_key = data.hashstring(str(random()))
        agent_id = data.hashstring(str(random()))
        polling_interval = 300 * 1000
        data_type = DATA_FLOAT
        _pattoo_value = 27
        _timestamp = int(time.time() * 1000)
        ts_start = _timestamp

        for count in range(0, 10):
            timestamp = _timestamp + (polling_interval * count)
            ts_stop = timestamp
            pattoo_value = _pattoo_value * count
            insert = PattooDBrecord(
                pattoo_checksum=checksum,
                pattoo_key=pattoo_key,
                pattoo_agent_id=agent_id,
                pattoo_agent_polling_interval=polling_interval,
                pattoo_timestamp=timestamp,
                pattoo_data_type=data_type,
                pattoo_value=pattoo_value * count,
                pattoo_agent_polled_target='pattoo_agent_polled_target',
                pattoo_agent_program='pattoo_agent_program',
                pattoo_agent_hostname='pattoo_agent_hostname',
                pattoo_metadata=[]
            )

            # Create checksum entry in the DB, then update the data table
            idx_datapoint = datapoint.idx_datapoint(insert)
            _data.append(IDXTimestampValue(
                idx_datapoint=idx_datapoint,
                polling_interval=polling_interval,
                timestamp=timestamp,
                value=pattoo_value))

            # Append to expected results
            expected.append(
                {'timestamp': times.normalized_timestamp(
                    polling_interval, timestamp), 'value': pattoo_value}
            )

        # Insert rows of new data
        lib_data.insert_rows(_data)

        # Test
        obj = DataPoint(idx_datapoint)
        result = obj.data(ts_start, ts_stop)
        self.assertEqual(result, expected)


def _idx_datapoint():
    """Create a new DataPoint db entry.

    Args:
        value: Value to convert

    Returns:
        result: idx_datapoint value for new DataPoint

    """
    # Initialize key variables
    polling_interval = 1

    # Create a new Agent entry
    agent_id = data.hashstring(str(random()))
    agent_target = data.hashstring(str(random()))
    agent_program = data.hashstring(str(random()))
    agent.insert_row(agent_id, agent_target, agent_program)
    idx_agent = agent.exists(agent_id, agent_target)

    # Create entry and check
    _checksum = data.hashstring(str(random()))
    result = datapoint.checksum_exists(_checksum)
    datapoint.insert_row(
        _checksum, DATA_FLOAT, polling_interval, idx_agent)
    result = datapoint.checksum_exists(_checksum)
    return result


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
