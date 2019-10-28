"""Pattoo version routes."""

# Flask imports
from flask import Blueprint

# Define the STATUS global variable
STATUS = Blueprint('STATUS', __name__)


@STATUS.route('/status')
def index():
    """Function for handling home route.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    return 'Pattoo is Operational.\n'
