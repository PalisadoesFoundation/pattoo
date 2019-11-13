"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint, jsonify

# pattoo imports
from pattoo.db import db
from pattoo.db.tables import DataPoint

# Define the various global variables
REST_API_DATAPOINT = Blueprint('REST_API_DATAPOINT', __name__)


@REST_API_DATAPOINT.route('/<int:idx_datapoint>')
def route_idx_datapoint(idx_datapoint):
    """Provide data from the DataPoint table.

    Args:
        idx_datapoint: Data.idx_datapoint key

    Returns:
        _result: JSONify dict of DataPoint row values

    """
    # Initialize key variables
    _result = {}
    listing = []

    # Get the _result
    with db.db_query(20019) as session:
        rows = session.query(
            DataPoint.idx_datapoint,
            DataPoint.checksum,
            DataPoint.data_label,
            DataPoint.data_index,
            DataPoint.data_type,
            DataPoint.enabled,
            DataPoint.last_timestamp,
            DataPoint.idx_datasource).filter(
                DataPoint.idx_datapoint == idx_datapoint)

    # Return
    for row in rows:
        _result['idx_datapoint'] = row.idx_datapoint
        _result['checksum'] = row.checksum
        _result['data_label'] = row.data_label
        _result['data_index'] = row.data_index
        _result['data_type'] = row.data_type
        _result['enabled'] = row.enabled
        _result['last_timestamp'] = row.last_timestamp
        _result['idx_datasource'] = row.idx_datasource
        listing.append(_result)
    result = jsonify(listing)
    return result


@REST_API_DATAPOINT.route('')
def route_idx_datapoints():
    """Provide data from the DataPoint table.

    Args:
        None

    Returns:
        listing: JSONify list of dicts containing DataPoint row values

    """
    # Initialize key variables
    listing = []

    # Get the _result
    with db.db_query(20014) as session:
        rows = session.query(
            DataPoint.idx_datapoint,
            DataPoint.checksum,
            DataPoint.data_label,
            DataPoint.data_index,
            DataPoint.data_type,
            DataPoint.enabled,
            DataPoint.last_timestamp,
            DataPoint.idx_datasource)

    # Return
    for row in rows:
        _result = {}
        _result['idx_datapoint'] = row.idx_datapoint
        _result['checksum'] = row.checksum
        _result['data_label'] = row.data_label
        _result['data_index'] = row.data_index
        _result['data_type'] = row.data_type
        _result['enabled'] = row.enabled
        _result['last_timestamp'] = row.last_timestamp
        _result['idx_datasource'] = row.idx_datasource
        listing.append(_result)
    result = jsonify(listing)
    return result
