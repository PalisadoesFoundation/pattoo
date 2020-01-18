#!/usr/bin/env python3
"""Administer the AgentGroup database table."""

from collections import namedtuple

# Import project libraries
from pattoo.db import db
from pattoo.db.models import AgentGroup, Agent


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
            AgentGroup.idx_agent_group == int(idx))

    # Return
    for _ in rows:
        result = True
        break
    return result


def exists(name):
    """Determine whether name exists in the AgentGroup table.

    Args:
        name: Agent group name

    Returns:
        result: AgentGroup.idx_agent_group value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20056) as session:
        rows = session.query(AgentGroup.idx_agent_group).filter(
            AgentGroup.name == name.encode())

    # Return
    for row in rows:
        result = row.idx_agent_group
        break
    return result


def insert_row(name):
    """Create the database AgentGroup row.

    Args:
        name: AgentGroup name

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(name, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20037, die=True) as session:
            session.add(
                AgentGroup(
                    name=name.encode()
                )
            )


def update_name(idx_agent_group, name):
    """Upadate a AgentGroup table entry.

    Args:
        idx_agent_group: AgentGroup idx_agent_group
        name: AgentGroup idx_agent_group name

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(name, str) is True:
        with db.db_modify(20010, die=False) as session:
            session.query(AgentGroup).filter(
                AgentGroup.idx_agent_group == idx_agent_group).update(
                    {'name': name.encode()}
                )


def assign(idx_agent_group, idx_pair_xlate_group):
    """Assign an agent_group to an key-pair translation group.

    Args:
        idx_agent_group: AgentGroup table index
        idx_pair_xlate_group: PairXlateGroup table index

    Returns:
        None

    """
    # Update
    with db.db_modify(20070, die=False) as session:
        session.query(AgentGroup).filter(
            AgentGroup.idx_agent_group == idx_agent_group).update(
                {'idx_pair_xlate_group': idx_pair_xlate_group}
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
        'Record',
        '''idx_agent_group name idx_agent \
agent_program agent_target enabled''')

    # Get the result
    with db.db_query(20050) as session:
        rows = session.query(AgentGroup)

    # Process
    for row in rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20055) as session:
            a_rows = session.query(
                Agent.agent_program,
                Agent.agent_polled_target,
                Agent.idx_agent).filter(
                    Agent.idx_agent_group == row.idx_agent_group)

        if a_rows.count() >= 1:
            # Agents assigned to the group
            for a_row in a_rows:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=row.enabled,
                            idx_agent_group=row.idx_agent_group,
                            idx_agent=a_row.idx_agent,
                            agent_program=a_row.agent_program.decode(),
                            agent_target=a_row.agent_polled_target.decode(),
                            name=row.name.decode()
                        )
                    )
                    first_agent = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            idx_agent_group='',
                            name='',
                            idx_agent=a_row.idx_agent,
                            agent_program=a_row.agent_program.decode(),
                            agent_target=a_row.agent_polled_target.decode()
                        )
                    )

        else:
            # Format only row for agent group
            result.append(
                Record(
                    enabled=row.enabled,
                    idx_agent_group=row.idx_agent_group,
                    name=row.name.decode(),
                    idx_agent='',
                    agent_program='',
                    agent_target=''
                )
            )

        # Add a spacer between agent groups
        result.append(Record(
            enabled='',
            idx_agent_group='',
            idx_agent='',
            agent_program='',
            agent_target='',
            name=''))

    return result
