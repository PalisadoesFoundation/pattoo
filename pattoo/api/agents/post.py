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
    # If a symmetric key has already been established, skip
    if 'symm_key' in session:
        message = 'Symmetric key already set'
        response = 208
        log.log2info(77707, message)
        return message, response


    # Read configuration
    config = Config()

    try:
        # Retrieves Pgpier class
        gpg = get_gnupg(PATTOO_API_AGENT_NAME, config)

        #Sets key ID
        gpg.set_keyid()

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
    log_mem = None

    if request.method == 'POST':

        # Get data from incoming agent POST
        try:
            # Get data from agent
            data_json = request.get_json(silent=False)
            data_dict = json.loads(data_json)
            log_mem = data_dict

            # Save email in session
            session['email'] = data_dict['pattoo_agent_email']

            # Save agent public key in keyring
            result = gpg.imp_pub_key(data_dict['pattoo_agent_key'])

            # Sent receive response
            response = 202
            message = 'Email and key received: {}, {}'\
                      .format(session['email'], result)

            log.log2info(77701, message)

        except Exception as e:
            log_msg = 'Invalid email and key entry: >>>{}<<<'.format(e)
            log_msg+= '--->{}<---'.format(log_mem)
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
            message = 'API information sent'
            log.log2info(77701, message)
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

    Args:
        None

    Returns:
        message (str): Validation response message
        response (int): HTTP response code
    """

    # If a symmetric key has already been established, skip
    if 'symm_key' in session:
        message = 'Symmetric key already set'
        response = 208
        log.log2info(77707, message)
        return message, response

    # Predefined error message and response
    response = 403
    message = 'Proceed to key exchange first'

    # If no nonce is set, inform agent to exchange keys
    if 'nonce' not in session:
        return message, response

    # Read configuration
    config = Config()

    try:
        # Retrieves Pgpier class
        gpg = get_gnupg(PATTOO_API_AGENT_NAME, config)

        #Sets key ID
        gpg.set_keyid()

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

    if request.method == 'POST':
        # Get data from incoming agent POST
        try:
            # Get data from agent
            data_json = request.get_json(silent=False)
            data_dict = json.loads(data_json)

            # Retrieved symmetrically encrypted nonce
            encrypted_nonce = data_dict['encrypted_nonce']

            # Retrieved encrypted symmetric key
            encrypted_sym_key = data_dict['encrypted_sym_key']

            # Decrypt symmetric key
            passphrase = gpg.passphrase
            decrypted_symm_key = gpg.decrypt_data(encrypted_sym_key, passphrase)

            # Symmetrically decrypt nonce
            nonce = gpg.symmetric_decrypt(encrypted_nonce, decrypted_symm_key)

            # Checks if the decrypted nonce matches one sent
            if nonce != session['nonce']:
                response = 401
                message = 'Nonce does not match'

                return message, response

            # Set symmetric key
            session['symm_key'] = decrypted_symm_key

            # Retrieve information from session
            agent_email = session['email']
            agent_fingerprint = gpg.email_to_key(agent_email)

            # Delete agent public key
            result = gpg.del_pub_key(agent_fingerprint)
            session.pop('email', None)
            session.pop('nonce', None)

            response = 200
            message = 'Symmetric key saved. Del public key: {}'\
                      .format(result)
            log.log2info(77702, message)

        except Exception as e:
            log_msg = 'Invalid email and key entry: >>>{}<<<'.format(e)
            log.log2warning(20505, log_msg)
            message = 'Message not received'
            response = 400

    return message, response

@POST.route('/encrypted', methods=['POST'])
def crypt_receive():
    """Receive encrypted data from agent

    Args:
        None

    Returns:
        message (str): Reception result
        response (int): HTTP response code
    """

    # Read configuration
    config = Config()
    cache_dir = config.agent_cache_directory(PATTOO_API_AGENT_NAME)

    try:
        # Retrieves Pgpier class
        gpg = get_gnupg(PATTOO_API_AGENT_NAME, config)

        #Sets key ID
        gpg.set_keyid()

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
    response = 400
    message = 'Proceed to key exchange first'

    # Block connection if a symmetric key was not stored
    if 'symm_key' not in session:
        message = 'No symmetric key'
        response = 403
        return message, response
    
    if request.method == 'POST':
        # Get data from agent
        data_json = request.get_json(silent=False)
        data_dict = json.loads(data_json)

        # Retrieved symmetrically encrypted data
        encrypted_data = data_dict['encrypted_data']

        # Symmetrically decrypt data
        data = gpg.symmetric_decrypt(encrypted_data, session['symm_key'])

        # Initialize key variables
        prefix = 'Invalid posted data.'

        posted_data = None
        source = None

        # Extract posted data and source
        try:
            data_extract = json.loads(data)
            posted_data = data_extract['data']
            source = data_extract['source']

        except Exception as e:
            log_message = 'Decrypted data extraction failed: {}'\
                          .format(e)
            log.log2warning(88001, log_message)

        log_message = 'Decrypted data extraction successful'
        log.log2info(77078, log_message)

        # Abort if posted_data isn't a list
        if isinstance(posted_data, dict) is False:
            log_message = '{} Not a dictionary'.format(prefix)
            log.log2warning(20024, log_message)
            abort(404)
        if len(posted_data) != len(CACHE_KEYS):
            log_message = ('''{} Incorrect length. Expected length of {}
                           '''.format(prefix, len(CACHE_KEYS)))
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
                     '{}{}{}_{}_{}.json'
                     .format(
                             cache_dir, os.sep, timestamp, source, suffix
                             )
                     )
        
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
        message = 'Decrypted and received'
        response = 202
        log.log2info(77077, message)
        
    return message, response
