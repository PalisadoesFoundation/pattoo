#!/usr/bin/env python3
"""pattoo ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import os
import random
from multiprocessing import get_context, Pool
import argparse

from sqlalchemy import UniqueConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, DATETIME
from sqlalchemy.dialects.mysql import VARBINARY
from sqlalchemy import Column
BASE = declarative_base()

#############################################################################
# Setup a global pool for database connections
#############################################################################
from __init__ import POOL
from db import db_modify


class Language(BASE):
    """Class defining the pt_language table of the database."""

    __tablename__ = 'pt_language'
    __table_args__ = (
        UniqueConstraint('code'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_language = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    code = Column(VARBINARY(512),
                  index=True, nullable=False, default=None)

    name = Column(
        VARBINARY(512),
        index=True, nullable=False, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Process CLI
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--context', help='Use get_context multiprocessing function used.',
        action='store_true')
    args = parser.parse_args()

    # Initialize key variables
    max_processes = 10
    arguments = [(x, ) for x in list(range(5000))]

    for argument in arguments:
        run_in_process(argument)

    # Create a pool of sub process resources
    if args.context is True:
        with get_context('spawn').Pool(processes=max_processes) as pool:
            pool.starmap(run_in_process, arguments)
    else:
        with Pool(processes=max_processes) as pool:
            pool.starmap(run_in_process, arguments)

    # Wait for all the processes to end and get results
    pool.join()


def run_in_process(count):
    """Process agent data.

    Args:
        count: Process count

    Returns:
        None

    """
    # Initialize key variables
    error_code = 27
    enabled = random.getrandbits(1)

    # Process data
    pid = os.getpid()
    print('Starting process: {}, Count: {}'.format(pid, count))
    with db_modify(error_code) as session:
        session.query(Language).filter(
            Language.idx_language == 1).update(
                {'idx_language': 1,
                 'enabled': enabled})
    print('Stopping process: {}, Count: {}'.format(pid, count))


if __name__ == '__main__':
    # Run script
    main()
