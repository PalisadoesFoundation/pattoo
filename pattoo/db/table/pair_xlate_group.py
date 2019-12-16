#!/usr/bin/env python3
"""Administer the PairXlateGroup database table."""

from collections import namedtuple

# PIP3 imports
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.models import PairXlateGroup, PairXlate, Language


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


def cli_show_dump(idx=None):
    """Get entire content of the table.

    Args:
        idx: idx_pair_xlate_group to filter on

    Returns:
        result: List of NamedTuples

    """
    # Initialize key variables
    result = []
    rows = []
    Record = namedtuple(
        'Record',
        '''idx_pair_xlate_group description language key translation \
enabled''')

    # Get the result
    if bool(idx) is False:
        with db.db_query(20071) as session:
            rows = session.query(PairXlateGroup)
    else:
        with db.db_query(20062) as session:
            rows = session.query(PairXlateGroup).filter(
                PairXlateGroup.idx_pair_xlate_group == idx)

    # Process
    for row in rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20061) as session:
            line_items = session.query(
                Language.code,
                PairXlate.key,
                PairXlate.description).filter(and_(
                    PairXlate.idx_pair_xlate_group == row.idx_pair_xlate_group,
                    PairXlate.idx_language == Language.idx_language
                    ))

        if line_items.count() >= 1:
            # PairXlates assigned to the group
            for line_item in line_items:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=row.enabled,
                            idx_pair_xlate_group=row.idx_pair_xlate_group,
                            language=line_item.code.decode(),
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
                            language=line_item.code.decode(),
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
                    language='',
                    key='',
                    translation='',
                    description=row.description.decode()
                )
            )

        # Add a spacer between agent groups
        result.append(Record(
            enabled='', idx_pair_xlate_group='', language='',
            key='', description='', translation=''))

    return result
