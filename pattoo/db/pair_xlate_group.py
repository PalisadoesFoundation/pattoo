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
    with db.db_query(20052) as session:
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
    with db.db_query(20056) as session:
        rows = session.query(PairXlateGroup.idx_language).filter(
            PairXlateGroup.description == description.encode())

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
        with db.db_modify(20037, die=True) as session:
            session.add(
                PairXlateGroup(
                    description=description.encode()
                )
            )


def update_description(idx_pair_xlate_group, description):
    """Upadate a PairXlateGroup table entry.

    Args:
        idx_pair_xlate_group: PairXlateGroup idx_pair_xlate_group
        description: PairXlateGroup idx_pair_xlate_group description

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(description, str) is True:
        with db.db_modify(20010, die=False) as session:
            session.query(PairXlateGroup).filter(
                PairXlateGroup.idx_pair_xlate_group == idx_pair_xlate_group.encode()).update(
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
        'Record', 'idx_pair_xlate_group description idx_pair_xlate pair_xlate_id enabled')

    # Get the result
    with db.db_query(20050) as session:
        rows = session.query(PairXlateGroup)

    # Process
    for row in rows:
        first_pair_xlate = True

        # Get pair_xlates for group
        with db.db_query(20055) as session:
            pair_xlate_rows = session.query(PairXlate.pair_xlate_id, PairXlate.idx_pair_xlate).filter(
                PairXlate.idx_pair_xlate_group == row.idx_pair_xlate_group)

        if pair_xlate_rows.count() >= 1:
            # PairXlates assigned to the group
            for pair_xlate_row in pair_xlate_rows:
                if first_pair_xlate is True:
                    # Format first row for pair_xlate group
                    result.append(
                        Record(
                            enabled=row.enabled,
                            idx_pair_xlate_group=row.idx_pair_xlate_group,
                            idx_pair_xlate=pair_xlate_row.idx_pair_xlate,
                            pair_xlate_id=pair_xlate_row.pair_xlate_id.decode(),
                            description=row.description.decode()
                        )
                    )
                    first_pair_xlate = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            idx_pair_xlate_group='',
                            idx_pair_xlate=pair_xlate_row.idx_pair_xlate,
                            pair_xlate_id=pair_xlate_row.pair_xlate_id.decode(),
                            description=''
                        )
                    )

        else:
            # Format only row for pair_xlate group
            result.append(
                Record(
                    enabled=row.enabled,
                    idx_pair_xlate_group=row.idx_pair_xlate_group,
                    idx_pair_xlate='',
                    pair_xlate_id='',
                    description=row.description.decode()
                )
            )

        # Add a spacer between pair_xlate groups
        result.append(Record(
            enabled='', idx_pair_xlate_group='', idx_pair_xlate='',
            pair_xlate_id='', description=''))

    return result
