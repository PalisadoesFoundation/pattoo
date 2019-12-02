#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random
import time

# PIP imports
from sqlalchemy import and_

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                os.path.abspath(os.path.join(
                        EXEC_DIR,
                        os.pardir)), os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/ingest/db') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/ingest/db" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from pattoo_shared.constants import DATA_FLOAT

from tests.libraries.configuration import UnittestConfig
from pattoo.constants import IDXTimestampValue
from pattoo.ingest.db import insert, exists
from pattoo.ingest import get
from pattoo.db.tables import Data
from pattoo.db import db


class TestBasicFunctioins(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_timeseries(self):
        """Testing method / function timeseries."""
        # Initialize key variables
        checksum = data.hashstring(str(random()))
        data_type = DATA_FLOAT
        polling_interval = 10
        value = 27
        timestamp = int(time.time() * 1000)

        # Create checksum entry in the DB, then update the data table
        idx_datapoint = get.idx_datapoint(
            checksum, data_type, polling_interval)
        _data = [IDXTimestampValue(
            idx_datapoint=idx_datapoint,
            polling_interval=polling_interval,
            timestamp=timestamp,
            value=value)]
        insert.timeseries(_data)

        # Verify that the data is there
        with db.db_query(20015) as session:
            rows = session.query(
                Data.value).filter(and_(
                    Data.idx_datapoint == idx_datapoint,
                    Data.timestamp == timestamp))
        for row in rows:
            self.assertEqual(row.value, value)

    def test_checksum(self):
        """Testing method / function checksum."""
        # Initialize key variables
        result = exists.checksum(-1)
        polling_interval = 1
        self.assertFalse(result)

        # Create entry and check
        checksum = data.hashstring(str(random()))
        result = exists.checksum(checksum)
        self.assertFalse(result)
        insert.checksum(checksum, DATA_FLOAT, polling_interval)
        result = exists.checksum(checksum)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_pairs(self):
        """Testing method / function pairs."""
        # Initialize key variables
        key = data.hashstring(str(random()))
        value = data.hashstring(str(random()))
        result = exists.pair(key, value)
        self.assertFalse(result)

        # Create entry and check
        insert.pairs((key, value))
        result = exists.pair(key, value)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))

    def test_glue(self):
        """Testing method / function glue."""
        # Initialize key variables
        polling_interval = 1
        checksum = data.hashstring(str(random()))
        key = data.hashstring(str(random()))
        value = data.hashstring(str(random()))

        # Insert values in tables
        insert.pairs((key, value))
        idx_pair = exists.pair(key, value)
        insert.checksum(checksum, DATA_FLOAT, polling_interval)
        idx_datapoint = exists.checksum(checksum)

        # Create entry and check
        result = exists.glue(idx_datapoint, idx_pair)
        self.assertFalse(result)
        insert.glue(idx_datapoint, idx_pair)
        result = exists.glue(idx_datapoint, idx_pair)
        self.assertTrue(bool(result))
        self.assertTrue(isinstance(result, int))


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
