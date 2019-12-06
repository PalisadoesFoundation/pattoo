#!/usr/bin/env python3
"""Pattoo multi-user operating system reporter daemon.

Retrieve's system data from remote host over HTTP.

"""

# Standard libraries
from __future__ import print_function
from time import sleep
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
from pattoo_shared import log
from pattoo_shared.agent import Agent, AgentCLI
from pattoo.constants import PATTOO_INGESTERD_NAME, PATTOO_INGESTER_SCRIPT
from pattoo.configuration import ConfigIngester as Config


class PollingAgent(Agent):
    """Agent that gathers data."""

    def __init__(self, parent):
        """Initialize the class.

        Args:
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        Agent.__init__(self, parent)

    def query(self):
        """Query all remote devices for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        config = Config()
        interval = config.ingester_interval()

        # Post data to the remote server
        while True:
            # Say what we are doing
            script = '{}{}{}'.format(
                _BIN_DIRECTORY, os.sep, PATTOO_INGESTER_SCRIPT)
            log_message = ('''\
Starting ingester script {}. Interval of {}s.'''.format(script, interval))
            log.log2info(20020, log_message)

            # Sleep
            sleep(interval)


def main():
    """Start the pattoo agent.

    Args:
        None

    Returns:
        None

    """
    # Poll
    agent_poller = PollingAgent(PATTOO_INGESTERD_NAME)

    # Do control
    cli = AgentCLI()
    cli.control(agent_poller)


if __name__ == "__main__":
    log.env()
    main()
