#!/usr/bin/env python3
"""Verifies the existence of various database table primary key values."""

# Import project libraries
from pattoo.db import pair, datapoint


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
    pair.insert_rows(_pairs)
    result = pair.idx_pairs(_pairs)

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
            if key.startswith('pattoo') is True:
                if key not in [
                        'pattoo_metadata', 'pattoo_key', 'pattoo_agent_id']:
                    continue

            if key == 'pattoo_metadata':
                # Process the metadata key-values
                rows.extend(value)
            else:
                # Process other key-values
                rows.append((str(key), str(value)))

    return sorted(rows)


def idx_datapoint(checksum, data_type, polling_interval):
    """Get the db DataPoint.idx_datapoint value for an PattooDBrecord object.

    Args:
        checksum: Checksum value
        data_type: Data type
        polling_interval: Polling interval

    Returns:
        _idx_datapoint: DataPoint._idx_datapoint value. None if unsuccessful

    """
    # Create an entry in the database Checksum table
    _idx_datapoint = datapoint.checksum_exists(checksum)
    if bool(_idx_datapoint) is False:
        datapoint.insert_row(checksum, data_type, polling_interval)
        _idx_datapoint = datapoint.checksum_exists(checksum)

    # Return
    return _idx_datapoint
