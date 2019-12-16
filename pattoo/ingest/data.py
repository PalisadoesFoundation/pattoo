#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import multiprocessing

# Import project libraries
from pattoo_shared.constants import DATA_NONE, DATA_STRING
from pattoo.constants import IDXTimestampValue, ChecksumLookup
from pattoo.ingest import get
from pattoo.db import misc
from pattoo.db.table import pair, glue, data, agent, datapoint


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
    pair.insert_rows(per_process_key_value_pairs)

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
        1) Get all the idx_datapoint and idx_pair values that exist in the
           PattooDBrecord data from the database. All the records MUST be
           from the same source.
        2) Add these idx values to tracking memory variables for speedy lookup
        3) Ignore non numeric data values sent
        4) Add data to the database. If new checksum values are found in the
           PattooDBrecord data, then create the new index values to the
           database, update the tracking memory variables before hand.

    """
    # Initialize key variables
    _data = {}

    # Return if there is nothint to process
    if bool(pattoo_db_records) is False:
        return

    # Get DataPoint.idx_datapoint and idx_pair values from db. This is used to
    # speed up the process by reducing the need for future database access.
    agent_id = pattoo_db_records[0].pattoo_agent_id
    checksum_table = misc.agent_checksums(agent_id)

    # Process data
    for pdbr in pattoo_db_records:
        # We only want to insert non-string, non-None values
        if pdbr.pattoo_data_type in [DATA_NONE, DATA_STRING]:
            continue

        # Get the idx_datapoint value for the PattooDBrecord
        if pdbr.pattoo_checksum in checksum_table:
            # Get last_timestamp for existing idx_datapoint entry
            idx_datapoint = checksum_table[
                pdbr.pattoo_checksum].idx_datapoint
        else:
            # Entry not in database. Update the database and get the
            # required idx_datapoint
            idx_datapoint = datapoint.idx_datapoint(pdbr)
            if bool(idx_datapoint) is True:
                # Update the lookup table
                checksum_table[
                    pdbr.pattoo_checksum] = ChecksumLookup(
                        idx_datapoint=idx_datapoint,
                        polling_interval=pdbr.pattoo_agent_polling_interval,
                        last_timestamp=1)

                # Update the Glue table
                idx_pairs = get.pairs(pdbr)
                glue.insert_rows(idx_datapoint, idx_pairs)
            else:
                continue

        # Append item to items
        if pdbr.pattoo_timestamp > checksum_table[
                pdbr.pattoo_checksum].last_timestamp:
            '''
            Add the Data table results to a dict in case we have duplicate
            posting over the API. We need to key off a unique time dependent
            value per datapoint to prevent different datapoints at the same
            point in time overwriting the value. This is specifically for
            removing duplicates for the _SAME_ datapoint at the same point in
            time as could possibly occur with the restart of an agent causing a
            double posting or network issues. We therefore use a tuple of
            idx_datapoint and timestamp.
            '''
            _data[(
                pdbr.pattoo_timestamp,
                idx_datapoint)] = IDXTimestampValue(
                    idx_datapoint=idx_datapoint,
                    polling_interval=pdbr.pattoo_agent_polling_interval,
                    timestamp=pdbr.pattoo_timestamp,
                    value=pdbr.pattoo_value)

    # Update the data table
    if bool(data):
        data.insert_rows(list(_data.values()))
