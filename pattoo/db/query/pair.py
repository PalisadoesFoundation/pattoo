#!/usr/bin/env python3
"""Pattoo classes querying the Pair table."""

# PIP libraries
from sqlalchemy import and_

# Import project libraries
from pattoo.db import db
from pattoo.db.tables import Glue, Pair


class PairDataPoint(object):
    """Class gathers key-pair information based on DataPoint index."""

    def __init__(self, idx_datapoint):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        rows = []
        self._pairs = {}

        # Get the ke-value pairs
        with db.db_query(20003) as session:
            rows = session.query(Pair.key, Pair.value).filter(and_(
                Glue.idx_datapoint == idx_datapoint,
                Pair.idx_pair == Glue.idx_pair))

        for row in rows:
            self._pairs[row.key.decode()] = row.value.decode()

    def pairs(self):
        """Provide key-value pairs.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        result = [{key: value} for key, value in sorted(self._pairs.items())]
        return result
