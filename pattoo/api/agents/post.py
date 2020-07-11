"""Pattoo. Posting Routes."""

# Standard imports
import os
import json
import sys
from random import randrange
import hashlib
import uuid

# Flask imports
from flask import Blueprint, request, abort, session, jsonify

# pattoo imports
from pattoo_shared import log
from pattoo_shared.constants import CACHE_KEYS
from pattoo_shared.configuration import ServerConfig as Config
from pattoo.constants import PATTOO_API_AGENT_NAME
from pattoo_shared.files import get_gnupg


# Define the POST global variable
POST = Blueprint('POST', __name__)


@POST.route('/receive/<source>', methods=['POST'])
def receive(source):
    """Handle the agent posting route.

    Args:
        source: Unique Identifier of an pattoo agent

    Returns:
        Text response of Received

    """
    # Initialize key variables
    prefix = 'Invalid posted data.'

    # Read configuration
    config = Config()
    cache_dir = config.agent_cache_directory(PATTOO_API_AGENT_NAME)

    # Get JSON from incoming agent POST
    try:
        posted_data = request.json
    except:
        # Don't crash if we cannot convert JSON
        abort(404)

    # Abort if posted_data isn't a list
    if isinstance(posted_data, dict) is False:
        log_message = '{} Not a dictionary'.format(prefix)
        log.log2warning(20024, log_message)
        abort(404)
    if len(posted_data) != len(CACHE_KEYS):
        log_message = ('''\
{} Incorrect length. Expected length of {}'''.format(prefix, len(CACHE_KEYS)))
        log.log2warning(20019, log_message)
        abort(404)
    for key in posted_data.keys():
        if key not in CACHE_KEYS:
            log_message = '{} Invalid key'.format(prefix)
            log.log2warning(20018, log_message)
            abort(404)

    # Extract key values from posting
    try:
        timestamp = posted_data['pattoo_agent_timestamp']
    except:
        _exception = sys.exc_info()
        log_message = ('API Failure')
        log.log2exception(20025, _exception, message=log_message)
        abort(404)

    # Create filename. Add a suffix in the event the source is posting
    # frequently.
    suffix = str(randrange(100000)).zfill(6)
    json_path = (
        '{}{}{}_{}_{}.json'.format(
            cache_dir, os.sep, timestamp, source, suffix))

    # Create cache file
    try:
        with open(json_path, 'w+') as temp_file:
            json.dump(posted_data, temp_file)
    except Exception as err:
        log_message = '{}'.format(err)
        log.log2warning(20016, log_message)
        abort(404)
    except:
        _exception = sys.exc_info()
        log_message = ('API Failure')
        log.log2exception(20017, _exception, message=log_message)
        abort(404)

    # Return
    return 'OK'


@POST.route('/status')
def index():
    """Provide the status page.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    return 'The Pattoo Agent API is Operational.\n'


@POST.route('/key', methods=['POST', 'GET'])
def xch_key():
    """Handles public key exhange
    Args:
        None

    Returns:
        message (str): Key exchange response
        response (int): HTTP response code
    """
    # Read configuration
    config = Config()

    try:
        # Retrieves Pgpier class
        gpg = get_gnupg(PATTOO_API_AGENT_NAME, config)

        # Checks if a Pgpier object exists
        if gpg is None:
            raise Exception('Could not retrieve Pgpier for {}'
                            .format(PATTOO_API_AGENT_NAME))
    except Exception as e:
        response = 500
        message = 'Server error'
        
        log_msg = 'Could not retrieve Pgpier: >>>{}<<<'.format(e)
        log.log2warning(20500, log_msg)
        return message, response

    response = 400
    message = 'Error'

    if request.method == 'POST':

        # Get data from incoming agent POST
        try:
            data_byte = request.stream.read()

            # Decode UTF-8 bytes to Unicode, and convert single quotes
            # to double quotes to make it valid JSON
            data_str = data_byte.decode('utf8').replace("'", '"')

            # Load the JSON to a Python list
            data_dict = json.loads(data_str)

            # Save email and public key in session
            session['email'] = data_dict['pattoo_agent_email']

            # Save agent public key in keyring
            result = gpg.imp_pub_key(data_dict['pattoo_agent_key'])

            # Sent receive response
            response = 202
            message = 'Email and key received: {}, {}'\
                      .format(session['email'], result)

        except Exception as e:
            log_msg = 'Invalid email and key entry: >>>{}<<<'.format(e)
            log.log2warning(20501, log_msg)
            message = 'Key not received'

    if request.method == 'GET':
        # Predefined error if email and key was not sent first
        response = 403
        message = 'Send email and key first'
        if 'email' in session:
            # Generate server nonce
            session['nonce'] = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

            # Set email address in Pgpier object
            gpg.set_email()

            # Export public key
            api_key = gpg.exp_pub_key()
            api_email = gpg.email_addr
            api_nonce = session['nonce']

            # Retrieve information from session
            agent_email = session['email']
            agent_fingerprint = gpg.email_to_key(agent_email)

            # Trust agent key
            gpg.trust_key(agent_fingerprint)

            # Encrypt api nonce with agent public key
            encrypted_nonce = gpg.encrypt_data(api_nonce, agent_fingerprint)

            data = {'api_email': api_email, 'api_key': api_key,
                    'encrypted_nonce': encrypted_nonce}

            # Send api email, public key and encrypted nonce
            response = 200
            return jsonify(data=data), response

    return message, response

@POST.route('/validation', methods=['POST'])
def valid_key():
    """Handles validation by decrypting the received symmetric key from
    the agent and then symmetrically decrypting the nonce from
    agent and check if it's the same as the nonce sent

    The symmetric key is stored in session so that it can be attached
    to the cached data for future decryption

    The agent public key is then deleted
    """

    # Read configuration
    config = Config()

    try:
        # Retrieves Pgpier class
        gpg = get_gnupg(PATTOO_API_AGENT_NAME, config)

        # Checks if a Pgpier object exists
        if gpg is None:
            raise Exception('Could not retrieve Pgpier for {}'
                            .format(PATTOO_API_AGENT_NAME))
    except Exception as e:
        response = 500
        message = 'Server error'
        
        log_msg = 'Could not retrieve Pgpier: >>>{}<<<'.format(e)
        log.log2warning(20500, log_msg)
        return message, response

    # Predefined error message and response
    response = 403
    message = 'Proceed to key exchange first'

    # If no nonce is set, inform agent to exchange keys
    if 'nonce' not in session:
        return message, response

    if request.method == 'POST':
        # Get data from incoming agent POST
        try:
            data_byte = request.stream.read()

            # Decode UTF-8 bytes to Unicode, and convert single quotes
            # to double quotes to make it valid JSON
            data_str = data_byte.decode('utf8').replace("'", '"')

            # Load the JSON to a Python list
            data_dict = json.loads(data_str)

        except Exception as e:
            log_msg = 'Invalid email and key entry: >>>{}<<<'.format(e)
            log.log2warning(20501, log_msg)
            message = 'Key not received'
            response = 400

    return message, response
