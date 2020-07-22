"""pattoo ORM Schema for the Favorite table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import Favorite as FavoriteModel
from pattoo.db.schema import utils


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
