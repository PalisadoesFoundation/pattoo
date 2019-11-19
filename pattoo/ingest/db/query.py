#!/usr/bin/env python3
"""Queries various database tables for ingest related data."""

# PIP libraries
from sqlalchemy import and_, tuple_

# Import project libraries
from pattoo.constants import ChecksumLookup
from pattoo.db import db
from pattoo.db.tables import Checksum, Glue, Pair


def idx_checksums(_checksums):
    """Get all the checksum values for a specific data_source.

    Args:
        _checksums: List of checksum values

    Returns:
        result: List of Checksum.idx_checksum values

    """
    # Initialize key variables
    result = []

    # Encode the checksums for database lookups
    if isinstance(_checksums, list) is False:
        _checksums = [_checksums]
    _checksums = [item.encode() for item in _checksums]

    # Get the data from the database
    with db.db_query(20003) as session:
        rows = session.query(
            Checksum.idx_checksum).filter(
                Checksum.checksum.in_(_checksums))

    # Return
    for row in rows:
        result.append(row.idx_checksum)
    return sorted(result)


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
                Pair.key == 'data_source'.encode(),
                Pair.value == data_source.encode()
            ))

    # Return
    for row in rows:
        result[row.checksum] = ChecksumLookup(
            idx_checksum=row.idx_checksum,
            last_timestamp=row.last_timestamp)
    return result


def glue(_idx_checksums):
    """Get all the checksum values for a specific data_source.

    Args:
        _idx_checksums: List idx_checksum values

    Returns:
        result: Dict of idx_checksum values keyed by Checksum.checksum

    """
    # Initialize key variables
    result = []
    rows = []

    # Create a list if it doesn't exist
    if isinstance(_idx_checksums, list) is False:
        _idx_checksums = [_idx_checksums]

    # Get the data from the database
    with db.db_query(20014) as session:
        rows = session.query(
            Glue.idx_pair).filter(Glue.idx_checksum.in_(_idx_checksums))

    # Return
    for row in rows:
        result.append(row.idx_pair)
    return sorted(result)


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
    return sorted(result)
