#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys


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

from pattoo_shared import data
from pattoo_shared.configuration import Config

from tests.libraries.configuration import UnittestConfig
from pattoo.api.web import PATTOO_API_WEB as APP


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

    def test_index(self):
        """Testing method / function index."""
        # Initialize key variables
        expected = 'The Pattoo Web API is Operational.\n'

        # Create URL
        config = Config()
        agent_url = config.web_api_server_url(graphql=False)
        url = agent_url.replace('/rest/data', '/status')

        # Check response
        with requests.get(url) as response:
            result = response.text
        self.assertEqual(expected, result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
