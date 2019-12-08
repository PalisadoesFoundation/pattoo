#!/usr/bin/env python3
"""Queries various database tables for ingest related data."""

# PIP libraries
from sqlalchemy import and_, tuple_

# Import project libraries
from pattoo.constants import ChecksumLookup
from pattoo.db import db
from pattoo.db.tables import DataPoint, Glue, Pair


def idx_datapoints(_checksums):
    """Get all the checksum values for a specific source.

    Args:
        _checksums: List of checksum values

    Returns:
        result: List of DataPoint.idx_datapoint values

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
            DataPoint.idx_datapoint).filter(
                DataPoint.checksum.in_(_checksums))

    # Return
    for row in rows:
        result.append(row.idx_datapoint)
    return sorted(result)


def checksums(source):
    """Get all the checksum values for a specific source.

    Args:
        source: PattooDBrecord object source

    Returns:
        result: Dict of idx_datapoint values keyed by DataPoint.checksum

    """
    # Result
    result = {}
    rows = []

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            DataPoint.checksum,
            DataPoint.last_timestamp,
            DataPoint.polling_interval,
            DataPoint.idx_datapoint).filter(and_(
                Glue.idx_datapoint == DataPoint.idx_datapoint,
                Glue.idx_pair == Pair.idx_pair,
                Pair.key == 'pattoo_agent_id'.encode(),
                Pair.value == source.encode()
            ))

    # Return
    for row in rows:
        result[row.checksum.decode()] = ChecksumLookup(
            idx_datapoint=row.idx_datapoint,
            polling_interval=row.polling_interval,
            last_timestamp=row.last_timestamp)
    return result


def glue(_idx_datapoints):
    """Get all the checksum values for a specific source.

    Args:
        _idx_datapoints: List idx_datapoint values

    Returns:
        result: Dict of idx_datapoint values keyed by DataPoint.checksum

    """
    # Initialize key variables
    result = []
    rows = []

    # Create a list if it doesn't exist
    if isinstance(_idx_datapoints, list) is False:
        _idx_datapoints = [_idx_datapoints]

    # Get the data from the database
    with db.db_query(20014) as session:
        rows = session.query(
            Glue.idx_pair).filter(Glue.idx_datapoint.in_(_idx_datapoints))

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
