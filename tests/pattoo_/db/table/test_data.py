#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random

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
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}db{0}table'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo_shared import data as lib_data
from pattoo_shared.constants import PattooDBrecord
from pattoo.constants import IDXTimestampValue
from pattoo_shared.constants import DATA_FLOAT
from tests.libraries.configuration import UnittestConfig
from pattoo.db.models import Data
from pattoo.db.table import data, datapoint
from pattoo.db import db


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_insert_rows(self):
        """Testing method / function insert_rows."""
        # Initialize key variables
        checksum = lib_data.hashstring(str(random()))
        agent_id = lib_data.hashstring(str(random()))
        data_type = DATA_FLOAT
        polling_interval = 10
        pattoo_value = 27
        pattoo_key = lib_data.hashstring(str(random()))
        timestamp = int(time.time() * 1000)

        insert = PattooDBrecord(
            pattoo_checksum=checksum,
            pattoo_key=pattoo_key,
            pattoo_agent_id=agent_id,
            pattoo_agent_polling_interval=polling_interval,
            pattoo_timestamp=timestamp,
            pattoo_data_type=data_type,
            pattoo_value=pattoo_value,
            pattoo_agent_polled_target='pattoo_agent_polled_target',
            pattoo_agent_program='pattoo_agent_program',
            pattoo_agent_hostname='pattoo_agent_hostname',
            pattoo_metadata=[]
        )

        # Create checksum entry in the DB, then update the data table
        idx_datapoint = datapoint.idx_datapoint(insert)
        _data = [IDXTimestampValue(
            idx_datapoint=idx_datapoint,
            polling_interval=polling_interval,
            timestamp=timestamp,
            value=pattoo_value)]
        data.insert_rows(_data)

        # Verify that the data is there
        with db.db_query(20015) as session:
            rows = session.query(
                Data.value).filter(and_(
                    Data.idx_datapoint == idx_datapoint,
                    Data.timestamp == timestamp))
        for row in rows:
            self.assertEqual(row.value, pattoo_value)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
