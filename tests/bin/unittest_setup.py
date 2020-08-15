#!/usr/bin/env python3
"""Class used to create the configuration file used for unittesting.

NOTE!! This script CANNOT import any pattoo libraries. Doing so risks
libraries trying to access a configuration or configuration directory that
doesn't yet exist. This is especially important when running cloud based
automated tests such as 'Travis CI'.

"""

# Standard imports
from __future__ import print_function
import os
import sys

# Try to create a working PYTHONPATH
DEV_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(DEV_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}bin'.format(os.sep)
if DEV_DIR.endswith(_EXPECTED) is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from tests.libraries.configuration import UnittestConfig

from pattoo.configuration import ConfigPattoo as Config
from pattoo.db import URL
from pattoo.db.models import BASE
from sqlalchemy import create_engine
from pattoo_shared import log


def main():
    """Verify that we are ready to run tests."""

    # Check environment
    config = UnittestConfig()
    _ = config.create()
    _mysql()


def _mysql():
    """Create database tables.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    config = Config()
    pool_size = config.db_pool_size()
    max_overflow = config.db_max_overflow()

    # Add MySQL to the pool
    engine = create_engine(
        URL, echo=True,
        encoding='utf8',
        max_overflow=max_overflow,
        pool_size=pool_size, pool_recycle=3600)

    # Try to create the database
    print('Connecting to configured database. Altering character set.')
    try:
        sql_string = ('''\
ALTER DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci\
'''.format(config.db_name()))
        engine.execute(sql_string)
    except:
        log_message = (
            '''\
ERROR: Cannot connect to database "{}" on server "{}". Verify database server \
is started. Verify database is created. Verify that the configured database \
authentication is correct.'''.format(config.db_name(), config.db_hostname()))
        log.log2die(20086, log_message)

    # Apply schemas
    print('Creating database tables.')
    BASE.metadata.create_all(engine)


if __name__ == '__main__':
    # Do the unit test
    main()
