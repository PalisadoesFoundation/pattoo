#!/usr/bin/env python3
"""Pattoo WSGI script.

Serves as a Gunicorn WSGI entry point for pattoo-os

"""

# Standard libraries
from __future__ import print_function
import sys
import os

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _BIN_DIRECTORY.endswith('/pattoo-agents/bin') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo-agents/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Pattoo libraries
from pattooagents.agent import Agent, AgentAPI, AgentCLI
from pattooagents.constants import PATTOO_OS_SPOKED, PATTOO_OS_SPOKED_PROXY
from pattooagents.agents.os import configuration
from pattooagents.agents.os.api import API


def main():
    """Control the Gunicorn WSGI."""
    # Create Gunicorn object to daemonize
    agent_api = Agent(PATTOO_OS_SPOKED_PROXY)

    # Create Flask object to daemonize
    config = configuration.ConfigSpoked()
    agent_gunicorn = AgentAPI(
        PATTOO_OS_SPOKED, PATTOO_OS_SPOKED_PROXY, config, API)

    # Do control (Gunicorn first, Daemonized query second)
    cli = AgentCLI()
    cli.control(agent_gunicorn)
    cli.control(agent_api)


if __name__ == '__main__':
    main()
