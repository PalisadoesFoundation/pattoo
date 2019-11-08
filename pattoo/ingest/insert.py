#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# PIP libraries
import pymysql
from sqlalchemy import and_

# Import project libraries
from pattoo_shared.variables import (AgentPolledData, DeviceGateway)

from pattoo.db import db
from pattoo.db.orm import Agent, DataSource, DataVariable


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
    # Initialize key variables
    success = False

    # Filter invalid data
    if None in [agent_id, agent_hostname, agent_program, polling_interval]:
        return False
    if isinstance(agent_id, str) is False:
        return False
    if isinstance(agent_hostname, str) is False:
        return False
    if isinstance(agent_program, str) is False:
        return False
    if isinstance(polling_interval, int) is False:
        return False

    # Insert and get the new idx_agent value
    row = Agent(
        agent_id=agent_id.encode(),
        agent_hostname=agent_hostname.encode(),
        agent_program=agent_program.encode(),
        polling_interval=polling_interval
    )
    database = db.Database()
    try:
        database.add(row, 1145)
        success = True
    except pymysql.IntegrityError:
        # There may be a duplicate agent name if this is a brand
        # new database and there is a flurry of updates from multiple
        # agents. This is OK, pass.
        #
        # We are expecting a 'pymysql.err.IntegrityError' but for some
        # reason it could not be caught.
        pass

    # Return
    return success


def idx_datasource(idx_agent=None, gateway=None, device=None):
    """Create the db DataSource.idx_datasource value.

    Args:
        idx_agent: Agent.idx_agent value
        gateway: Agent gateway
        device: Device from which the Agent gateway got the data

    Returns:
        result: DataSource.idx_datasource value

    """
    # Initialize key variables
    success = False
    _idx_agent = idx_agent

    # Filter invalid data
    if None in [_idx_agent, gateway, device]:
        return False
    if isinstance(_idx_agent, int) is False:
        return False
    if isinstance(gateway, str) is False:
        return False
    if isinstance(device, str) is False:
        return False

    # Insert and get the new idx_datasource value
    row = DataSource(
        idx_agent=_idx_agent,
        gateway=gateway.encode(),
        device=device.encode()
    )
    database = db.Database()
    try:
        database.add(row, 1145)
        success = True
    except pymysql.IntegrityError:
        # There may be a duplicate agent name if this is a brand
        # new database and there is a flurry of updates from multiple
        # agents. This is OK, pass.
        #
        # We are expecting a 'pymysql.err.IntegrityError' but for some
        # reason it could not be caught.
        pass

    # Return
    return success


def idx_datavariable(
        idx_datasource=None, checksum=None, data_label=None, data_index=None,
        data_type=None, timestamp=None):
    """Create the db DataVariable.idx_datavariable value.

    Args:
        idx_datasource: DataSource table index for the DataVariable row
        data_label: data_label value
        data_index: data_index value
        data_type: data_type value
        checksum: Agent checksum
        timestamp: timestamp value

    Returns:
        result: DataSource.idx_datavariable value

    """
    # Initialize key variables
    success = False
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

    # Insert and get the new idx_datavariable value
    row = DataVariable(
        idx_datasource=idx_datasource,
        checksum=checksum.encode(),
        data_label=data_label.encode(),
        data_index=data_index.encode(),
        data_type=data_type,
        last_timestamp=timestamp
    )
    database = db.Database()
    try:
        database.add(row, 1145)
        success = True
    except pymysql.IntegrityError:
        # There may be a duplicate agent name if this is a brand
        # new database and there is a flurry of updates from multiple
        # agents. This is OK, pass.
        #
        # We are expecting a 'pymysql.err.IntegrityError' but for some
        # reason it could not be caught.
        pass

    # Return
    return success
