#!/usr/bin/env python3
"""Pattoo classes querying the Pair table."""

# PIP libraries
from sqlalchemy import and_, tuple_

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


def pair_exists(key, value):
    """Get the db Pair table for key-value pair.

    Args:
        key: Key-value pair key
        value: Key-value pair value

    Returns:
        result: Pair.idx_pair value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20006) as session:
        rows = session.query(Pair.idx_pair).filter(and_(
            Pair.key == key.encode(),
            Pair.value == value.encode()
            ))

    # Return
    for row in rows:
        result = row.idx_pair
        break
    return result


def insert_rows(items):
    """Create db Pair table entries.

    Args:
        items: List of lists, or list of key-value pairs

    Returns:
        None

    """
    # Initialize key variables
    _rows = []
    uniques = {}
    all_kvs = []

    # Make list if not so
    if isinstance(items, list) is False:
        items = [items]

    # Create a single list of key-value pairs.
    # Add them to a dict to make the pairs unique.
    for item in items:
        if isinstance(item, list):
            all_kvs.extend(item)
        else:
            all_kvs.append(item)
    for _kv in all_kvs:
        uniques[_kv] = None

    # Insert the key-value pairs into the database
    for (key, value), _ in uniques.items():
        # Skip pre-existing pairs
        if bool(pair_exists(key, value)) is True:
            continue

        # Add values to list for future insertion
        _row = Pair(key=key.encode(), value=value.encode())
        _rows.append(_row)

    if bool(_rows) is True:
        with db.db_modify(20007, die=True) as session:
            session.add_all(_rows)


def idx_pairs(_items):
    """Get the db Pair table indices based on key, value pairs.

    Args:
        _items: List of (key, value) tuples

    Returns:
        result: list of Pair.idx_pair values

    """
    # Initialize key variables
    result = []

    # Encode the items
    items = [(key.encode(), value.encode()) for key, value in _items]

    # Get the data from the database
    with db.db_query(20011) as session:
        rows = session.query(
            Pair.idx_pair).filter(tuple_(Pair.key, Pair.value).in_(items))

    # Return
    for row in rows:
        result.append(row.idx_pair)
    return sorted(result)
