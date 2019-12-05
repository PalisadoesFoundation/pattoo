#!/usr/bin/env python3
"""Pattoo WSGI script.

Serves as a Gunicorn WSGI entry point for pattoo-api

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
from pattoo_shared import log
from pattoo_shared.variables import AgentAPIVariable
from pattoo_shared.agent import Agent, AgentCLI, AgentAPI
from pattoo.constants import (
    PATTOO_API_AGENT_EXECUTABLE, PATTOO_API_AGENT_PROXY)
from pattoo.configuration import ConfigAgent as Config
from pattoo.api.agents import PATTOO_API_AGENT


def main():
    """Main function to start the Gunicorn WSGI."""
    # Get PID filenename for Gunicorn
    agent_gunicorn = Agent(PATTOO_API_AGENT_PROXY)

    # Get configuration
    config = Config()
    aav = AgentAPIVariable(
        ip_bind_port=config.ip_bind_port(),
        ip_listen_address=config.ip_listen_address())
    agent_api = AgentAPI(
        PATTOO_API_AGENT_EXECUTABLE,
        PATTOO_API_AGENT_PROXY,
        aav,
        PATTOO_API_AGENT)

    # Do control (API first, Gunicorn second)
    cli = AgentCLI()
    cli.control(agent_api)
    cli.control(agent_gunicorn)


if __name__ == '__main__':
    log.env()
    main()
