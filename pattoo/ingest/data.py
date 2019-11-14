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
from pattoo.db.tables import Data, Agent, DataSource, DataPoint
from pattoo.ingest import exists
from pattoo.ingest import insert


def mulitiprocess(grouping_pattoo_db_records):
    """Get the database Agent.idx_agent value for an AgentPolledData object.

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
        agent_id: Agent ID

    Returns:
        result: Dict of idx_datapoint values keyed by DataPoint.checksum

    """
    # Result
    result = {}

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            DataPoint.checksum,
            DataPoint.last_timestamp,
            DataPoint.idx_datapoint).filter(and_(
                Agent.agent_id == agent_id.encode(),
                Agent.idx_agent == DataSource.idx_agent,
                DataSource.idx_datasource == DataPoint.idx_datasource
            ))

    # Return
    for found_row in rows:
        item = IDXTimestamp(
            idx_datapoint=found_row.idx_datapoint,
            timestamp=found_row.last_timestamp)
        checksum = found_row.checksum.decode()
        result[checksum] = item
    return result


def process_rows(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: PattooDBrecord oject list sorted by
            timestamp for a single agent_id.
        checksum_table: Shared Dict of of idx_datapoint and last_timestamp DB
            data keyed by agent_id

    Returns:
        None

    """
    # Initialize key variables
    items = []

    # Return if there is nothint to process
    if bool(pattoo_db_records) is False:
        return

    # Get Agent ID
    agent_id = pattoo_db_records[0].agent_id
    checksum_table = get_checksums(agent_id)

    # Process data
    for row in pattoo_db_records:
        if row.checksum in checksum_table:
            # Get last_timestamp for existing idx_datapoint entry
            _idxt = checksum_table[row.checksum]
            idx_datapoint = _idxt.idx_datapoint
            last_timestamp = _idxt.timestamp
        else:
            # Entry not in database. Update the database and get the
            # required idx_datapoint
            _idxt = _get_idx_datapoint(row)
            if bool(_idxt) is True:
                idx_datapoint = _idxt.idx_datapoint
                last_timestamp = _idxt.timestamp

                # Update the lookup table
                checksum_table[row.checksum] = _idxt
            else:
                continue

        # Append item to items
        if (row.timestamp > last_timestamp) and (
                row.data_type not in [DATA_NONE, DATA_STRING]):
            items.append(IDXTimestampValue(
                idx_datapoint=idx_datapoint,
                timestamp=row.timestamp,
                value=row.value))

    # Update the data table
    if bool(items):
        _update_data_table(items)


def _update_data_table(items):
    """Insert all data values for an agent into database.

    Args:
        items: List of IDXTimestampValue objects

    Returns:
        None

    """
    # Initialize key varialbes
    db_data_rows = []
    last_timestamps = {}

    # Process all the DataPoint values
    for item in sorted(items, key=attrgetter('timestamp')):
        # Get the most recent timestamp for each idx_datapoint
        if item.idx_datapoint not in last_timestamps:
            last_timestamps[item.idx_datapoint] = item.timestamp
        else:
            if last_timestamps[item.idx_datapoint] < item.timestamp:
                last_timestamps[item.idx_datapoint] = item.timestamp

        # Cache data for database update
        row = Data(
            idx_datapoint=item.idx_datapoint,
            timestamp=item.timestamp,
            value=item.value
        )
        db_data_rows.append(row)

    # Update the last_timestamp
    for idx_datapoint, timestamp in last_timestamps.items():
        with db.db_modify(20010, die=False) as session:
            # Update the last_timestamp
            session.query(DataPoint).filter(
                and_(DataPoint.idx_datapoint == idx_datapoint,
                     DataPoint.enabled == 1)).update(
                         {'last_timestamp': timestamp})

    # Update the data table
    if bool(db_data_rows) is True:
        try:
            with db.db_modify(20007) as session:
                session.add_all(db_data_rows)
        except:
            log_message = ('''\
Failed to update timeseries data for DataPoint.checksum.''')
            log.log2info(20011, log_message)


def _get_idx_datapoint(row):
    """Populate tables with foreign keys pointing to the Data table.

    Args:
        row: PattooShared.converter.extract NamedTuple

    Returns:
        result: IDXTimestamp object of idx_datapoint and timestamp.
            None if unsuccessful.
    """
    # Do nothing if OK.
    result = exists.idx_datapoint(row.checksum)
    if bool(result) is True:
        return result

    # Create an entry in the database Agent table if necessary
    idx_agent = _create_idx_agent(
        agent_id=row.agent_id,
        agent_hostname=row.agent_hostname,
        agent_program=row.agent_program,
        polling_interval=row.polling_interval)

    # Stop if row cannot be processed
    if bool(idx_agent) is False:
        return None

    # Create an entry in the database DataSource table if necessary
    idx_datasource = _create_idx_datasource(
        idx_agent=idx_agent,
        gateway=row.gateway,
        device=row.device)

    # Stop if row cannot be processed
    if bool(idx_datasource) is False:
        return None

    # Create an entry in the database DataSource table if necessary
    result = _create_idx_datapoint(
        idx_datasource=idx_datasource,
        data_label=row.data_label,
        data_index=row.data_index,
        data_type=row.data_type,
        checksum=row.checksum,
        timestamp=row.timestamp)

    # Stop if row cannot be processed
    if bool(result) is False:
        return None

    # Return
    return result


def _create_idx_agent(
        agent_id=None, agent_hostname=None, agent_program=None,
        polling_interval=None):
    """Get the database Agent.idx_agent value for an AgentPolledData object.

    Args:
        apd: AgentPolledData object

    Returns:
        idx_agent: Agent.idx_agent value. None if unsuccessful

    """
    # Create an entry in the database Agent table
    idx_agent = exists.idx_agent(
        agent_id=agent_id,
        agent_hostname=agent_hostname,
        agent_program=agent_program,
        polling_interval=polling_interval)
    if bool(idx_agent) is False:
        insert.idx_agent(
            agent_id=agent_id,
            agent_hostname=agent_hostname,
            agent_program=agent_program,
            polling_interval=polling_interval)
        idx_agent = exists.idx_agent(
            agent_id=agent_id,
            agent_hostname=agent_hostname,
            agent_program=agent_program,
            polling_interval=polling_interval)

    # Return
    return idx_agent


def _create_idx_datasource(idx_agent=None, gateway=None, device=None):
    """Get the db DataSource.idx_datasource values for an AgentPolledData obj.

    Args:
        idx_agent: Agent.idx_agent value
        gateway: Agent gateway
        device: Device from which the Agent gateway got the data

    Returns:
        idx_datasource: DataSource.idx_datasource value. None if unsuccessful.

    """
    # Create an entry in the database DataSource table
    idx_datasource = exists.idx_datasource(
        idx_agent=idx_agent,
        gateway=gateway,
        device=device)
    if bool(idx_datasource) is False:
        insert.idx_datasource(
            idx_agent=idx_agent,
            gateway=gateway,
            device=device)
        idx_datasource = exists.idx_datasource(
            idx_agent=idx_agent,
            gateway=gateway,
            device=device)

    # Return
    return idx_datasource


def _create_idx_datapoint(
        idx_datasource=None, data_label=None, data_index=None,
        data_type=None, checksum=None, timestamp=None):
    """Get db DataPoint.idx_datapoint values for an AgentPolledData obj.

    Args:
        idx_datasource: DataSource table index for the DataPoint row
        data_label: data_label value
        data_index: data_index value
        data_type: data_type value
        checksum: Agent checksum
        timestamp: timestamp value

    Returns:
        _idxt: IDXTimestamp of idx_datapoint and timestamp.
            None if unsuccessful.

    """
    # Create an entry in the database DataPoint table
    _idxt = exists.idx_datapoint(checksum)
    if bool(_idxt) is False:
        insert.idx_datapoint(
            idx_datasource=idx_datasource,
            data_label=data_label,
            data_index=data_index,
            data_type=data_type,
            checksum=checksum,
            last_timestamp=timestamp)
        _idxt = exists.idx_datapoint(checksum)

    # Return
    return _idxt
