#!/usr/bin/env python3
"""Inserts various database values required during ingest."""

# PIP3 imports
import numpy as np
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import and_

from pattoo_shared import times
from pattoo_shared.constants import (
    DATA_INT, DATA_FLOAT, DATA_COUNT64, DATA_COUNT)

# Import project libraries
from pattoo.db import db
from pattoo.db.models import DataPoint as _DataPoint
from pattoo.db.models import Data
from pattoo.db.table import agent


class DataPoint(object):
    """Get data relevant to a DataPoint entry in the database."""

    def __init__(self, _idx_datapoint):
        """Instantiate the class.

        Args:
            idx_datapoint: DataPoint index

        Returns:
            None

        """
        # Initialize key variables
        found = False
        self._idx_datapoint = int(_idx_datapoint)

        # Initialize keys for use by methods
        self._result = {}
        keys = [
            'idx_agent', 'checksum ', 'data_type', 'last_timestamp ',
            'polling_interval', 'enabled']
        for key in keys:
            self._result[key] = None

        try:
            # Deal with that as well
            with db.db_query(20028) as session:
                row = session.query(_DataPoint).filter(
                    _DataPoint.idx_datapoint == self._idx_datapoint).one()
                found = True
        except MultipleResultsFound as _:
            pass
        except NoResultFound as _:
            pass

        # Massage data
        if found is True:
            # Assign values
            self._result['idx_agent'] = row.idx_agent
            self._result['checksum'] = row.checksum.decode()
            self._result['data_type'] = row.data_type
            self._result['exists'] = True
            self._result['last_timestamp'] = row.last_timestamp
            self._result['polling_interval'] = row.polling_interval
            self._result['enabled'] = row.enabled

    def enabled(self):
        """Get enabled status.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self._result['enabled']
        return value

    def idx_agent(self):
        """Get idx_agent status.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self._result['idx_agent']
        return value

    def checksum(self):
        """Get checksum status.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self._result['checksum']
        return value

    def data_type(self):
        """Get data_type status.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self._result['data_type']
        return value

    def exists(self):
        """Get exists status.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self._result['exists']
        return value

    def last_timestamp(self):
        """Return list of cabinet IDs for customer.

        Args:
            None

        Returns:
            value: value to return


        """
        # Initialize key variables
        value = self._result['last_timestamp']
        return value

    def polling_interval(self):
        """Return current commit ID for customer.

        Args:
            None

        Returns:
            value: value to return


        """
        # Initialize key variables
        value = self._result['polling_interval']
        return value

    def data(self, ts_start, ts_stop):
        """Create list of dicts of counter values retrieved from database.

        Args:
            ts_start: Start time for query
            ts_stop: Stop time for query

        Returns:
            result: List of key-value pair dicts

        """
        # Initialize key variables
        data_type = self.data_type()
        _pi = self.polling_interval()
        places = 10
        result = []

        # Return nothing if the DataPoint does not exist
        if self.exists() is False:
            return result

        # Make sure we have entries for entire time range
        timestamps = times.timestamps(ts_start, ts_stop, _pi)
        nones = {_key: None for _key in timestamps}

        # Get data from database
        with db.db_query(20092) as session:
            rows = session.query(Data.timestamp, Data.value).filter(and_(
                Data.timestamp <= ts_stop, Data.timestamp >= ts_start,
                Data.idx_datapoint == self._idx_datapoint)).order_by(
                    Data.timestamp).all()

        # Put values into a dict for ease of processing
        for row in rows:
            # Find the first timestamp in the sorted list that is greater than
            # that found in the database
            timestamp = times.normalized_timestamp(_pi, row.timestamp)
            rounded_value = round(float(row.value), places)
            nones[timestamp] = rounded_value

        if data_type in [DATA_INT, DATA_FLOAT]:
            # Process non-counter values
            result = _response(nones)

        elif data_type in [DATA_COUNT64, DATA_COUNT] and len(rows) > 1:
            # Process counter values by calculating the difference between
            # successive values
            result = _counters(nones, _pi, places)

        return result


def _counters(nones, polling_interval, places):
    """Create list of dicts of counter values retrieved from database.

    Args:
        nones: Dict of values keyed by timestamp
        polling_interval: Polling interval
        places: Number of places to round values

    Returns:
        result: List of key-value pair dicts

    """
    # Initialize key variables
    final = {}

    # Create list of timestamps and values
    timestamps = []
    values = []
    for timestamp, value in sorted(nones.items()):
        timestamps.append(timestamp)
        values.append(value)

    # Remove first timestamp value as it isn't necessary
    # after deltas are created
    timestamps = timestamps[1:]

    # Create an array for ease of readability.
    # Convert to None values to nans to make deltas without errors
    values_array = np.array(values).astype(np.float)

    '''
    Sometimes we'll get unsigned counter values in the database that roll over
    to zero. This result in a negative delta.

    We convert the result to abs(result). Python3 integers have no size limit
    so you can't use logic like this to fix it:

    (value.current + integer.type.max - value.previous)

    '''
    deltas = np.abs(np.diff(values_array))
    for key, delta in enumerate(deltas):
        # Null values means absent data and therefore no change
        if np.isnan(delta):
            tps = None
        else:
            # Calculate the value as a transaction per second value
            tps = round((delta / polling_interval) * 1000, places)
        final[timestamps[key]] = tps

    # Return the result
    result = _response(final)
    return result


def _response(nones):
    """Create list of dicts.

    Args:
        nones: Dict of values keyed by timestamp

    Returns:
        result: List of key-value pair dicts

    """
    # Return a list of dicts
    result = []
    for timestamp, value in sorted(nones.items()):
        result.append({'timestamp': timestamp, 'value': value})
    return result


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
    """Get the db _DataPoint.idx_datapoint value for specific checksum.

    Args:
        checksum: PattooShared.converter.extract NamedTuple checksum

    Returns:
        result: _DataPoint.idx_datapoint value

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20040) as session:
        rows = session.query(_DataPoint.idx_datapoint).filter(
            _DataPoint.checksum == _checksum.encode())

    # Return
    for row in rows:
        result = row.idx_datapoint
        break
    return result


def insert_row(_checksum, data_type, polling_interval, idx_agent):
    """Create the database _DataPoint.checksum value.

    Args:
        _checksum: _DataPoint value
        data_type: Type of data
        polling_interval: Polling interval
        idx_agent: Agent table index (ForeignKey)

    Returns:
        None

    """
    # Filter invalid data
    if isinstance(_checksum, str) is True:
        # Insert and get the new checksum value
        _row = _DataPoint(
            checksum=_checksum.encode(),
            polling_interval=polling_interval,
            idx_agent=idx_agent,
            data_type=data_type)
        with db.db_modify(20034, die=True) as session:
            session.add(_row)
