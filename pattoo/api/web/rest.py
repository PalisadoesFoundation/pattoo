"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint, jsonify, request, Response
from sqlalchemy import and_

# pattoo imports
from pattoo import data
from pattoo import uri
from pattoo.db import db
from pattoo.db.tables import Data

# Define the various global variables
REST_DATA = Blueprint('REST_DATA', __name__)
# REST_DATAPOINT = Blueprint('REST_DATAPOINT', __name__)
# REST_DATASOURCE = Blueprint('REST_DATASOURCE', __name__)
# REST_AGENT = Blueprint('REST_AGENT', __name__)


@REST_DATA.route('/data/<int:idx_datapoint>')
def index():
    """Provide the status page.

    Args:
        idx_datapoint: Data.idx_datapoint key

    Returns:
        Home Page

    """
    # Initialize key variables
    _result = []
    secondsago = data.integerize(request.args.get('secondsago'))
    (ts_start, ts_stop) = uri.chart_timestamp_args(secondsago)

    # Get the _result
    with db.db_query(20005) as session:
        rows = session.query(Data.value, Data.timestamp).filter(and_(
            Data.timestamp < ts_stop, Data.timestamp > ts_start))

    # Return
    for row in rows:
        _result.append(
            {'timestamp': row.timestamp, 'value': row.value}
        )
    result = jsonify(_result)
    return result
