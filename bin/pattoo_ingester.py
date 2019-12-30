#!/usr/bin/env python3
"""Pattoo agent data cache ingester.

Used to add data to backend database

"""

# Standard libraries
import sys
import os
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
from pattoo_shared import log
from pattoo_shared import converter
from pattoo.constants import PATTOO_API_AGENT_NAME

from pattoo.ingest import files


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
    # Process cache
    args = arguments()
    success = files.process_cache(
        batch_size=args.batch_size, max_duration=args.max_duration)
    sys.exit(int(not success))


def arguments():
    """Get the CLI arguments.

    Args:
        None

    Returns:
        args: NamedTuple of argument values


    """
    # Get config
    config = Config()

    # Get cache directory
    directory = config.agent_cache_directory(PATTOO_API_AGENT_NAME)

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
        '-m', '--max_duration',
        default=3600,
        type=int,
        help='''\
The maximum time in seconds that the script should run. This reduces the risk \
of not keeping up with the cache data updates. Default=3600''')

    # Return
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    log.env()
    main()
