#!/usr/bin/env python3
"""CLI import testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse
import tempfile
import csv

# SQLALCHMEY Imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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
from pattoo.cli.cli import _SET
from pattoo.db.models import BASE, PairXlateGroup, Language

# Pattoo unittest imports
from tests.pattoo_.cli.setup_db import (create_tables, teardown_tables,
                                            DB_URI)
from tests.libraries.configuration import UnittestConfig


class TestSet(unittest.TestCase):
    """Tests CLI set module"""
    pass

