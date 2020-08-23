#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random, uniform

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
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}api{0}web'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo_shared import data, log, converter
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig, WebConfig
from pattoo.api.web import PATTOO_API_WEB as APP
from pattoo.constants import IDXTimestampValue
from pattoo.db.table import datapoint
from pattoo.db.table import data as lib_data
from pattoo.db.table import user
from pattoo.constants import DbRowUser


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
        config = WebConfig()

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

        # Creating required test admin
        test_admin = {
            "username" : "pattoo_test",
            "first_name" : "Pattoo Test",
            "last_name": "Pattoo Test",
            "password": "pattoo_test_password",
            "role": 0,
            "password_expired": 0,
            "enabled": 1
        }
        user.insert_row(DbRowUser(**test_admin))

        # Get accesss token to make test queries
        acesss_query = ('''\
mutations{
    authenticate(Input: {
        username: {},
        password: {}
    }) {
        accessToken
        refreshToken
  }
}

''').format(test_admin['username'], test_admin['password'])

        access_request = _get(acesss_query)
        acesss_token = access_request['data']['authenticate']['accessToken']

        # Test
        query = ('''\
{
 allDatapoints(idxDatapoint: {}, token: {}) {
    edges {
      node {
        checksum
      }
    }
  }
}
'''.format(idx_datapoint, acesss_token))

        # Test
        graphql_result = _get(query)
        result = graphql_result['data']['allDatapoints']['edges'][0]['node']
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
    config = WebConfig()
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
