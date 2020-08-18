"""pattoo ORM Schema for the Chart table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_graphql_auth import (mutation_jwt_required, get_jwt_identity,
                                AuthInfoField)

# pattoo imports
from pattoo.db import db
from pattoo.db.models import Chart as ChartModel
from pattoo.db.schema import utils
from pattoo_shared.constants import DATA_INT


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


class ProctectedChart(graphene.Union):
    class Meta:
        types = (Chart, AuthInfoField)


class CreateChartInput(graphene.InputObjectType, ChartAttribute):
    """Arguments to create a Chart."""
    pass


class CreateChart(graphene.Mutation):
    """Create a Chart Mutation."""

    chart = graphene.Field(
        lambda: ProctectedChart, description='Chart created by this mutation.')

    class Arguments:
        Input = CreateChartInput(required=True)
        token = graphene.String()

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info_, Input):
        data = _input_to_dictionary(Input)

        chart = ChartModel(**data)
        with db.db_modify(20142, close=False) as session:
            session.add(chart)

        return CreateChart(chart=chart)


class UpdateChartInput(graphene.InputObjectType, ChartAttribute):
    """Arguments to update a Chart.

    InputFields are used in mutations to allow nested input data for mutations

    To use an InputField you define an InputObjectType that specifies the
    structure of your input data

    """

    # Provide a description of the ID
    idx_chart = graphene.String(
        required=True, description='Chart index value.')


class UpdateChart(graphene.Mutation):
    """Update a Chart."""
    chart = graphene.Field(
        lambda: ProctectedChart, description='Chart updated by this mutation.')

    class Arguments:
        Input = UpdateChartInput(required=True)
        token = graphene.String()

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info_, Input):
        data = _input_to_dictionary(Input)

        # Update database
        with db.db_modify(20143) as session:
            session.query(ChartModel).filter_by(
                idx_chart=data['idx_chart']).update(data)

        # Get code from database
        with db.db_query(20144, close=False) as session:
            chart = session.query(ChartModel).filter_by(
                idx_chart=data['idx_chart']).first()

        return UpdateChart(chart=chart)


def _input_to_dictionary(input_):
    """Convert.

    Args:
        input_: GraphQL "data" dictionary structure from mutation

    Returns:
        result: Dict of inputs

    """
    # 'column' is a dict of DB model 'non string' column names and their types
    column = {
        'idx_chart': DATA_INT,
        'enabled': DATA_INT
    }
    result = utils.input_to_dictionary(input_, column=column)
    return result
