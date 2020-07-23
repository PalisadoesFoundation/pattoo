"""pattoo ORM Schema utility functions."""

from graphql_relay.node.node import from_global_id
from pattoo_shared import log


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


def input_to_dictionary(input_):
    """Method to convert Graphene inputs into dictionary.

    Args:
        input_: GraphQL "data" dictionary structure from mutation

    Returns:
        dictionary: Dict of inputs

    """
    # Initialize key variables
    dictionary = {}

    # Process each key from the imput
    for key in input_:
        # Convert GraphQL global id to database id
        if key[-2:] == 'id':
            input_[key] = from_global_id(input_[key])[1]
        else:
            # Otherwise the key is related to the database.
            # We only use Unicode data in the tables, so we need to convert.
            if isinstance(input_[key], str):
                input_[key] = input_[key].encode()

        dictionary[key] = input_[key]
    return dictionary
