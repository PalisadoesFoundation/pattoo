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
            by agent_id and sorted by timestamp. This data is obtained from
            PattooShared.converter.extract

    Returns:
        None

    """
    # Initialize key variables
    arguments = []
    sub_processes_in_pool = max(1, multiprocessing.cpu_count() * 2)

    # Setup the arguments for multiprocessing
    arguments = [(_, ) for _ in grouping_pattoo_db_records]

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        kvs_4_agents = pool.starmap(_get_key_values, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Update the database with key value pairs
    _insert_key_values(kvs_4_agents)

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        pool.starmap(_process_rows, arguments)

    # Wait for all the processes to end and get results
    pool.join()


def _get_key_values(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: PattooDBrecord oject list sorted by
            timestamp for a single agent_id.

    Returns:
        result: List of key value pair tuples

    """
    # Initialize key variables
    result = []
    for pattoo_db_record in pattoo_db_records:
        result.extend(exists.key_values(pattoo_db_record))
    return result


def _insert_key_values(kvs_4_agents):
    """Insert key value pairs from cache PattooDBrecord objects into the db.

    Args:
        kvs_4_agents: List of lists of key-value pairs. Each list was extracted
            from a different agent's list of PattooDBrecord objects.

    Returns:
        result: List of key value pair tuples

    """
    uniques = {}
    all_kvs = []

    # Create a single list of key-value pairs.
    # Add them to a dict to make the pairs unique.
    for kvs_4_agent in kvs_4_agents:
        all_kvs.extend(kvs_4_agent)
    for _kv in all_kvs:
        uniques[_kv] = None

    # Insert the key-value pairs into the database
    for (key, value) in uniques.keys():
        if bool(exists.pair(key, value)) is False:
            insert.pair(key, value)


def _process_rows(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: PattooDBrecord oject list sorted by
            timestamp for a single agent_id.

    Returns:
        None

    """
    # Initialize key variables
    items = []

    # Return if there is nothint to process
    if bool(pattoo_db_records) is False:
        return

    # Get Checksum ID
    checksum_table = _get_checksums(pattoo_db_records[0])

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
            result = _create_idx_checksum(pattoo_db_record.checksum)
            if bool(result) is True:
                idx_checksum = result

                # Update the lookup table
                checksum_table[pattoo_db_record.checksum] = idx_checksum

                # Update the Glue table
                idx_pairs = exists.pairs(pattoo_db_record)
                insert.glue(idx_checksum, idx_pairs)
            else:
                continue

        # Append item to items
        items.append(IDXTimestampValue(
            idx_checksum=idx_checksum,
            timestamp=pattoo_db_record.timestamp,
            value=pattoo_db_record.value))

    # Update the data table
    if bool(items):
        insert.timeseries(items)


def _get_checksums(pattoo_db_record):
    """Get all the checksum values for a specific agent_id.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        result: Dict of idx_checksum values keyed by Checksum.checksum

    """
    # Result
    result = {}
    rows = []
    agent_id = pattoo_db_record.agent_id

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            Checksum.checksum,
            Checksum.idx_checksum).filter(and_(
                Glue.idx_checksum == Checksum.idx_checksum,
                Glue.idx_pair == Pair.idx_pair,
                Pair.key == agent_id.encode()
            ))

    # Return
    for row in rows:
        result[row.checksum] = row.idx_checksum
    return result


def _create_idx_checksum(checksum):
    """Get the db Checksum.idx_checksum value for an PattooDBrecord object.

    Args:
        apd: ChecksumPolledData object

    Returns:
        idx_checksum: Checksum.idx_checksum value. None if unsuccessful

    """
    # Create an entry in the database Checksum table
    idx_checksum = exists.idx_checksum(checksum)
    if bool(idx_checksum) is False:
        insert.checksum(checksum)
        idx_checksum = exists.idx_checksum(checksum)

    # Return
    return idx_checksum
