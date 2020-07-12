#!/usr/bin/env python3
"""Pattoo classes querying the Favorite table."""

# PIP3 imports
from sqlalchemy import and_

# Import project libraries
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.models import Favorite
from pattoo.constants import DbRowFavorite


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_favorite

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20046) as session:
        rows = session.query(Favorite.idx_favorite).filter(
            Favorite.idx_favorite == idx)

    # Return
    for _ in rows:
        result = True
        break
    return bool(result)


def exists(idx_chart, idx_user):
    """Determine whether name exists in the Favorite table.

    Args:
        idx_chart: Chart table index
        idx_user: User table index

    Returns:
        result: Favorite.idx_favorite value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get name from database
    with db.db_query(20031) as session:
        rows = session.query(Favorite.idx_favorite).filter(
            and_(Favorite.idx_chart == idx_chart,
                 Favorite.idx_user == idx_user))

    # Return
    for row in rows:
        result = row.idx_favorite
        break
    return result


def insert_row(row):
    """Create a Favorite table entry.

    Args:
        row: DbRowFavorite object

    Returns:
        None

    """
    # Verify values
    if bool(row) is False or isinstance(row, DbRowFavorite) is False:
        log_message = 'Invalid favorite type being inserted'
        log.log2die(20033, log_message)

    # Insert
    row = Favorite(
        idx_chart=row.idx_chart,
        idx_user=row.idx_user,
        order=row.order,
        enabled=int(bool(row.enabled)),
        )
    with db.db_modify(20032, die=True) as session:
        session.add(row)
