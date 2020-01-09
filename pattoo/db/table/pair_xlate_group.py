#!/usr/bin/env python3
"""Administer the PairXlateGroup database table."""

from collections import namedtuple

# PIP3 imports
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.models import (
    PairXlateGroup, PairXlate, Language, AgentGroup, Agent)


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_pair_xlate_group

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False

    # Get the result
    with db.db_query(20064) as session:
        rows = session.query(PairXlateGroup.idx_pair_xlate_group).filter(
            PairXlateGroup.idx_pair_xlate_group == idx)

    # Return
    for _ in rows:
        result = True
        break
    return result


def exists(description):
    """Determine whether description exists in the PairXlateGroup table.

    Args:
        description: PairXlate group description

    Returns:
        result: PairXlateGroup.idx_pair_xlate_group value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20066) as session:
        rows = session.query(PairXlateGroup.idx_pair_xlate_group).filter(
            PairXlateGroup.description == description.strip().encode())

    # Return
    for row in rows:
        result = row.idx_pair_xlate_group
        break
    return result


def insert_row(description):
    """Create the database PairXlateGroup row.

    Args:
        description: PairXlateGroup description

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(description, str) is True:
        # Insert and get the new pair_xlate value
        with db.db_modify(20063, die=True) as session:
            session.add(
                PairXlateGroup(
                    description=description.strip().encode()
                )
            )


def update_description(idx, description):
    """Upadate a PairXlateGroup table entry.

    Args:
        idx: PairXlateGroup idx_pair_xlate_group
        description: PairXlateGroup idx_pair_xlate_group description

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(description, str) is True:
        with db.db_modify(20065, die=False) as session:
            session.query(PairXlateGroup).filter(
                PairXlateGroup.idx_pair_xlate_group == int(idx)).update(
                    {'description': description.strip().encode()}
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
        '''idx_pair_xlate_group translation_group_description idx_agent_group \
agent_group_description enabled''')

    # Get the result
    with db.db_query(20062) as session:
        x_rows = session.query(PairXlateGroup)

    # Process
    for x_row in x_rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20061) as session:
            a_rows = session.query(
                AgentGroup.description,
                AgentGroup.idx_agent_group).filter(
                    AgentGroup.idx_pair_xlate_group == x_row.idx_pair_xlate_group)

        if a_rows.count() >= 1:
            # Agents assigned to the group
            for a_row in a_rows:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=x_row.enabled,
                            idx_pair_xlate_group=x_row.idx_pair_xlate_group,
                            idx_agent_group=a_row.idx_agent_group,
                            agent_group_description=a_row.description.decode(),
                            translation_group_description=x_row.description.decode()
                        )
                    )
                    first_agent = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            idx_pair_xlate_group='',
                            translation_group_description='',
                            idx_agent_group=a_row.idx_agent_group,
                            agent_group_description=a_row.description.decode()
                        )
                    )

        else:
            # Format only row for agent group
            result.append(
                Record(
                    enabled=x_row.enabled,
                    idx_pair_xlate_group=x_row.idx_pair_xlate_group,
                    translation_group_description=x_row.description.decode(),
                    idx_agent_group='',
                    agent_group_description=''
                )
            )

        # Add a spacer between agent groups
        result.append(Record(
            enabled='',
            idx_pair_xlate_group='',
            idx_agent_group='',
            agent_group_description='',
            translation_group_description=''))

    return result
