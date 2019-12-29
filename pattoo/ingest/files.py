#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Standard imports
import os
import time


# Import project libraries
from pattoo_shared import log, files, converter
from pattoo.configuration import ConfigIngester as Config
from pattoo.constants import PATTOO_API_AGENT_NAME, PATTOO_INGESTER_NAME
from .records import Records


class Cache(object):
    """Process ingest cache data."""

    def __init__(self, batch_size=500, age=0):
        """Initialize the class.

        Args:
            batch_size: Number of files to read
            age: Minimum age of files to be read per batch

        Returns:
            None

        """
        # Get cache directory
        config = Config()
        directory = config.agent_cache_directory(PATTOO_API_AGENT_NAME)
        self._batch_id = int(time.time() * 1000)

        # Read data from cache. Stop if there is no data found.
        self._data = files.read_json_files(
            directory, die=False, age=age, count=batch_size)

        # Save the number of files read
        self.files = len(self._data)

    def records(self):
        """Create PattooDBrecord objects from cache directory.

        Args:
            None

        Returns:
            result: List of list of PattooDBrecord objects grouped by agent_id

        """
        # Initialize list of files that have been processed
        _cache = {}
        result = []

        # Read data from files
        for filepath, json_data in sorted(self._data):
            # Get data from JSON file. Convert to rows of key-pairs
            if bool(json_data) is True and isinstance(json_data, dict) is True:
                pdbrs = converter.cache_to_keypairs(json_data)
                if bool(pdbrs) is False:
                    log_message = ('''\
File {} has invalid data. It will not be processed'''.format(filepath))
                    log.log2info(20026, log_message)
                    continue

                # Group data by agent_id
                pattoo_agent_id = pdbrs[0].pattoo_agent_id
                if pattoo_agent_id in _cache:
                    _cache[pattoo_agent_id].extend(pdbrs)
                else:
                    _cache[pattoo_agent_id] = pdbrs

        # Aggregate data
        if bool(_cache) is True:
            for _, item in sorted(_cache.items()):
                result.append(item)

        # Return
        return result

    def purge(self):
        """Purge cache files.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        filepaths = [filepath for filepath, _ in self._data]

        # Delete cache files after processing
        for filepath in filepaths:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    log_message = ('''\
Error deleting cache file {}.'''.format(filepath))
                    log.log2warning(20110, log_message)

    def ingest(self):
        """Ingest cache data into the database.

        Args:
            None

        Returns:
            records: Number of records processed

        """
        # Log
        log_message = ('''\
Processing ingest cache files. Batch ID: {}'''.format(self._batch_id))
        log.log2debug(20004, log_message)

        # Process
        _data = self.records()
        _records = Records(_data)
        _records.ingest()
        self.purge()

        # Log
        log_message = ('''\
Finished processing ingest cache files. Batch ID: {}'''.format(self._batch_id))
        log.log2debug(20117, log_message)

        # Determine the number of key pairs read
        records = 0
        for item in _data:
            records += len(item)
        return records


def process_cache(batch_size=500, max_duration=3600, fileage=10):
    """Ingest data.

    Args:
        batch_size: Number of files to process at a time
        max_duration: Maximum duration
        fileage: Minimum age of files to be processed in seconds

    Returns:
        None

    Method:
        1) Read the files in the cache directory older than a threshold
        2) Process the data in the files
        3) Repeat, if new files are found that are older than the threshold,
           or we have been running too long.

        Batches of files are read to reduce the risk of overloading available
        memory, and ensure we can exit if we are running too long.

    """
    # Initialize key variables
    records = 0
    start = time.time()
    looptime = 0
    files_read = 0

    # Get cache directory
    config = Config()
    directory = config.agent_cache_directory(PATTOO_API_AGENT_NAME)

    # Log what we are doing
    log_message = 'Processing ingest cache.'
    log.log2info(20085, log_message)

    # Get the number of files in the directory
    files_found = len(
        [_ for _ in os.listdir(directory) if _.endswith('.json')])

    # Create lockfile.
    _lock()

    # Process the files in batches to reduce the database connection count
    # This can cause errors
    while True:
        # Agents constantly update files. We don't want an infinite loop
        # situation where we always have files available that are newer than
        # the desired fileage.
        loopstart = time.time()
        fileage = fileage + looptime

        # Automatically stop if we are going on too long.(1 of 2)
        duration = loopstart - start
        if duration > max_duration:
            log_message = ('''\
Stopping ingester after exceeding the maximum runtime duration of {}s. \
This can be adjusted on the CLI.'''.format(max_duration))
            log.log2info(20022, log_message)
            break

        # Automatically stop if we are going on too long.(2 of 2)
        if files_read >= files_found:
            # No need to log. This is an expected outcome.
            break

        # Read data from cache. Stop if there is no data found.
        cache = Cache(batch_size=batch_size, age=fileage)
        count = cache.ingest()

        # Automatically stop if we are going on too long.(2 of 2)
        if bool(cache.files) is False:
            # No need to log. This is an expected outcome.
            break

        # Get the records processed, looptime and files read
        records += count
        files_read += cache.files
        looptime = max(time.time() - loopstart, looptime)

    # Print result
    duration = time.time() - start
    if bool(records) is True and bool(duration) is True:
        log_message = ('''\
Agent cache ingest completed. {0} records processed in {1:.2f} seconds, \
{2:.2f} records / second. {3} files read. \
'''.format(records, duration, records / duration, files_read))
        log.log2info(20084, log_message)
    else:
        log_message = 'No files found to ingest'
        log.log2info(20021, log_message)

    # Delete lockfile
    _lock(delete=True)


def _lock(delete=False):
    """Create a lock file.

    Args:
        delete: Delete the file if true

    Returns:
        None

    """
    # Initialize key variables
    config = Config()
    lockfile = files.lock_file(PATTOO_INGESTER_NAME, config)

    # Lock
    if bool(delete) is False:
        if os.path.exists(lockfile) is True:
            log_message = ('''\
Lockfile {} exists. Will not start ingester script. Is another Ingester \
instance running? If not, delete the lockfile and rerun this script.\
'''.format(lockfile))
            log.log2die(20023, log_message)
        else:
            open(lockfile, 'a').close()
    else:
        if os.path.exists(lockfile) is True:
            try:
                os.remove(lockfile)
            except:
                log_message = ('Error deleting lockfile {}.'.format(lockfile))
                log.log2warning(20107, log_message)
        else:
            log_message = ('Lockfile {} not found.'.format(lockfile))
            log.log2warning(20108, log_message)
