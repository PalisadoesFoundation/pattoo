#!/usr/bin/env python3
"""Administer the AgentGroup database table."""

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import AgentGroup


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_agent_group

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False

    # Get the result
    with db.db_query(20046) as session:
        rows = session.query(AgentGroup.idx_agent_group).filter(
            AgentGroup.idx_agent_group == idx)

    # Return
    for _ in rows:
        result = True
        break
    return result


def group_exists(agent_program):
    """Get the db AgentGroup.idx_agent_group value for specific agent.

    Args:
        agent_program: Pattoo agent program name

    Returns:
        result: AgentGroup.idx_agent_group value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20045) as session:
        rows = session.query(AgentGroup.idx_agent_group).filter(
            AgentGroup.agent_program == agent_program.encode())

    # Return
    for row in rows:
        result = row.idx_agent_group
        break
    return result


def insert_row(agent_program, description):
    """Create the database AgentGroup.agent value.

    Args:
        agent_program: Pattoo agent program name
        description: AgentGroup description

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(agent_program, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20037, die=True) as session:
            session.add(
                AgentGroup(
                    agent_program=agent_program.encode(),
                    description=description.encode()
                )
            )
