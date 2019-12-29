"""Pattoo. Posting Routes."""

# Standard imports
import os
import json
import sys
from random import randrange

# Flask imports
from flask import Blueprint, request, abort

# pattoo imports
from pattoo_shared import log
from pattoo_shared.constants import CACHE_KEYS
from pattoo_shared import configuration
from pattoo.constants import PATTOO_API_AGENT_NAME


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
    config = configuration.Config()
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
