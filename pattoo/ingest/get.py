#!/usr/bin/env python3
"""Verifies the existence of various database table primary key values."""

# Import project libraries
from pattoo.ingest.db import exists, insert, query


def pairs(pattoo_db_record):
    """Create db Pair table entries.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        result: List of Pair.idx_pair database index values

    """
    # Initialize key variables
    result = []

    # Get key-values
    _pairs = key_value_pairs(pattoo_db_record)

    # Get list of pairs in the database
    insert.pairs(_pairs)
    result = query.pairs(_pairs)

    # Return
    return result


def key_value_pairs(pattoo_db_records):
    """Create a list of key-value pairs.

    Args:
        pattoo_db_records: List of PattooDBrecord objects

    Returns:
        rows: List of (key, value) tuples

    """
    # Initialize key variables
    rows = []

    if isinstance(pattoo_db_records, list) is False:
        pattoo_db_records = [pattoo_db_records]

    for pattoo_db_record in pattoo_db_records:
        # Iterate over NamedTuple
        for key, value in sorted(pattoo_db_record._asdict().items()):

            # Ignore keys that don't belong in the Pair table
            if key in ['timestamp', 'value', 'checksum', 'data_type']:
                continue

            if key == 'metadata':
                # Process the metadata key-values
                rows.extend(value)
            else:
                # Process other key-values
                rows.append((str(key), str(value)))

    return rows


def idx_checksum(checksum, data_type):
    """Get the db Checksum.idx_checksum value for an PattooDBrecord object.

    Args:
        checksum: Checksum value
        data_type: Data type

    Returns:
        _idx_checksum: Checksum._idx_checksum value. None if unsuccessful

    """
    # Create an entry in the database Checksum table
    _idx_checksum = exists.checksum(checksum)
    if bool(_idx_checksum) is False:
        insert.checksum(checksum, data_type)
        _idx_checksum = exists.checksum(checksum)

    # Return
    return _idx_checksum
