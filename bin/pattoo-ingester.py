#!/usr/bin/env python3
"""Pattoo agent data cache ingester.

Used to add data to backend database

"""

# Standard libraries
import sys
import os
from pprint import pprint

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
    result = []
    agent_id_rows = {}
    muliprocessing_data = []
    filepath = None
    count = 0

    # Read data from cache
    config = Config()
    directory = config.agent_cache_directory(PATTOO_API_AGENT_EXECUTABLE)
    directory_data = files.read_json_files(directory, die=False)

    # Read data into a list of tuples
    # [(filepath, AgentPolledData obj), (filepath, AgentPolledData obj) ...]
    for filepath, json_data in directory_data:
        apd = converter.convert(json_data)
        if isinstance(apd, AgentPolledData) is True:
            if apd.valid is True:
                # Create an entry to store time sorted data from each agent
                if apd.agent_id not in agent_id_rows:
                    agent_id_rows[apd.agent_id] = []

                # Get data from agent and append it
                rows = converter.extract(apd)
                # print(rows)
                agent_id_rows[apd.agent_id].extend(rows)
                result.append((filepath, apd))
                count += len(rows)

    # Multiprocess the data
    for _, item in sorted(agent_id_rows.items()):
        muliprocessing_data.append(item)
    data.mulitiprocess(muliprocessing_data)

    # Print result
    print('\n{} records processed.\n'.format(count))


if __name__ == '__main__':
    main()
