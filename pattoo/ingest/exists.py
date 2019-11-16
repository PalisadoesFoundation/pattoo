#!/usr/bin/env python3
"""Verifies the existence of various database table primary key values."""

# PIP libraries
from sqlalchemy import and_

from pattoo_shared import log

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Pair, Checksum


def idx_checksum(checksum):
    """Get the db Checksum.idx_checksum value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: Checksum.idx_checksum value

    """
    # Initialize key variables
    result = False

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(Checksum.idx_checksum).filter(
            Checksum.checksum == checksum.encode())

    # Return
    for row in rows:
        result = row.idx_checksum
        break
    return result


def pair(key, value):
    """Get the db Pair table for key-value pair.

    Args:
        _key: Key-value pair key
        value: Key-value pair value

    Returns:
        result: Pair.idx_pair value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20006) as session:
        rows = session.query(Pair.idx_pair).filter(and_(
            Pair.key == str(key).encode(),
            Pair.value == str(value).encode()
            ))

    # Return
    for row in rows:
        result = row.idx_pair
        break
    return result


def pairs(pattoo_db_record):
    """Create db Pair table entries.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        None

    """
    # Initialize key variables
    result = []

    # Get key-values
    _kvs = key_values(pattoo_db_record)

    # Get list of pairs in the database
    for key, value in _kvs:
        idx_pair = pair(key, value)
        if bool(idx_pair) is True:
            result.append(idx_pair)

    # Return
    return result


def key_values(pattoo_db_record):
    """Create db Pair table entries.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        None

    """
    # Initialize key variables
    rows = []

    # Iterate over NamedTuple
    for _key, _value in pattoo_db_record._asdict().items():
        # Convert to string values
        key = str(_key)

        # Ignore keys that don't belong in the Pair table
        if key in ['timestamp', 'value', 'checksum']:
            continue

        if key == 'metadata':
            # Process the metadata key-values
            for _mkey, _mvalue in _value:
                rows.append((str(_mkey), str(_mvalue)))
        else:
            # Process other key-values
            rows.append((key, str(_value)))

    return rows
