"""Initialize the PATTOO_API_WEB module."""

# Import PIP3 libraries
from flask import Flask

# Define the global URL prefix
from pattoo_shared.constants import PATTOO_API_WEB_PREFIX

# Import PATTOO_API_WEB Blueprints
from pattoo.db import db_session
from pattoo.api.web.graphql import GRAPHQL

# Setup flask
PATTOO_API_WEB = Flask(__name__)

# https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
# https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

@PATTOO_API_WEB.teardown_appcontext
def shutdown_session(exception=None):
    """Support the home route.

    Args:
        None

    Returns:
        GraphQL goodness

    """
    db_session.remove()


# Register Blueprints
PATTOO_API_WEB.register_blueprint(
    GRAPHQL, url_prefix=PATTOO_API_WEB_PREFIX)
