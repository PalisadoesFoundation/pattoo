"""Pattoo. Posting Routes."""

# Standard imports
import os
import json
import sys

# Flask imports
from flask import Blueprint, request, abort

# pattoo imports
from pattoo_shared import log
from pattoo_shared.constants import PATTOO_API_AGENT_EXECUTABLE, CACHE_KEYS
from pattoo_shared import configuration


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
    cache_dir = config.agent_cache_directory(PATTOO_API_AGENT_EXECUTABLE)

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
        log_message = '{} Incorrect length'.format(prefix)
        log.log2warning(20019, log_message)
        abort(404)
    for key in posted_data.keys():
        if key not in CACHE_KEYS:
            log_message = '{} Invalid key'.format(prefix)
            log.log2warning(20018, log_message)
            abort(404)

    # Extract key values from posting
    try:
        timestamp = int(posted_data['datapoints'][0]['timestamp'])
    except:
        abort(404)

    # Create a hash of the agent_hostname
    json_path = (
        '{}{}{}_{}.json'.format(
            cache_dir, os.sep, timestamp, source))

    # Create cache file
    try:
        with open(json_path, 'w+') as temp_file:
            json.dump(posted_data, temp_file)
    except Exception as err:
        log_message = '{}'.format(err)
        log.log2warning(20016, log_message)
        abort(404)
    except:
        log_message = ("""API Failure: [{}, {}, {}]\
""".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
        log.log2warning(20017, log_message)
        abort(404)

    # Return
    return 'OK'
