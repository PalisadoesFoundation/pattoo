"""pattoo ORM Schema for the DataPoint table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import DataPoint as DataPointModel
from pattoo.db.schema import utils


class DataPointAttribute():
    """Descriptive attributes of the DataPoint table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datapoint = graphene.String(
        description='DataPoint index.')

    idx_agent = graphene.String(
        description='Agent table index. (ForeignKey)')

    checksum = graphene.String(
        resolver=utils.resolve_checksum,
        description='Unique DataPoint checksum.')

    data_type = graphene.String(
        description=(
            'Type of data, (String, Integer, Float, Counter, Counter64)'))

    last_timestamp = graphene.String(
        description=('''\
Timestamp when the Data table was last updated for this datapoint.'''))

    polling_interval = graphene.String(
        description='Updating interval in milliseconds for the datapoint.')

    enabled = graphene.String(
        description='True if enabled.')


class DataPoint(SQLAlchemyObjectType, DataPointAttribute):
    """DataPoint node."""

    class Meta:
        """Define the metadata."""

        model = DataPointModel
        interfaces = (graphene.relay.Node,)
