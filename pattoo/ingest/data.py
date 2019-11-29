#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import multiprocessing

# Import project libraries
from pattoo_shared.constants import DATA_NONE, DATA_STRING
from pattoo.constants import IDXTimestampValue, ChecksumLookup
from pattoo.ingest.db import insert, query
from pattoo.ingest import get


def mulitiprocess(grouping_pattoo_db_records):
    """Insert PattooDBrecord objects into the database.

    Args:
        grouping_pattoo_db_records: List of PattooDBrecord oject lists grouped
            by source and sorted by timestamp. This data is obtained from
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
            get.key_value_pairs, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Update the database with key value pairs
    insert.pairs(per_process_key_value_pairs)

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        pool.starmap(_process_rows, arguments)

    # Wait for all the processes to end and get results
    pool.join()


def _process_rows(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: List of dicts read from cache files.

    Returns:
        None

    Method:
        1) Get all the idx_checksum and idx_pair values that exist in the
           PattooDBrecord data from the database. All the records MUST be
           from the same source.
        2) Add these idx values to tracking memory variables for speedy lookup
        3) Ignore non numeric data values sent
        4) Add data to the database. If new checksum values are found in the
           PattooDBrecord data, then create the new index values to the
           database, update the tracking memory variables before hand.

    """
    # Initialize key variables
    data = {}

    # Return if there is nothint to process
    if bool(pattoo_db_records) is False:
        return

    # Get Checksum.idx_checksum and idx_pair values from db. This is used to
    # speed up the process by reducing the need for future database access.
    source = pattoo_db_records[0].pattoo_source
    checksum_table = query.checksums(source)

    # Process data
    for pattoo_db_record in pattoo_db_records:
        # We only want to insert non-string, non-None values
        if pattoo_db_record.pattoo_data_type in [DATA_NONE, DATA_STRING]:
            continue

        # Get the idx_checksum value for the PattooDBrecord
        if pattoo_db_record.pattoo_checksum in checksum_table:
            # Get last_timestamp for existing idx_checksum entry
            idx_checksum = checksum_table[
                pattoo_db_record.pattoo_checksum].idx_checksum
        else:
            # Entry not in database. Update the database and get the
            # required idx_checksum
            idx_checksum = get.idx_checksum(
                pattoo_db_record.pattoo_checksum,
                pattoo_db_record.pattoo_data_type,
                pattoo_db_record.pattoo_polling_interval)
            if bool(idx_checksum) is True:
                # Update the lookup table
                checksum_table[
                    pattoo_db_record.pattoo_checksum] = ChecksumLookup(
                        idx_checksum=idx_checksum,
                        polling_interval=pattoo_db_record.pattoo_polling_interval,
                        last_timestamp=1)

                # Update the Glue table
                idx_pairs = get.pairs(pattoo_db_record)
                insert.glue(idx_checksum, idx_pairs)
            else:
                continue

        # Append item to items
        if pattoo_db_record.pattoo_timestamp > checksum_table[
                pattoo_db_record.pattoo_checksum].last_timestamp:
            '''
            Add the Data table results to a dict in case we have duplicate
            posting over the API. We need to key off a unique time dependent
            value per datapoint to prevent different datapoints at the same
            point in time overwriting the value. This is specifically for
            removing duplicates for the _SAME_ datapoint at the same point in
            time as could possibly occur with the restart of an agent causing a
            double posting or network issues. We therefore use a tuple of
            idx_checksum and timestamp.
            '''
            data[(
                pattoo_db_record.pattoo_timestamp,
                idx_checksum)] = IDXTimestampValue(
                    idx_checksum=idx_checksum,
                    polling_interval=pattoo_db_record.pattoo_polling_interval,
                    timestamp=pattoo_db_record.pattoo_timestamp,
                    value=pattoo_db_record.pattoo_value)

    # Update the data table
    if bool(data):
        insert.timeseries(list(data.values()))
