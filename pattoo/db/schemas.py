#!/usr/bin/env python3
"""pattoo ORM Schema classes.

Used for defining GraphQL interaction

Based on the pages at:

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

"""
# PIP3 imports
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

# pattoo imports
from pattoo.db.tables import (
        Data as DataTable,
        Pair as PairTable,
        DataPoint as DataPointTable,
        Glue as GlueTable
    )


class DataAttribute(object):
    """Descriptive attributes of the Data table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datapoint = graphene.String(
        description='DataPoint index.')

    timestamp = graphene.String(
        description='Data collection timestamp.')

    value = graphene.String(
        description='Data value.')


class Data(SQLAlchemyObjectType, DataAttribute):
    """Data node."""

    class Meta:
        """Define the metadata."""

        model = DataTable
        interfaces = (graphene.relay.Node,)


class DataConnections(relay.Connection):
    """GraphQL / SQlAlchemy Connection to the Data table."""

    class Meta:
        """Define the metadata."""

        node = Data


class PairAttribute(object):
    """Descriptive attributes of the Pair table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair = graphene.String(
        description='Pair index.')

    key = graphene.String(
        description='Key-value pair key.')

    value = graphene.String(
        description='Key-value pair value.')


class Pair(SQLAlchemyObjectType, PairAttribute):
    """Pair node."""

    class Meta:
        """Define the metadata."""

        model = PairTable
        interfaces = (graphene.relay.Node,)


class PairConnections(relay.Connection):
    """GraphQL / SQlAlchemy Connection to the Pair table."""

    class Meta:
        """Define the metadata."""

        node = Pair


class DataPointAttribute(object):
    """Descriptive attributes of the DataPoint table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datapoint = graphene.String(
        description='DataPoint index.')

    checksum = graphene.String(
        description='DataPoint value.')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class DataPoint(SQLAlchemyObjectType, DataPointAttribute):
    """DataPoint node."""

    class Meta:
        """Define the metadata."""

        model = DataPointTable
        interfaces = (graphene.relay.Node,)


class DataPointConnections(relay.Connection):
    """GraphQL / SQlAlchemy Connection to the DataPoint table."""

    class Meta:
        """Define the metadata."""

        node = DataPoint


class GlueAttribute(object):
    """Descriptive attributes of the Glue table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair = graphene.String(
        description='Pair table index.')

    idx_datapoint = graphene.String(
        description='DataPoint table index.')


class Glue(SQLAlchemyObjectType, GlueAttribute):
    """Glue node."""

    class Meta:
        """Define the metadata."""

        model = GlueTable
        interfaces = (graphene.relay.Node,)


class GlueConnections(relay.Connection):
    """GraphQL / SQlAlchemy Connection to the Glue table."""

    class Meta:
        """Define the metadata."""

        node = Glue


class Query(graphene.ObjectType):
    """Define GraphQL queries."""

    node = relay.Node.Field()

    glue = graphene.relay.Node.Field(Glue)
    all_glues = SQLAlchemyConnectionField(GlueConnections)

    datapoint = graphene.relay.Node.Field(DataPoint)
    all_datapoints = SQLAlchemyConnectionField(DataPointConnections)

    pair = graphene.relay.Node.Field(Pair)
    all_pairs = SQLAlchemyConnectionField(PairConnections)

    data = graphene.relay.Node.Field(Data)
    all_data = SQLAlchemyConnectionField(DataConnections)


# Make the schema global
SCHEMA = graphene.Schema(query=Query)
