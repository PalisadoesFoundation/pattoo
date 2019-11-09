#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import multiprocessing
from operator import attrgetter
import time

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo_shared.constants import DATA_NONE, DATA_STRING
from pattoo_shared import log
from pattoo import LastTimestamp, LastTimestampValue
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
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())
    arguments = [(_, ) for _ in allrows]

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        pool.starmap(process_agent_rows, arguments)

    # Wait for all the processes to end and get results
    pool.join()


def process_agent_rows(rows):
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
    checksums = _agent_checksums(rows[0])

    # Process data
    _rows = sorted(rows, key=attrgetter('timestamp'))
    for row in _rows:
        # Do memory lookup for data if it's already in the database
        if row.checksum in checksums:
            items.append(LastTimestampValue(
                idx_datavariable=checksums[row.checksum],
                last_timestamp=row.timestamp,
                value=row.value))
        else:
            # Update the database with supporting metadata and get the
            # required idx_datavariable if not already in the database
            result = process(row)
            if bool(result) is True:
                items.append(result)

    # Update the data table
    _update_data_table(items)


def _update_data_table(items):
    """Insert all data values for an agent into database.

    Args:
        items: List of LastTimestampValue objects

    Returns:
        None

    """
    # Initialize key varialbes
    db_data_rows = []

    # Update the last_timestamp
    for item in items:
        # Assume we are going to fail until the transaction succeeds
        success = False

        with db.db_modify(20010, die=False) as session:
            # Update the last_timestamp
            success = session.query(DataVariable).filter(
                and_(DataVariable.idx_datavariable == item.idx_datavariable,
                     DataVariable.enabled == 1)).update(
                         {'last_timestamp': item.last_timestamp})

        # Cache data for database update
        if bool(success) is True:
            row = Data(
                idx_datavariable=item.idx_datavariable,
                timestamp=item.last_timestamp,
                value=item.value
            )
            db_data_rows.append(row)
        else:
            log_message = ('''\
Failed to update Data table for idx_datavariable {} at timestamp {}.\
'''.format(item.idx_datavariable, item.last_timestamp))
            log.log2info(21008, log_message)

    # Update the data table
    if bool(db_data_rows) is True:
        try:
            with db.db_modify(20007) as session:
                session.add_all(db_data_rows)
        except:
            log_message = ('''\
Failed to update timeseries data for DataVariable.checksum.''')
            log.log2info(20011, log_message)


def _agent_checksums(row):
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
        items = session.query(
            DataVariable.checksum,
            DataVariable.idx_datavariable).filter(and_(
                Agent.agent_id == row.agent_id.encode(),
                Agent.idx_agent == DataSource.idx_agent,
                DataSource.idx_datasource == DataVariable.idx_datasource,
                DataSource.gateway == row.gateway.encode(),
                DataSource.device == row.device.encode(),
            ))

    # Return
    if bool(items.count()) is True:
        for item in items:
            checksum = item.checksum.decode()
            result[checksum] = item.idx_datavariable
    return result


def process(row):
    """Insert agent data value into database.

    Args:
        row: PattooShared.converter.extract NamedTuple

    Returns:
        None

    """
    # Do nothing if OK.
    result = process_metadata(row)
    if bool(result) is False:
        return None

    # Only update data and last_timestamp if data is more current
    # and if we are working with numeric values
    if (result.last_timestamp < row.timestamp) and (
            row.data_type not in [DATA_NONE, DATA_STRING]):
        _result = LastTimestampValue(
            idx_datavariable=result.idx_datavariable,
            last_timestamp=row.timestamp,
            value=row.value)
        return _result

    # Return
    return None


def process_metadata(row):
    """Populate tables with foreign keys pointing to the Data table.

    Args:
        row: PattooShared.converter.extract NamedTuple

    Returns:
        result: NamedTuple keyed by idx_datavariable and last_timestamp

    """
    # Do nothing if OK.
    result = exists.idx_datavariable_checksum(row.checksum)
    if bool(result) is True:
        return result

    # Create an entry in the database Agent table if necessary
    idx_agent = process_agent_table(
        agent_id=row.agent_id, agent_hostname=row.agent_hostname,
        agent_program=row.agent_program, polling_interval=row.polling_interval)

    # Stop if row cannot be processed
    if bool(idx_agent) is False:
        return

    # Create an entry in the database DataSource table if necessary
    idx_datasource = process_datasource_table(
        idx_agent=idx_agent, gateway=row.gateway, device=row.device)

    # Stop if row cannot be processed
    if bool(idx_datasource) is False:
        return

    # Create an entry in the database DataSource table if necessary
    idx_datavariable = process_datavariable_table(
        idx_datasource=idx_datasource, data_label=row.data_label,
        data_index=row.data_index, data_type=row.data_type,
        checksum=row.checksum, timestamp=row.timestamp)

    # Stop if row cannot be processed
    if bool(idx_datavariable) is False:
        return

    # Return
    result = LastTimestamp(idx_datavariable=idx_datavariable, last_timestamp=1)
    return result


def process_agent_table(
        agent_id=None, agent_hostname=None, agent_program=None,
        polling_interval=None):
    """Get the database Agent.idx_agent value for an AgentPolledData object.

    Args:
        apd: AgentPolledData object

    Returns:
        idx_agent: Agent.idx_agent value, None if unsuccessful

    """
    # Create an entry in the database Agent table
    idx_agent = exists.idx_agent(
        agent_id=agent_id,
        agent_hostname=agent_hostname,
        agent_program=agent_program,
        polling_interval=polling_interval)
    if bool(idx_agent) is False:
        success = insert.idx_agent(
            agent_id=agent_id,
            agent_hostname=agent_hostname,
            agent_program=agent_program,
            polling_interval=polling_interval)
        if bool(success) is True:
            idx_agent = exists.idx_agent(
                agent_id=agent_id,
                agent_hostname=agent_hostname,
                agent_program=agent_program,
                polling_interval=polling_interval)
        else:
            return None

    # Return
    return idx_agent


def process_datasource_table(idx_agent=None, gateway=None, device=None):
    """Get the db DataSource.idx_datasource values for an AgentPolledData obj.

    Args:
        idx_agent: Agent.idx_agent value
        gateway: Agent gateway
        device: Device from which the Agent gateway got the data

    Returns:
        result: List of NamedTuple values (gateway, device)

    """
    # Create an entry in the database DataSource table
    idx_datasource = exists.idx_datasource(
        idx_agent=idx_agent,
        gateway=gateway,
        device=device)
    if bool(idx_datasource) is False:
        success = insert.idx_datasource(
            idx_agent=idx_agent,
            gateway=gateway,
            device=device)
        if bool(success) is True:
            idx_datasource = exists.idx_datasource(
                idx_agent=idx_agent,
                gateway=gateway,
                device=device)
        else:
            return None

    # Return
    return idx_datasource


def process_datavariable_table(
        idx_datasource=None, data_label=None, data_index=None,
        data_type=None, checksum=None, timestamp=None):
    """Get the db DataVariable.idx_datavariable values for an AgentPolledData obj.

    Args:
        idx_datasource: DataSource table index for the DataVariable row
        data_label: data_label value
        data_index: data_index value
        data_type: data_type value
        checksum: Agent checksum
        timestamp: timestamp value

    Returns:
        result: List of NamedTuple values (checksum, data_label)

    """
    # Create an entry in the database DataVariable table
    idx_datavariable = exists.idx_datavariable(
        idx_datasource=idx_datasource,
        data_label=data_label,
        data_index=data_index,
        data_type=data_type,
        checksum=checksum,
        timestamp=timestamp)
    if bool(idx_datavariable) is False:
        success = insert.idx_datavariable(
            idx_datasource=idx_datasource,
            data_label=data_label,
            data_index=data_index,
            data_type=data_type,
            checksum=checksum,
            timestamp=timestamp)
        if bool(success) is True:
            idx_datavariable = exists.idx_datavariable(
                idx_datasource=idx_datasource,
                data_label=data_label,
                data_index=data_index,
                data_type=data_type,
                checksum=checksum,
                timestamp=timestamp)
        else:
            return None

    # Return
    return idx_datavariable
