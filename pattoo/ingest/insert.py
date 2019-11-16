#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Checksum, Pair, Glue, Data
from pattoo.ingest import exists


def timeseries(items):
    """Insert timeseries data.

    Args:
        items: List of IDXTimestampValue objects

    Returns:
        result: Checksum.checksum value

    """
    # Initialize key variables
    rows = []

    # Update the data
    for item in items:
        # Insert data
        row = Data(
            idx_checksup=item.idx_checksup,
            timestamp=item.timestamp,
            value=item.value
        )
    with db.db_modify(20012, die=True) as session:
        session.add_all(rows)


def checksum(_checksum):
    """Create the database Checksum.checksum value.

    Args:
        _checksum: Checksum value

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(_checksum, str) is True:
        # Insert and get the new checksum value
        row = Checksum(checksum=_checksum.encode())
        with db.db_modify(20001, die=True) as session:
            session.add(row)


def pairs(pattoo_db_record):
    """Create db Pair table entries.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        None

    """
    # Initialize key variables
    rows = []

    # Iterate over NamedTuple
    for key, value in pattoo_db_record._asdict().iteritems():
        if key in ['timestamp', 'value', 'checksum']:
            continue

        # Skip pre-existing pairs
        if exists.pair(key, value) is False:
            continue

        # Insert and get the new idx_datasource value
        row = Pair(key=key.encode(), value=value.encode())
        rows.append(row)

    if bool(rows) is True:
        with db.db_modify(20002, die=True) as session:
            session.add_all(rows)


def glue(idx_checksum, idx_pairs):
    """Create db Pair table entries.

    Args:
        idx_checksum: Checksum.idx_checksum
        idx_pairs: List of Pair.idx_pair values

    Returns:
        None

    """
    # Initialize key variables
    rows = []

    # Iterate over NamedTuple
    for idx_pair in idx_pairs:
        # Insert and get the new idx_datasource value
        row = Glue(idx_pair=idx_pair, idx_checksum=idx_checksum)
        rows.append(row)

    if bool(rows) is True:
        with db.db_modify(20002, die=True) as session:
            session.add_all(rows)
