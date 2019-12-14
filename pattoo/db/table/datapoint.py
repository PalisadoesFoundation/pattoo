#!/usr/bin/env python3
"""Inserts various database values required during ingest."""


# Import project libraries
from pattoo.db import db
from pattoo.db.models import DataPoint


def checksum_exists(_checksum):
    """Get the db DataPoint.idx_datapoint value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: DataPoint.idx_datapoint value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20040) as session:
        rows = session.query(DataPoint.idx_datapoint).filter(
            DataPoint.checksum == _checksum.encode())

    # Return
    for row in rows:
        result = row.idx_datapoint
        break
    return result


def insert_row(_checksum, data_type, polling_interval):
    """Create the database DataPoint.checksum value.

    Args:
        _checksum: DataPoint value
        data_type: Type of data
        polling_interval: Polling interval

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(_checksum, str) is True:
        # Insert and get the new checksum value
        _row = DataPoint(
            checksum=_checksum.encode(),
            polling_interval=polling_interval,
            data_type=data_type)
        with db.db_modify(20034, die=True) as session:
            session.add(_row)
