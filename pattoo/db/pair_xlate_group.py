#!/usr/bin/env python3
"""Administer the PairXlateGroup database table."""

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import PairXlateGroup


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
    with db.db_query(20005) as session:
        rows = session.query(PairXlateGroup.idx_pair_xlate_group).filter(
            PairXlateGroup.idx_pair_xlate_group == idx)

    # Return
    for _ in rows:
        result = True
        break
    return result


def group_exists(name):
    """Get the db PairXlateGroup.idx_pair_xlate_group value for specific agent.

    Args:
        name: PairXlateGroup name

    Returns:
        result: PairXlateGroup.idx_pair_xlate_group value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(PairXlateGroup.idx_pair_xlate_group).filter(
            PairXlateGroup.name == name.encode())

    # Return
    for row in rows:
        result = row.idx_pair_xlate_group
        break
    return result


def insert_row(name, description):
    """Create the database PairXlateGroup.agent value.

    Args:
        name: PairXlateGroup name
        description: PairXlateGroup description

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(name, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20001, die=True) as session:
            session.add(PairXlateGroup(name=name.encode(),
                                       description=description.encode()))
