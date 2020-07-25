"""pattoo ORM Schema for the Glue table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import Glue as GlueModel


class GlueAttribute():
    """Descriptive attributes of the Glue table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair = graphene.String(
        description='Pair table index. (ForeignKey)')

    idx_datapoint = graphene.String(
        description='DataPoint table index. (ForeignKey)')


class Glue(SQLAlchemyObjectType, GlueAttribute):
    """Glue node."""

    class Meta:
        """Define the metadata."""

        model = GlueModel
        interfaces = (graphene.relay.Node,)
