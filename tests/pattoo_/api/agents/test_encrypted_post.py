#!/usr/bin/env python3
"""Unit test for encrypted post which includes
the suite of the key exchange (receive public key
and email address of agent via POST, send API
email address, public key and nonce encrypted
by agent public key via GET), the validation
(receive symmetrically encrypted nonce, and the
symmetric key encrypted by the public key of the
API; decrypt everything and check if the decrypted
nonce is the same as what was sent to the agent.
Add the new symmetric key to the session and remove
everything else from the session), and the receiving
of symmetrically encrypted data"""

# Import Python libraries
import os
import unittest
import sys

# Import Flask testing components
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
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}api{0}agents'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Import Pattoo dependencies
from pattoo_shared import data, converter, files
from pattoo_shared.constants import DATA_INT
from pattoo_shared.phttp import PostAgent, EncryptedPostAgent
from pattoo_shared.configuration import Config, ServerConfig
from pattoo_shared.variables import (
    DataPoint, TargetDataPoints, AgentPolledData)
from pattoo.api.agents import PATTOO_API_AGENT as APP
from pattoo.constants import PATTOO_API_AGENT_NAME
from tests.libraries.configuration import UnittestConfig


class TestEncryptedPost(LiveServerTestCase):
    """Unit testing for encrypted post suite"""

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

    def setUp(self):
        """This will run each time before a test is performed
        """
        print('setUp')
        gconfig = Config()  # Get config for Pgpier

        # Create Pgpier object for the API
        api_gpg = files.set_gnupg(PATTOO_API_AGENT_NAME, gconfig, "api_test@example.com")

    def test_encrypted_post(self):
        """Test that the API can receive and decrypt
        encrypted data from agent"""

        # Initialize key variables
        config = ServerConfig()

        # Get Pgpier object
        gconfig = Config()  # Get config for Pgpier

        # Create Pgpier object for the agent
        agent_gpg = files.set_gnupg("test_encrypted_agent", gconfig,
                        "agent_test@example.com")

        # Make agent data
        agent_data = _make_agent_data()

        # Turn agent data into a dict to be compared to
        # the data received by the API
        expected = converter.posting_data_points(
            converter.agentdata_to_post(agent_data)
            )

        # Make encrypted post
        post_encrypted = EncryptedPostAgent(agent_data, agent_gpg)
        post_encrypted.post()

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

def _make_agent_data():
    """Create generate data to post to API server"""
    # Initialize key variables
    config = Config()
    polling_interval = 60
    pattoo_agent_program = 1
    pattoo_agent_polled_target = 2
    pattoo_key = '3'
    pattoo_value = 4

    # We want to make sure we get a different AgentID each time
    filename = files.agent_id_file(pattoo_agent_program, config)
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

    # Return agent data
    return apd


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
