#!/usr/bin/env python3
"""Pattoo agent data cache ingester.

Used to add data to backend database

"""

# Standard libraries
import sys
import os
import time
import argparse

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _BIN_DIRECTORY.endswith('/pattoo/bin') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Pattoo libraries
from pattoo_shared.configuration import Config
from pattoo_shared import files
from pattoo_shared import daemon
from pattoo_shared import log
from pattoo_shared import converter
from pattoo_shared.constants import PATTOO_API_AGENT_EXECUTABLE

from pattoo.ingest import data


def main():
    """Ingest data.

    Args:
        None

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
    script = os.path.realpath(__file__)
    records = 0
    fileage = 10
    start = int(time.time())
    looptime = 0
    files_read = 0

    # Get cache directory
    config = Config()
    directory = config.agent_cache_directory(PATTOO_API_AGENT_EXECUTABLE)

    # Get the CLI arguments
    args = arguments(config)
    files_per_batch = args.batch_size
    max_duration = args.duration

    # Log what we are doing
    log_message = 'Running script {}.'.format(script)
    log.log2info(21003, log_message)

    # Get the number of files in the directory
    files_found = len(
        [_ for _ in os.listdir(directory) if _.endswith('.json')])

    # Create lockfile
    lock()

    # Process the files in batches to reduce the database connection count
    # This can cause errors
    while True:
        # Agents constantly update files. We don't want an infinite loop
        # situation where we always have files available that are newer than
        # the desired fileage.
        loopstart = time.time()
        _fileage = max(fileage, (looptime * 2) + fileage)

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

        # Read data from cache
        directory_data = files.read_json_files(
            directory, die=False, age=_fileage, count=files_per_batch)
        if bool(directory_data) is False:
            break

        # Log what we are doing
        files_to_process = len(os.listdir(directory))
        log_message = 'Processing {} of {} cache files.'.format(
            min(files_per_batch, files_to_process), files_to_process)
        log.log2info(21009, log_message)

        # Process the data
        count = process(directory_data)

        # Get the records processed, looptime and files read
        records += count
        looptime = max(time.time() - loopstart, looptime)
        files_read += len(directory_data)

    # Print result
    stop = int(time.time())
    duration = stop - start
    if bool(records) is True and bool(duration) is True:
        log_message = ('''\
Agent cache ingest completed. {0} records processed in {1} seconds, {2:.2f} \
records / second. {3} files read. \
'''.format(records, duration, records / duration, files_read))
        log.log2info(21004, log_message)
    else:
        log_message = 'No files found to ingest'
        log.log2info(20021, log_message)

    # Delete lockfile
    lock(delete=True)


def process(directory_data):
    """Ingest data.

    Args:
        directory_data: List of tuples from pattoo_shared.read_json_files

    Returns:
        None

    """
    # Initialize list of files that have been processed
    filepaths = []
    _cache = {}
    count = 0
    muliprocessing_data = []

    # Read data from files
    for filepath, json_data in sorted(directory_data):
        # Log what we are doing
        log_message = 'Processing cache file {}.'.format(filepath)
        log.log2debug(20004, log_message)
        filepaths.append(filepath)

        # Get data from JSON file. Convert to rows of key-pairs
        if bool(json_data) is True and isinstance(json_data, list) is True:
            if len(json_data) == 2:
                (data_source, polled_data) = json_data
                keypairs = converter.cache_to_keypairs(
                    data_source, polled_data)
                count += len(keypairs)
                if data_source in _cache:
                    _cache[data_source].extend(keypairs)
                else:
                    _cache[data_source] = keypairs

    # Multiprocess the data
    for _, item in sorted(_cache.items()):
        muliprocessing_data.append(item)
    data.mulitiprocess(muliprocessing_data)

    # Delete source files after processing
    for filepath in filepaths:
        log_message = 'Deleting cache file {}'.format(filepath)
        log.log2debug(20009, log_message)
        if os.path.exists(filepath):
            os.remove(filepath)

    # Return
    return count


def lock(delete=False):
    """Create a lock file.

    Args:
        delete: Delete the file if true

    Returns:
        None

    """
    # Initialize key variables
    agent_name = 'pattoo-ingester'
    lockfile = daemon.lock_file(agent_name)

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
        os.remove(lockfile)


def arguments(config):
    """Get the CLI arguments.

    Args:
        config:
            Config object

    Returns:
        args: NamedTuple of argument values


    """
    # Get cache directory
    directory = config.agent_cache_directory(PATTOO_API_AGENT_EXECUTABLE)

    # Get arguments
    parser = argparse.ArgumentParser(
        description='''\
Program to ingest cached agent data from the {} directory into the database.\
'''.format(directory)
    )

    parser.add_argument(
        '-b', '--batch_size',
        default=500,
        type=int,
        help='''\
The number of files to process at a time. Smaller batch sizes may help when \
you are memory or database connection constrained. Default=500''')

    parser.add_argument(
        '-d', '--duration',
        default=3600,
        type=int,
        help='''\
The maximum time in seconds that the script should run. This reduces the risk \
of not keeping up with the cache data updates. Default=3600''')

    # Return
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
