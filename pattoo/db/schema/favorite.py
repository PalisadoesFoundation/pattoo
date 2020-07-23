"""pattoo ORM Schema for the Favorite table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db import db
from pattoo.db.models import Favorite as FavoriteModel
from pattoo.db.schema import utils
from pattoo_shared.constants import DATA_INT


class FavoriteAttribute():
    """Descriptive attributes of the Favorite table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_favorite = graphene.String(
        description='Favorite index.')

    idx_user = graphene.String(
        description='User table foreign key')

    idx_chart = graphene.String(
        description='Chart table foreign key.')

    order = graphene.String(
        description='Order of favorite in list.')

    enabled = graphene.String(
        description='True if enabled.')


class Favorite(SQLAlchemyObjectType, FavoriteAttribute):
    """Favorite node."""

    class Meta:
        """Define the metadata."""

        model = FavoriteModel
        interfaces = (graphene.relay.Node,)


class CreateFavoriteInput(graphene.InputObjectType, FavoriteAttribute):
    """Arguments to create a Favorite."""
    pass


class CreateFavorite(graphene.Mutation):
    """Create a Favorite Mutation."""

    favorite = graphene.Field(
        lambda: Favorite, description='Favorite created by this mutation.')

    class Arguments:
        Input = CreateFavoriteInput(required=True)

    def mutate(self, info_, Input):
        data = _input_to_dictionary(Input)

        favorite = FavoriteModel(**data)
        with db.db_modify(20149, close=False) as session:
            session.add(favorite)

        return CreateFavorite(favorite=favorite)


class UpdateFavoriteInput(graphene.InputObjectType, FavoriteAttribute):
    """Arguments to update a Favorite.

    InputFields are used in mutations to allow nested input data for mutations

    To use an InputField you define an InputObjectType that specifies the
    structure of your input data

    """

    # Provide a description of the ID
    idx_favorite = graphene.String(
        required=True, description='Favorite index value.')


class UpdateFavorite(graphene.Mutation):
    """Update a Favorite."""
    favorite = graphene.Field(
        lambda: Favorite, description='Favorite updated by this mutation.')

    class Arguments:
        Input = UpdateFavoriteInput(required=True)

    def mutate(self, info_, Input):
        data = _input_to_dictionary(Input)

        # Update database
        with db.db_modify(20153) as session:
            session.query(FavoriteModel).filter_by(
                idx_favorite=data['idx_favorite']).update(data)

        # Get code from database
        with db.db_query(20154, close=False) as session:
            favorite = session.query(FavoriteModel).filter_by(
                idx_favorite=data['idx_favorite']).first()

        return UpdateFavorite(favorite=favorite)


def _input_to_dictionary(input_):
    """Convert.

    Args:
        input_: GraphQL "data" dictionary structure from mutation

    Returns:
        result: Dict of inputs

    """
    # 'column' is a dict of DB model 'non string' column names and their types
    column = {
        'idx_favorite': DATA_INT,
        'idx_user': DATA_INT,
        'idx_chart': DATA_INT,
        'order': DATA_INT,
        'enabled': DATA_INT
    }
    result = utils.input_to_dictionary(input_, column=column)
    return result
