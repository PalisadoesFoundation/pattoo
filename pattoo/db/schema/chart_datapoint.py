"""pattoo ORM Schema for the DataPoint table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db import db
from pattoo.db.models import ChartDataPoint as ChartDataPointModel
from pattoo.db.schema import utils
from pattoo_shared.constants import DATA_INT


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


class CreateChartDataPointInput(
        graphene.InputObjectType, ChartDataPointAttribute):
    """Arguments to create a ChartDataPoint entry."""
    pass


class CreateChartDataPoint(graphene.Mutation):
    """Create a ChartDataPoint Mutation."""

    chart_datapoint = graphene.Field(
        lambda: ChartDataPoint,
        description='ChartDataPoint created by this mutation.')

    class Arguments:
        Input = CreateChartDataPointInput(required=True)

    def mutate(self, info_, Input):
        data = _input_to_dictionary(Input)

        chart_datapoint = ChartDataPointModel(**data)
        with db.db_modify(20147, close=False) as session:
            session.add(chart_datapoint)

        return CreateChartDataPoint(chart_datapoint=chart_datapoint)


class UpdateChartDataPointInput(
        graphene.InputObjectType, ChartDataPointAttribute):
    """Arguments to update a ChartDataPoint entry.

    InputFields are used in mutations to allow nested input data for mutations

    To use an InputField you define an InputObjectType that specifies the
    structure of your input data

    """

    # Provide a description of the ID
    idx_chart_datapoint = graphene.String(
        required=True, description='ChartDataPoint index value.')


class UpdateChartDataPoint(graphene.Mutation):
    """Update a ChartDataPoint entry."""
    chart_datapoint = graphene.Field(
        lambda: ChartDataPoint,
        description='ChartDataPoint updated by this mutation.')

    class Arguments:
        Input = UpdateChartDataPointInput(required=True)

    def mutate(self, info_, Input):
        data = _input_to_dictionary(Input)

        # Update database
        with db.db_modify(20145) as session:
            session.query(ChartDataPointModel).filter_by(
                idx_chart_datapoint=data['idx_chart_datapoint']).update(data)

        # Get code from database
        with db.db_query(20146, close=False) as session:
            chart_datapoint = session.query(ChartDataPointModel).filter_by(
                idx_chart_datapoint=data['idx_chart_datapoint']).first()

        return UpdateChartDataPoint(chart_datapoint=chart_datapoint)


def _input_to_dictionary(input_):
    """Convert.

    Args:
        input_: GraphQL "data" dictionary structure from mutation

    Returns:
        result: Dict of inputs

    """
    # 'column' is a dict of DB model 'non string' column names and their types
    column = {
        'idx_chart_datapoint': DATA_INT,
        'idx_datapoint': DATA_INT,
        'idx_chart': DATA_INT,
        'enabled': DATA_INT
    }
    result = utils.input_to_dictionary(input_, column=column)
    return result
