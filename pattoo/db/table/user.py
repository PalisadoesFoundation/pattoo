"""Pattoo classes querying the User table."""

# Python imports
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
        # Initialize key variables
        row = None
        self.idx_user = None
        self.first_name = None
        self.last_name = None
        self.role = None
        self.password_expired = None
        self.enabled = None
        self.exists = False
        self._username = username

        # Get data
        with db.db_query(20162) as session:
            row = session.query(
                _User).filter(_User.username == username.encode()).first()

        # Assign variables
        if not (row is None):
            self.idx_user = row.idx_user
            self.first_name = row.first_name.decode()
            self.last_name = row.last_name.decode()
            self.role = row.role
            self.password_expired = bool(row.password_expired)
            self.enabled = bool(row.enabled)
            self.username = username
            self.exists = True

    def valid_password(self, value):
        """Get.

        Args:
            value: New value to apply

        Returns:
            result: True if valid

        """
        # Initialize key variables
        result = False

        if bool(self.exists) is True:
            # Get password from database
            with db.db_query(20141) as session:
                password = session.query(
                    _User.password).filter(
                        _User.username == self._username.encode()).one()

            # Determine state of password
            found = password[0].decode()
            salt = found.split('$')[2]
            expected = crypt.crypt(value, '$6${}'.format(salt))
            result = bool(found == expected)

        return result


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
        with db.db_modify(20156, die=True) as session:
            session.query(_User).filter(
                _User.username == self._username.encode()
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
        with db.db_modify(20157, die=True) as session:
            session.query(_User).filter(
                _User.username == self._username.encode()
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
        with db.db_modify(20158, die=True) as session:
            session.query(_User).filter(
                _User.username == self._username.encode()
            ).update({'password': _value})

    def role(self, value):
        """Modify.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        _value = int(value)
        with db.db_modify(20159, die=True) as session:
            session.query(_User).filter(
                _User.username == self._username.encode()
            ).update({'role': _value})

    def password_expired(self, value):
        """Set the password_expired flag.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        with db.db_modify(20160, die=True) as session:
            session.query(_User).filter(
                _User.username == self._username.encode()
            ).update({'password_expired': int(bool(value))})

    def enabled(self, value):
        """Modify enabled status.

        Args:
            value: New value to apply

        Returns:
            None

        """
        # Update
        with db.db_modify(20161, die=True) as session:
            session.query(_User).filter(
                _User.username == self._username.encode()
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
    role = int(row.role)
    password_expired = int(row.password_expired)
    enabled = int(bool(row.enabled))

    # Insert
    row = _User(
        username=username.encode(),
        password=crypt.crypt(password).encode(),
        first_name=first_name.encode(),
        last_name=last_name.encode(),
        role=role,
        password_expired=password_expired,
        enabled=enabled
        )

    with db.db_modify(20054, die=True) as session:
        session.add(row)
