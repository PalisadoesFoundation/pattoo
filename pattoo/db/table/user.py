#!/usr/bin/env python3
"""Pattoo classes querying the User table."""

# Import project libraries
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.models import User
from pattoo.constants import DbRowUser


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_user

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20096) as session:
        rows = session.query(User.idx_user).filter(
            User.idx_user == idx)

    # Return
    for _ in rows:
        result = True
        break
    return bool(result)


def exists(username):
    """Determine whether name exists in the User table.

    Args:
        username: user name

    Returns:
        result: User.idx_user value

    """
    # Initialize key variables
    result = False
    rows = []

    # Lowercase the name
    username = username.lower().strip()

    # Get name from database
    with db.db_query(20031) as session:
        rows = session.query(User.idx_user).filter(
            User.username == username.encode())

    # Return
    for row in rows:
        result = row.idx_user
        break
    return result


def insert_row(row):
    """Create a User table entry.

    Args:
        row: DbRowUser object

    Returns:
        None

    """
    # Verify values
    if bool(row) is False or isinstance(row, DbRowUser) is False:
        log_message = 'Invalid user type being inserted'
        log.log2die(20070, log_message)

    # Lowercase the name
    username = row.username.strip()[:MAX_KEYPAIR_LENGTH]
    password = row.password[:MAX_KEYPAIR_LENGTH]
    first_name = row.first_name.strip()[:MAX_KEYPAIR_LENGTH]
    last_name = row.last_name.strip()[:MAX_KEYPAIR_LENGTH]
    user_type = int(row.user_type)
    change_password = int(row.change_password)
    enabled = int(bool(row.enabled))

    # Insert
    row = User(
        username=username.encode(),
        password=password.encode(),
        first_name=first_name.encode(),
        last_name=last_name.encode(),
        user_type=user_type,
        change_password=change_password,
        enabled=enabled
        )
    with db.db_modify(20054, die=True) as session:
        session.add(row)
