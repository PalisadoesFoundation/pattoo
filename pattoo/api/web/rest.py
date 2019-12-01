"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint, jsonify, request
from sqlalchemy import and_

# pattoo imports
from pattoo import data
from pattoo import uri
from pattoo.db import db
from pattoo.db.tables import Data

# Define the various global variables
REST_API_DATA = Blueprint('REST_API_DATA', __name__)


@REST_API_DATA.route('/data/<int:idx_checksum>')
def route_data(idx_checksum):
    """Provide data from the Data table.

    Args:
        idx_checksum: Checksum.idx_checksum key

    Returns:
        _result: JSONify list of dicts {timestamp: value} from the Data table.

    """
    # Initialize key variables
    _result = []
    secondsago = data.integerize(request.args.get('secondsago'))
    (ts_start, ts_stop) = uri.chart_timestamp_args(secondsago)

    # Get the _result
    with db.db_query(20020) as session:
        rows = session.query(Data.value, Data.timestamp).filter(and_(
            Data.timestamp < ts_stop, Data.timestamp > ts_start,
            Data.idx_checksum == idx_checksum))

    # Return
    for row in rows:
        _result.append({row.timestamp: row.value})
    result = jsonify(_result)
    return result
