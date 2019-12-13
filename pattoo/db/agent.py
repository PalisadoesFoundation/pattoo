#!/usr/bin/env python3
"""Administer the Agent database table."""

from collections import namedtuple

# PIP3 imports
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Agent


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_agent

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20027) as session:
        rows = session.query(Agent.idx_agent).filter(
            Agent.idx_agent == idx)

    # Return
    for _ in rows:
        result = True
        break
    return bool(result)


def exists(agent_id, agent_target):
    """Get the db Agent.idx_agent value for specific Agent.

    Args:
        agent_id: Agent ID
        agent_target: Agent polled target

    Returns:
        result: Agent.idx_agent value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20039) as session:
        rows = session.query(Agent.idx_agent).filter(and_(
            Agent.agent_id == agent_id.encode(),
            Agent.agent_polled_target == agent_target.encode(),
            ))

    # Return
    for row in rows:
        result = row.idx_agent
        break
    return result


def insert_row(agent_id, agent_target, agent_program, idx_agent_group=1):
    """Create the database Agent.agent value.

    Args:
        agent_id: Agent ID value (pattoo_agent_id)
        agent_target: Agent target (pattoo_agent_polled_target)
        agent_program: Agent program (pattoo_agent_program)
        idx_agent_group: AgentGroup table ForeignKey

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(agent_id, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20036, die=True) as session:
            session.add(Agent(agent_id=agent_id.encode(),
                              agent_polled_target=agent_target.encode(),
                              agent_program=agent_program.encode(),
                              idx_agent_group=idx_agent_group))


def unique_keys():
    """Get entire content of the table.

    Args:
        None

    Returns:
        result: List of NamedTuples

    """
    # Initialize key variables
    result = []
    rows = []

    # Get the result
    with db.db_query(20045) as session:
        rows = session.query(Agent.agent_polled_target, Agent.agent_id).filter(
            Agent.enabled == 1)

    # Process
    for row in rows:
        result.append(
            (row.agent_id.decode(), row.agent_polled_target.decode()))
    return result


def assign(idx_agent, idx_agent_group):
    """Assign an agent to an agent group.

    Args:
        idx_agent: Agent index
        idx_agent_group: Agent group index

    Returns:
        None

    """
    # Update
    with db.db_modify(20059, die=False) as session:
        session.query(Agent).filter(
            Agent.idx_agent == idx_agent).update(
                {'idx_agent_group': idx_agent_group}
            )


def cli_show_dump():
    """Get entire content of the table.

    Args:
        None

    Returns:
        result: List of NamedTuples

    """
    # Initialize key variables
    result = []

    # Get the result
    with db.db_query(20042) as session:
        rows = session.query(Agent)

    # Process
    for row in rows:
        Record = namedtuple(
            'Record', 'idx_agent agent_program agent_target agent_id enabled')
        result.append(
            Record(
                idx_agent=row.idx_agent,
                enabled=row.enabled,
                agent_program=row.agent_program.decode(),
                agent_target=row.agent_polled_target.decode(),
                agent_id=row.agent_id.decode()))
    return result
