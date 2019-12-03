#!/usr/bin/env python3
"""Pattoo agent data cache ingester.

Used to add data to backend database

"""

# Standard libraries
import sys
import os
from pprint import pprint
from copy import deepcopy

# PIP imports
import numpy as np

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _BIN_DIRECTORY.endswith('/pattoo/bin') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Pattoo libraries
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

# pattoo imports
from pattoo_shared.constants import (
    DATA_INT, DATA_FLOAT, DATA_COUNT64, DATA_COUNT)
from pattoo import data
from pattoo import uri
from pattoo.db import db
from pattoo.db.tables import Data, DataPoint
from pattoo_shared import times


def main():
    """Ingest data."""
    # Initialize key variables
    idx_datapoint = 3
    found = False
    (ts_start, ts_stop) = uri.chart_timestamp_args()

    try:
        # Deal with that as well
        with db.db_query(20128) as session:
            metadata = session.query(
                DataPoint.data_type, DataPoint.polling_interval).filter(
                    DataPoint.idx_datapoint == idx_datapoint).one()
            found = True
    except MultipleResultsFound as _:
        pass
    except NoResultFound as _:
        pass

    # Get the _result
    if found is True:
        _query(idx_datapoint, ts_start, ts_stop, metadata)


def _query(idx_datapoint, ts_start, ts_stop, metadata):
    """Create list of dicts of counter values retrieved from database.

    Args:
        nones: Dict of values keyed by timestamp
        polling_interval: Polling interval
        places: Number of places to round values

    Returns:
        result: List of key-value pair dicts

    """
    # Initialize key variables
    data_type = metadata.data_type
    polling_interval = metadata.polling_interval
    places = 10
    result = []

    # Make sure we have entries for entire time range
    (norm_ts_stop, _) = times.normalized_timestamp(
        polling_interval, timestamp=ts_stop)
    (norm_ts_start, _) = times.normalized_timestamp(
        polling_interval, timestamp=ts_start)
    nones = {_key: None for _key in range(
        norm_ts_start, norm_ts_stop, polling_interval)}

    # Get data from database
    with db.db_query(20127) as session:
        rows = session.query(Data.timestamp, Data.value).filter(and_(
            Data.timestamp < ts_stop, Data.timestamp > ts_start,
            Data.idx_datapoint == idx_datapoint)).order_by(
                Data.timestamp).all()

    # Put values into a dict for ease of processing
    for row in rows:
        # Get timestamp to the nearest polling_interval bounary
        (timestamp, _) = times.normalized_timestamp(
            polling_interval, timestamp=row.timestamp)
        rounded_value = round(float(row.value), places)
        nones[timestamp] = rounded_value

    if data_type in [DATA_INT, DATA_FLOAT]:
        # Process non-counter values
        result = _response(nones)

    elif data_type in [DATA_COUNT64, DATA_COUNT] and len(rows) > 1:
        # Process counter values by calculating the difference between
        # successive values
        result = _counters(nones, polling_interval, places)

    return result


def _counters(nones, polling_interval, places):
    """Create list of dicts of counter values retrieved from database.

    Args:
        nones: Dict of values keyed by timestamp
        polling_interval: Polling interval
        places: Number of places to round values

    Returns:
        result: List of key-value pair dicts

    """
    # Initialize key variables
    final = {}

    # Create list of timestamps and values
    timestamps = []
    values = []
    for timestamp, value in sorted(nones.items()):
        timestamps.append(timestamp)
        values.append(value)

    # Remove first timestamp value as it isn't necessary
    # after deltas are created
    timestamps = timestamps[1:]

    # Create an array for ease of readability.
    # Convert to None values to nans to make deltas without errors
    values_array = np.array(values).astype(np.float)

    '''
    Sometimes we'll get unsigned counter values in the database that roll over
    to zero. This result in a negative delta.

    We convert the result to abs(result). Python3 integers have no size limit
    so you can't use logic like this to fix it:

    (value.current + integer.type.max - value.previous)

    '''
    deltas = np.abs(np.diff(values_array))
    for key, delta in enumerate(deltas):
        # Calculate the value as a transaction per second value
        tps = round((delta / polling_interval) * 1000, places)
        final[timestamps[key]] = tps

    for i in deltas:
        print(i)

    # Return the result
    result = _response(final)
    return result


def _response(nones):
    """Create list of dicts.

    Args:
        nones: Dict of values keyed by timestamp

    Returns:
        result: List of key-value pair dicts

    """
    # Return a list of dicts
    result = []
    for timestamp, value in nones.items():
        result.append({'timestamp': timestamp, 'value': value})
    return result


if __name__ == '__main__':
    main()
