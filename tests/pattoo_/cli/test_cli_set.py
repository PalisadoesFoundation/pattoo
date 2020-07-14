#!/usr/bin/env python3
"""CLI import testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse
import tempfile
import csv

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}cli'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from pattoo.cli.cli_set import (process, _process_language,
                                   _process_pair_xlate_group)
from pattoo.db import db
from pattoo.cli.cli import _Set
from pattoo.db.models import BASE, PairXlateGroup, Language

# Pattoo unittest imports
from tests.bin.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig


class TestSet(unittest.TestCase):
    """Tests CLI set module"""

    travis_ci = os.getenv('travis_ci')

    def set_fn(self):
        pass

    @classmethod
    def setUpClass(self):
        """Setup tables in pattoo_unittest database"""

        self.language_count = 1
        # Skips class setup if using travis-ci
        if not self.travis_ci:
            # Create test tables for Import test
            self.tables = [PairXlateGroup.__table__, Language.__table__]

            # Returns engine object
            self.engine = create_tables(self.tables)

            # Creating session object to make updates to tables in test
            # database
            with db.db_modify(30001) as session:
                # Instantiation of test data in each table
                session.add(Language('en'.encode(), 'English'.encode(), 1))
                session.add(PairXlateGroup('pair_1'.encode(), 1))

                self.language_count = session.query(Language).count()
                session.commit()

    @classmethod
    def tearDownClass(self):
        """End session and drop all test tables from pattoo_unittest database"""

        # Skips class teardown if using travis-ci
        if not self.travis_ci:
            teardown_tables(self.tables, self.engine)

    def test_process(self):
        """Test import argument process function"""

        # Setting up args parseer
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest='action')
        _Set(subparser)
        args = parser.parse_args([])

        # Testing for invalid args.qualifier
        args.qualifier = ''
        self.assertIsNone(process(args))

        args = parser.parse_args(['set', 'language', '--code', 'en', '--name',
                                  'english'])
        with self.assertRaises(SystemExit) as em:
            print(process(args))


if __name__ == "__main__":
    # Make sure the environment is OK to run unittests
    config = UnittestConfig()
    config.create()

    # Do the unit test
    unittest.main()
