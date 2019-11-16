#!/usr/bin/env python3
"""Verifies the existence of various database table primary key values."""

# PIP libraries
from sqlalchemy import and_

from pattoo_shared import log

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Agent, Pair, Checksum
from pattoo import IDXTimestamp


def idx_checksum(checksum):
    """Get the db Checksum.idx_checksum value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: Checksum.idx_checksum value

    """
    # Initialize key variables
    result = False

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(Checksum.idx_checksum).filter(
            Checksum.checksum == checksum.encode())

    # Return
    for row in rows:
        result = row.idx_checksum
        break
    return result


def pair(key, value):
    """Get the db Pair table for key-value pair.

    Args:
        key: Key-value pair key
        value: Key-value pair value

    Returns:
        result: Pair.idx_pair value

    """
    # Initialize key variables
    result = False

    # Get the result
    with db.db_query(20005) as session:
        rows = session.query(Pair.idx_pair).filter(and_(
            Pair.key == key.encode(),
            Pair.value == value.encode()
            ))

    # Return
    for row in rows:
        result = row.idx_checksum
        break
    return result


def pairs(pattoo_db_record):
    """Create db Pair table entries.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        None

    """
    # Initialize key variables
    result = []

    # Iterate over NamedTuple
    for key, value in pattoo_db_record._asdict().iteritems():
        if key in ['timestamp', 'value', 'checksum']:
            continue

        # Get the result
        with db.db_query(20005) as session:
            rows = session.query(Pair.idx_pair).filter(and_(
                Pair.key == key.encode(),
                Pair.value == value.encode()
                ))

        # Return
        for row in rows:
            result.append(row.idx_pair)

    # Return
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
