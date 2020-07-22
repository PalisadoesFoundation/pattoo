"""pattoo ORM Schema for the Chart table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db import db
from pattoo.db.models import Chart as ChartModel
from pattoo.db.schema import utils


class ChartAttribute():
    """Descriptive attributes of the Chart table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_chart = graphene.String(
        description='Chart index.')

    name = graphene.String(
        resolver=utils.resolve_name,
        description='Chart name.')

    checksum = graphene.String(
        resolver=utils.resolve_checksum,
        description='Chart checksum.')

    enabled = graphene.String(
        description='True if enabled.')


class Chart(SQLAlchemyObjectType, ChartAttribute):
    """Chart node."""

    class Meta:
        """Define the metadata."""

        model = ChartModel
        interfaces = (graphene.relay.Node,)


class CreateChartInput(graphene.InputObjectType, ChartAttribute):
    """Arguments to create a chart."""
    pass


class CreateChart(graphene.Mutation):
    """Create a chart Mutation."""

    chart = graphene.Field(
        lambda: Chart, description='Chart created by this mutation.')

    class Arguments:
        input_ = CreateChartInput(required=True)

    def mutate(self, info_, input_):
        data = utils.input_to_dictionary(input_)

        chart = ChartModel(**data)
        with db.db_modify(20036, die=True) as session:
            session.add(chart)

        return CreateChart(chart=chart)


class UpdateChartInput(graphene.InputObjectType, ChartAttribute):
    """Arguments to update a chart.

    InputFields are used in mutations to allow nested input data for mutations

    To use an InputField you define an InputObjectType that specifies the
    structure of your input data

    """

    # Provide a description of the ID
    id = graphene.ID(required=True, description='Global ID of the chart.')


class UpdateChart(graphene.Mutation):
    """Update a chart."""
    chart = graphene.Field(
        lambda: Chart, description='Chart updated by this mutation.')

    class Arguments:
        input_ = UpdateChartInput(required=True)

    def mutate(self, info_, input_):
        data = utils.input_to_dictionary(input_)

        # Update database
        with db.db_modify(20036, die=True) as session:
            session.query(ChartModel).filter_by(id=data['id']).update(data)

        # Get code from database
        with db.db_query(20038) as session:
            chart = session.query(ChartModel).filter_by(id=data['id']).first()

        return UpdateChart(chart=chart)
