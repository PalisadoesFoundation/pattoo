#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random

# PIP3 imports
import requests
from flask_testing import TestCase, LiveServerTestCase
from flask_caching import Cache


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}test_pattoo{0}api{0}web'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo_shared import data, times
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from pattoo_shared.configuration import Config

from tests.libraries.configuration import UnittestConfig
from pattoo.api.web import PATTOO_API_WEB as APP
from pattoo.constants import IDXTimestampValue
from pattoo.db.table import datapoint
from pattoo.db.table import data as lib_data
from pattoo.db.table.datapoint import DataPoint
from pattoo import uri


class TestBasicFunctions(LiveServerTestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def create_app(self):
        """Create the test APP for flask.

        Args:
            None

        Returns:
            app: Flask object

        """
        # Create APP and set configuration
        app = APP
        config = Config()

        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = config.web_api_ip_bind_port()
        os.environ['FLASK_ENV'] = 'development'

        # Clear the flask cache
        cache = Cache(config={'CACHE_TYPE': 'null'})
        cache.init_app(app)

        # Return
        return app

    def test_route_data(self):
        """Testing method / function route_data."""
        # Initialize key variables
        secondsago = 3600
        ts_start = uri.chart_timestamp_args(secondsago)

        # Initialize key variables
        _data = []
        checksum = data.hashstring(str(random()))
        pattoo_key = data.hashstring(str(random()))
        agent_id = data.hashstring(str(random()))
        _pi = 300 * 1000
        data_type = DATA_FLOAT
        now = int(time.time()) * 1000
        count = 0

        for timestamp in range(ts_start, now, _pi):
            insert = PattooDBrecord(
                pattoo_checksum=checksum,
                pattoo_key=pattoo_key,
                pattoo_agent_id=agent_id,
                pattoo_agent_polling_interval=_pi,
                pattoo_timestamp=timestamp,
                pattoo_data_type=data_type,
                pattoo_value=count,
                pattoo_agent_polled_target='pattoo_agent_polled_target',
                pattoo_agent_program='pattoo_agent_program',
                pattoo_agent_hostname='pattoo_agent_hostname',
                pattoo_metadata=[]
            )
            count += 1

            # Create checksum entry in the DB, then update the data table
            idx_datapoint = datapoint.idx_datapoint(insert)
            _data.append(IDXTimestampValue(
                idx_datapoint=idx_datapoint,
                polling_interval=_pi,
                timestamp=timestamp,
                value=count))

        # Insert rows of new data
        lib_data.insert_rows(_data)

        # Test
        obj = DataPoint(idx_datapoint)
        ts_stop = obj.last_timestamp()
        expected = obj.data(ts_start, ts_stop)

        # Create URL
        config = Config()
        url = ('{}/{}'.format(
            config.web_api_server_url(graphql=False),
            idx_datapoint))

        # Check response
        with requests.get(url) as response:
            result = response.json()

        count = 0
        for item in result:
            ts_norm = times.normalized_timestamp(_pi, ts_start)
            if item['timestamp'] < ts_norm:
                self.assertIsNone(item['value'])
            else:
                self.assertEqual(item, expected[count])
                count += 1


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
