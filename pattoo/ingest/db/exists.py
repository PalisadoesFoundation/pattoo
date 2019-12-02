#!/usr/bin/env python3
"""Verifies the existence of various database data required for ingest."""

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Pair, DataPoint, Glue


def checksum(_checksum):
    """Get the db DataPoint.idx_datapoint value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: DataPoint.idx_datapoint value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(DataPoint.idx_datapoint).filter(
            DataPoint.checksum == _checksum.encode())

    # Return
    for row in rows:
        result = row.idx_datapoint
        break
    return result


def pair(key, value):
    """Get the db Pair table for key-value pair.

    Args:
        key: Key-value pair key
        value: Key-value pair value

    Returns:
        result: Pair.idx_pair value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20006) as session:
        rows = session.query(Pair.idx_pair).filter(and_(
            Pair.key == key.encode(),
            Pair.value == value.encode()
            ))

    # Return
    for row in rows:
        result = row.idx_pair
        break
    return result


def glue(_idx_datapoint, idx_pair):
    """Determine existence of idx_datapoint, idx_pair in the Glue db table.

    Args:
        _idx_datapoint: DataPoint.idx_datapoint table index
        idx_pair: Pair.idx_pair table index

    Returns:
        result: True if it exists

    """
    # Initialize idx_datapoint variables
    result = False
    rows = []

    # Ignore certain restricted idx_datapoints
    with db.db_query(20008) as session:
        rows = session.query(Glue.idx_pair).filter(and_(
            Glue.idx_datapoint == _idx_datapoint,
            Glue.idx_pair == idx_pair,
            Pair.idx_pair == Glue.idx_pair,
            DataPoint.idx_datapoint == Glue.idx_datapoint
            ))

    # Return
    for _ in rows:
        result = True
        break
    return result
