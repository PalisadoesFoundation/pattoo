#!/usr/bin/env python3
"""Pattoo agent data cache ingester.

Used to add data to backend database

"""

# Standard libraries
import sys
import os
import collections
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


def main():
    """Ingest data.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    result = []
    filepath = None

    # Read data from cache
    config = Config()
    directory = config.agent_cache_directory(PATTOO_API_AGENT_EXECUTABLE)
    directory_data = files.read_json_files(directory, die=False)

    # Read data into a list of tuples
    # [(filepath, AgentPolledData obj), (filepath, AgentPolledData obj) ...]
    for filepath, json_data in directory_data:
        agentdata = converter.convert(json_data)
        if isinstance(agentdata, AgentPolledData) is True:
            if agentdata.active is True:
                result.append((filepath, agentdata))
                row = extract(agentdata)
                break

    # Show results prior to writing code to add to database.
    if bool(filepath) is True:
        print('\n{}\n'.format(filepath))
        pprint(row)


def extract(agentdata):
    """Ingest data.

    Args:
        agentdata: AgentPolledData object

    Returns:
        rows: List of named tuples containing data

    """
    # Initialize key variables
    rows = []
    datatuple = collections.namedtuple(
        'Values', '''\
agent_id agent_program agent_hostname timestamp polling_interval device
data_label data_index value data_type''')

    # Return if invalid data
    if bool(agentdata.active) is False:
        return []

    # Assign agent values
    agent_id = agentdata.agent_id
    agent_program = agentdata.agent_program
    agent_hostname = agentdata.agent_hostname
    timestamp = agentdata.timestamp
    polling_interval = agentdata.polling_interval
    agent_program = agentdata.agent_program

    # Cycle through the data
    for dvh in agentdata.data:
        # Ignore bad data
        if dvh.active is False:
            continue

        # Get data
        device = dvh.device
        for _dv in dvh.data:
            data_label = _dv.data_label
            data_index = _dv.data_index
            value = _dv.value
            data_type = _dv.data_type

            # Assign values to tuple
            row = datatuple(
                agent_id=agent_id, agent_program=agent_program,
                agent_hostname=agent_hostname, timestamp=timestamp,
                polling_interval=polling_interval, device=device,
                data_label=data_label, data_index=data_index,
                value=value, data_type=data_type)
            rows.append(row)

    # Return
    return rows



if __name__ == '__main__':
    main()
