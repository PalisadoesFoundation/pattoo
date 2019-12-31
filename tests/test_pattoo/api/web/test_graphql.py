#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random, uniform
from pprint import pprint

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

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/api/web') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/api/web" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data, log, converter
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig
from pattoo.api.web import PATTOO_API_WEB as APP
from pattoo.configuration import ConfigPattoo as Config
from pattoo.constants import IDXTimestampValue
from pattoo.db.table import datapoint
from pattoo.db.table import data as lib_data


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

    def test_route_graphql(self):
        """Testing method / function add_url_rule (graphql)."""
        # Initialize key variables
        _data = []
        pattoo_checksum = data.hashstring(str(random()))
        pattoo_key = data.hashstring(str(random()))
        agent_id = data.hashstring(str(random()))
        pattoo_agent_polled_target = data.hashstring(str(random()))
        _pi = 300 * 1000
        data_type = DATA_FLOAT
        timestamp = int(time.time()) * 1000
        pattoo_value = round(uniform(1, 100), 5)

        insert = PattooDBrecord(
            pattoo_checksum=pattoo_checksum,
            pattoo_key=pattoo_key,
            pattoo_agent_id=agent_id,
            pattoo_agent_polling_interval=_pi,
            pattoo_timestamp=timestamp,
            pattoo_data_type=data_type,
            pattoo_value=pattoo_value,
            pattoo_agent_polled_target=pattoo_agent_polled_target,
            pattoo_agent_program='pattoo_agent_program',
            pattoo_agent_hostname='pattoo_agent_hostname',
            pattoo_metadata=[]
        )

        # Create checksum entry in the DB, then update the data table
        idx_datapoint = datapoint.idx_datapoint(insert)
        _data.append(IDXTimestampValue(
            idx_datapoint=idx_datapoint,
            polling_interval=_pi,
            timestamp=timestamp,
            value=pattoo_value))

        # Insert rows of new data
        lib_data.insert_rows(_data)

        # Test
        query = ('''\
{
  filterIdxDatapoint(idxDatapoint: "IDX") {
    checksum
  }
}
'''.replace('IDX', str(idx_datapoint)))

        # Test
        graphql_result = _get(query)
        result = graphql_result['data']['filterIdxDatapoint'][0]
        self.assertEqual(result['checksum'], pattoo_checksum)


def _get(query):
    """Get pattoo API server GraphQL query results.

    Args:
        query: GraphQL query string

    Returns:
        result: Dict of JSON response

    """
    # Initialize key variables
    success = False
    config = Config()
    result = None

    # Get the data from the GraphQL API
    url = config.web_api_server_url()
    try:
        response = requests.get(url, params={'query': query})

        # Trigger HTTP errors if present
        response.raise_for_status()
        success = True
    except requests.exceptions.Timeout as err:
        # Maybe set up for a retry, or continue in a retry loop
        log_message = ('''\
Timeout when attempting to access {}. Message: {}\
'''.format(url, err))
        log.log2die(20121, log_message)
    except requests.exceptions.TooManyRedirects as err:
        # Tell the user their URL was bad and try a different one
        log_message = ('''\
Too many redirects when attempting to access {}. Message: {}\
'''.format(url, err))
        log.log2die(20116, log_message)
    except requests.exceptions.HTTPError as err:
        log_message = ('''\
HTTP error when attempting to access {}. Message: {}\
'''.format(url, err))
        log.log2die(20118, log_message)
    except requests.exceptions.RequestException as err:
        # catastrophic error. bail.
        log_message = ('''\
Exception when attempting to access {}. Message: {}\
'''.format(url, err))
        log.log2die(20119, log_message)
    except:
        log_message = ('''API Failure: [{}, {}, {}]\
'''.format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
        log.log2die(20120, log_message)

    # Process the data
    if bool(success) is True:
        result = response.json()
    return result


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
