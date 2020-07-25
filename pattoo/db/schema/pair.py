"""pattoo ORM Schema for the Pair table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import Pair as PairModel
from pattoo.db.schema import utils


class PairAttribute():
    """Descriptive attributes of the Pair table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair = graphene.String(
        description='Pair index.')

    key = graphene.String(
        resolver=utils.resolve_key,
        description='Key-value pair key.')

    value = graphene.String(
        resolver=utils.resolve_value,
        description='Key-value pair value.')


class Pair(SQLAlchemyObjectType, PairAttribute):
    """Pair node."""

    class Meta:
        """Define the metadata."""

        model = PairModel
        interfaces = (graphene.relay.Node,)
