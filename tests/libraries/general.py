"""Module of general functions."""

# Standard imports
import random
import hashlib


def random_string():
    """Creates random string.

    Args:
        None

    Return:
        result: string

    """
    # Return
    salt = str(random.getrandbits(128))
    result = hashlib.sha224(salt.encode()).hexdigest()
    return result
