"""pattoo ORM Schema for User Authentication"""

# PIP3 imports
import graphene
from graphql import GraphQLError
from flask_graphql_auth import create_access_token, create_refresh_token

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
        username, password = Input['username'], Input['password']

        # Username and password authentication
        idx_user, enabled = _user.authenticate(username, password)

        # Verifying that authentication was successful and that the user is
        # enabled
        if (idx_user != None and bool(enabled)) is False:
            err = ('''Authentication Failure: incorrect credentials or user not
                   enabled!''')
            raise GraphQLError(err)

        # Creating tokens
        access_token = create_access_token(idx_user)
        refresh_token = create_refresh_token(idx_user)

        return AuthMutation(access_token, refresh_token)
