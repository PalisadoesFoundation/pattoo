#!/usr/bin/env python3
"""pattoo ORM Schema classes.

Used for defining GraphQL interaction

Based on the pages at:

    Basic Setup
    ===========

    https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial
    https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

    Filtering based on DB column values
    ===================================
    https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-361978832

"""
# PIP3 imports
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

# Required for InstrumentedQuery
from graphene.utils.str_converters import to_snake_case
from graphene.relay.connection import PageInfo
from graphql_relay.connection.arrayconnection import connection_from_list_slice
from sqlalchemy import desc, asc

# pattoo imports
from pattoo.db.models import (
        Data as DataModel,
        Pair as PairModel,
        DataPoint as DataPointModel,
        Glue as GlueModel,
        Language as LanguageModel,
        PairXlateGroup as PairXlateGroupModel,
        PairXlate as PairXlateModel,
        AgentXlate as AgentXlateModel,
        Agent as AgentModel,
        User as UserModel,
        Favorite as FavoriteModel,
        Chart as ChartModel,
        ChartDataPoint as ChartDataPointModel
    )


def resolve_first_name(obj, _):
    """Convert 'first_name' from bytes to string."""
    return obj.first_name.decode()


def resolve_last_name(obj, _):
    """Convert 'last_name' from bytes to string."""
    return obj.last_name.decode()


def resolve_username(obj, _):
    """Convert 'username' from bytes to string."""
    return obj.username.decode()


def resolve_password(obj, _):
    """Convert 'password' from bytes to string."""
    return obj.password.decode()


def resolve_checksum(obj, _):
    """Convert 'checksum' from bytes to string."""
    return obj.checksum.decode()


def resolve_key(obj, _):
    """Convert 'key' from bytes to string."""
    return obj.key.decode()


def resolve_value(obj, _):
    """Convert 'value' from bytes to string."""
    return obj.value.decode()


def resolve_translation(obj, _):
    """Convert 'translation' from bytes to string."""
    return obj.translation.decode()


def resolve_name(obj, _):
    """Convert 'name' from bytes to string."""
    return obj.name.decode()


def resolve_agent_id(obj, _):
    """Convert 'agent_id' from bytes to string."""
    return obj.agent_id.decode()


def resolve_agent_program(obj, _):
    """Convert 'agent_program' from bytes to string."""
    return obj.agent_program.decode()


def resolve_agent_polled_target(obj, _):
    """Convert 'agent_polled_target' from bytes to string."""
    return obj.agent_polled_target.decode()


def resolve_code(obj, _):
    """Convert 'code' from bytes to string."""
    return obj.code.decode()


def resolve_units(obj, _):
    """Convert 'units' from bytes to string."""
    return obj.units.decode()


###############################################################################
# Add filtering support:
#
# https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-361978832
#
# Simpler solution with less functionality:
# https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-341824371
#
###############################################################################

class InstrumentedQuery(SQLAlchemyConnectionField):
    """Class to allow GraphQL filtering by SQlAlchemycolumn name.

    Add filtering support:
    https://github.com/graphql-python/graphene-sqlalchemy/issues/27#issuecomment-361978832

    """

    def __init__(self, type_, **kwargs):
        self.query_args = {}
        for key, value in type_._meta.fields.items():
            if isinstance(value, graphene.Field):
                # Test
                field_type = value.type
                if isinstance(field_type, graphene.NonNull):
                    field_type = field_type.of_type
                self.query_args[key] = field_type()
        args = kwargs.pop('args', dict())
        args.update(self.query_args)
        args['sort_by'] = graphene.List(graphene.String, required=False)
        SQLAlchemyConnectionField.__init__(self, type_, args=args, **kwargs)

    def get_query(self, model, info, **args):
        """Replace the get_query method."""
        query_filters = {k: v for k, v in args.items() if k in self.query_args}

        # Convert all string values to unicode for database
        # non-numeric column lookups
        query_filters = {k: (v.encode() if isinstance(
            v, str) else v) for k, v in query_filters.items()}

        query = model.query.filter_by(**query_filters)
        if 'sort_by' in args:
            criteria = [self.get_order_by_criterion(
                model, *arg.split(' ')) for arg in args['sort_by']]
            query = query.order_by(*criteria)
        return query

    def connection_resolver(
            self, resolver, connection, model, root, info, **args):
        query = resolver(
            root, info, **args) or self.get_query(model, info, **args)
        count = query.count()
        connection = connection_from_list_slice(
            query,
            args,
            slice_start=0,
            list_length=count,
            list_slice_length=count,
            connection_type=connection,
            pageinfo_type=PageInfo,
            edge_type=connection.Edge,
        )
        connection.iterable = query
        connection.length = count
        return connection

    @staticmethod
    def get_order_by_criterion(model, name, direction='asc'):
        order_functions = {'asc': asc, 'desc': desc}
        return order_functions[
            direction.lower()](getattr(model, to_snake_case(name)))

###############################################################################
# Map database table columns to igraphql attributes
###############################################################################


class DataAttribute():
    """Descriptive attributes of the Data table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datapoint = graphene.String(
        description='DataPoint index. (ForeignKey)')

    timestamp = graphene.String(
        description='Data collection timestamp.')

    value = graphene.String(
        description='Data value.')


class Data(SQLAlchemyObjectType, DataAttribute):
    """Data node."""

    class Meta:
        """Define the metadata."""

        model = DataModel
        interfaces = (graphene.relay.Node,)


class PairAttribute():
    """Descriptive attributes of the Pair table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair = graphene.String(
        description='Pair index.')

    key = graphene.String(
        resolver=resolve_key,
        description='Key-value pair key.')

    value = graphene.String(
        resolver=resolve_value,
        description='Key-value pair value.')


class Pair(SQLAlchemyObjectType, PairAttribute):
    """Pair node."""

    class Meta:
        """Define the metadata."""

        model = PairModel
        interfaces = (graphene.relay.Node,)


class DataPointAttribute():
    """Descriptive attributes of the DataPoint table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_datapoint = graphene.String(
        description='DataPoint index.')

    idx_agent = graphene.String(
        description='Agent table index. (ForeignKey)')

    checksum = graphene.String(
        resolver=resolve_checksum,
        description='Unique DataPoint checksum.')

    data_type = graphene.String(
        description=(
            'Type of data, (String, Integer, Float, Counter, Counter64)'))

    last_timestamp = graphene.String(
        description=('''\
Timestamp when the Data table was last updated for this datapoint.'''))

    polling_interval = graphene.String(
        description='Updating interval in milliseconds for the datapoint.')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class DataPoint(SQLAlchemyObjectType, DataPointAttribute):
    """DataPoint node."""

    class Meta:
        """Define the metadata."""

        model = DataPointModel
        interfaces = (graphene.relay.Node,)


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


class ChartAttribute():
    """Descriptive attributes of the Chart table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_chart = graphene.String(
        description='Chart index.')

    name = graphene.String(
        resolver=resolve_name,
        description='Chart name.')

<<<<<<< HEAD
=======
    checksum = graphene.String(
        resolver=resolve_checksum,
        description='Chart checksum.')

>>>>>>> 923ddfdbc8b5092e9017f41cea7a51c3ebf84a99
    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class Chart(SQLAlchemyObjectType, ChartAttribute):
    """Chart node."""

    class Meta:
        """Define the metadata."""

        model = ChartModel
        interfaces = (graphene.relay.Node,)


class ChartDataPointAttribute():
    """Descriptive attributes of the ChartDataPoint table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_chart_datapoint = graphene.String(
        description='ChartDataPoint index.')

    idx_datapoint = graphene.String(
        description='DataPoint table foreign key')

    idx_chart = graphene.String(
        description='Chart table foreign key.')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class ChartDataPoint(SQLAlchemyObjectType, ChartDataPointAttribute):
    """ChartDataPoint node."""

    class Meta:
        """Define the metadata."""

        model = ChartDataPointModel
        interfaces = (graphene.relay.Node,)


class FavoriteAttribute():
    """Descriptive attributes of the Favorite table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_favorite = graphene.String(
        description='Favorite index.')

    idx_user = graphene.String(
        description='User table foreign key')

    idx_chart = graphene.String(
        description='Chart table foreign key.')

    order = graphene.String(
        description='Order of favorite in list.')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class Favorite(SQLAlchemyObjectType, FavoriteAttribute):
    """Favorite node."""

    class Meta:
        """Define the metadata."""

        model = FavoriteModel
        interfaces = (graphene.relay.Node,)


class LanguageAttribute():
    """Descriptive attributes of the Language table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_language = graphene.String(
        description='Language table index.')

    code = graphene.String(
        resolver=resolve_code,
        description='Language code.')

    name = graphene.String(
        resolver=resolve_name,
        description='Name associated to language code.')


class Language(SQLAlchemyObjectType, LanguageAttribute):
    """Language node."""

    class Meta:
        """Define the metadata."""

        model = LanguageModel
        interfaces = (graphene.relay.Node,)


class UserAttribute():
    """Descriptive attributes of the User table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_user = graphene.String(
        description='User index.')

    first_name = graphene.String(
        resolver=resolve_first_name,
        description='First name.')

    last_name = graphene.String(
        resolver=resolve_last_name,
        description='Last name.')

    username = graphene.String(
        resolver=resolve_username,
        description='Username.')

    password = graphene.String(
        resolver=resolve_password,
        description='Password.')

    enabled = graphene.String(
        description='True if the DataPoint is enabled.')


class User(SQLAlchemyObjectType, UserAttribute):
    """User node."""

    class Meta:
        """Define the metadata."""

        model = UserModel
        interfaces = (graphene.relay.Node,)


class PairXlateGroupAttribute():
    """Descriptive attributes of the PairXlateGroup table.

    A generic class to mutualize description of attributes for both queries
    and mutations.

    """

    idx_pair_xlate_group = graphene.String(
        description='PairXlateGroup table index.')

    name = graphene.String(
        resolver=resolve_name,
        description='Name of translation group.')

    enabled = graphene.String(
        description='"True" if the group is enabled.')


class PairXlateGroup(SQLAlchemyObjectType, PairXlateGroupAttribute):
    """PairXlateGroup node."""

    class Meta:
        """Define the metadata."""

        model = PairXlateGroupModel
        interfaces = (graphene.relay.Node,)


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
        resolver=resolve_key,
        description=('''\
Key-pair key. Part of a composite primary key with "idx_language" and \
"idx_pair_xlate_group"'''))

    translation = graphene.String(
        resolver=resolve_translation,
        description='Translation for the Key-pair key.')

    units = graphene.String(
        resolver=resolve_units,
        description='Units of measure for the Key-pair key.')

    enabled = graphene.String(
        description='"True" if enabled.')


class PairXlate(SQLAlchemyObjectType, PairXlateAttribute):
    """PairXlate node."""

    class Meta:
        """Define the metadata."""

        model = PairXlateModel
        interfaces = (graphene.relay.Node,)


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
        resolver=resolve_agent_id,
        description='Agent identifier.')

    agent_polled_target = graphene.String(
        resolver=resolve_agent_polled_target,
        description='Source of the Agent\'s data')

    agent_program = graphene.String(
        resolver=resolve_agent_program,
        description='Name of the Agent program that retrieved the data.')

    enabled = graphene.String(
        description='"True" if the Agent is enabled.')


class Agent(SQLAlchemyObjectType, AgentAttribute):
    """Agent node."""

    class Meta:
        """Define the metadata."""

        model = AgentModel
        interfaces = (graphene.relay.Node,)


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
        resolver=resolve_agent_program,
        description=('Agent progam'))

    translation = graphene.String(
        resolver=resolve_translation,
        description='Translation of the agent program name.')

    enabled = graphene.String(
        description='"True" if enabled.')


class AgentXlate(SQLAlchemyObjectType, AgentXlateAttribute):
    """AgentXlate node."""

    class Meta:
        """Define the metadata."""

        model = AgentXlateModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    """Define GraphQL queries."""

    node = relay.Node.Field()

    # Results as a single entry filtered by 'id' and as a list
    glue = graphene.relay.Node.Field(Glue)
    all_glues = InstrumentedQuery(Glue)

    # Results as a single entry filtered by 'id' and as a list
    datapoint = graphene.relay.Node.Field(DataPoint)
    all_datapoints = InstrumentedQuery(DataPoint)

    # Results as a single entry filtered by 'id' and as a list
    pair = graphene.relay.Node.Field(Pair)
    all_pairs = InstrumentedQuery(Pair)

    # Results as a single entry filtered by 'id' and as a list
    data = graphene.relay.Node.Field(Data)
    all_data = InstrumentedQuery(Data)

    # Results as a single entry filtered by 'id' and as a list
    language = graphene.relay.Node.Field(Language)
    all_language = InstrumentedQuery(Language)

    # Results as a single entry filtered by 'id' and as a list
    pair_xlate_group = graphene.relay.Node.Field(PairXlateGroup)
    all_pair_xlate_group = InstrumentedQuery(PairXlateGroup)

    # Results as a single entry filtered by 'id' and as a list
    pair_xlate = graphene.relay.Node.Field(PairXlate)
    all_pair_xlate = InstrumentedQuery(PairXlate)

    # Results as a single entry filtered by 'id' and as a list
    agent_xlate = graphene.relay.Node.Field(AgentXlate)
    all_agent_xlate = InstrumentedQuery(AgentXlate)

    # Results as a single entry filtered by 'id' and as a list
    agent = graphene.relay.Node.Field(Agent)
    all_agent = InstrumentedQuery(Agent)

    # Results as a single entry filtered by 'id' and as a list
    chart = graphene.relay.Node.Field(Chart)
    all_chart = InstrumentedQuery(Chart)

    # Results as a single entry filtered by 'id' and as a list
    user = graphene.relay.Node.Field(User)
    all_user = InstrumentedQuery(User)

    # Results as a single entry filtered by 'id' and as a list
    favorite = graphene.relay.Node.Field(Favorite)
    all_favorite = InstrumentedQuery(Favorite)

    # Results as a single entry filtered by 'id' and as a list
    chart_datapoint = graphene.relay.Node.Field(ChartDataPoint)
    all_chart_datapoint = InstrumentedQuery(ChartDataPoint)


# Make the schema global
SCHEMA = graphene.Schema(query=Query)
