#!/usr/bin/env python3
"""Pattoo classes querying the Language table."""

# Import project libraries
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.tables import Language as _Language


def exists(code):
    """Determine whether code exists in the Language table.

    Args:
        code: language code

    Returns:
        result: Language.idx_language value

    """
    # Initialize key variables
    result = False
    rows = []

    # Ignore certain restricted keys
    with db.db_query(20031) as session:
        rows = session.query(_Language.idx_language).filter(
            _Language.code == code.encode())

    # Return
    for row in rows:
        result = row.idx_language
        break
    return result


def insert_row(_code, description=''):
    """Create a Language table entry.

    Args:
        code: Language code
        description: Language code description

    Returns:
        None

    """
    # Verify values
    if bool(description) is False or isinstance(description, str) is False:
        _description = 'Change me. Language name not provided.'
    else:
        _description = description[:MAX_KEYPAIR_LENGTH]
    if bool(_code) is False or isinstance(_code, str) is False:
        log_message = 'Language code "{}" is invalid'.format(_code)
        log.log2die(20033, log_message)

    # Insert
    with db.db_modify(20032, die=True) as session:
        session.add(_Language(
            code=_code.encode(), description=_description.encode()))
