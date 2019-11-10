#!/usr/bin/env python3
"""pattoo ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy.pool import QueuePool, Pool

# pattoo libraries
from pattoo_shared import log
from pattoo import configuration

#############################################################################
# Setup a global pool for database connections
#############################################################################
POOL = None
URL = None


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    use_mysql = True
    global POOL
    global URL
    pool_timeout = 30
    pool_recycle = min(10, pool_timeout - 10)

    # Get configuration
    config = configuration.Config()

    # Define SQLAlchemy parameters from configuration
    pool_size = config.db_pool_size()
    max_overflow = config.db_max_overflow()

    # Create DB connection pool
    if use_mysql is True:
        URL = ('mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'.format(
            config.db_username(), config.db_password(),
            config.db_hostname(), config.db_name()))

        # Add MySQL to the pool
        db_engine = create_engine(
            URL, echo=False,
            encoding='utf8',
            poolclass=QueuePool,
            max_overflow=max_overflow,
            pool_size=pool_size,
            pool_pre_ping=True,
            pool_recycle=pool_recycle,
            pool_timeout=pool_timeout)

        # Fix for multiprocessing
        _add_engine_pidguard(db_engine)

        POOL = sessionmaker(
            autoflush=True,
            autocommit=False,
            bind=db_engine
        )

    else:
        POOL = None


def _add_engine_pidguard(engine):
    """Add multiprocessing guards.

    Forces a connection to be reconnected if it is detected
    as having been shared to a sub-process.

    source
    ------

    http://docs.sqlalchemy.org/en/latest/faq/connections.html
    "How do I use engines / connections / sessions with
    Python multiprocessing, or os.fork()?"

    Args:
        engine: SQLalchemy engine instance

    Returns:
        None

    """
    @event.listens_for(engine, 'connect')
    def connect(dbapi_connection, connection_record):
        """Get the PID of the sub-process for connections.

        Args:
            dbapi_connection: Connection object
            connection_record: Connection record object

        Returns:
            None

        """
        connection_record.info['pid'] = os.getpid()

    @event.listens_for(engine, 'checkout')
    def checkout(dbapi_connection, connection_record, connection_proxy):
        """Checkout sub-processes connection for sub-processing if needed.

            Checkout is called when a connection is retrieved from the Pool.

        Args:
            dbapi_connection: Connection object
            connection_record: Connection record object
            connection_proxy: Connection proxy object

        Returns:
            None

        """
        # Get PID of main process
        pid = os.getpid()

        # Detect if this is a sub-process
        if connection_record.info['pid'] != pid:
            # substitute log.debug() or similar here as desired
            log_message = ('''\
Parent process {} forked ({}) with an open database connection, \
which is being discarded and recreated.\
'''.format(connection_record.info['pid'], pid))
            log.log2debug(21027, log_message)

            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError('''\
Connection record belongs to pid {}, attempting to check out in pid {}\
'''.format(connection_record.info['pid'], pid))


if __name__ == 'pattoo.db':
    main()
