#!/usr/bin/env python3
"""Verifies the existence of various database table primary key values."""

# Standard imports
import collections

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.orm import Agent, DataSource, DataVariable


def idx_datavariable_checksum(checksum):
    """Get the db DataVariable.idx_datavariable value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: DataVariable.idx_datavariable value

    """
    # Initialize key variables
    result = None
    datatuple = collections.namedtuple(
        'Values', 'idx_datavariable last_timestamp')

    # Filter invalid data
    if isinstance(checksum, str) is False:
        return None

    # Get the result
    database = db.Database()
    session = database.session()
    rows = session.query(DataVariable).filter(
        DataVariable.checksum == checksum.encode())

    # Return
    if bool(rows.count()) is True:
        result = datatuple(
            idx_datavariable=rows[0].idx_datavariable,
            last_timestamp=rows[0].last_timestamp)
    return result


def idx_agent(
        agent_id=None, agent_hostname=None, agent_program=None,
        polling_interval=None):
    """Get the database Agent.idx_agent value.

    Args:
        agent_id: Agent ID
        agent_hostname: Agent hostname
        agent_program: Agent program name
        polling_interval: Agent polling interval

    Returns:
        result: Agent.idx_agent value

    """
    # Initialize key variables
    result = None

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

    # Get the result
    database = db.Database()
    session = database.session()
    rows = session.query(Agent).filter(and_(
        Agent.agent_id == agent_id.encode(),
        Agent.agent_hostname == agent_hostname.encode(),
        Agent.agent_program == agent_program.encode(),
        Agent.polling_interval == polling_interval))

    # Return
    if bool(rows.count()) is True:
        result = rows[0].idx_agent
    return result


def idx_datasource(idx_agent, gateway, device):
    """Get the db DataSource.idx_datasource value.

    Args:
        idx_agent: Agent.idx_agent value
        gateway: Agent gateway
        device: Device from which the Agent gateway got the data

    Returns:
        result: DataSource.idx_datasource value

    """
    # Initialize key variables
    result = None
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

    # Get the result
    database = db.Database()
    session = database.session()
    rows = session.query(DataSource).filter(and_(
        DataSource.idx_agent == _idx_agent,
        DataSource.gateway == gateway.encode(),
        DataSource.device == device.encode()))

    # Return
    if bool(rows.count()) is True:
        result = rows[0].idx_datasource
    return result


def idx_datavariable(
        idx_datasource=None, checksum=None, data_label=None, data_index=None,
        data_type=None, timestamp=None):
    """Get the db DataVariable.idx_datavariable value.

    Args:
        idx_datasource: DataSource table index for the DataVariable row
        data_label: data_label value
        data_index: data_index value
        data_type: data_type value
        checksum: Agent checksum
        timestamp: timestamp value

    Returns:
        result: DataSource.idx_datasource value

    """
    # Initialize key variables
    result = None
    _idx_datasource = idx_datasource

    # Filter invalid data
    if None in [_idx_datasource, checksum, data_label, data_index,
                data_type, timestamp]:
        return False
    if isinstance(_idx_datasource, int) is False:
        return False
    if isinstance(checksum, str) is False:
        return False
    if isinstance(data_label, str) is False:
        return False
    if isinstance(data_index, str) is False:
        return False
    if isinstance(data_type, int) is False:
        return False
    if isinstance(timestamp, int) is False:
        return False

    # Get the result
    database = db.Database()
    session = database.session()
    rows = session.query(DataVariable).filter(and_(
        DataVariable.idx_datasource == idx_datasource,
        DataVariable.last_timestamp == timestamp,
        DataVariable.checksum == checksum.encode(),
        DataVariable.data_label == data_label.encode(),
        DataVariable.data_index == data_index.encode(),
        DataVariable.data_type == data_type))

    # Return
    if bool(rows.count()) is True:
        result = rows[0].idx_datavariable
    return result
