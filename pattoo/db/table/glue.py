#!/usr/bin/env python3
"""Verifies the existence of various database data required for ingest."""

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Pair, DataPoint, Glue


def glue_exists(_idx_datapoint, idx_pair):
    """Determine existence of idx_datapoint, idx_pair in the Glue db table.

    Args:
        _idx_datapoint: DataPoint.idx_datapoint table index
        idx_pair: Pair.idx_pair table index

    Returns:
        result: True if it exists

    """
    # Initialize idx_datapoint variables
    result = False
    rows = []

    # Ignore certain restricted idx_datapoints
    with db.db_query(20008) as session:
        rows = session.query(Glue.idx_pair).filter(and_(
            Glue.idx_datapoint == _idx_datapoint,
            Glue.idx_pair == idx_pair,
            Pair.idx_pair == Glue.idx_pair,
            DataPoint.idx_datapoint == Glue.idx_datapoint
            ))

    # Return
    for _ in rows:
        result = True
        break
    return result


def insert_rows(idx_datapoint, _idx_pairs):
    """Create db Pair table entries.

    Args:
        idx_datapoint: DataPoint.idx_datapoint
        _idx_pairs: List of Pair.idx_pair values

    Returns:
        None

    """
    # Initialize key variables
    rows = []

    # Create a list for processing if not available
    if isinstance(_idx_pairs, list) is False:
        _idx_pairs = [_idx_pairs]

    # Iterate over _idx_pairs
    for idx_pair in _idx_pairs:
        pair_exists = glue_exists(idx_datapoint, idx_pair)
        if bool(pair_exists) is False:
            # Insert and get the new idx_datasource value
            row = Glue(idx_pair=idx_pair, idx_datapoint=idx_datapoint)
            rows.append(row)

    if bool(rows) is True:
        with db.db_modify(20002, die=True) as session:
            session.add_all(rows)


def idx_pairs(_idx_datapoints):
    """Get all the checksum values for a specific source.

    Args:
        _idx_datapoints: List idx_datapoint values

    Returns:
        result: Dict of idx_datapoint values keyed by DataPoint.checksum

    """
    # Initialize key variables
    result = []
    rows = []

    # Create a list if it doesn't exist
    if isinstance(_idx_datapoints, list) is False:
        _idx_datapoints = [_idx_datapoints]

    # Get the data from the database
    with db.db_query(20014) as session:
        rows = session.query(
            Glue.idx_pair).filter(Glue.idx_datapoint.in_(_idx_datapoints))

    # Return
    for row in rows:
        result.append(row.idx_pair)
    return sorted(result)
