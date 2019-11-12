"""Pattoo version routes."""

# Flask imports
from flask import Blueprint

# pattoo imports
from flask_graphql import GraphQLView
from pattoo.db.schemas import SCHEMA

# Define the GRAPHQL global variable
GRAPHQL = Blueprint('GRAPHQL', __name__)

# Create the base GraphQL route
GRAPHQL.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=SCHEMA,
        graphiql=False))

# Create the base iGraphQL route
GRAPHQL.add_url_rule(
    '/igraphql',
    view_func=GraphQLView.as_view(
        'igraphql',
        schema=SCHEMA,
        graphiql=True))
