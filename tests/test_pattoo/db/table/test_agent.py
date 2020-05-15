#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}test_pattoo{0}db{0}table'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo_shared import data
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import agent, pair_xlate_group
from pattoo.db.models import Agent
from pattoo.db import db


class TestBasicFunctions(unittest.TestCase):
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
        # Create a translation
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
        # Add an entry to the database
        name = data.hashstring(str(random()))
        pair_xlate_group.insert_row(name)

        # Make sure it exists
        idx_pair_xlate_group = pair_xlate_group.exists(name)

        # Verify the index exists
        result = pair_xlate_group.idx_exists(idx_pair_xlate_group)
        self.assertTrue(result)

        # Prepare for adding an entry to the database
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))

        # Make sure it does not exist
        result = agent.exists(agent_id, agent_target)
        self.assertFalse(bool(result))

        # Add an entry to the database
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Assign
        agent.assign(idx_agent, idx_pair_xlate_group)

        # Get assigned idx_pair_xlate_group for the agent group
        with db.db_query(20099) as session:
            result = session.query(Agent.idx_pair_xlate_group).filter(
                Agent.idx_agent == idx_agent).one()
        idx_new = result.idx_pair_xlate_group
        self.assertEqual(idx_pair_xlate_group, idx_new)

    def test_idx_pair_xlate_group(self):
        """Testing method / function idx_pair_xlate_group."""
        # Create a new PairXlateGroup entry
        translation = data.hashstring(str(random()))
        pair_xlate_group.insert_row(translation)
        idx_pair_xlate_group = pair_xlate_group.exists(translation)

        # Add an entry to the database
        agent_id = data.hashstring(str(random()))
        agent_target = data.hashstring(str(random()))
        agent_program = data.hashstring(str(random()))
        agent.insert_row(agent_id, agent_target, agent_program)
        idx_agent = agent.exists(agent_id, agent_target)

        # Assign Agent got PairXlateGroup
        agent.assign(idx_agent, idx_pair_xlate_group)

        # Test
        result = agent.idx_pair_xlate_group(agent_id)
        self.assertEqual(result, idx_pair_xlate_group)

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
