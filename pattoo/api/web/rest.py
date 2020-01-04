"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint, jsonify, request

# pattoo imports
from pattoo.api.web import CACHE
from pattoo import data
from pattoo import uri
from pattoo.db.table.datapoint import DataPoint

# Define the various global variables
REST_API_DATA = Blueprint('REST_API_DATA', __name__)


@REST_API_DATA.route('/data/<int:idx_datapoint>')
@CACHE.cached(query_string=True, timeout=10)
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
    ts_start = uri.chart_timestamp_args(idx_datapoint, secondsago)

    # Get data
    _datapoint = DataPoint(idx_datapoint)
    ts_stop = _datapoint.last_timestamp()
    _result = _datapoint.data(ts_start, ts_stop)

    # Return
    result = jsonify(_result)
    return result
