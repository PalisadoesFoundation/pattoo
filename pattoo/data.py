#!/usr/bin/env python3
"""Pattoo classes that manage various data."""

# Import project libraries
from pattoo_shared import configuration
from pattoo_shared.configuration import Config as ConfigShared


class Ingest(object):
    """Update database with data received from agents."""

    def __init__(self, apd):
        """Initialize the class.

        Args:
            apd: AgentPolledData object

        Returns:
            None

        """
        # Initialize key variables
        self._apd = apd
        self._idx_agent = None
        self._idx_datasource = None
