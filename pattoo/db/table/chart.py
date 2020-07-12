#!/usr/bin/env python3
"""Pattoo classes querying the Chart table."""

# Import project libraries
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.models import Chart
from pattoo.constants import DbRowChart


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_chart

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20046) as session:
        rows = session.query(Chart.idx_chart).filter(
            Chart.idx_chart == idx)

    # Return
    for _ in rows:
        result = True
        break
    return bool(result)


def exists(checksum):
    """Determine whether checksum exists in the Chart table.

    Args:
        checksum: chart checksum

    Returns:
        result: Chart.idx_chart value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get checksum from database
    with db.db_query(20031) as session:
        rows = session.query(Chart.idx_chart).filter(
            Chart.checksum == checksum.encode())

    # Return
    for row in rows:
        result = row.idx_chart
        break
    return result


def insert_row(row):
    """Create a User table entry.

    Args:
        row: DbRowChart object

    Returns:
        None

    """
    # Verify values
    if bool(row) is False or isinstance(row, DbRowChart) is False:
        log_message = 'Invalid user type being inserted'
        log.log2die(20033, log_message)

    # Lowercase the name
    name = row.name.strip()[:MAX_KEYPAIR_LENGTH]
    checksum = row.checksum.strip()[:MAX_KEYPAIR_LENGTH]
    enabled = int(bool(row.enabled))

    # Insert
    row = Chart(
        name=name.encode(),
        checksum=checksum.encode(),
        enabled=enabled,
        )
    with db.db_modify(20032, die=True) as session:
        session.add(row)
