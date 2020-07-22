"""pattoo ORM Schema utility functions."""

from graphql_relay.node.node import from_global_id


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


def input_to_dictionary(_input):
    """Method to convert Graphene inputs into dictionary.

    Args:
        _input: GraphQL input

    Returns:
        dictionary: Dict of inputs

    """
    dictionary = {}
    for key in _input:
        # Convert GraphQL global id to database id
        if key[-2:] == 'id':
            _input[key] = from_global_id(_input[key])[1]
        dictionary[key] = _input[key]
    return dictionary
