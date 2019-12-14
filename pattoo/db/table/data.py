#!/usr/bin/env python3
"""Inserts various database values required during ingest."""

# Standard libraries
from operator import attrgetter

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.models import Data, DataPoint


def insert_rows(items):
    """Insert timeseries data.

    Args:
        items: List of IDXTimestampValue objects

    Returns:
        result: DataPoint.checksum value

    """
    # Initialize key variables
    _rows = []
    last_timestamps = {}
    polling_intervals = {}

    # Update the data
    for item in sorted(items, key=attrgetter('timestamp')):
        # Insert data
        value = round(item.value, 10)
        _rows.append(
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
        with db.db_modify(20047, die=False) as session:
            session.query(DataPoint).filter(
                and_(DataPoint.idx_datapoint == idx_datapoint,
                     DataPoint.enabled == 1)).update(
                         {'last_timestamp': timestamp,
                          'polling_interval': polling_intervals[idx_datapoint]}
                     )

    # Update after updating the last timestamp. Helps to prevent
    # 'Duplicate entry' errors in the event you need to re-run the ingester
    # after a previous crash.
    if bool(_rows) is True:
        with db.db_modify(20012, die=True) as session:
            session.add_all(_rows)
