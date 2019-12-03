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
from pattoo import data
from pattoo import uri
from pattoo.db import db
from pattoo.db.tables import Data, DataPoint

# Define the various global variables
REST_API_DATA = Blueprint('REST_API_DATA', __name__)


@REST_API_DATA.route('/data/<int:idx_datapoint>')
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
    """Ingest data."""
    # Initialize key variables
    data_type = metadata.data_type
    polling_interval = metadata.polling_interval
    places = 10
    values = []

    # Make sure we have entries for entire time range
    (norm_ts_stop, _) = times.normalized_timestamp(
        polling_interval, timestamp=ts_stop)
    (norm_ts_start, _) = times.normalized_timestamp(
        polling_interval, timestamp=ts_start)
    result = {_key: None for _key in range(
        norm_ts_start, norm_ts_stop, polling_interval)}

    with db.db_query(20027) as session:
        rows = session.query(Data.timestamp, Data.value).filter(and_(
            Data.timestamp < ts_stop, Data.timestamp > ts_start,
            Data.idx_datapoint == idx_datapoint)).order_by(
                Data.timestamp).all()

    if data_type in [DATA_INT, DATA_FLOAT]:
        # Process non-counter values
        for row in rows:
            # Get timestamp to the nearest polling_interval bounary
            (timestamp, _) = times.normalized_timestamp(
                polling_interval, timestamp=row.timestamp)
            rounded_value = round(float(row.value), places)
            values.append({'timestamp': timestamp, 'value': rounded_value})

    elif data_type in [DATA_COUNT64, DATA_COUNT] and len(rows) > 1:
        # Process counter values by calculating the difference between
        # successive values
        array = np.asarray(rows)
        timestamps = array[:, 0].tolist()[1:]

        '''
        Sometimes we'll get unsigned counter values that roll over to zero.
        This will result in the delta being negative. We need a way to detect
        this and make the delta value be:

        value.current + integer.type.max - value.previous

        '''
        if data_type == DATA_COUNT:
            deltas = np.diff(array[:, 1].astype(np.int32))
        else:
            deltas = np.diff(array[:, 1].astype(np.int64))
        for key, delta in enumerate(deltas):
            # Get timestamp to the nearest polling_interval bounary
            (timestamp, _) = times.normalized_timestamp(
                polling_interval, timestamp=timestamps[key])

            # Calculate the value as a transaction per second value
            rounded_delta = round((delta / polling_interval) * 1000, places)
            values.append({'timestamp': timestamp, 'value': rounded_delta})

    # Return
    return values
