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

# Pattoo imports
from pattoo_shared import log
from pattoo_shared import encrypt
from pattoo_shared.constants import CACHE_KEYS

from pattoo.constants import PATTOO_API_AGENT_NAME
from pattoo import configuration

encryption = encrypt.Encryption(
    PATTOO_API_AGENT_NAME,
    configuration.ConfigAgentAPId().api_email_address()
)

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
    # Get JSON from incoming agent POST
    try:
        data = request.json
    except:
        # Don't crash if we cannot convert JSON
        abort(500, description='Invalid data format received.')

    # Save data
    success = _save_data(data, source)
    if bool(success) is False:
        abort(500, description='Invalid JSON data received.')

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
def key_exchange():
    """Process public key exhange.

    Args:
        None

    Returns:
        result: Various responses

    """
    # Initialize key variables
    required_keys = ['pattoo_agent_email', 'pattoo_agent_key']

    # If a symmetric key has already been established, skip
    if 'symm_key' in session:
        log_message = 'Symmetric key already set.'
        log.log2info(20148, log_message)
        return (log_message, 208)
    #
    # # Start encryption process
    # try:
    #     encryption = encrypt.Encryption(
    #         PATTOO_API_AGENT_NAME,
    #         config.api_email_address()
    #     )
    #
    # except:
    #     _exception = sys.exc_info()
    #     log_message = ('Server error. Cannot Initialize encryption')
    #     log.log2exception(20167, _exception, message=log_message)
    #     return (log_message, 500)

    # Get data from incoming agent POST
    if request.method == 'POST':
        try:
            # Get data from agent
            data_dict = json.loads(request.get_json(silent=False))
        except:
            _exception = sys.exc_info()
            log_message = 'Client sent corrupted JSON data'
            log.log2exception(20167, _exception, message=log_message)
            return (log_message, 500)

        # Check for minimal keys
        for key in required_keys:
            if key not in data_dict.keys():
                log_message = '''\
Required JSON key "{}" missing in key exchange'''.format(key)
                log.log2warning(20018, log_message)
                abort(404)

        # Save email in session
        session['email'] = data_dict['pattoo_agent_email']

        # Save agent public key in keyring
        encryption.pimport(data_dict['pattoo_agent_key'])
        return('Key received', 202)

    # Get data from incoming agent POST
    if request.method == 'GET':
        if 'email' in session:
            # Generate server nonce
            session['nonce'] = hashlib.sha256(
                str(uuid.uuid4()).encode()).hexdigest()

            # Retrieve information from session. Set previously in POST
            agent_fingerprint = encryption.fingerprint(session['email'])

            # Trust agent key
            encryption.trust(agent_fingerprint)

            # Encrypt api nonce with agent public key
            encrypted_nonce = encryption.encrypt(
                session['nonce'], agent_fingerprint)

            data_dict = {
                'api_email': encryption.email,
                'api_key': encryption.pexport(),
                'encrypted_nonce': encrypted_nonce
            }

            # Send api email, public key and encrypted nonce
            log_message = 'API information sent'
            log.log2info(20170, log_message)
            return jsonify(data_dict)

        # Otherwise send error message
        return ('Send email and key first', 403)

    # Return aborted status
    abort(400)


@POST.route('/validation', methods=['POST'])
def valid_key():
    """Validate remote agent.

    Process:

    1) Decrypt the symmetric key received from the agent
    2) Decrypting the nonce from agent
    3) Verify that nonce is the same as originally sent.
    4) Store symmetric key in session to be used for future decryption.
    6) Delete the agent public key

    Args:
        None

    Returns:
        message (str): Validation response message
        response (int): HTTP response code

    """
    # If a symmetric key has already been established, skip
    if 'symm_key' in session:
        log_message = 'Symmetric key already set.'
        log.log2info(20171, log_message)
        return (log_message, 208)

    # If no nonce is set, inform agent to exchange keys
    if 'nonce' not in session:
        return ('Proceed to key exchange first', 403)

    # Start encryption process
    # try:
    #     encryption = encrypt.Encryption(
    #         PATTOO_API_AGENT_NAME,
    #         config.api_email_address()
    #     )
    #
    # except:
    #     _exception = sys.exc_info()
    #     log_message = ('Server error. Cannot Initialize encryption')
    #     log.log2exception(20167, _exception, message=log_message)
    #     return (log_message, 500)

    # Get data from incoming agent POST
    if request.method == 'POST':
        try:
            # Get data from agent
            data_dict = json.loads(request.get_json(silent=False))
        except:
            _exception = sys.exc_info()
            log_message = 'Client sent corrupted validation JSON data'
            log.log2exception(20174, _exception, message=log_message)
            return (log_message, 500)

        # Decrypt symmetric key
        symmetric_key = encryption.decrypt(data_dict['encrypted_sym_key'])

        # Symmetrically decrypt nonce
        nonce = encryption.sdecrypt(
            data_dict['encrypted_nonce'], symmetric_key)

        # Checks if the decrypted nonce matches one sent
        if nonce != session['nonce']:
            return ('Nonce does not match', 401)

        # Delete agent public key
        encryption.pdelete(encryption.fingerprint(session['email']))

        # Session parameter cleanup
        session['symm_key'] = symmetric_key
        session.pop('email', None)
        session.pop('nonce', None)

        # Return response
        log_message = 'Symmetric key saved'
        log.log2info(20173, log_message)
        return (log_message, 200)

    # Otherwise abort
    abort(404)


@POST.route('/encrypted', methods=['POST'])
def crypt_receive():
    """Receive encrypted data from agent

    Args:
        None

    Returns:
        message (str): Reception result
        response (int): HTTP response code
    """
    # If a symmetric key has already been established, skip
    if 'symm_key' not in session:
        log_message = 'No session symmetric key'
        log.log2info(20171, log_message)
        return (log_message, 208)

    # Start encryption process
    # try:
    #     encryption = encrypt.Encryption(
    #         PATTOO_API_AGENT_NAME,
    #         config.api_email_address()
    #     )
    #
    # except:
    #     _exception = sys.exc_info()
    #     log_message = ('Server error. Cannot Initialize encryption')
    #     log.log2exception(20175, _exception, message=log_message)
    #     return (log_message, 500)

    if request.method == 'POST':
        try:
            # Get data from agent
            data_dict = json.loads(request.get_json(silent=False))
        except:
            _exception = sys.exc_info()
            log_message = 'Client sent corrupted validation JSON data'
            log.log2exception(20174, _exception, message=log_message)
            return (log_message, 500)

        # Symmetrically decrypt data
        data = encryption.sdecrypt(
            data_dict['encrypted_data'], session['symm_key'])

        # Extract posted data and source
        try:
            final_data = json.loads(data)
        except:
            _exception = sys.exc_info()
            log_message = 'Decrypted data extraction failed'
            log.log2exception(20174, _exception, message=log_message)
            abort(500, description=log_message)

        # Save data
        success = _save_data(final_data['data'], final_data['source'])
        if bool(success) is False:
            abort(500, description='Invalid JSON data received.')

        # Return
        log_message = 'Decrypted and received'
        log.log2info(20184, log_message)
        return(log_message, 202)

    # Otherwise abort
    return ('Proceed to key exchange first', 400)


def _save_data(data, source):
    """Handle the agent posting route.

    Args:
        data: Data dict received from agents

    Returns:
        success: True if successful

    """
    # Initialize key variables
    success = False
    prefix = 'Invalid posted data.'

    # Read configuration
    config = configuration.ConfigAgentAPId()
    cache_dir = config.agent_cache_directory(PATTOO_API_AGENT_NAME)

    # Abort if data isn't a list
    if isinstance(data, dict) is False:
        log_message = '{} Not a dictionary'.format(prefix)
        log.log2warning(20024, log_message)
        abort(404)
    if len(data) != len(CACHE_KEYS):
        log_message = ('''\
{} Incorrect length. Expected length of {}'''.format(prefix, len(CACHE_KEYS)))
        log.log2warning(20019, log_message)
        return success

    # Basic integrity check of required JSON fields
    for key in data.keys():
        if key not in CACHE_KEYS:
            log_message = '{} Invalid key'.format(prefix)
            log.log2warning(20018, log_message)
            return success

    # Extract key values from posting
    try:
        timestamp = data['pattoo_agent_timestamp']
    except:
        _exception = sys.exc_info()
        log_message = ('API Failure')
        log.log2exception(20025, _exception, message=log_message)
        return success

    # Create filename. Add a suffix in the event the source is posting
    # frequently.
    suffix = str(randrange(100000)).zfill(6)
    json_path = (
        '{}{}{}_{}_{}.json'.format(
            cache_dir, os.sep, timestamp, source, suffix))

    # Create cache file
    try:
        with open(json_path, 'w+') as temp_file:
            json.dump(data, temp_file)
    except Exception as err:
        log_message = '{}'.format(err)
        log.log2warning(20016, log_message)
        return success
    except:
        _exception = sys.exc_info()
        log_message = ('API Failure')
        log.log2exception(20017, _exception, message=log_message)
        return success

    # Return
    success = True
    return success
