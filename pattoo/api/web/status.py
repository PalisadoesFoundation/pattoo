"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint

# Define the various global variables
API_STATUS = Blueprint('API_STATUS', __name__)


@API_STATUS.route('/status')
def index():
    """Provide the status page.

    Args:
        None

    Returns:
        Status page

    """
    # Return
    return 'The Pattoo Web API is Operational.\n'
