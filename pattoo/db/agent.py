#!/usr/bin/env python3
"""Administer the Agent database table."""

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Agent


def agent_exists(agent_id):
    """Get the db Agent.idx_agent value for specific agent.

    Args:
        agent_id: Agent ID

    Returns:
        result: Agent.idx_agent value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20042) as session:
        rows = session.query(Agent.idx_agent).filter(
            Agent.agent_id == agent_id.encode())

    # Return
    for row in rows:
        result = row.idx_agent.decode()
        break
    return result


def insert_row(agent_id, idx_agent_group):
    """Create the database Agent.agent value.

    Args:
        agent_id: Agent ID value
        idx_agent_group: AgentGroup table ForeignKey

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(agent_id, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20036, die=True) as session:
            session.add(Agent(agent_id=agent_id.encode(),
                              idx_agent_group=idx_agent_group))
