#!/usr/bin/env python3
"""pattoo ORM Schema classes.

Used for defining GraphQL interaction

"""
# PIP3 imports
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

# pattoo imports
from pattoo.db.tables import (
        Data as DataTable,
        DataPoint as DataPointTable,
        DataSource as DataSourceTable,
        Agent as AgentTable
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


class DataConnection(relay.Connection):
    """GraphQL / SQlAlchemy Connection to the Data table."""

    class Meta:
        """Define the metadata."""

        node = Data


class DataPointAttribute(object):
    """Descriptive attributes of the DataPoint table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datasource = graphene.String(
        description='DataSource index.')

    checksum = graphene.String(
        description='Unique DataPoint checksum.')

    data_label = graphene.String(
        description='Agent assigned label for the DataPoint.')

    data_index = graphene.String(
        description='Agent assigned index for the DataPoint.')

    data_type = graphene.String(
        description='Agent assigned data type for the DataPoint.')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')

    last_timestamp = graphene.String(
        description='Last DataPoint update time in the Data table.')


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


class DataSourceAttribute(object):
    """Descriptive attributes of the DataSource table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datasource = graphene.String(
        description='DataSource index.')

    idx_agent = graphene.String(
        description='Agent index.')

    device = graphene.String(
        description='Device that reported the DataPoint value.')

    gateway = graphene.String(
        description='Intermediary gateway between Agent and Device.')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class DataSource(SQLAlchemyObjectType, DataSourceAttribute):
    """DataSource node."""

    class Meta:
        """Define the metadata."""

        model = DataSourceTable
        interfaces = (graphene.relay.Node,)


class DataSourceConnections(relay.Connection):
    """GraphQL / SQlAlchemy Connection to the DataSource table."""

    class Meta:
        """Define the metadata."""

        node = DataSource


class AgentAttribute(object):
    """Descriptive attributes of the Agent table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_agent = graphene.String(
        description='Agent index.')

    agent_id = graphene.String(
        description='Unique agent generated ID.')

    agent_hostname = graphene.String(
        description='Hostname of the Agent server.')

    agent_program = graphene.String(
        description='Name of the agent program that retrieved the DataPoint.')

    polling_interval = graphene.String(
        description='Frequency of polling DataPoint values by the agent..')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class Agent(SQLAlchemyObjectType, AgentAttribute):
    """Agent node."""

    class Meta:
        """Define the metadata."""

        model = AgentTable
        interfaces = (graphene.relay.Node,)


class AgentConnections(relay.Connection):
    """GraphQL / SQlAlchemy Connection to the Agent table."""

    class Meta:
        """Define the metadata."""

        node = Agent


class Query(graphene.ObjectType):
    """Define GraphQL queries."""

    node = relay.Node.Field()

    agent = graphene.relay.Node.Field(Agent)
    all_agents = SQLAlchemyConnectionField(AgentConnections)

    datasource = graphene.relay.Node.Field(DataSource)
    all_datasources = SQLAlchemyConnectionField(DataSourceConnections)

    datapoint = graphene.relay.Node.Field(DataPoint)
    all_datapoints = SQLAlchemyConnectionField(DataPointConnections)


# Make the schema global
SCHEMA = graphene.Schema(query=Query)
