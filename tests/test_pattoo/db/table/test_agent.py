#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/db/table') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/db/table" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import agent, agent_group
from pattoo.db.models import Agent
from pattoo.db import db


class TestBasicFunctioins(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_idx_exists(self):
        """Testing method / function idx_exists."""
        # Add an entry to the database
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)

        # Make sure it exists
        idx_agent = agent.exists(agent_id, agent_target)

        # Verify the index exists
        result = agent.idx_exists(idx_agent)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method / function exists."""
        # Create a description
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))

        # Make sure it does not exist
        result = agent.exists(agent_id, agent_target)
        self.assertFalse(bool(result))

        # Add database row
        agent.insert_row(agent_id, agent_target, agent_program)

        # Make sure it exists
        result = agent.exists(agent_id, agent_target)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Add an entry to the database
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)

        # Make sure it exists
        idx_agent = agent.exists(agent_id, agent_target)

        # Verify the index exists
        result = agent.idx_exists(idx_agent)
        self.assertTrue(result)

    def test_assign(self):
        """Testing method / function assign."""
        # Create a new AgentGroup entry
        description = data.hashstring(str(random()))
        agent_group.insert_row(description)
        idx_agent_group = agent_group.exists(description)

        # Prepare for adding an entry to the database
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))

        # Make sure it does not exist
        result = agent.exists(agent_id, agent_target)
        self.assertFalse(bool(result))

        # Add an entry to the database
        agent_group.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Get current idx_agent for the agent
        with db.db_query(20001) as session:
            result = session.query(Agent.idx_agent_group).filter(
                Agent.idx_agent == idx_agent).one()
        idx_original = result.idx_agent_group
        self.assertNotEqual(idx_agent_group, idx_original)

        # Assign
        agent.assign(idx_agent, idx_agent_group)

        # Get current idx_agent_group for the agent group
        with db.db_query(20099) as session:
            result = session.query(Agent.idx_agent_group).filter(
                Agent.idx_agent == idx_agent).one()
        idx_new = result.idx_agent_group
        self.assertEqual(idx_agent_group, idx_new)

    def test_idx_pair_xlate_group(self):
        """Testing method / function idx_pair_xlate_group."""
        pass

    def test_cli_show_dump(self):
        """Testing method / function cli_show_dump."""
        # Add an entry to the database
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)

        # Make sure it exists
        idx_agent = agent.exists(agent_id, agent_target)

        result = agent.cli_show_dump()
        for item in result:
            if item.idx_agent == idx_agent:
                self.assertEqual(item.agent_target, agent_target)
                self.assertEqual(item.agent_program, agent_program)
                break


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
