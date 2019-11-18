"""Initialize the PATTOO_API_WEB module."""

# Import PIP3 libraries
from flask import Flask

# Define the global URL prefix
from pattoo_shared.constants import PATTOO_API_SITE_PREFIX

# Import PATTOO_API_WEB Blueprints
from pattoo.db import POOL
from pattoo.api.web.graphql import GRAPHQL
from pattoo.api.web.data import REST_API_DATA

# Setup REST URI prefix
PATTOO_API_WEB_REST_PREFIX = '{}/rest'.format(PATTOO_API_SITE_PREFIX)

# Setup flask
PATTOO_API_WEB = Flask(__name__)

# Register Blueprints
PATTOO_API_WEB.register_blueprint(
    GRAPHQL, url_prefix=PATTOO_API_SITE_PREFIX)
PATTOO_API_WEB.register_blueprint(
    REST_API_DATA, url_prefix='{}/data'.format(PATTOO_API_WEB_REST_PREFIX))


@PATTOO_API_WEB.teardown_appcontext
def shutdown_session(exception=None):
    """Support the home route.

    Args:
        None

    Returns:
        GraphQL goodness

    """
    POOL.remove()


@PATTOO_API_WEB.route('/status')
def index():
    """Provide the status page.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    return 'The Pattoo Web API is Operational.\n'
