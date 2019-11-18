#!/usr/bin/env python3

"""Class to process connection."""

from contextlib import contextmanager

# PIP3 imports
from sqlalchemy import and_

# pattoo libraries
from pattoo_shared import log
from pattoo.db import POOL
from pattoo.db.tables import Checksum


@contextmanager
def db_modify(error_code, die=True):
    """Provide a transactional scope around Update / Insert operations.

    From https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    Args:
        error_code: Error code to use in messages
        die: Die if True

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
        session.close()


@contextmanager
def db_query(error_code):
    """Provide a transactional scope around Query operations.

    From https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    Args:
        error_code: Error code to use in messages

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
        session.close()


def connectivity():
    """Check connectivity to the database.

    Args:
        None

    Returns:
        valid: True if connectivity is OK

    """
    # Initialize key variables
    valid = False

    # Do test
    with db_query(20008) as session:
        result = session.query(Checksum.idx_checksum).filter(
            and_(Checksum.idx_checksum == 1,
                 Checksum.checksum == '-1'.encode()))
        for _ in result:
            break
        valid = True

    # Return
    return valid
