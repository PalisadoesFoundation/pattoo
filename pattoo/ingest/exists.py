#!/usr/bin/env python3
"""Verifies the existence of various database table primary key values."""

# PIP libraries
from sqlalchemy import and_

from pattoo_shared import log

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Agent, DataSource, DataVariable
from pattoo import TimestampValue


def idx_datavariable(checksum):
    """Get the db DataVariable.idx_datavariable value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: DataVariable.idx_datavariable value

    """
    # Initialize key variables
    result = None

    # Filter invalid data
    if isinstance(checksum, str) is False:
        return None

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(
            DataVariable.idx_datavariable,
            DataVariable.last_timestamp).filter(
                DataVariable.checksum == checksum.encode())

    # Return
    for row in rows:
        result = TimestampValue(
            idx_datavariable=row.idx_datavariable,
            timestamp=row.last_timestamp)
        break
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
    with db.db_query(20008) as session:
        rows = session.query(Agent.idx_agent).filter(and_(
            Agent.agent_id == agent_id.encode(),
            Agent.agent_hostname == agent_hostname.encode(),
            Agent.agent_program == agent_program.encode(),
            Agent.polling_interval == polling_interval))

    # Return
    for row in rows:
        result = row.idx_agent
        break
    return result


def idx_datasource(idx_agent=None, gateway=None, device=None):
    """Get the db DataSource.idx_datasource value.

    Args:
        _idx_agent: Agent.idx_agent value
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
    with db.db_query(20006) as session:
        rows = session.query(DataSource.idx_datasource).filter(and_(
            DataSource.idx_agent == _idx_agent,
            DataSource.gateway == gateway.encode(),
            DataSource.device == device.encode()))

    # Return
    for row in rows:
        result = row.idx_datasource
        break
    return result
