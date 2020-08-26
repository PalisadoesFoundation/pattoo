"""Initialize the PATTOO_API_WEB module."""

# Python Module Imports
import os
import datetime

# Import PIP3 libraries
from flask import Flask
from flask_caching import Cache

# Define the global URL prefix
from pattoo_shared.constants import PATTOO_API_WEB_PREFIX

# Import pattoo modules
from pattoo.db import POOL
from pattoo.configuration import ConfigAPId as Config


# Setup REST URI prefix
PATTOO_API_WEB_REST_PREFIX = '{}/rest'.format(PATTOO_API_WEB_PREFIX)

# Setup flask and secret key config
PATTOO_API_WEB = Flask(__name__)


# Import GraphQLAuth from Flask-GraphQL-Auth
from flask_graphql_auth import GraphQLAuth

###############################################################################
#
# Setup Flask-GraphQL-Auth
#
###############################################################################

# Getting pattoo configuration and setting JWT secrete key
config = Config()
PATTOO_API_WEB.config['JWT_SECRET_KEY'] = config.jwt_secret_key()
PATTOO_API_WEB.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.acesss_token_exp()
PATTOO_API_WEB.config['JWT_REFRESH_TOKEN_EXPIRES'] = config.refresh_token_exp()

# Initialize authentication for pattoo api web flask app instance
auth = GraphQLAuth(PATTOO_API_WEB)

# Setup memcache. Required for all API imports
CACHE = Cache(PATTOO_API_WEB, config={'CACHE_TYPE': 'simple'})

# Import PATTOO_API_WEB Blueprints (MUST be done after CACHE)
from pattoo.api.web.graphql import GRAPHQL
from pattoo.api.web.rest import REST_API_DATA
from pattoo.api.web.status import API_STATUS

# Importing and instantiating CORs on GRAPHQL and REST API endpoints
# from flask_cors import CORS

# CORS(GRAPHQL)

# Register Blueprints
PATTOO_API_WEB.register_blueprint(
    GRAPHQL, url_prefix=PATTOO_API_WEB_PREFIX)
PATTOO_API_WEB.register_blueprint(
    API_STATUS, url_prefix=PATTOO_API_WEB_PREFIX)
PATTOO_API_WEB.register_blueprint(
    REST_API_DATA, url_prefix=PATTOO_API_WEB_REST_PREFIX)


@PATTOO_API_WEB.teardown_appcontext
def shutdown_session(exception=None):
    """Remove any unused POOL sessions after flask query.

    This is really important. Repeated requests to a URI after a database
    update could return current and previous depending on whether a previously
    cached connection is reused. This prevents this possibility.

    https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/

    Which states:

    'To use SQLAlchemy in a declarative way with your application, you just
    have to put the following code into your application module. Flask will
    automatically remove database sessions at the end of the request or when
    the application shuts down.'

    Overrides shutdown_session() method found in:

    https://github.com/pallets/flask-sqlalchemy/blob/master/flask_sqlalchemy/__init__.py

    Args:
        exception: Unused override value for exception.

    Returns:
        None

    """
    POOL.remove()
