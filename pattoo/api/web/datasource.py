"""Pattoo version routes."""

# PIP libraries
from flask import Blueprint, jsonify

# pattoo imports
from pattoo.db import db
from pattoo.db.tables import DataSource

# Define the various global variables
REST_API_DATASOURCE = Blueprint('REST_API_DATASOURCE', __name__)


@REST_API_DATASOURCE.route('/<int:idx_datasource>')
def route_idx_datasource(idx_datasource):
    """Provide data from the DataSource table.

    Args:
        idx_datasource: DataSource.idx_datasource key

    Returns:
        _result: JSONify dict of DataSource row values

    """
    # Initialize key variables
    _result = {}

    # Get the _result
    with db.db_query(20015) as session:
        rows = session.query(
            DataSource.idx_datasource,
            DataSource.idx_agent,
            DataSource.device,
            DataSource.gateway,
            DataSource.enabled).filter(
                DataSource.idx_datasource == idx_datasource)

    # Return
    for row in rows:
        _result['idx_datasource'] = row.idx_datasource
        _result['idx_agent'] = row.idx_agent
        _result['device'] = row.device
        _result['gateway'] = row.gateway
        _result['enabled'] = row.enabled
    result = jsonify(_result)
    return result


@REST_API_DATASOURCE.route('')
def route_idx_datasources():
    """Provide data from the DataSource table.

    Args:
        None

    Returns:
        listing: JSONify list of dicts containing DataSource row values

    """
    # Initialize key variables
    listing = []

    # Get the _result
    with db.db_query(20016) as session:
        rows = session.query(
            DataSource.idx_datasource,
            DataSource.idx_agent,
            DataSource.device,
            DataSource.gateway,
            DataSource.enabled)

    # Return
    for row in rows:
        _result = {}
        _result['idx_datasource'] = row.idx_datasource
        _result['idx_agent'] = row.idx_agent
        _result['device'] = row.device
        _result['gateway'] = row.gateway
        _result['enabled'] = row.enabled
        listing.append(_result)
    result = jsonify(listing)
    return result
