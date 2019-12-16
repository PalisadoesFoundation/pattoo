#!/usr/bin/env python3
"""Inserts various database values required during ingest."""

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.models import DataPoint, Glue, Pair, Agent
from pattoo.constants import ChecksumLookup


def agent_checksums(agent_id):
    """Get all the checksum values for a specific agent_id.

    Args:
        agent_id: PattooDBrecord object agent_id

    Returns:
        result: Dict of idx_datapoint values keyed by DataPoint.checksum

    """
    # Result
    result = {}
    rows = []

    # Get the data from the database
    with db.db_query(20013) as session:
        rows = session.query(
            DataPoint.checksum,
            DataPoint.last_timestamp,
            DataPoint.polling_interval,
            DataPoint.idx_datapoint).filter(and_(
                Glue.idx_datapoint == DataPoint.idx_datapoint,
                Glue.idx_pair == Pair.idx_pair,
                Agent.agent_id == agent_id.encode(),
                DataPoint.idx_agent == Agent.idx_agent
            ))

    # Return
    for row in rows:
        result[row.checksum.decode()] = ChecksumLookup(
            idx_datapoint=row.idx_datapoint,
            polling_interval=row.polling_interval,
            last_timestamp=row.last_timestamp)
    return result
