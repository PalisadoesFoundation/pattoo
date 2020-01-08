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
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/ingest') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/ingest" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import pair, datapoint
from pattoo.ingest import get


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_pairs(self):
        """Testing method / function pairs."""
        pair1 = ('key1', data.hashstring(str(random())))
        pair2 = ('key2', data.hashstring(str(random())))
        pap = 'y'

        # Create a PattooDBrecord
        record = PattooDBrecord(
            pattoo_checksum='1',
            pattoo_key='3',
            pattoo_agent_id=4,
            pattoo_agent_polling_interval=1,
            pattoo_timestamp=5,
            pattoo_data_type=DATA_FLOAT,
            pattoo_value=6,
            pattoo_agent_polled_target='x',
            pattoo_agent_program=pap,
            pattoo_agent_hostname='z',
            pattoo_metadata=[pair1, pair2]
        )

        # Pairs shouldn't exist
        self.assertFalse(pair.pair_exists(
            get.make_key(pap, pair1[0]), pair1[1]))
        self.assertFalse(pair.pair_exists(
            get.make_key(pap, pair2[0]), pair2[1]))

        # Insert items
        result = get.pairs(record)
        self.assertTrue(pair.pair_exists(
            get.make_key(pap, pair1[0]), pair1[1]))
        self.assertTrue(pair.pair_exists(
            get.make_key(pap, pair2[0]), pair2[1]))
        self.assertTrue(pair.pair_exists(
            get.make_key(pap, pair1[0]), pair1[1]) in result)
        self.assertTrue(pair.pair_exists(
            get.make_key(pap, pair2[0]), pair2[1]) in result)

    def test_key_value_pairs(self):
        """Testing method / function key_value_pairs."""
        # Create a PattooDBrecord
        record = PattooDBrecord(
            pattoo_checksum='1',
            pattoo_key='3',
            pattoo_agent_polling_interval=1,
            pattoo_agent_id=4,
            pattoo_timestamp=5,
            pattoo_data_type=DATA_FLOAT,
            pattoo_value=6,
            pattoo_agent_polled_target='x',
            pattoo_agent_program='y',
            pattoo_agent_hostname='z',
            pattoo_metadata=[('key1', 'value'), ('key2', 'value')]
        )

        # Test
        expected = [
            ('pattoo_key', 'y_3'), ('y_key1', 'value'), ('y_key2', 'value')
        ]
        result = get.key_value_pairs(record)
        self.assertEqual(sorted(result), expected)

        # Test with a list
        result = get.key_value_pairs([record])
        self.assertEqual(result, expected)

    def test_make_key(self):
        """Testing method / function make_key."""
        # Test
        expected = '7_8'
        result = get.make_key(7, 8)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
