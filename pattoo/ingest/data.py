#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import multiprocessing

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo_shared.constants import DATA_NONE, DATA_STRING
from pattoo.constants import IDXTimestampValue
from pattoo.db import db
from pattoo.db.tables import Checksum, Glue, Pair
from pattoo.ingest import exists
from pattoo.ingest import insert


def mulitiprocess(grouping_pattoo_db_records):
    """Insert PattooDBrecord objects into the database.

    Args:
        grouping_pattoo_db_records: List of PattooDBrecord oject lists grouped
            by data_source and sorted by timestamp. This data is obtained from
            PattooShared.converter.extract

    Returns:
        None

    Method:
        1) Extract all the key-value pairs from the data
        2) Update the database with pairs not previously seen
        3) Add the remaining data to the database using the pair
           indices created in (2)

    """
    # Initialize key variables
    arguments = []
    sub_processes_in_pool = max(1, multiprocessing.cpu_count() * 2)

    # Setup the arguments for multiprocessing
    arguments = [(_, ) for _ in grouping_pattoo_db_records]

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        per_process_key_value_pairs = pool.starmap(
            _get_key_value_pairs, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Update the database with key value pairs
    _insert_key_value_pairs(per_process_key_value_pairs)

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        pool.starmap(_process_rows, arguments)

    # Wait for all the processes to end and get results
    pool.join()


def _get_key_value_pairs(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: List of dicts read from cache files.

    Returns:
        result: List of key value pair tuples

    """
    # Initialize key variables
    result = []
    for pattoo_db_record in pattoo_db_records:
        result.extend(exists.key_value_pairs(pattoo_db_record))
    return result


def _insert_key_value_pairs(items):
    """Insert key value pairs from cache PattooDBrecord objects into the db.

    Args:
        items: List of lists of key-value pairs. Each list was extracted from
            a different data_source's list of PattooDBrecord objects.

    Returns:
        result: List of key value pair tuples

    """
    uniques = {}
    all_kvs = []

    # Create a single list of key-value pairs.
    # Add them to a dict to make the pairs unique.
    for item in items:
        all_kvs.extend(item)
    for _kv in all_kvs:
        uniques[_kv] = None

    # Insert the key-value pairs into the database
    for (key, value), _ in uniques.items():
        if bool(exists.pair(key, value)) is False:
            insert.pair(key, value)


def _process_rows(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: List of dicts read from cache files.

    Returns:
        None

    Method:
        1) Get all the idx_checksum and idx_pair values that exist in the
           PattooDBrecord data from the database. All the records MUST be
           from the same data_source.
        2) Add these idx values to tracking memory variables for speedy lookup
        3) Ignore non numeric data values sent
        4) Add data to the database. If new checksum values are found in the
           PattooDBrecord data, then create the new index values to the
           database, update the tracking memory variables before hand.

    """
    # Initialize key variables
    items = []
    idx_pairs_2_insert = []

    # Return if there is nothint to process
    if bool(pattoo_db_records) is False:
        return

    # Get Checksum.idx_checksum and idx_pair values from db. This is used to
    # speed up the process by reducing the need for future database access.
    checksum_table = _get_checksums(pattoo_db_records[0])
    glue_idx_pairs = _get_glue(checksum_table.values())

    # Process data
    for pattoo_db_record in pattoo_db_records:
        # We only want to insert non-string, non-None values
        if pattoo_db_record.data_type in [DATA_NONE, DATA_STRING]:
            continue

        # Get the idx_checksum value for the PattooDBrecord
        if pattoo_db_record.checksum in checksum_table:
            # Get last_timestamp for existing idx_checksum entry
            idx_checksum = checksum_table[pattoo_db_record.checksum]
        else:
            # Entry not in database. Update the database and get the
            # required idx_checksum
            result = _create_idx_checksum(
                pattoo_db_record.checksum, pattoo_db_record.data_type)
            if bool(result) is True:
                idx_checksum = result

                # Update the lookup table
                checksum_table[pattoo_db_record.checksum] = idx_checksum

                # Update the Glue table
                idx_pairs = exists.pairs(pattoo_db_record)
                for idx_pair in idx_pairs:
                    if idx_pair not in glue_idx_pairs:
                        idx_pairs_2_insert.append(idx_pair)
                        glue_idx_pairs.append(idx_pair)
                insert.glue(idx_checksum, idx_pairs_2_insert)
            else:
                continue

        # Append item to items
        items.append(IDXTimestampValue(
            idx_checksum=idx_checksum,
            timestamp=pattoo_db_record.data_timestamp,
            value=pattoo_db_record.data_value))

    # Update the data table
    if bool(items):
        insert.timeseries(items)


def _get_checksums(pattoo_db_record):
    """Get all the checksum values for a specific data_source.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        result: Dict of idx_checksum values keyed by Checksum.checksum

    """
    # Result
    result = {}
    rows = []
    data_source = pattoo_db_record.data_source

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            Checksum.checksum,
            Checksum.idx_checksum).filter(and_(
                Glue.idx_checksum == Checksum.idx_checksum,
                Glue.idx_pair == Pair.idx_pair,
                Pair.key == data_source.encode()
            ))

    # Return
    for row in rows:
        result[row.checksum] = row.idx_checksum
    return result


def _get_glue(idx_checksums):
    """Get all the checksum values for a specific data_source.

    Args:
        checksums: Dict of idx_checksum values keyed by checksum

    Returns:
        result: Dict of idx_checksum values keyed by Checksum.checksum

    """
    # Initialize key variables
    result = []

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            Glue.idx_pair).filter(Glue.idx_checksum.in_(idx_checksums))

    # Return
    for row in rows:
        result.append(row.idx_pair)
    return result


def _create_idx_checksum(checksum, data_type):
    """Get the db Checksum.idx_checksum value for an PattooDBrecord object.

    Args:
        checksum: Checksum value
        data_type: Data type

    Returns:
        idx_checksum: Checksum.idx_checksum value. None if unsuccessful

    """
    # Create an entry in the database Checksum table
    idx_checksum = exists.idx_checksum(checksum)
    if bool(idx_checksum) is False:
        insert.checksum(checksum, data_type)
        idx_checksum = exists.idx_checksum(checksum)

    # Return
    return idx_checksum
