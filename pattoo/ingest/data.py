#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import multiprocessing
from operator import attrgetter

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo_shared.constants import DATA_NONE, DATA_STRING
from pattoo_shared import log
from pattoo import IDXTimestamp, IDXTimestampValue
from pattoo.db import db
from pattoo.db.tables import Data, Checksum, DataSource, DataPoint
from pattoo.ingest import exists
from pattoo.ingest import insert


def mulitiprocess(grouping_pattoo_db_records):
    """Get the database Checksum.idx_checksum value for an ChecksumPolledData object.

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
        pool.starmap(process_rows, arguments)

    # Wait for all the processes to end and get results
    pool.join()


def get_checksums(agent_id):
    """Get all the checksum values for a specific agent_id.

    Args:
        agent_id: Checksum ID

    Returns:
        result: Dict of idx_checksum values keyed by DataPoint.checksum

    """
    # Result
    result = {}

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            DataPoint.checksum,
            DataPoint.last_timestamp,
            DataPoint.idx_checksum).filter(and_(
                Checksum.agent_id == agent_id.encode(),
                Checksum.idx_checksum == DataSource.idx_checksum,
                DataSource.idx_datasource == DataPoint.idx_datasource
            ))

    # Return
    for found_row in rows:
        item = IDXTimestamp(
            idx_checksum=found_row.idx_checksum,
            timestamp=found_row.last_timestamp)
        checksum = found_row.checksum.decode()
        result[checksum] = item
    return result


def process_rows(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: PattooDBrecord oject list sorted by
            timestamp for a single agent_id.
        checksum_table: Shared Dict of of idx_checksum and last_timestamp DB
            data keyed by agent_id

    Returns:
        None

    """
    # Initialize key variables
    items = []

    # Return if there is nothint to process
    if bool(pattoo_db_records) is False:
        return

    # Get Checksum ID
    agent_id = pattoo_db_records[0].agent_id
    checksum_table = get_checksums(agent_id)

    # Process data
    for row in pattoo_db_records:
        # We only want to insert non-string, non-None values
        if row.data_type in [DATA_NONE, DATA_STRING]:
            continue

        # Get the idx_checksum value for the PattooDBrecord
        if row.checksum in checksum_table:
            # Get last_timestamp for existing idx_checksum entry
            idx_checksum = checksum_table[row.checksum]
        else:
            # Entry not in database. Update the database and get the
            # required idx_checksum
            result = _create_idx_checksum(row.checksum)
            if bool(result) is True:
                idx_checksum = result

                # Update the lookup table
                checksum_table[row.checksum] = idx_checksum

                # Update the Glue table
                idx_pairs = exists.pairs(row)
                insert.glue(idx_checksum, idx_pairs)
            else:
                continue

        # Append item to items
        items.append(IDXTimestampValue(
            idx_checksum=idx_checksum,
            timestamp=row.timestamp,
            value=row.value))

    # Update the data table
    if bool(items):
        insert.timeseries(items)


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
