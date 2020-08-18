"""pattoo ORM Schema for the User table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError
from flask_graphql_auth import (mutation_jwt_required, get_jwt_identity,
                                AuthInfoField)

# pattoo imports
from pattoo.db import db
from pattoo.db.models import User as UserModel
from pattoo.db.table import user as _user
from pattoo.db.schema import utils
from pattoo_shared.constants import DATA_INT


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

    is_admin = graphene.String(
        description='Admin.')

    enabled = graphene.String(
        description='True if enabled.')


class User(SQLAlchemyObjectType, UserAttribute):
    """User node."""

    class Meta:
        """Define the metadata."""

        model = UserModel
        interfaces = (graphene.relay.Node,)


class ProtectedUser(graphene.Union):
    class Meta:
        types = (User, AuthInfoField)


class CreateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to create a User."""

    password = graphene.String(description='Password.')


class CreateUser(graphene.Mutation):
    """Create a User Mutation."""

    user = graphene.Field(lambda: ProtectedUser,
                          description='User created by this mutation.')

    class Arguments:
        Input = CreateUserInput(required=True)
        token = graphene.String()

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info_, Input):
        data = _input_to_dictionary(Input)
        token_idx_user = get_jwt_identity()

        # Checking that the user creating the new user is an admin
        if _user.is_admin(token_idx_user) is False:
            raise GraphQLError('Only admins can create a new user!')

        # Checking that a given username is not taken
        idx_user = _user.exists(data['username'].decode())
        if bool(idx_user) == True:
            raise GraphQLError('Username already exists!')

        # Generating password and salt User data
        data['password'], data['salt'] = \
        _user.generate_password_hash(data['password'].decode())

        user = UserModel(**data)
        with db.db_modify(20150, close=False) as session:
            session.add(user)

        return CreateUser(user)


class UpdateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to update a User.

    InputFields are used in mutations to allow nested input data for mutations

    To use an InputField you define an InputObjectType that specifies the
    structure of your input data

    """

    # Provide a description of the ID
    idx_user = graphene.String(
        required=True, description='User index value.')


class UpdateUser(graphene.Mutation):
    """Update a User."""
    user = graphene.Field(lambda: ProtectedUser,
                          description='User updated by this mutation.')

    class Arguments:
        Input = UpdateUserInput(required=True)
        token = graphene.String()

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info_, Input):
        data = _input_to_dictionary(Input)

        # Update database
        with db.db_modify(20151) as session:
            session.query(UserModel).filter_by(
                idx_user=data['idx_user']).update(data)

        # Get code from database
        with db.db_query(20152, close=False) as session:
            user = session.query(UserModel).filter_by(
                idx_user=data['idx_user']).first()

        return UpdateUser(user=user)


def _input_to_dictionary(input_):
    """Convert.

    Args:
        input_: GraphQL "data" dictionary structure from mutation

    Returns:
        result: Dict of inputs

    """
    # 'column' is a dict of DB model 'non string' column names and their types
    column = {
        'idx_user': DATA_INT,
        'enabled': DATA_INT
    }
    result = utils.input_to_dictionary(input_, column=column)
    return result
