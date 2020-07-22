"""pattoo ORM Schema for the DataPoint table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import ChartDataPoint as ChartDataPointModel


class ChartDataPointAttribute():
    """Descriptive attributes of the ChartDataPoint table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_chart_datapoint = graphene.String(
        description='ChartDataPoint index.')

    idx_datapoint = graphene.String(
        description='DataPoint table foreign key')

    idx_chart = graphene.String(
        description='Chart table foreign key.')

    enabled = graphene.String(
        description='True if enabled.')


class ChartDataPoint(SQLAlchemyObjectType, ChartDataPointAttribute):
    """ChartDataPoint node."""

    class Meta:
        """Define the metadata."""

        model = ChartDataPointModel
        interfaces = (graphene.relay.Node,)
