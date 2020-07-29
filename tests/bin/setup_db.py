#!/usr/bin/env python3
"""Test database table setup"""

# Standard Python imports
import os
import sys

# SQLALCHMEY Imports
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}bin'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo Imports
from pattoo.db.models import BASE

DB_NAME = 'pattoo_unittest'
DB_NAME_ERROR = '''An error occurred: {} database does not exist!\nPlease create
before running tests!'''.format(DB_NAME)
DB_URI='mysql://:@localhost/{}'.format(DB_NAME)

def create_tables(tables):
    """Create mock tables for testing in DB_NAME

    Args:
        tables: list of table objects

    Return:
        engine: engine object return allow for persistence of the same object
        that can be used to tear down the tables and for session handling within
        unittest.

    """
    engine = create_engine(DB_URI)

    try:
        BASE.metadata.drop_all(engine, tables=tables)
        BASE.metadata.create_all(engine, tables=tables)
    except OperationalError as e:
        print(DB_NAME_ERROR)
        print('Error Message: {}'.format(e))
        sys.exit(0)
    return engine

def teardown_tables(engine):
    """Dispose of test tables stored in DB_NAME

    Args:
        tables: list of table objects

    Return:
        None

    """
    # Ensures engine object is valid
    if engine is None:
        print('Please pass an engine object')
        sys.exit(0)

    try:
        BASE.metadata.bind.remove()
        BASE.metadata.drop_all(engine)
    except OperationalError:
        print(DB_NAME_ERROR)
        sys.exit(0)
