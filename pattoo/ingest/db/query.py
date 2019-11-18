#!/usr/bin/env python3
"""Queries various database tables for ingest related data."""

# PIP libraries
from sqlalchemy import and_, tuple_

# Import project libraries
from pattoo.constants import ChecksumLookup
from pattoo.db import db
from pattoo.db.tables import Checksum, Glue, Pair


def checksums(data_source):
    """Get all the checksum values for a specific data_source.

    Args:
        data_source: PattooDBrecord object data_source

    Returns:
        result: Dict of idx_checksum values keyed by Checksum.checksum

    """
    # Result
    result = {}
    rows = []

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            Checksum.checksum,
            Checksum.last_timestamp,
            Checksum.idx_checksum).filter(and_(
                Glue.idx_checksum == Checksum.idx_checksum,
                Glue.idx_pair == Pair.idx_pair,
                Pair.key == data_source.encode()
            ))

    # Return
    for row in rows:
        result[row.checksum] = ChecksumLookup(
            idx_checksum=row.idx_checksum,
            last_timestamp=row.last_timestamp)
    return result


def glue(idx_checksums):
    """Get all the checksum values for a specific data_source.

    Args:
        checksums: List idx_checksum values

    Returns:
        result: Dict of idx_checksum values keyed by Checksum.checksum

    """
    # Initialize key variables
    result = []

    # Get the data from the database
    with db.db_query(20011) as session:
        rows = session.query(
            Glue.idx_pair).filter(Glue.idx_checksum.in_(idx_checksums))

    # Return
    for row in rows:
        result.append(row.idx_pair)
    return result


def pairs(_items):
    """Get the db Pair table indices based on key, value pairs.

    Args:
        _items: List of (key, value) tuples

    Returns:
        result: list of Pair.idx_pair values

    """
    # Initialize key variables
    result = []

    # Encode the items
    items = [(key.encode(), value.encode()) for key, value in _items]

    # Get the data from the database
    with db.db_query(20011) as session:
        rows = session.query(
            Pair.idx_pair).filter(tuple_(Pair.key, Pair.value).in_(items))

    # Return
    for row in rows:
        result.append(row.idx_pair)
    return result
