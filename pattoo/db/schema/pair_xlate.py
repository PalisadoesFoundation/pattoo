"""pattoo ORM Schema for the PairXlate table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import PairXlate as PairXlateModel
from pattoo.db.schema import utils


class PairXlateAttribute():
    """Descriptive attributes of the PairXlate table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair_xlate = graphene.String(
        description='PairXlate table index.')

    idx_pair_xlate_group = graphene.String(
        description='PairXlateGroup table index (ForeignKey).')

    idx_language = graphene.String(
        description='Language table index (ForeignKey).')

    key = graphene.String(
        resolver=utils.resolve_key,
        description=('''\
Key-pair key. Part of a composite primary key with "idx_language" and \
"idx_pair_xlate_group"'''))

    translation = graphene.String(
        resolver=utils.resolve_translation,
        description='Translation for the Key-pair key.')

    units = graphene.String(
        resolver=utils.resolve_units,
        description='Units of measure for the Key-pair key.')

    enabled = graphene.String(
        description='"True" if enabled.')


class PairXlate(SQLAlchemyObjectType, PairXlateAttribute):
    """PairXlate node."""

    class Meta:
        """Define the metadata."""

        model = PairXlateModel
        interfaces = (graphene.relay.Node,)
