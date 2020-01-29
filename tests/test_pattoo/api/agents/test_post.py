#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
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
        '/pattoo/tests/test_pattoo/api/agents') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/api/agents" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data, converter, files
from pattoo_shared.constants import DATA_INT
from pattoo_shared.phttp import PostAgent
from pattoo_shared.configuration import Config, ServerConfig
from pattoo_shared.variables import (
    DataPoint, TargetDataPoints, AgentPolledData)
from pattoo.api.agents import PATTOO_API_AGENT as APP
from pattoo.constants import PATTOO_API_AGENT_NAME
from tests.libraries.configuration import UnittestConfig


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
        app.config['LIVESERVER_PORT'] = config.agent_api_ip_bind_port()
        os.environ['FLASK_ENV'] = 'development'

        # Clear the flask cache
        cache = Cache(config={'CACHE_TYPE': 'null'})
        cache.init_app(app)

        # Return
        return app

    def test_receive(self):
        """Testing method / function receive."""
        # Initialize key variables
        config = ServerConfig()
        apd = _create_apd()
        expected = converter.posting_data_points(
            converter.agentdata_to_post(apd))

        # Post data
        post = PostAgent(apd)
        post.post()

        # Read data from directory
        cache_directory = config.agent_cache_directory(PATTOO_API_AGENT_NAME)
        cache_data = files.read_json_files(cache_directory)

        # Test
        self.assertEqual(len(cache_data), 1)
        self.assertEqual(len(cache_data[0]), 2)
        result = cache_data[0][1]

        # Result and expected are not quite the same. 'expected' will have
        # lists of tuples where 'result' will have lists of lists
        for key, value in result.items():
            if key != 'pattoo_datapoints':
                self.assertEqual(value, expected[key])
        self.assertEqual(
            result['pattoo_datapoints']['datapoint_pairs'],
            expected['pattoo_datapoints']['datapoint_pairs'])

        # Test list of tuples
        for key, value in result[
                'pattoo_datapoints']['key_value_pairs'].items():
            self.assertEqual(
                tuple(value),
                expected['pattoo_datapoints']['key_value_pairs'][int(key)])

        # Revert cache_directory
        for filename in os.listdir(cache_directory):
            # Examine all the '.json' files in directory
            if filename.endswith('.json'):
                # Read file and add to string
                filepath = '{}{}{}'.format(cache_directory, os.sep, filename)
                os.remove(filepath)


def _create_apd():
    """Testing method / function records."""
    # Initialize key variables
    config = Config()
    polling_interval = 20
    pattoo_agent_program = 1
    pattoo_agent_polled_target = 2
    pattoo_key = '3'
    pattoo_value = 4
    pattoo_agent_hostname = 5

    # We want to make sure we get a different AgentID each time
    filename = files.agent_id_file(
        pattoo_agent_program, pattoo_agent_hostname, config)
    if os.path.isfile(filename) is True:
        os.remove(filename)

    # Setup AgentPolledData
    apd = AgentPolledData(pattoo_agent_program, polling_interval)

    # Initialize TargetDataPoints
    ddv = TargetDataPoints(pattoo_agent_polled_target)

    # Setup DataPoint
    data_type = DATA_INT
    variable = DataPoint(pattoo_key, pattoo_value, data_type=data_type)

    # Add data to TargetDataPoints
    ddv.add(variable)

    # Create a result
    apd.add(ddv)
    return apd


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
