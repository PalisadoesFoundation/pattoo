#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import collections
import multiprocessing
from operator import attrgetter

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo_shared.constants import DATA_NONE, DATA_STRING
from pattoo.db import db
from pattoo.db.orm import DataVariable
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
    # Process data
    _rows = sorted(rows, key=attrgetter('timestamp'))
    for row in _rows:
        process(row)


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
        return

    # Update the Data table
    idx_datavariable = result.idx_datavariable
    last_timestamp = result.last_timestamp

    # Only update data and last_timestamp if data is more current
    # and if we are working with numeric values
    if (last_timestamp < row.timestamp) and (
            row.data_type not in [DATA_NONE, DATA_STRING]):
        insert.timeseries(
            idx_datavariable=idx_datavariable,
            value=row.value,
            timestamp=row.timestamp)

        # Update the DataVariable table
        database = db.Database()
        session = database.db_session()

        # Update
        session.query(DataVariable).filter(
            and_(DataVariable.idx_datavariable == idx_datavariable,
                 DataVariable.enabled == 1)).update(
                     {'last_timestamp': row.timestamp})
        database.db_commit(session, 1057)


def process_metadata(row):
    """Populate tables with foreign keys pointing to the Data table.

    Args:
        row: PattooShared.converter.extract NamedTuple

    Returns:
        result: NamedTuple keyed by idx_datavariable and last_timestamp

    """
    # Initialize key variables
    datatuple = collections.namedtuple(
        'Values', 'idx_datavariable last_timestamp')

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
    result = datatuple(idx_datavariable=idx_datavariable, last_timestamp=1)
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
