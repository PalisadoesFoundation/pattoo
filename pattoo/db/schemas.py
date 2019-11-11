#!/usr/bin/env python3
"""pattoo ORM Schema classes.

Used for defining GraphQL interaction

"""
# PIP3 imports
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene

# pattoo imports
from db.tables import (
    Data as DataTable,
    )


# Create a generic class to mutualize description of attributes for
# both queries and mutations
class DataAttribute(object):
    """Descriptive attributes of the Data table."""

    idx_datapoint = graphene.String(description='DataPoint Index.')
    timestamp = graphene.String(description='Data collection timestamp.')
    value = graphene.String(description='Data value.')


class Data(SQLAlchemyObjectType, DataAttribute):
    """Data node."""

    class Meta:
        """Define metadata of the node."""

        model = DataTable
        interfaces = (graphene.relay.Node,)
