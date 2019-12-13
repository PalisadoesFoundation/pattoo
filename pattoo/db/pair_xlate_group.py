#!/usr/bin/env python3
"""Administer the PairXlateGroup database table."""

from collections import namedtuple

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import PairXlateGroup, PairXlate


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
        result: PairXlateGroup.idx_language value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20066) as session:
        rows = session.query(PairXlateGroup.idx_language).filter(
            PairXlateGroup.description == description.strip().encode())

    # Return
    for row in rows:
        result = row.idx_language
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
                PairXlateGroup.idx_pair_xlate_group == idx.encode()).update(
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
        'idx_pair_xlate_group description idx_pair_xlate key translation enabled')

    # Get the result
    with db.db_query(20062) as session:
        rows = session.query(PairXlateGroup)

    # Process
    for row in rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20061) as session:
            line_items = session.query(
                PairXlate.key,
                PairXlate.description).filter(
                    PairXlate.idx_pair_xlate_group == row.idx_pair_xlate_group)

        if line_items.count() >= 1:
            # PairXlates assigned to the group
            for line_item in line_items:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=row.enabled,
                            idx_pair_xlate_group=row.idx_pair_xlate_group,
                            idx_pair_xlate=line_item.idx_pair_xlate,
                            key=line_item.key.decode(),
                            translation=line_item.description.decode(),
                            description=row.description.decode()
                        )
                    )
                    first_agent = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            idx_pair_xlate_group='',
                            idx_pair_xlate=line_item.idx_pair_xlate,
                            key=line_item.key.decode(),
                            translation=line_item.description.decode(),
                            description=''
                        )
                    )

        else:
            # Format only row for agent group
            result.append(
                Record(
                    enabled=row.enabled,
                    idx_pair_xlate_group=row.idx_pair_xlate_group,
                    idx_pair_xlate='',
                    key='',
                    translation='',
                    description=row.description.decode()
                )
            )

        # Add a spacer between agent groups
        result.append(Record(
            enabled='', idx_pair_xlate_group='', idx_pair_xlate='',
            key='', description='', translation=''))

    return result
