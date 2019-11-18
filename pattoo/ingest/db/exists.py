#!/usr/bin/env python3
"""Verifies the existence of various database data required for ingest."""

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Pair, Checksum, Glue


def idx_checksum(checksum):
    """Get the db Checksum.idx_checksum value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: Checksum.idx_checksum value

    """
    # Initialize key variables
    result = False

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(Checksum.idx_checksum).filter(
            Checksum.checksum == checksum.encode())

    # Return
    for row in rows:
        result = row.idx_checksum
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
    for _ in rows:
        result = True
        break
    return result


def glue(_idx_checksum, idx_pair):
    """Determine existence of idx_checksum, idx_pair in the Glue db table.

    Args:
        _idx_checksum: Checksum.idx_checksum table index
        idx_pair: Pair.idx_pair table index

    Returns:
        result: True if it exists

    """
    # Initialize idx_checksum variables
    result = False
    rows = []

    # Ignore certain restricted idx_checksums
    with db.db_query(20008) as session:
        rows = session.query(Glue.idx_pair).filter(and_(
            Glue.idx_checksum == _idx_checksum,
            Glue.idx_pair == idx_pair,
            Pair.idx_pair == Glue.idx_pair,
            Checksum.idx_checksum == Glue.idx_checksum
            ))

    # Return
    for _ in rows:
        result = True
        break
    return result
