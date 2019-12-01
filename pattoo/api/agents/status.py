"""Pattoo. Status routes."""

# Flask imports
from flask import Blueprint

# Define the STATUS global variable
STATUS = Blueprint('STATUS', __name__)


@STATUS.route('/status')
def index():
    """Provide the status page.

    Args:
        None

    Returns:
        Status page

    """
    # Return
    return 'The Pattoo Agent API is Operational.\n'
