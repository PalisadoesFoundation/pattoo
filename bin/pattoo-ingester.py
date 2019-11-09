#!/usr/bin/env python3
"""Pattoo agent data cache ingester.

Used to add data to backend database

"""

# Standard libraries
import sys
import os

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
from pattoo_shared.constants import PATTOO_API_AGENT_EXECUTABLE
from pattoo_shared.configuration import Config
from pattoo_shared import files
from pattoo_shared import log
from pattoo_shared import converter
from pattoo_shared.variables import AgentPolledData

from pattoo.ingest import data

def main():
    """Ingest data.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    agent_id_rows = {}
    muliprocessing_data = []
    script = os.path.realpath(__file__)
    count = 0
    fileage = 10
    files_per_batch = 5

    # Log what we are doing
    log_message = 'Running script {}.'.format(script)
    log.log2info(21003, log_message)

    # Get cache directory
    config = Config()
    directory = config.agent_cache_directory(PATTOO_API_AGENT_EXECUTABLE)

    # Process the files in batches to reduce the database connection count
    # This can cause errors
    while True:
        # Initialize list of files that have been processed
        filepaths = []

        # Read data from cache
        directory_data = files.read_json_files(
            directory, die=False, age=fileage, count=files_per_batch)
        if bool(directory_data) is False:
            break

        # Log what we are doing
        log_message = 'Processing {} of {} cache files.'.format(
            files_per_batch, len(os.listdir(directory)))
        log.log2info(21009, log_message)

        # Read data into a list of tuples
        # [(filepath, AgentPolledData obj),
        #    (filepath, AgentPolledData obj) ...]
        for filepath, json_data in sorted(directory_data):
            # Get data from JSON file
            apd = converter.convert(json_data)
            filepaths.append(filepath)

            # Convert data in JSON file to rows of
            # PattooShared.constants.PattooDBrecord objects
            if isinstance(apd, AgentPolledData) is True:
                if apd.valid is True:
                    # Create an entry to store time sorted data from each agent
                    if apd.agent_id not in agent_id_rows:
                        agent_id_rows[apd.agent_id] = []

                    # Get data from agent and append it
                    rows = converter.extract(apd)
                    agent_id_rows[apd.agent_id].extend(rows)
                    count += len(rows)

        # Multiprocess the data
        for _, item in sorted(agent_id_rows.items()):
            muliprocessing_data.append(item)
        data.mulitiprocess(muliprocessing_data)

        # Delete source files after processing
        for filepath in filepaths:
            os.remove(filepath)

    # Print result
    log_message = (
        'Script {} completed. {} records processed.'.format(script, count))
    log.log2info(21004, log_message)


if __name__ == '__main__':
    main()
