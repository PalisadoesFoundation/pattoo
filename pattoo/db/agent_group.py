#!/usr/bin/env python3
"""Administer the AgentGroup database table."""

from collections import namedtuple

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import AgentGroup, Agent


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
    with db.db_query(20052) as session:
        rows = session.query(AgentGroup.idx_agent_group).filter(
            AgentGroup.idx_agent_group == idx)

    # Return
    for _ in rows:
        result = True
        break
    return result


def exists(description):
    """Determine whether description exists in the AgentGroup table.

    Args:
        description: Agent group description

    Returns:
        result: AgentGroup.idx_language value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20056) as session:
        rows = session.query(AgentGroup.idx_language).filter(
            AgentGroup.description == description.encode())

    # Return
    for row in rows:
        result = row.idx_language
        break
    return result


def insert_row(description):
    """Create the database AgentGroup row.

    Args:
        description: AgentGroup description

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(description, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20037, die=True) as session:
            session.add(
                AgentGroup(
                    description=description.encode()
                )
            )


def update_description(idx_agent_group, description):
    """Upadate a AgentGroup table entry.

    Args:
        idx_agent_group: AgentGroup idx_agent_group
        description: AgentGroup idx_agent_group description

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(description, str) is True:
        with db.db_modify(20010, die=False) as session:
            session.query(AgentGroup).filter(
                AgentGroup.idx_agent_group == idx_agent_group.encode()).update(
                    {'description': description.encode()}
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
    Record = namedtuple(
        'Record', 'idx_agent_group description idx_agent agent_id enabled')

    # Get the result
    with db.db_query(20050) as session:
        rows = session.query(AgentGroup)

    # Process
    for row in rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20055) as session:
            agent_rows = session.query(Agent.agent_id, Agent.idx_agent).filter(
                Agent.idx_agent_group == row.idx_agent_group)

        if agent_rows.count() >= 1:
            # Agents assigned to the group
            for agent_row in agent_rows:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=row.enabled,
                            idx_agent_group=row.idx_agent_group,
                            idx_agent=agent_row.idx_agent,
                            agent_id=agent_row.agent_id.decode(),
                            description=row.description.decode()
                        )
                    )
                    first_agent = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            idx_agent_group='',
                            idx_agent=agent_row.idx_agent,
                            agent_id=agent_row.agent_id.decode(),
                            description=''
                        )
                    )

        else:
            # Format only row for agent group
            result.append(
                Record(
                    enabled=row.enabled,
                    idx_agent_group=row.idx_agent_group,
                    idx_agent='',
                    agent_id='',
                    description=row.description.decode()
                )
            )

        # Add a spacer between agent groups
        result.append(Record(
            enabled='', idx_agent_group='', idx_agent='',
            agent_id='', description=''))

    return result
