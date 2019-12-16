#!/usr/bin/env python3
"""Check correct database setup.

Attempts to create database tables.

"""

# Main python libraries
from __future__ import print_function
import sys
import os

# PIP3 imports
from sqlalchemy import create_engine

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
if EXEC_DIR.endswith('/pattoo/setup') is True:
    sys.path.append(ROOT_DIR)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)


# Pattoo libraries
from pattoo_shared import log
from pattoo.configuration import ConfigPattoo as Config
from pattoo.db import URL
from pattoo.db.models import BASE
from pattoo.db.table import agent_group, language, pair_xlate_group


def insertions():
    """Insert the necessary table ForeignKey values to satisfy defaults.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    description = 'Pattoo Default'

    print('??: Attempting to insert default database table entries.')

    # Insert into Language
    if language.idx_exists(1) is False:
        language.insert_row('en', 'English')

    # Insert into PairXlateGroup
    if pair_xlate_group.idx_exists(1) is False:
        pair_xlate_group.insert_row(description)

    # Insert into AgentGroup
    if agent_group.idx_exists(1) is False:
        agent_group.insert_row(description)

    print('OK: Database table entries inserted.')


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
    print('??: Attempting to Connect to configured database.')
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
    print('OK: Database connected.')
    print('??: Attempting to create database tables.')
    BASE.metadata.create_all(engine)
    print('OK: Database tables created.')


def main():
    """Configure database.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    use_mysql = True

    # Create DB
    if use_mysql is True:
        _mysql()

    # Insert ForeignKey values
    insertions()


if __name__ == '__main__':
    # Run setup
    main()
