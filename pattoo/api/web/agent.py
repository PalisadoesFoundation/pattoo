"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint, jsonify

# pattoo imports
from pattoo.db import db
from pattoo.db.tables import Agent

# Define the various global variables
REST_API_AGENT = Blueprint('REST_API_AGENT', __name__)


@REST_API_AGENT.route('/<int:idx_agent>')
def route_idx_agent(idx_agent):
    """Provide data from the Agent table.

    Args:
        idx_agent: Agent.idx_agent key

    Returns:
        _result: JSONify dict of Agent row values

    """
    # Initialize key variables
    _result = {}
    listing = []

    # Get the _result
    with db.db_query(20018) as session:
        rows = session.query(
            Agent.idx_agent,
            Agent.agent_id,
            Agent.agent_program,
            Agent.agent_hostname,
            Agent.polling_interval,
            Agent.enabled).filter(
                Agent.idx_agent == idx_agent)

    # Return
    for row in rows:
        _result['idx_agent'] = row.idx_agent
        _result['agent_id'] = row.agent_id
        _result['agent_program'] = row.agent_program
        _result['agent_hostname'] = row.agent_hostname
        _result['polling_interval'] = row.polling_interval
        _result['enabled'] = row.enabled
        listing.append(_result)
    result = jsonify(listing)
    return result


@REST_API_AGENT.route('')
def route_idx_agents():
    """Provide data from the Agent table.

    Args:
        None

    Returns:
        listing: JSONify list of dicts containing Agent row values

    """
    # Initialize key variables
    listing = []

    # Get the _result
    with db.db_query(20017) as session:
        rows = session.query(
            Agent.idx_agent,
            Agent.agent_id,
            Agent.agent_program,
            Agent.agent_hostname,
            Agent.polling_interval,
            Agent.enabled)

    # Return
    for row in rows:
        _result = {}
        _result['idx_agent'] = row.idx_agent
        _result['agent_id'] = row.agent_id
        _result['agent_program'] = row.agent_program
        _result['agent_hostname'] = row.agent_hostname
        _result['polling_interval'] = row.polling_interval
        _result['enabled'] = row.enabled
        listing.append(_result)
    result = jsonify(listing)
    return result
