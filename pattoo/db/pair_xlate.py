#!/usr/bin/env python3
"""Administer the PairXlate database table."""

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import PairXlate


def pair_xlate_exists(name):
    """Get the db PairXlate.idx_pair_xlate value for specific agent.

    Args:
        name: PairXlate name

    Returns:
        result: PairXlate.idx_pair_xlate value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(PairXlate.idx_pair_xlate).filter(
            PairXlate.name == name.encode())

    # Return
    for row in rows:
        result = row.idx_pair_xlate
        break
    return result


def insert_row(name, description, idx_language, idx_pair_xlate_group):
    """Create the database PairXlate.agent value.

    Args:
        name: PairXlate name
        description: PairXlate description
        idx_language: Language table index
        idx_pair_xlate_group: PairXlateGroup table index

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(name, str) is True:
        # Insert and get the new agent value
        with db.db_modify(20001, die=True) as session:
            session.add(
                PairXlate(
                    name=name.encode(),
                    description=description.encode(),
                    idx_language=idx_language,
                    idx_pair_xlate_group=idx_pair_xlate_group
                )
            )
