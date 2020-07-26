#!/usr/bin/env python3
"""Administer the PairXlateGroup database table."""

from collections import namedtuple

# Import project libraries
from pattoo.db import db
from pattoo.db.models import PairXlateGroup, Agent


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


def exists(name):
    """Determine whether name exists in the PairXlateGroup table.

    Args:
        name: PairXlate group name

    Returns:
        result: PairXlateGroup.idx_pair_xlate_group value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20066) as session:
        rows = session.query(PairXlateGroup.idx_pair_xlate_group).filter(
            PairXlateGroup.name == name.strip().encode())

    # Return
    for row in rows:
        result = row.idx_pair_xlate_group
        break
    return result


def insert_row(name):
    """Create the database PairXlateGroup row.

    Args:
        name: PairXlateGroup name

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(name, str) is True:
        # Insert and get the new pair_xlate value
        with db.db_modify(20063, die=True) as session:
            session.add(
                PairXlateGroup(
                    name=name.strip().encode()
                )
            )


def update_name(idx, name):
    """Upadate a PairXlateGroup table entry.

    Args:
        idx: PairXlateGroup idx_pair_xlate_group
        name: PairXlateGroup idx_pair_xlate_group name

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(name, str) is True:
        with db.db_modify(20065, die=False) as session:
            session.query(PairXlateGroup).filter(
                PairXlateGroup.idx_pair_xlate_group == int(idx)).update(
                    {'name': name.strip().encode()}
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
        '''idx_pair_xlate_group translation_group_name \
agent_program agent_polled_target enabled''')

    # Get the result
    with db.db_query(20062) as session:
        x_rows = session.query(PairXlateGroup)

    # Process
    for x_row in x_rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20061) as session:
            a_rows = session.query(
                Agent.agent_program,
                Agent.agent_polled_target.label('apt')).filter(
                    Agent.idx_pair_xlate_group == x_row.idx_pair_xlate_group)

        if a_rows.count() >= 1:
            # Agents assigned to the group
            for a_row in a_rows:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=x_row.enabled,
                            idx_pair_xlate_group=x_row.idx_pair_xlate_group,
                            agent_program=a_row.agent_program.decode(),
                            agent_polled_target=a_row.apt.decode(),
                            translation_group_name=x_row.name.decode()
                        )
                    )
                    first_agent = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            idx_pair_xlate_group='',
                            translation_group_name='',
                            agent_polled_target=a_row.apt.decode(),
                            agent_program=a_row.agent_program.decode()
                        )
                    )

        else:
            # Format only row for agent group
            result.append(
                Record(
                    enabled=x_row.enabled,
                    idx_pair_xlate_group=x_row.idx_pair_xlate_group,
                    translation_group_name=x_row.name.decode(),
                    agent_polled_target='',
                    agent_program=''
                )
            )

        # Add a spacer between agent groups
        result.append(Record(
            enabled='',
            idx_pair_xlate_group='',
            agent_polled_target='',
            agent_program='',
            translation_group_name=''))

    return result
