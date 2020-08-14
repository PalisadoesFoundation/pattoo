"""pattoo ORM Schema for the Language table."""

# PIP3 imports
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_graphql_auth import AuthInfoField

# pattoo imports
from pattoo.db.models import Language as LanguageModel
from pattoo.db.schema import utils


class LanguageAttribute():
    """Descriptive attributes of the Language table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_language = graphene.String(
        description='Language table index.')

    code = graphene.String(
        resolver=utils.resolve_code,
        description='Language code.')

    name = graphene.String(
        resolver=utils.resolve_name,
        description='Name associated to language code.')


class Language(SQLAlchemyObjectType, LanguageAttribute):
    """Language node."""

    class Meta:
        """Define the metadata."""

        model = LanguageModel
        interfaces = (graphene.relay.Node,)

class ProtectedLanguage(graphene.Union):
    class Meta:
        types = (Language, AuthInfoField)
