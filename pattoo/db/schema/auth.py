"""pattoo ORM Schema for User Authentication"""

# PIP3 imports
import graphene
from graphql import GraphQLError
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_header_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required
)

# pattoo imports
from pattoo.db.table import user as _user


class AuthMutationInput(graphene.InputObjectType):
    """Arguments for user authentication"""

    username = graphene.String(required=True, description='Username.')
    password = graphene.String(required=True, description='Password.')

class AuthMutation(graphene.Mutation):
    """Handles user authentication.

    Handles authentication an distribution of access tokens to allow for
    users to access server resources

    """
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        Input = AuthMutationInput(required=True)

    def mutate(self, info, Input):
        # Username and password authentication
        auth, enabled =_user.authenticate(Input['username'], Input['password'])

        # Verifying that authentication was successful and that the user is
        # enabled
        if (not auth or bool(enabled) is False):
            err = '''Authentication Failure: incorrect credentials or user not
            enabled!'''
            raise GraphQLError(err)

        # Creating tokens
        access_token = create_access_token(Input['username'])
        refresh_token = create_refresh_token(Input['username'])

        return AuthMutation(access_token, refresh_token)

