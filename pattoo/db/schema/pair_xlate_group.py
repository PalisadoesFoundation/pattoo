"""pattoo ORM Schema for the PairXlateGroup table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import PairXlateGroup as PairXlateGroupModel
from pattoo.db.schema import utils


class PairXlateGroupAttribute():
    """Descriptive attributes of the PairXlateGroup table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair_xlate_group = graphene.String(
        description='PairXlateGroup table index.')

    name = graphene.String(
        resolver=utils.resolve_name,
        description='Name of translation group.')

    enabled = graphene.String(
        description='"True" if enabled.')


class PairXlateGroup(SQLAlchemyObjectType, PairXlateGroupAttribute):
    """PairXlateGroup node."""

    class Meta:
        """Define the metadata."""

        model = PairXlateGroupModel
        interfaces = (graphene.relay.Node,)
