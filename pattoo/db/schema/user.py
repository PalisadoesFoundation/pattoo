"""pattoo ORM Schema for the User table."""

# Standard importations
import crypt

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# pattoo imports
from pattoo.db import db
from pattoo.db.models import User as UserModel
from pattoo.db.schema import utils
from pattoo_shared.constants import DATA_INT
from pattoo.db.table.user import User as UserTable


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

    password_expired = graphene.String(
        resolver=utils.resolve_username,
        description='Change password if True.')

    role = graphene.String(
        resolver=utils.resolve_username,
        description='Type of user.')

    enabled = graphene.String(
        description='True if enabled.')


class UserAttributeWithPassword(UserAttribute):
    """Descriptive attributes of the User table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    password = graphene.String(
        resolver=utils.resolve_password,
        description='Password.')


class User(SQLAlchemyObjectType, UserAttribute):
    """User node."""

    class Meta:
        """Define the metadata."""

        model = UserModel
        interfaces = (graphene.relay.Node,)

        # Hide certain fields as a tuple
        exclude_fields = ('password', )


class CreateUserInput(graphene.InputObjectType, UserAttributeWithPassword):
    """Arguments to create a User."""
    pass


class CreateUser(graphene.Mutation):
    """Create a User Mutation."""

    user = graphene.Field(
        lambda: User, description='User created by this mutation.')

    class Arguments:
        Input = CreateUserInput(required=True)

    def mutate(self, info_, Input):
        data = _input_to_dictionary(Input)
        user = UserModel(**data)

        # Create user only if they don't already exist
        person = UserTable(user.username.decode())
        if person.exists is False:
            with db.db_modify(20150, close=False) as session:
                session.add(user)
            return CreateUser(user=user)

        # Return nothing otherwise
        return None


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
    user = graphene.Field(
        lambda: User, description='User updated by this mutation.')

    class Arguments:
        Input = UpdateUserInput(required=True)

    def mutate(self, info_, Input):
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

    # Get password and encrypt
    password = input_.get('password')
    if password is not None:
        input_['password'] = crypt.crypt(password)

    result = utils.input_to_dictionary(input_, column=column)
    return result
