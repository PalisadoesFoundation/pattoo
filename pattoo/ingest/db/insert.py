#!/usr/bin/env python3
"""Inserts various database values required during ingest."""

# Standard libraries
from operator import attrgetter

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import DataPoint, Pair, Glue, Data
from pattoo.ingest.db import exists


def timeseries(items):
    """Insert timeseries data.

    Args:
        items: List of IDXTimestampValue objects

    Returns:
        result: DataPoint.checksum value

    """
    # Initialize key variables
    rows = []
    last_timestamps = {}
    polling_intervals = {}

    # Update the data
    for item in sorted(items, key=attrgetter('timestamp')):
        # Insert data
        value = round(item.value, 10)
        rows.append(
            Data(idx_datapoint=item.idx_datapoint,
                 timestamp=item.timestamp,
                 value=value)
        )

        # Get the most recent timestamp for each idx_datapoint
        if item.idx_datapoint in last_timestamps:
            last_timestamps[item.idx_datapoint] = max(
                item.timestamp, last_timestamps[item.idx_datapoint])
        else:
            last_timestamps[item.idx_datapoint] = item.timestamp
        polling_intervals[item.idx_datapoint] = item.polling_interval

    # Update the last_timestamp
    for idx_datapoint, timestamp in last_timestamps.items():
        with db.db_modify(20010, die=False) as session:
            session.query(DataPoint).filter(
                and_(DataPoint.idx_datapoint == idx_datapoint,
                     DataPoint.enabled == 1)).update(
                         {'last_timestamp': timestamp,
                          'polling_interval': polling_intervals[idx_datapoint]}
                     )

    # Update after updating the last timestamp. Helps to prevent
    # 'Duplicate entry' errors in the event you need to re-run the ingester
    # after a previous crash.
    if bool(rows) is True:
        with db.db_modify(20012, die=True) as session:
            session.add_all(rows)


def checksum(_checksum, data_type, polling_interval):
    """Create the database DataPoint.checksum value.

    Args:
        _checksum: DataPoint value
        data_type: Type of data
        polling_interval: Polling interval

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(_checksum, str) is True:
        # Insert and get the new checksum value
        row = DataPoint(
            checksum=_checksum.encode(),
            polling_interval=polling_interval,
            data_type=data_type)
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

    # Make list if not so
    if isinstance(items, list) is False:
        items = [items]

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
        # Skip pre-existing pairs
        if bool(exists.pair(key, value)) is True:
            continue

        # Add values to list for future insertion
        row = Pair(key=key.encode(), value=value.encode())
        rows.append(row)

    if bool(rows) is True:
        with db.db_modify(20007, die=True) as session:
            session.add_all(rows)


def glue(idx_datapoint, idx_pairs):
    """Create db Pair table entries.

    Args:
        idx_datapoint: DataPoint.idx_datapoint
        idx_pairs: List of Pair.idx_pair values

    Returns:
        None

    """
    # Initialize key variables
    rows = []

    # Create a list for processing if not available
    if isinstance(idx_pairs, list) is False:
        idx_pairs = [idx_pairs]

    # Iterate over idx_pairs
    for idx_pair in idx_pairs:
        pair_exists = exists.glue(idx_datapoint, idx_pair)
        if bool(pair_exists) is False:
            # Insert and get the new idx_datasource value
            row = Glue(idx_pair=idx_pair, idx_datapoint=idx_datapoint)
            rows.append(row)

    if bool(rows) is True:
        with db.db_modify(20002, die=True) as session:
            session.add_all(rows)
