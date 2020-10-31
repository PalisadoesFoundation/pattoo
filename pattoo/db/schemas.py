#!/usr/bin/env python3
"""pattoo ORM Schema classes.

Used for defining GraphQL interaction

Based on the pages at:

    Basic Setup
    ===========

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

    Filtering based on DB column values
    ===================================
    https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-361978832

"""
# PIP3 imports
import graphene
from graphene import relay
from graphene.utils.str_converters import to_snake_case
from graphene.relay.connection import PageInfo
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql import GraphQLError
from graphql_relay.connection.arrayconnection import connection_from_list_slice
from sqlalchemy import desc, asc
from flask_graphql_auth import query_jwt_required, AuthInfoField

# Import schemas
from pattoo.db import db
from pattoo.db.table import user as table_user
from pattoo.db.models import User as UserModel
from pattoo.db.schema.agent import Agent
from pattoo.db.schema.agent_xlate import AgentXlate
from pattoo.db.schema import chart as chart_
from pattoo.db.schema import chart_datapoint as chart_datapoint_
from pattoo.db.schema.data import Data
from pattoo.db.schema.datapoint import DataPoint
from pattoo.db.schema import favorite as favorite_
from pattoo.db.schema.glue import Glue
from pattoo.db.schema.language import Language
from pattoo.db.schema.pair import Pair
from pattoo.db.schema.pair_xlate_group import PairXlateGroup
from pattoo.db.schema.pair_xlate import PairXlate
from pattoo.db.schema import user as user_
from pattoo.db.schema import auth

###############################################################################
# Add filtering support:
#
# https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-361978832
#
# Simpler solution with less functionality:
# https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-341824371
#
###############################################################################

class InstrumentedQuery(SQLAlchemyConnectionField):
    """Class to allow GraphQL filtering by SQlAlchemycolumn name.

    Add filtering support:
    https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-361978832

    """

    def __init__(self, type_, **kwargs):
        """InstrumentedQuery constructor"""
        self.query_args = {}
        for key, value in type_._meta.fields.items():
            if isinstance(value, graphene.Field):
                # Test
                field_type = value.type
                if isinstance(field_type, graphene.NonNull):
                    field_type = field_type.of_type
                self.query_args[key] = field_type()

        # Retrieving field keys and names
        args = kwargs.pop('args', dict())
        args.update(self.query_args)
        args['sort_by'] = graphene.List(graphene.String, required=False)

        # Required token field
        args['token'] = graphene.String(required=True)

        SQLAlchemyConnectionField.__init__(self, type_, args=args, **kwargs)

    @query_jwt_required
    def get_query(self, model, info, **args):
        """Replace the get_query method."""
        query_filters = {k: v for k, v in args.items() if k in self.query_args}

        # Convert all string values to unicode for database
        # non-numeric column lookups
        query_filters = {k: (v.encode() if isinstance(
            v, str) else v) for k, v in query_filters.items()}

        query = model.query.filter_by(**query_filters)
        if 'sort_by' in args:
            criteria = [self.get_order_by_criterion(
                model, *arg.split(' ')) for arg in args['sort_by']]
            query = query.order_by(*criteria)
        return query

    def connection_resolver(
            self, resolver, connection, model, root, info, **args):
        query = resolver(
            root, info, **args) or self.get_query(model, info, **args)

        if type(query) == AuthInfoField:
            message = query.message

            if query.message == "Invalid header padding":
                message = "Invalid Token Provided"

            raise GraphQLError(message)

        count = query.count()

        connection = connection_from_list_slice(
            query,
            args,
            slice_start=0,
            list_length=count,
            list_slice_length=count,
            connection_type=connection,
            pageinfo_type=PageInfo,
            edge_type=connection.Edge,
        )
        connection.iterable = query
        connection.length = count
        return connection

    @staticmethod
    def get_order_by_criterion(model, name, direction='asc'):
        order_functions = {'asc': asc, 'desc': desc}
        return order_functions[
            direction.lower()](getattr(model, to_snake_case(name)))

###############################################################################
# Map database table columns to igraphql attributes
###############################################################################


class Mutation(graphene.ObjectType):
    """Define GraphQL mutations"""

    # Chart Mutations
    createChart = chart_.CreateChart.Field()
    updateChart = chart_.UpdateChart.Field()

    # Chart Datapoints Mutation
    createChartDataPoint = chart_datapoint_.CreateChartDataPoint.Field()
    updateChartDataPoint = chart_datapoint_.UpdateChartDataPoint.Field()

    # Chart Favorites Mutation
    createFavorite = favorite_.CreateFavorite.Field()
    updateFavorite = favorite_.UpdateFavorite.Field()

    # User Mutations
    createUser = user_.CreateUser.Field()
    updateUser = user_.UpdateUser.Field()

    # Authentication mutations
    authenticate = auth.AuthMutation.Field()
    authRefresh = auth.RefreshMutation.Field()


class Query(graphene.ObjectType):
    """Define GraphQL queries."""

    # Query types
    glue = InstrumentedQuery(Glue)
    datapoint = InstrumentedQuery(DataPoint)
    pair = InstrumentedQuery(Pair)
    data = InstrumentedQuery(Data)
    language = InstrumentedQuery(Language)
    pair_xlate_group = InstrumentedQuery(PairXlateGroup)
    pair_xlate = InstrumentedQuery(PairXlate)
    agent_xlate = InstrumentedQuery(AgentXlate)
    agent = InstrumentedQuery(Agent)
    chart = InstrumentedQuery(chart_.Chart)
    user = InstrumentedQuery(user_.User)
    favorite = InstrumentedQuery(favorite_.Favorite)
    chart_datapoint = InstrumentedQuery(chart_datapoint_.ChartDataPoint)

    # Query for username / password queries
    authenticate = graphene.List(
        user_.User,
        username=graphene.String(required=True),
        password=graphene.String(required=True)
    )

    def resolve_authenticate(self, info, **kwargs):
        """Filter by row by User.username and User.password."""
        # Initialize key variables
        result = None

        # Determine valid password
        username_ = kwargs.get('username')
        password_ = kwargs.get('password')
        user_object = table_user.User(username_)
        valid = user_object.valid_password(password_)
        lookup = username_ if bool(valid) is True else ''

        # Get data and return
        if bool(valid) is True:
            with db.db_query(20152, close=False) as session:
                result = session.query(
                    UserModel
                    ).filter(
                        UserModel.username == lookup.encode())
        return result


# Make the schema global
SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
