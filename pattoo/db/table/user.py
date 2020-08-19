"""Pattoo classes querying the User table."""

import crypt

# Import project libraries
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.models import User as _User
from pattoo.constants import DbRowUser


class User():
    """User modification class."""

    def __init__(self, username):
        """Initialize the class.

        Args:
            username: Name of user

        Returns:
            None

        """
        # Integrity test
        if bool(exists(username)) is False:
            log_message = 'Username "{}" does not exist.'.format(username)
            log.log2die(20091, log_message)

        # Get data
        with db.db_query(20141) as session:
            self._user = session.query(
                _User).filter(username=username.encode())

    def first_name(self):
        """Get first name.

        Args:
            None

        Returns:
            result: metadata value

        """
        # Return
        return self._user.first_name.decode()

    def last_name(self):
        """Get last name.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self._user.last_name.decode()

    def valid_password(self, value):
        """Get.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Initialize key variables
        found = self._user.password.decode()
        (_, salt, __) = found.split('$')
        expected = crypt.crypt(value, '$6${}'.format(salt))
        return bool(found == expected)

    def user_type(self):
        """Get.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self._user.user_type

    def change_password(self):
        """Set the change_password flag.

        Args:
            None

        Returns:
            None

        """
        # Return
        return bool(self._user.change_password)

    def enabled(self):
        """Get enabled status.

        Args:
            None

        Returns:
            None

        """
        # Return
        return bool(self._user.enabled)


class Modify():
    """User modification class."""

    def __init__(self, username):
        """Initialize the class.

        Args:
            username: Name of user

        Returns:
            None

        """
        # Initialize key variables
        if bool(exists(username)) is True:
            self._username = username
        else:
            log_message = 'Username "{}" does not exist.'.format(username)
            log.log2die(20155, log_message)

    def first_name(self, value):
        """Modify first name.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        _value = value.strip()[:MAX_KEYPAIR_LENGTH].encode()
        with db.db_modify(20156, die=False) as session:
            session.query(_User).filter(
                _User.username == self._username
            ).update({'first_name': _value})

    def last_name(self, value):
        """Modify last name.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        _value = value.strip()[:MAX_KEYPAIR_LENGTH].encode()
        with db.db_modify(20157, die=False) as session:
            session.query(_User).filter(
                _User.username == self._username
            ).update({'last_name': _value})

    def password(self, value):
        """Modify.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Initialize key variables
        _value = crypt.crypt(value).encode()
        with db.db_modify(20158, die=False) as session:
            session.query(_User).filter(
                _User.username == self._username
            ).update({'password': _value})

    def user_type(self, value):
        """Modify.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        _value = int(value)
        with db.db_modify(20159, die=False) as session:
            session.query(_User).filter(
                _User.username == self._username
            ).update({'user_type': _value})

    def change_password(self, value):
        """Set the change_password flag.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        with db.db_modify(20160, die=False) as session:
            session.query(_User).filter(
                _User.username == self._username
            ).update({'change_password': int(bool(value))})

    def enabled(self, value):
        """Modify enabled status.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        with db.db_modify(20161, die=False) as session:
            session.query(_User).filter(
                _User.username == self._username
            ).update({'enabled': int(bool(value))})


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
        rows = session.query(_User.idx_user).filter(
            _User.idx_user == idx)

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
        rows = session.query(_User.idx_user).filter(
            _User.username == username.encode())

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
    row = _User(
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
