#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import multiprocessing
import sys
import time
import random

# PIP3 imports
import tblib.pickling_support
tblib.pickling_support.install()


# Import project libraries
from pattoo_shared.constants import DATA_NONE, DATA_STRING
from pattoo_shared import log
from pattoo.constants import IDXTimestampValue, ChecksumLookup
from pattoo.ingest import get
from pattoo.db import misc
from pattoo.db.table import pair, glue, data, datapoint
from pattoo.configuration import ConfigIngester as Config


class ExceptionWrapper(object):
    """Class to handle unexpected exceptions with multiprocessing.

    Based on:
        https://stackoverflow.com/questions/6126007/python-getting-a-traceback-from-a-multiprocessing-process

        _NOTE_ The subprocess needs to return a value for this to work.
        Returning an implicit "None" isn't sufficient

    """

    def __init__(self, error_exception):
        """Initialize the class.

        Args:
            error_exception: Exception object

        Returns:
            None

        """
        # Process
        self._error_exception = error_exception
        (self._etype, self._evalue, self._etraceback) = sys.exc_info()

    def re_raise(self):
        """Extend the re_raise method.

        Args:
            None

        Returns:
            None

        """
        # Log message
        log.log2exception(20114, (self._etype, self._evalue, self._etraceback))

        # Process traceback
        raise self._error_exception.with_traceback(self._etraceback)


class Records(object):
    """Process data using multiprocessing."""

    def __init__(self, pattoo_db_records_lists):
        """Initialize the class.

        Args:
            pattoo_db_records_lists: List of PattooDBrecord oject lists
                grouped by source and sorted by timestamp. This data is
                obtained from PattooShared.converter.extract

        Returns:
            None

        """
        # Initialize key variables
        config = Config()

        # Setup the arguments for multiprocessing
        self._arguments = [
            (_, ) for _ in pattoo_db_records_lists if bool(_) is True]
        self._multiprocess = config.multiprocessing()
        self._pool_size = multiprocessing.cpu_count()

    def multiprocess_pairs(self):
        """Update rows in the Pair database table if necessary.

        Do all multiprocessing outside of the class for consistent results
        without unexpected hanging waiting for pool.join() to happen.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        pattoo_db_records_lists_tuple = self._arguments
        pool_size = self._pool_size

        # Create a pool of sub process resources
        with multiprocessing.Pool(processes=pool_size) as pool:

            # Create sub processes from the pool
            per_process_key_value_pairs = pool.starmap(
                _process_kvps_exception, pattoo_db_records_lists_tuple)

        # Wait for all the processes to end and get results
        pool.join()

        # Test for exceptions
        for result in per_process_key_value_pairs:
            if isinstance(result, ExceptionWrapper):
                result.re_raise()

        # Update the database with key value pairs
        pair.insert_rows(per_process_key_value_pairs)

    def multiprocess_data(self):
        """Insert rows into the Data and DataPoint tables as necessary.

        Do all multiprocessing outside of the class for consistent results
        without unexpected hanging waiting for pool.join() to happen.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        pattoo_db_records_lists_tuple = self._arguments
        pool_size = self._pool_size

        # Troubleshooting log
        log_message = 'Processing {} agents from cache'.format(
            len(pattoo_db_records_lists_tuple))
        log.log2debug(20009, log_message)

        # Create a pool of sub process resources
        with multiprocessing.Pool(processes=pool_size) as pool:

            # Create sub processes from the pool
            results = pool.starmap(
                _process_data_exception, pattoo_db_records_lists_tuple)

        # Wait for all the processes to end and get results
        pool.join()

        # Test for exceptions
        for result in results:
            if isinstance(result, ExceptionWrapper):
                result.re_raise()

    def singleprocess_pairs(self):
        """Update rows in the Pair database table if necessary.

        Args:
            None

        Returns:
            None

        """
        # Process data
        pairs = []
        for item in self._arguments:
            row = item[0]
            per_process_key_value_pairs = get.key_value_pairs(row)
            pairs.append(per_process_key_value_pairs)

        # Insert
        pair.insert_rows(pairs)

    def singleprocess_data(self):
        """Insert rows into the Data and DataPoint tables as necessary.

        Args:
            None

        Returns:
            None

        """
        # Process data
        for item in self._arguments:
            row = item[0]
            process_db_records(row)

    def ingest(self):
        """Insert rows into the Data and DataPoint tables as necessary.

        Args:
            None

        Returns:
            None

        """
        # Update
        if self._multiprocess is True:
            # Process pairs
            self.multiprocess_pairs()

            # Process data
            self.multiprocess_data()

        else:
            # Process pairs
            self.singleprocess_pairs()

            # Process data
            self.singleprocess_data()


def _process_kvps_exception(pattoo_db_records):
    """Get all the key-value pairs found.

    Traps any exceptions and return them for processing. Very helpful in
    troubleshooting multiprocessing

    Args:
        pattoo_db_records: List of dicts read from cache files.

    Returns:
        None

    """
    # Initialize key variables
    result = []

    '''
    Sleep for a short random time. We have seen where on very fast systems
    SQLAlchemy will hang the creation of multiprocessing subprocesses. The
    typical behaviour is the creation of one fewer
    pattoo.db._add_engine_pidguard() log messages than agents to process.
    These messages correspond to the creation of a subprocess which immediately
    invalidates a parent process's DB connection that will cause errors
    if used, which provided the clue to the source of the problem.

    Though SQLAlchemy isn't used by key_value_pairs. It's added as a
    future precaution in case it does.
    '''
    time.sleep((random.random() / 10) + 0.1)

    # Execute
    try:
        result = get.key_value_pairs(pattoo_db_records)
    except Exception as error:
        _exception = sys.exc_info()
        log.log2exception(20133, _exception)
        return ExceptionWrapper(error)
    except:
        _exception = sys.exc_info()
        log.log2exception_die(20111, _exception)

    # Return
    return result


def _process_data_exception(pattoo_db_records):
    """Insert all data values for an agent into database.

    Traps any exceptions and return them for processing. Very helpful in
    troubleshooting multiprocessing

    Args:
        pattoo_db_records: List of dicts read from cache files.

    Returns:
        None

    """
    # Initialize

    '''
    Sleep for a short random time. We have seen where on very fast systems
    SQLAlchemy will hang the creation of multiprocessing subprocesses. The
    typical behaviour is the creation of one fewer
    pattoo.db._add_engine_pidguard() log messages than agents to process.
    These messages correspond to the creation of a subprocess which immediately
    invalidates a parent process's DB connection that will cause errors
    if used, which provided the clue to the source of the problem.
    '''
    time.sleep((random.random() / 10) + 0.1)

    # Execute
    try:
        process_db_records(pattoo_db_records)
    except Exception as error:
        _exception = sys.exc_info()
        log.log2exception(20132, _exception)
        return ExceptionWrapper(error)
    except:
        _exception = sys.exc_info()
        log.log2exception_die(20109, _exception)

    # Return
    return None


def process_db_records(pattoo_db_records):
    """Insert all data values for an agent into database.

    Args:
        pattoo_db_records: List of dicts read from cache files.

    Returns:
        None

    Method:
        1) Get all the idx_datapoint and idx_pair values that exist in the
           PattooDBrecord data from the database. All the records MUST be
           from the same source.
        2) Add these idx values to tracking memory variables for speedy lookup
        3) Ignore non numeric data values sent
        4) Add data to the database. If new checksum values are found in the
           PattooDBrecord data, then create the new index values to the
           database, update the tracking memory variables before hand.

    """
    # Initialize key variables
    _data = {}

    # Return if there is nothint to process
    if bool(pattoo_db_records) is False:
        return

    # Get DataPoint.idx_datapoint and idx_pair values from db. This is used to
    # speed up the process by reducing the need for future database access.
    agent_id = pattoo_db_records[0].pattoo_agent_id
    checksum_table = misc.agent_checksums(agent_id)

    # Process data
    for pdbr in pattoo_db_records:
        # We only want to insert non-string, non-None values
        if pdbr.pattoo_data_type in [DATA_NONE, DATA_STRING]:
            continue

        # Get the idx_datapoint value for the PattooDBrecord
        if pdbr.pattoo_checksum in checksum_table:
            # Get last_timestamp for existing idx_datapoint entry
            idx_datapoint = checksum_table[
                pdbr.pattoo_checksum].idx_datapoint
        else:
            # Entry not in database. Update the database and get the
            # required idx_datapoint
            idx_datapoint = datapoint.idx_datapoint(pdbr)
            if bool(idx_datapoint) is True:
                # Update the lookup table
                checksum_table[
                    pdbr.pattoo_checksum] = ChecksumLookup(
                        idx_datapoint=idx_datapoint,
                        polling_interval=int(
                            pdbr.pattoo_agent_polling_interval),
                        last_timestamp=1)

                # Update the Glue table
                idx_pairs = get.pairs(pdbr)
                glue.insert_rows(idx_datapoint, idx_pairs)
            else:
                continue

        # Append item to items
        if pdbr.pattoo_timestamp > checksum_table[
                pdbr.pattoo_checksum].last_timestamp:
            '''
            Add the Data table results to a dict in case we have duplicate
            posting over the API. We need to key off a unique time dependent
            value per datapoint to prevent different datapoints at the same
            point in time overwriting the value. This is specifically for
            removing duplicates for the _SAME_ datapoint at the same point in
            time as could possibly occur with the restart of an agent causing a
            double posting or network issues. We therefore use a tuple of
            idx_datapoint and timestamp.
            '''
            _data[(
                pdbr.pattoo_timestamp,
                idx_datapoint)] = IDXTimestampValue(
                    idx_datapoint=idx_datapoint,
                    polling_interval=int(pdbr.pattoo_agent_polling_interval),
                    timestamp=pdbr.pattoo_timestamp,
                    value=pdbr.pattoo_value)

    # Update the data table
    if bool(_data) is True:
        data.insert_rows(list(_data.values()))

    # Log message
    log_message = ('''\
Finished cache data processing for agent_id: {}'''.format(agent_id))
    log.log2debug(20113, log_message)
