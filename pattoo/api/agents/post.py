"""Pattoo. Posting Routes."""

# Standard imports
import os
import json

# Flask imports
from flask import Blueprint, request, abort

# pattoo imports
from pattoo_shared import log
from pattoo_shared.constants import PATTOO_API_AGENT_EXECUTABLE
from pattoo_shared import configuration


# Define the POST global variable
POST = Blueprint('POST', __name__)


@POST.route('/receive/<agent_id>', methods=['POST'])
def receive(agent_id):
    """Function for handling the agent posting route.

    Args:
        agent_id: Unique Identifier of an pattoo agent

    Returns:
        Text response of Received

    """
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
    if isinstance(posted_data, list) is False:
        abort(404)

    # Extract key values from posting
    try:
        timestamp = int(posted_data[0]['timestamp'])
    except:
        abort(404)

    # Create a hash of the agent_hostname
    json_path = (
        '{}{}{}_{}.json'.format(
            cache_dir, os.sep, timestamp, agent_id))

    # Create cache file
    with open(json_path, "w+") as temp_file:
        json.dump(posted_data, temp_file)

    # Return
    return 'OK'
