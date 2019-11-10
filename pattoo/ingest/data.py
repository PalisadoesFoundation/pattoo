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
from pattoo import TimestampValue, IDXTimestampValue
from pattoo.db import db
from pattoo.db.orm import Data, Agent, DataSource, DataVariable
from pattoo.ingest import exists
from pattoo.ingest import insert


def mulitiprocess(allrows):
    """Get the database Agent.idx_agent value for an AgentPolledData object.

    Args:
        allrows: List of lists. Each row is a list of
            PattooShared.converter.extract NamedTuple objects from a single
            agent.

    Returns:
        None

    """
    # Initialize key variables
    sub_processes_in_pool = max(1, multiprocessing.cpu_count() * 2)
    arguments = [(_, ) for _ in allrows]

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        pool.starmap(process_rows, arguments)

    # Wait for all the processes to end and get results
    pool.join()


def process_rows(rows):
    """Insert all data values for an agent into database.

    Args:
        rows: List of PattooShared.converter.extract NamedTuple objects from
            the same agent SORTED by timestamp

    Returns:
        None

    """
    # Initialize key variables
    items = []

    # Return if there is nothint to process
    if bool(rows) is False:
        return

    # Get checksum values for this agent_id from the DataVariable table
    firstrow = rows[0]
    checksums = get_checksums(firstrow)

    # Process data
    for row in rows:
        if row.checksum in checksums:
            # Get last_timestamp for existing idx_datavariable entry
            _dv = checksums[row.checksum]
            idx_datavariable = _dv.idx_datavariable
            last_timestamp = _dv.timestamp
        else:
            # Entry not in database. Update the database and get the
            # required idx_datavariable
            _dv = get_idx_datavariable(row)
            if bool(_dv) is True:
                idx_datavariable = _dv.idx_datavariable
                last_timestamp = _dv.timestamp
            else:
                continue

        # Append item to items
        if (row.timestamp > last_timestamp) and (
                row.data_type not in [DATA_NONE, DATA_STRING]):
            items.append(IDXTimestampValue(
                idx_datavariable=idx_datavariable,
                timestamp=row.timestamp,
                value=row.value))

    # Update the data table
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

    # Update the last_timestamp
    for item in sorted(items, key=attrgetter('timestamp')):
        with db.db_modify(20010, die=False) as session:
            # Update the last_timestamp
            session.query(DataVariable).filter(
                and_(DataVariable.idx_datavariable == item.idx_datavariable,
                     DataVariable.enabled == 1)).update(
                         {'last_timestamp': item.timestamp})

        # Cache data for database update
        row = Data(
            idx_datavariable=item.idx_datavariable,
            timestamp=item.timestamp,
            value=item.value
        )
        db_data_rows.append(row)

    # Update the data table
    if bool(db_data_rows) is True:
        try:
            with db.db_modify(20007) as session:
                session.add_all(db_data_rows)
        except:
            log_message = ('''\
Failed to update timeseries data for DataVariable.checksum.''')
            log.log2info(20011, log_message)


def get_checksums(row):
    """Get all the checksum values for a specific agent_id.

    Args:
        row: PattooShared.converter.extract NamedTuple

    Returns:
        result: Dict of idx_datavariable values keyed by DataVariable.checksum

    """
    # Result
    result = {}

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            DataVariable.checksum,
            DataVariable.last_timestamp,
            DataVariable.idx_datavariable).filter(and_(
                Agent.agent_id == row.agent_id.encode(),
                Agent.idx_agent == DataSource.idx_agent,
                DataSource.idx_datasource == DataVariable.idx_datasource
            ))

    # Return
    for found_row in rows:
        item = TimestampValue(
            idx_datavariable=found_row.idx_datavariable,
            timestamp=found_row.last_timestamp)
        checksum = found_row.checksum.decode()
        result[checksum] = item
    return result


def get_idx_datavariable(row):
    """Populate tables with foreign keys pointing to the Data table.

    Args:
        row: PattooShared.converter.extract NamedTuple

    Returns:
        result: TimestampValue of idx_datavariable and timestamp.
            None if unsuccessful.
    """
    # Do nothing if OK.
    result = exists.idx_datavariable(row.checksum)
    if bool(result) is True:
        return result

    # Create an entry in the database Agent table if necessary
    idx_agent = create_idx_agent(
        agent_id=row.agent_id,
        agent_hostname=row.agent_hostname,
        agent_program=row.agent_program,
        polling_interval=row.polling_interval)

    # Stop if row cannot be processed
    if bool(idx_agent) is False:
        return None

    # Create an entry in the database DataSource table if necessary
    idx_datasource = create_idx_datasource(
        idx_agent=idx_agent,
        gateway=row.gateway,
        device=row.device)

    # Stop if row cannot be processed
    if bool(idx_datasource) is False:
        return None

    # Create an entry in the database DataSource table if necessary
    result = create_idx_datavariable(
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


def create_idx_agent(
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


def create_idx_datasource(idx_agent=None, gateway=None, device=None):
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


def create_idx_datavariable(
        idx_datasource=None, data_label=None, data_index=None,
        data_type=None, checksum=None, timestamp=None):
    """Get db DataVariable.idx_datavariable values for an AgentPolledData obj.

    Args:
        idx_datasource: DataSource table index for the DataVariable row
        data_label: data_label value
        data_index: data_index value
        data_type: data_type value
        checksum: Agent checksum
        timestamp: timestamp value

    Returns:
        _tv: TimestampValue of idx_datavariable and timestamp.
            None if unsuccessful.

    """
    # Create an entry in the database DataVariable table
    _tv = exists.idx_datavariable(checksum)
    if bool(_tv) is False:
        insert.idx_datavariable(
            idx_datasource=idx_datasource,
            data_label=data_label,
            data_index=data_index,
            data_type=data_type,
            checksum=checksum,
            last_timestamp=timestamp)
        _tv = exists.idx_datavariable(checksum)

    # Return
    return _tv
