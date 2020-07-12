#!/usr/bin/env python3
"""Pattoo classes querying the ChartDataPoint table."""

# PIP3 imports
from sqlalchemy import and_

# Import project libraries
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.models import ChartDataPoint
from pattoo.constants import DbRowChartDataPoint


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_chart_datapoint

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20097) as session:
        rows = session.query(ChartDataPoint.idx_chart_datapoint).filter(
            ChartDataPoint.idx_chart_datapoint == idx)

    # Return
    for _ in rows:
        result = True
        break
    return bool(result)


def exists(idx_chart, idx_datapoint):
    """Determine whether name exists in the ChartDataPoint table.

    Args:
        idx_chart: Chart table index
        idx_datapoint: DataPoint table index

    Returns:
        result: ChartDataPoint.idx_chart_datapoint value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get name from database
    with db.db_query(20037) as session:
        rows = session.query(ChartDataPoint.idx_chart_datapoint).filter(
            and_(ChartDataPoint.idx_chart == idx_chart,
                 ChartDataPoint.idx_datapoint == idx_datapoint))

    # Return
    for row in rows:
        result = row.idx_chart_datapoint
        break
    return result


def insert_row(row):
    """Create a ChartDataPoint table entry.

    Args:
        row: DbRowChartDataPoint object

    Returns:
        None

    """
    # Verify values
    if bool(row) is False or isinstance(row, DbRowChartDataPoint) is False:
        log_message = 'Invalid chart_datapoint type being inserted'
        log.log2die(20033, log_message)

    # Insert
    row = ChartDataPoint(
        idx_chart=row.idx_chart,
        idx_datapoint=row.idx_datapoint,
        enabled=int(bool(row.enabled)),
        )
    with db.db_modify(20032, die=True) as session:
        session.add(row)
