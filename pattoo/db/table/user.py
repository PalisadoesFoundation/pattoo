#!/usr/bin/env python3
"""Pattoo classes querying the User table."""

# Python imports
import secrets
from hashlib import blake2b

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
    salt = row.salt[:MAX_KEYPAIR_LENGTH]
    first_name = row.first_name.strip()[:MAX_KEYPAIR_LENGTH]
    last_name = row.last_name.strip()[:MAX_KEYPAIR_LENGTH]
    is_admin = int(bool(row.is_admin))
    enabled = int(bool(row.enabled))

    # Insert
    row = User(
        username=username.encode(),
        password=password,
        salt=salt,
        first_name=first_name.encode(),
        last_name=last_name.encode(),
        is_admin=is_admin,
        enabled=enabled,
        )

    with db.db_modify(20054, die=True) as session:
        session.add(row)

def generate_password_hash(password, salt=None):
    """Generates a unique password hash using blake2b hash function

    Args:
        password: user password to be hashed
        salt: optional salt to be used

    Return
        password_hash: hashed password
        salt: additional byte string to generate unique password hash

    """

    # Generating salt and initial hash function from blake2b hash algorithm
    if bool(salt) is False:
        salt = secrets.token_bytes(blake2b.SALT_SIZE)
    blake2b_hash = blake2b(digest_size=blake2b.MAX_DIGEST_SIZE, salt=salt)
    blake2b_hash.update(password)

    # Extracting digest from blake2b_hash
    password_hash = blake2b_hash.hexdigest().encode()
    return password_hash, salt


def verify_password(password, db_password, salt):
    """Verifies that a given password matches a given database password

    Args:
        password: password user possibly entered on a frontend.
        db_password: password retrieved from the database to be used for
        comparison.
        salt: Additional salting string used to generate unique hash.

    Return:
        verify: boolean indicating whether both passwords are the same.

    """
    verify = False

    # Creating password hash to make comparison with db_password
    password_hash, _ = generate_password_hash(password, salt=salt)

    # Verifying if passwords are the same
    verify = bool(password_hash == db_password)
    return verify


# TODO Throw error if querying to database fails
def is_admin(user_id):
    """Determines whether a given user is an admin

    Args:
        user_id: User ID to be queried

    Return:
        _is_admin: Boolean indicating whether user associated with user_id is an
        admin or not.

    """
    _is_admin = False

    # Querying user table
    with db.db_query(20155) as session:
        query = session.query(User).filter(User.idx_user ==
                                                user_id).first()
        _is_admin = bool(query.is_admin)
    return _is_admin


def authenticate(username, password):
    """Validates that a given username and password matches a user within the
    database

    Args:
        username: String containing the username of a possible system user
        password: String containing the password of associated username

    Return:
        auth: Boolean indicating if authentication was successful

    """
    auth = False

    # Querying  user table
    with db.db_query(20156) as session:
        query = session.query(User).filter(User.username ==
                                                username).first()

        # Checking that a given user exists
        if bool(query) is True:

            # Checking that password matches
            auth = bool(User.password.decode() == password)
    return auth
