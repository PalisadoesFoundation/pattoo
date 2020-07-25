"""pattoo ORM Schema for the AgentXlate table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import AgentXlate as AgentXlateModel
from pattoo.db.schema import utils


class AgentXlateAttribute():
    """Descriptive attributes of the AgentXlate table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_agent_xlate = graphene.String(
        description='AgentXlate table index.')

    idx_language = graphene.String(
        description='Language table index (ForeignKey).')

    agent_program = graphene.String(
        resolver=utils.resolve_agent_program,
        description=('Agent progam'))

    translation = graphene.String(
        resolver=utils.resolve_translation,
        description='Translation of the agent program name.')

    enabled = graphene.String(
        description='True if enabled.')


class AgentXlate(SQLAlchemyObjectType, AgentXlateAttribute):
    """AgentXlate node."""

    class Meta:
        """Define the metadata."""

        model = AgentXlateModel
        interfaces = (graphene.relay.Node,)
