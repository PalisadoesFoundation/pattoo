#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Agent, DataSource, DataPoint, Data


def timeseries(
        idx_datapoint=None, timestamp=None, value=None,):
    """Insert timeseries data.

    Args:
        idx_datapoint: Agent ID
        timestamp: Agent hostname
        value: Agent program name

    Returns:
        result: Agent.idx_agent value

    """
    # Initialize key variables
    _idx_datapoint = idx_datapoint

    # Filter invalid data
    if None in [_idx_datapoint, timestamp, value]:
        return None
    if isinstance(_idx_datapoint, int) is False:
        return None
    if isinstance(timestamp, int) is False:
        return None
    if isinstance(value, (float, int)) is False:
        return None

    # Insert data
    row = Data(
        idx_datapoint=_idx_datapoint,
        timestamp=timestamp,
        value=value
    )
    with db.db_modify(20012, die=False) as session:
        session.add(row)


def idx_agent(
        agent_id=None, agent_hostname=None, agent_program=None,
        polling_interval=None):
    """Create the database Agent.idx_agent value.

    Args:
        agent_id: Agent ID
        agent_hostname: Agent hostname
        agent_program: Agent program name
        polling_interval: Agent polling interval

    Returns:
        result: Agent.idx_agent value

    """
    # Filter invalid data
    if None in [agent_id, agent_hostname, agent_program, polling_interval]:
        return None
    if isinstance(agent_id, str) is False:
        return None
    if isinstance(agent_hostname, str) is False:
        return None
    if isinstance(agent_program, str) is False:
        return None
    if isinstance(polling_interval, int) is False:
        return None

    # Insert and get the new idx_agent value
    row = Agent(
        agent_id=agent_id.encode(),
        agent_hostname=agent_hostname.encode(),
        agent_program=agent_program.encode(),
        polling_interval=polling_interval
    )
    with db.db_modify(20001, die=False) as session:
        session.add(row)


def idx_datasource(
        idx_agent=None, gateway=None, device=None, device_type=None):
    """Create the db DataSource.idx_datasource value.

    Args:
        idx_agent: Agent.idx_agent value
        gateway: Agent gateway
        device: Device from which the Agent gateway got the data

    Returns:
        result: DataSource.idx_datasource value

    """
    # Initialize key variables
    _idx_agent = idx_agent

    # Filter invalid data
    if None in [_idx_agent, gateway, device]:
        return None
    if isinstance(_idx_agent, int) is False:
        return None
    if isinstance(gateway, str) is False:
        return None
    if isinstance(device, str) is False:
        return None
    if isinstance(device_type, int) is False and device_type is not None:
        return None

    # Insert and get the new idx_datasource value
    row = DataSource(
        idx_agent=_idx_agent,
        gateway=gateway.encode(),
        device=device.encode(),
        device_type=device_type
    )
    with db.db_modify(20002, die=False) as session:
        session.add(row)


def idx_datapoint(
        idx_datasource=None, checksum=None, data_label=None, data_index=None,
        data_type=None, last_timestamp=None):
    """Create the db DataPoint.idx_datapoint value.

    Args:
        idx_datasource: DataSource table index for the DataPoint row
        data_label: data_label value
        data_index: data_index value
        data_type: data_type value
        checksum: Agent checksum
        timestamp: timestamp value

    Returns:
        result: DataSource.idx_datapoint value

    """
    # Initialize key variables
    _idx_datasource = idx_datasource

    # Filter invalid data
    if None in [_idx_datasource, checksum, data_label, data_index,
                data_type, last_timestamp]:
        return None
    if isinstance(_idx_datasource, int) is False:
        return None
    if isinstance(checksum, str) is False:
        return None
    if isinstance(data_label, str) is False:
        return None
    if isinstance(data_index, str) is False:
        return None
    if isinstance(data_type, int) is False:
        return None
    if isinstance(last_timestamp, int) is False:
        return None

    # Insert and get the new idx_datapoint value
    row = DataPoint(
        idx_datasource=idx_datasource,
        checksum=checksum.encode(),
        data_label=data_label.encode(),
        data_index=data_index.encode(),
        data_type=data_type,
        last_timestamp=last_timestamp
    )
    with db.db_modify(20003, die=False) as session:
        session.add(row)
