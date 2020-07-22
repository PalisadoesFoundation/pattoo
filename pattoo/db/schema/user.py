"""pattoo ORM Schema for the User table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db.models import User as UserModel
from pattoo.db.schema import utils


class UserAttribute():
    """Descriptive attributes of the User table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_user = graphene.String(
        description='User index.')

    first_name = graphene.String(
        resolver=utils.resolve_first_name,
        description='First name.')

    last_name = graphene.String(
        resolver=utils.resolve_last_name,
        description='Last name.')

    username = graphene.String(
        resolver=utils.resolve_username,
        description='Username.')

    password = graphene.String(
        resolver=utils.resolve_password,
        description='Password.')

    enabled = graphene.String(
        description='True if enabled.')


class User(SQLAlchemyObjectType, UserAttribute):
    """User node."""

    class Meta:
        """Define the metadata."""

        model = UserModel
        interfaces = (graphene.relay.Node,)
