#!/usr/bin/env python3
"""Inserts various database values required during ingest."""

# Standard libraries
from operator import attrgetter

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Checksum, Pair, Glue, Data
from pattoo.ingest.db import exists


def timeseries(items):
    """Insert timeseries data.

    Args:
        items: List of IDXTimestampValue objects

    Returns:
        result: Checksum.checksum value

    """
    # Initialize key variables
    rows = []
    last_timestamps = {}

    # Update the data
    for item in sorted(items, key=attrgetter('timestamp')):
        # Insert data
        value = round(item.value, 10)
        rows.append(
            Data(idx_checksum=item.idx_checksum,
                 timestamp=item.timestamp,
                 value=value)
        )

        # Get the most recent timestamp for each idx_checksum
        if item.idx_checksum in last_timestamps:
            last_timestamps[item.idx_checksum] = max(
                item.timestamp, last_timestamps[item.idx_checksum])
        else:
            last_timestamps[item.idx_checksum] = item.timestamp

    # Update
    if bool(rows) is True:
        with db.db_modify(20012, die=True) as session:
            session.add_all(rows)

    # Update the last_timestamp
    for idx_checksum, timestamp in last_timestamps.items():
        with db.db_modify(20010, die=False) as session:
            # Update the last_timestamp
            session.query(Checksum).filter(
                and_(Checksum.idx_checksum == idx_checksum,
                     Checksum.enabled == 1)).update(
                         {'last_timestamp': timestamp})


def checksum(_checksum, data_type):
    """Create the database Checksum.checksum value.

    Args:
        _checksum: Checksum value
        data_type: Type of data

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(_checksum, str) is True:
        # Insert and get the new checksum value
        row = Checksum(checksum=_checksum.encode(), data_type=data_type)
        with db.db_modify(20001, die=True) as session:
            session.add(row)


def pairs(items):
    """Create db Pair table entries.

    Args:
        items: List of lists, or list of key-value pairs

    Returns:
        None

    """
    # Initialize key variables
    rows = []
    uniques = {}
    all_kvs = []

    # Create a single list of key-value pairs.
    # Add them to a dict to make the pairs unique.
    for item in items:
        if isinstance(item, list):
            all_kvs.extend(item)
        else:
            all_kvs.append(item)
    for _kv in all_kvs:
        uniques[_kv] = None

    # Insert the key-value pairs into the database
    for (key, value), _ in uniques.items():
        # Skip non-metadata pre-existing pairs
        if exists.pair(key, value) is True:
            continue

        # Insert and get the new idx_datasource value
        row = Pair(key=key.encode(), value=value.encode())
        rows.append(row)

    if bool(rows) is True:
        with db.db_modify(20007, die=True) as session:
            session.add_all(rows)


def glue(idx_checksum, idx_pairs):
    """Create db Pair table entries.

    Args:
        idx_checksum: Checksum.idx_checksum
        idx_pairs: List of Pair.idx_pair values

    Returns:
        None

    """
    # Initialize key variables
    rows = []

    # Iterate over NamedTuple
    for idx_pair in idx_pairs:
        pair_exists = exists.glue(idx_checksum, idx_pair)
        if bool(pair_exists) is False:
            # Insert and get the new idx_datasource value
            row = Glue(idx_pair=idx_pair, idx_checksum=idx_checksum)
            rows.append(row)

    if bool(rows) is True:
        with db.db_modify(20002, die=True) as session:
            session.add_all(rows)
