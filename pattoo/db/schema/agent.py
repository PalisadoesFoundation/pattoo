"""pattoo ORM Schema for the Agent table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import Agent as AgentModel
from pattoo.db.schema import utils


class AgentAttribute():
    """Descriptive attributes of the Agent table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_agent = graphene.String(
        description='Agent table index.')

    idx_pair_xlate_group = graphene.String(
        description='PairXlateGroup table index. (ForeignKey)')

    agent_id = graphene.String(
        resolver=utils.resolve_agent_id,
        description='Agent identifier.')

    agent_polled_target = graphene.String(
        resolver=utils.resolve_agent_polled_target,
        description='Source of the Agent\'s data')

    agent_program = graphene.String(
        resolver=utils.resolve_agent_program,
        description='Name of the Agent program that retrieved the data.')

    enabled = graphene.String(
        description='True if enabled.')


class Agent(SQLAlchemyObjectType, AgentAttribute):
    """Agent node."""

    class Meta:
        """Define the metadata."""

        model = AgentModel
        interfaces = (graphene.relay.Node,)
