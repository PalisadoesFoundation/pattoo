#!/usr/bin/env python3
"""Pattoo multi-user operating system reporter daemon.

Retrieve's system data from remote host over HTTP.

"""

# Standard libraries
from __future__ import print_function
from time import sleep, time
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
from pattoo_shared import files
from pattoo_shared.agent import Agent, AgentCLI
from pattoo.constants import PATTOO_INGESTERD_NAME, PATTOO_INGESTER_SCRIPT
from pattoo.configuration import ConfigIngester as Config
from pattoo import sysinfo


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
        """Query all remote targets for data.

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
            # Get start time
            ts_start = time()

            # Say what we are doing
            script = '{}{}{}'.format(
                _BIN_DIRECTORY, os.sep, PATTOO_INGESTER_SCRIPT)
            log_message = ('''\
Starting ingester script {}. Interval of {}s.'''.format(script, interval))
            log.log2info(20020, log_message)

            # Check lockfile status
            _running = check_lockfile()

            # Process
            if _running is False:
                result = files.execute(script, die=False)
                if bool(result) is True:
                    log_message = ('''\
    Ingester failed to run. Please check log files for possible causes.''')
                    log.log2warning(20029, log_message)
            else:
                log_message = ('''\
Ingester is unexpectedly still running. Check your parameters of error logs \
for possible causes.''')
                log.log2warning(20129, log_message)

            # Sleep. The duration could exceed the polling interval. Set sleep
            # time to the polling interval when this occurs.
            duration = time() - ts_start
            if duration > interval:
                log_message = ('''Ingestion exceeded configured \
"ingester_interval" parameter by {:6.2f}s.'''.format(duration - interval))
            sleep_time = min(interval, abs(interval - duration))
            log_message = (
                'Ingester sleeping for {:6.2f}s.'.format(sleep_time))
            log.log2info(20100, log_message)
            sleep(sleep_time)


def check_lockfile():
    """Delete lockfile if found and ingester is not running.

    Args:
        None

    Returns:
        running: True if ingester script is running

    """
    # Initialize key variables
    agent_name = 'pattoo_ingester'
    config = Config()
    lockfile = files.lock_file(agent_name, config)

    # Script running
    running = sysinfo.process_running(PATTOO_INGESTER_SCRIPT)

    # Delete lockfile if found and ingester is not running.
    # Caused by possible crash.
    if os.path.exists(lockfile) is True and running is False:
        os.remove(lockfile)
        log_message = ('''\
Lock file {} found, but the {} script is not running\
'''.format(lockfile, PATTOO_INGESTER_SCRIPT))
        log.log2warning(20030, log_message)

    return running


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
