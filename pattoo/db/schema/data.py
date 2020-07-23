"""pattoo ORM Schema for the Data table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import Data as DataModel


class DataAttribute():
    """Descriptive attributes of the Data table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datapoint = graphene.String(
        description='DataPoint index. (ForeignKey)')

    timestamp = graphene.String(
        description='Data collection timestamp.')

    value = graphene.String(
        description='Data value.')


class Data(SQLAlchemyObjectType, DataAttribute):
    """Data node."""

    class Meta:
        """Define the metadata."""

        model = DataModel
        interfaces = (graphene.relay.Node,)
