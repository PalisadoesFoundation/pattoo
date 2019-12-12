#!/usr/bin/env python3
"""Administer the AgentGroup database table."""

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import AgentGroup


def agent_group_exists(name):
    """Get the db AgentGroup.idx_agent_group value for specific agent.

    Args:
        name: AgentGroup name

    Returns:
        result: AgentGroup.idx_agent_group value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(AgentGroup.idx_agent_group).filter(
            AgentGroup.name == name.encode())

    # Return
    for row in rows:
        result = row.idx_agent_group
        break
    return result


def insert_row(name, description, idx_pair_xlate_group):
    """Create the database AgentGroup.agent value.

    Args:
        name: AgentGroup name
        description: AgentGroup description
        idx_pair_xlate_group: PairXlateGroup table index

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(name, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20001, die=True) as session:
            session.add(
                AgentGroup(
                    name=name.encode(),
                    description=description.encode(),
                    idx_pair_xlate_group=idx_pair_xlate_group
                )
            )
