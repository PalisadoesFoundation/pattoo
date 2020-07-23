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
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene.utils.str_converters import to_snake_case
from graphene.relay.connection import PageInfo
from graphql_relay.connection.arrayconnection import connection_from_list_slice
from sqlalchemy import desc, asc

# Import schemas
from pattoo.db.schema.agent import Agent
from pattoo.db.schema.agent_xlate import AgentXlate
from pattoo.db.schema import user as user_
from pattoo.db.schema import chart as chart_
from pattoo.db.schema import chart_datapoint as chart_datapoint_
from pattoo.db.schema.data import Data
from pattoo.db.schema.datapoint import DataPoint
from pattoo.db.schema.favorite import Favorite
from pattoo.db.schema.glue import Glue
from pattoo.db.schema.language import Language
from pattoo.db.schema.pair import Pair
from pattoo.db.schema.pair_xlate_group import PairXlateGroup
from pattoo.db.schema.pair_xlate import PairXlate


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
        self.query_args = {}
        for key, value in type_._meta.fields.items():
            if isinstance(value, graphene.Field):
                # Test
                field_type = value.type
                if isinstance(field_type, graphene.NonNull):
                    field_type = field_type.of_type
                self.query_args[key] = field_type()
        args = kwargs.pop('args', dict())
        args.update(self.query_args)
        args['sort_by'] = graphene.List(graphene.String, required=False)
        SQLAlchemyConnectionField.__init__(self, type_, args=args, **kwargs)

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
    createChart = chart_.CreateChart.Field()
    updateChart = chart_.UpdateChart.Field()
    createChartDataPoint = chart_datapoint_.CreateChartDataPoint.Field()
    updateChartDataPoint = chart_datapoint_.UpdateChartDataPoint.Field()
    createUser = chart_datapoint_.CreateUser.Field()
    updateUser = chart_datapoint_.UpdateUser.Field()


class Query(graphene.ObjectType):
    """Define GraphQL queries."""

    node = relay.Node.Field()

    # Results as a single entry filtered by 'id' and as a list
    glue = graphene.relay.Node.Field(Glue)
    all_glues = InstrumentedQuery(Glue)

    # Results as a single entry filtered by 'id' and as a list
    datapoint = graphene.relay.Node.Field(DataPoint)
    all_datapoints = InstrumentedQuery(DataPoint)

    # Results as a single entry filtered by 'id' and as a list
    pair = graphene.relay.Node.Field(Pair)
    all_pairs = InstrumentedQuery(Pair)

    # Results as a single entry filtered by 'id' and as a list
    data = graphene.relay.Node.Field(Data)
    all_data = InstrumentedQuery(Data)

    # Results as a single entry filtered by 'id' and as a list
    language = graphene.relay.Node.Field(Language)
    all_language = InstrumentedQuery(Language)

    # Results as a single entry filtered by 'id' and as a list
    pair_xlate_group = graphene.relay.Node.Field(PairXlateGroup)
    all_pair_xlate_group = InstrumentedQuery(PairXlateGroup)

    # Results as a single entry filtered by 'id' and as a list
    pair_xlate = graphene.relay.Node.Field(PairXlate)
    all_pair_xlate = InstrumentedQuery(PairXlate)

    # Results as a single entry filtered by 'id' and as a list
    agent_xlate = graphene.relay.Node.Field(AgentXlate)
    all_agent_xlate = InstrumentedQuery(AgentXlate)

    # Results as a single entry filtered by 'id' and as a list
    agent = graphene.relay.Node.Field(Agent)
    all_agent = InstrumentedQuery(Agent)

    # Results as a single entry filtered by 'id' and as a list
    chart = graphene.relay.Node.Field(chart_.Chart)
    all_chart = InstrumentedQuery(chart_.Chart)

    # Results as a single entry filtered by 'id' and as a list
    user = graphene.relay.Node.Field(user_.User)
    all_user = InstrumentedQuery(user_.User)

    # Results as a single entry filtered by 'id' and as a list
    favorite = graphene.relay.Node.Field(Favorite)
    all_favorite = InstrumentedQuery(Favorite)

    # Results as a single entry filtered by 'id' and as a list
    chart_datapoint = graphene.relay.Node.Field(
        chart_datapoint_.ChartDataPoint)
    all_chart_datapoint = InstrumentedQuery(chart_datapoint_.ChartDataPoint)


# Make the schema global
SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
