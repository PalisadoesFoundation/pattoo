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
from pattoo.db.table import agent_group, pair_xlate_group
from pattoo.db.models import AgentGroup
from pattoo.db import db


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_idx_exists(self):
        """Testing method / function idx_exists."""
        # Add an entry to the database
        name = data.hashstring(str(random()))
        agent_group.insert_row(name)

        # Make sure it exists
        idx_agent_group = agent_group.exists(name)

        # Verify the index exists
        result = agent_group.idx_exists(idx_agent_group)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method / function exists."""
        # Create a name
        name = data.hashstring(str(random()))

        # Make sure it does not exist
        result = agent_group.exists(name)
        self.assertFalse(bool(result))

        # Add database row
        agent_group.insert_row(name)

        # Make sure it exists
        result = agent_group.exists(name)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method / function insert_row."""
        # Add an entry to the database
        name = data.hashstring(str(random()))
        agent_group.insert_row(name)

        # Make sure it exists
        idx_agent_group = agent_group.exists(name)

        # Verify the index exists
        result = agent_group.idx_exists(idx_agent_group)
        self.assertTrue(result)

    def test_update_name(self):
        """Testing method / function update_name."""
        # Add an entry to the database
        name = data.hashstring(str(random()))

        # Make sure it does not exist
        result = agent_group.exists(name)
        self.assertFalse(bool(result))

        # Add database row
        agent_group.insert_row(name)

        # Make sure it exists
        idx = agent_group.exists(name)
        self.assertTrue(bool(idx))

        # Get current name
        with db.db_query(20096) as session:
            result = session.query(AgentGroup.name).filter(
                AgentGroup.idx_agent_group == idx).one()

        # Test
        self.assertEqual(name, result.name.decode())

        # Update the name
        new_name = data.hashstring(str(random()))
        agent_group.update_name(idx, new_name)

        # Get current name
        with db.db_query(20097) as session:
            result = session.query(AgentGroup.name).filter(
                AgentGroup.idx_agent_group == idx).one()

        # Test
        self.assertEqual(new_name, result.name.decode())

    def test_assign(self):
        """Testing method / function assign."""
        # Create a new PairXlateGroup entry
        name = data.hashstring(str(random()))
        pair_xlate_group.insert_row(name)
        idx_pair_xlate_group = pair_xlate_group.exists(name)

        # Add an entry to the database
        name = data.hashstring(str(random()))
        agent_group.insert_row(name)

        # Make sure it exists
        idx_agent_group = agent_group.exists(name)

        # Get current idx_pair_xlate_group for the agent group
        with db.db_query(20095) as session:
            result = session.query(AgentGroup.idx_pair_xlate_group).filter(
                AgentGroup.idx_agent_group == idx_agent_group).one()
        idx_original = result.idx_pair_xlate_group
        self.assertNotEqual(idx_pair_xlate_group, idx_original)

        # Assign
        agent_group.assign(idx_agent_group, idx_pair_xlate_group)

        # Get current idx_pair_xlate_group for the agent group
        with db.db_query(20098) as session:
            result = session.query(AgentGroup.idx_pair_xlate_group).filter(
                AgentGroup.idx_agent_group == idx_agent_group).one()
        idx_new = result.idx_pair_xlate_group
        self.assertEqual(idx_pair_xlate_group, idx_new)

    def test_cli_show_dump(self):
        """Testing method / function cli_show_dump."""
        # Add an entry to the database
        name = data.hashstring(str(random()))
        agent_group.insert_row(name)

        # Make sure it exists
        idx_agent_group = agent_group.exists(name)

        result = agent_group.cli_show_dump()
        for item in result:
            if item.idx_agent_group == idx_agent_group:
                self.assertEqual(item.name, name)
                break


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
