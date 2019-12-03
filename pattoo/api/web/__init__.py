"""Initialize the PATTOO_API_WEB module."""

# Import PIP3 libraries
from flask import Flask
# from flask_cache import Cache

# Define the global URL prefix
from pattoo_shared.constants import PATTOO_API_WEB_PREFIX

# Import pattoo modules
from pattoo.db import POOL

# Setup REST URI prefix
PATTOO_API_WEB_REST_PREFIX = '{}/rest'.format(PATTOO_API_WEB_PREFIX)

# Setup flask
PATTOO_API_WEB = Flask(__name__)

# Setup memcache. Required for all API imports
# CACHE = Cache(PATTOO_API_WEB, config={'CACHE_TYPE': 'simple'})

# Import PATTOO_API_WEB Blueprints (MUST be done after CACHE)
from pattoo.api.web.graphql import GRAPHQL
from pattoo.api.web.rest import REST_API_DATA
from pattoo.api.web.status import API_STATUS

# Register Blueprints
PATTOO_API_WEB.register_blueprint(
    GRAPHQL, url_prefix=PATTOO_API_WEB_PREFIX)
PATTOO_API_WEB.register_blueprint(
    API_STATUS, url_prefix=PATTOO_API_WEB_PREFIX)
PATTOO_API_WEB.register_blueprint(
    REST_API_DATA, url_prefix=PATTOO_API_WEB_REST_PREFIX)


@PATTOO_API_WEB.teardown_appcontext
def shutdown_session(exception=None):
    """Support the home route.

    Args:
        None

    Returns:
        GraphQL goodness

    """
    POOL.remove()
