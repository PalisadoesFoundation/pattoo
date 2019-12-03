"""Pattoo version routes."""

# PIP libraries
import numpy as np
from flask import Blueprint, jsonify, request
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# pattoo imports
from pattoo_shared.constants import (
    DATA_INT, DATA_FLOAT, DATA_COUNT64, DATA_COUNT)
from pattoo_shared import times
from pattoo.api.web import CACHE
from pattoo import data
from pattoo import uri
from pattoo.db import db
from pattoo.db.tables import Data, DataPoint

# Define the various global variables
REST_API_DATA = Blueprint('REST_API_DATA', __name__)


@REST_API_DATA.route('/data/<int:idx_datapoint>')
@CACHE.cached(query_string=True, timeout=60)
def route_data(idx_datapoint):
    """Provide data from the Data table.

    Args:
        idx_datapoint: DataPoint.idx_datapoint key

    Returns:
        _result: JSONify list of dicts {timestamp: value} from the Data table.

    """
    # Initialize key variables
    _result = {}
    secondsago = data.integerize(request.args.get('secondsago'))
    (ts_start, ts_stop) = uri.chart_timestamp_args(secondsago)

    try:
        # Deal with that as well
        with db.db_query(20028) as session:
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
        _result = _query(idx_datapoint, ts_start, ts_stop, metadata)

    # Return
    result = jsonify(_result)
    return result


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
