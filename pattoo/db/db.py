#!/usr/bin/env python3

"""Class to process connection."""
import sys
from contextlib import contextmanager

# PIP3 imports
from sqlalchemy import and_

# pattoo libraries
from pattoo_shared import log
from pattoo.db import POOL
from pattoo.db.models import DataPoint


@contextmanager
def db_modify(error_code, die=True, close=True):
    """Provide a transactional scope around Update / Insert operations.

    From https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    Args:
        error_code: Error code to use in messages
        die: Die if True
        close: Close session if True. GraphQL mutations sometimes require the
            session to remain open.

    Returns:
        None

    """
    # Initialize key variables
    prefix = 'Unable to modify database.'

    # Create session from pool
    session = POOL()

    # Setup basic functions
    try:
        yield session
        session.commit()
    except Exception as exception_error:
        session.rollback()
        log_message = '{}. Error: "{}"'.format(prefix, exception_error)
        if bool(die) is True:
            log.log2die(error_code, log_message)
        else:
            log.log2info(error_code, log_message)
    except:
        session.rollback()
        log_message = '{}. Unknown error'.format(prefix)
        if bool(die) is True:
            log.log2die(error_code, log_message)
        else:
            log.log2info(error_code, log_message)
    finally:
        # Return the Connection to the pool
        if bool(close) is True:
            session.close()


@contextmanager
def db_query(error_code, close=True):
    """Provide a transactional scope around Query operations.

    From https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    Args:
        error_code: Error code to use in messages
        close: Close session if True. GraphQL mutations sometimes require the
            session to remain open.
    Returns:
        None

    """
    # Initialize key variables
    prefix = 'Unable to read database.'

    # Create session from pool
    session = POOL()

    # Setup basic functions
    try:
        yield session
    except Exception as exception_error:
        session.close()
        log_message = '{}. Error: "{}"'.format(prefix, exception_error)
        log.log2info(error_code, log_message)
    except:
        session.close()
        log_message = '{}. Unknown error'.format(prefix)
        log.log2info(error_code, log_message)
    finally:
        # Return the Connection to the pool
        if bool(close) is True:
            session.close()


def connectivity(die=True):
    """Check connectivity to the database.

    Args:
        die: Die if true

    Returns:
        valid: True if connectivity is OK

    """
    # Initialize key variables
    valid = False

    # Do test
    try:
        with db_query(20008) as session:
            rows = session.query(DataPoint.idx_datapoint).filter(
                and_(DataPoint.idx_datapoint == 1,
                     DataPoint.checksum == '-1'.encode()))
            for _ in rows:
                break
            valid = True
    except:
        _exception = sys.exc_info()
        log.log2exception_die(20115, _exception)

    # Log
    if valid is False:
        log_message = ('''\
No connectivity to database. Make sure the installation script has been run. \
Check log files and do appropriate troubleshooting.''')
        if bool(die) is False:
            log.log2warning(20083, log_message)
        else:
            log.log2die(20112, log_message)

    # Return
    return valid
