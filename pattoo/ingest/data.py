#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import collections

# PIP libraries
import pymysql
from sqlalchemy import and_

# Import project libraries
from pattoo_shared.variables import (
    AgentPolledData, DeviceGateway, DeviceDataVariables, DataVariable)
from pattoo_shared import data as lib_data

from pattoo.db import db
from pattoo.db.orm import Agent
from pattoo.ingest import exists
from pattoo.ingest import insert


def process(row):
    """Get the database Agent.idx_agent value for an AgentPolledData object.

    Args:
        row: PattooShared.converter.extract NamedTuple

    Returns:
        None

    """
    # Do nothing if OK.
    idx_datavariable = exists.idx_datavariable_checksum(row.checksum)
    if bool(idx_datavariable) is True:
        print('found')
        return

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
