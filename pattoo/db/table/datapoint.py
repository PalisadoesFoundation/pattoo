#!/usr/bin/env python3
"""Inserts various database values required during ingest."""


# Import project libraries
from pattoo.db import db
from pattoo.db.models import DataPoint
from pattoo.db.table import agent


def idx_datapoint(pattoo_db_record):
    """Get the db DataPoint.idx_datapoint value for a PattooDBrecord object.

    Args:
        pattoo_db_record: PattooDBrecord object

    Returns:
        _idx_datapoint: DataPoint._idx_datapoint value. None if unsuccessful

    """
    # Initialize key variables
    checksum = pattoo_db_record.pattoo_checksum
    data_type = pattoo_db_record.pattoo_data_type
    polling_interval = pattoo_db_record.pattoo_agent_polling_interval
    agent_id = pattoo_db_record.pattoo_agent_id
    agent_target = pattoo_db_record.pattoo_agent_polled_target
    agent_program = pattoo_db_record.pattoo_agent_program

    # Create an entry in the database Checksum table
    _idx_datapoint = checksum_exists(checksum)
    if bool(_idx_datapoint) is False:
        # Create a record in the Agent table
        idx_agent = agent.idx_agent(agent_id, agent_target, agent_program)

        # Create a record in the DataPoint table
        insert_row(checksum, data_type, polling_interval, idx_agent)
        _idx_datapoint = checksum_exists(checksum)

    # Return
    return _idx_datapoint


def checksum_exists(_checksum):
    """Get the db DataPoint.idx_datapoint value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: DataPoint.idx_datapoint value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20040) as session:
        rows = session.query(DataPoint.idx_datapoint).filter(
            DataPoint.checksum == _checksum.encode())

    # Return
    for row in rows:
        result = row.idx_datapoint
        break
    return result


def insert_row(_checksum, data_type, polling_interval, idx_agent):
    """Create the database DataPoint.checksum value.

    Args:
        _checksum: DataPoint value
        data_type: Type of data
        polling_interval: Polling interval
        idx_agent: Agent table index (ForeignKey)

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(_checksum, str) is True:
        # Insert and get the new checksum value
        _row = DataPoint(
            checksum=_checksum.encode(),
            polling_interval=polling_interval,
            idx_agent=idx_agent,
            data_type=data_type)
        with db.db_modify(20034, die=True) as session:
            session.add(_row)
