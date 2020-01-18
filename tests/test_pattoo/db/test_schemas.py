#!/usr/bin/env python3
"""Testing pattoo/db/db.py."""

import os
import unittest
import sys
import collections


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR,
            os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/db') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/db" \
directory. Please fix.''')
    sys.exit(2)


from tests.libraries.configuration import UnittestConfig
from pattoo.db import schemas


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test_resolve_checksum(self):
        """Testing method / function resolve_checksum."""
        # Test
        Tester = collections.namedtuple('Tester', 'checksum')
        expected = 'test'.encode()
        obj = Tester(checksum=expected)
        result = schemas.resolve_checksum(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_key(self):
        """Testing method / function resolve_key."""
        # Test
        Tester = collections.namedtuple('Tester', 'key')
        expected = 'test'.encode()
        obj = Tester(key=expected)
        result = schemas.resolve_key(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_value(self):
        """Testing method / function resolve_value."""
        # Test
        Tester = collections.namedtuple('Tester', 'value')
        expected = 'test'.encode()
        obj = Tester(value=expected)
        result = schemas.resolve_value(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_translation(self):
        """Testing method / function resolve_translation."""
        # Test
        Tester = collections.namedtuple('Tester', 'translation')
        expected = 'test'.encode()
        obj = Tester(translation=expected)
        result = schemas.resolve_translation(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_name(self):
        """Testing method / function resolve_name."""
        # Test
        Tester = collections.namedtuple('Tester', 'name')
        expected = 'test'.encode()
        obj = Tester(name=expected)
        result = schemas.resolve_name(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_agent_id(self):
        """Testing method / function resolve_agent_id."""
        # Test
        Tester = collections.namedtuple('Tester', 'agent_id')
        expected = 'test'.encode()
        obj = Tester(agent_id=expected)
        result = schemas.resolve_agent_id(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_agent_program(self):
        """Testing method / function resolve_agent_program."""
        # Test
        Tester = collections.namedtuple('Tester', 'agent_program')
        expected = 'test'.encode()
        obj = Tester(agent_program=expected)
        result = schemas.resolve_agent_program(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_agent_polled_target(self):
        """Testing method / function resolve_agent_polled_target."""
        # Test
        Tester = collections.namedtuple('Tester', 'agent_polled_target')
        expected = 'test'.encode()
        obj = Tester(agent_polled_target=expected)
        result = schemas.resolve_agent_polled_target(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_code(self):
        """Testing method / function resolve_code."""
        # Test
        Tester = collections.namedtuple('Tester', 'code')
        expected = 'test'.encode()
        obj = Tester(code=expected)
        result = schemas.resolve_code(obj, None)
        self.assertEqual(result, expected.decode())

    def test_resolve_filter_pair_xlate_key(self):
        """Testing method / function resolve_filter_pair_xlate_key."""
        pass

    def test_resolve_keys(self):
        """Testing method / function resolve_keys."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
