#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

# Import project libraries
from pattoo_shared import configuration
from pattoo_shared.configuration import Config as ConfigShared


class Config(ConfigShared):
    """Class gathers all configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_AGENT_OS_SPOKED constant

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        ConfigShared.__init__(self)

    def db_name(self):
        """Get db_name.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_name'

        # Process configuration
        result = configuration.search(key, sub_key, self._configuration)

        # Get result
        return result

    def db_username(self):
        """Get db_username.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_username'

        # Process configuration
        result = configuration.search(key, sub_key, self._configuration)

        # Get result
        return result

    def db_password(self):
        """Get db_password.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_password'

        # Process configuration
        result = configuration.search(key, sub_key, self._configuration)

        # Get result
        return result

    def db_hostname(self):
        """Get db_hostname.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_hostname'

        # Process configuration
        result = configuration.search(key, sub_key, self._configuration)

        # Get result
        return result

    def sqlalchemy_pool_size(self):
        """Get sqlalchemy_pool_size.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'sqlalchemy_pool_size'
        intermediate = configuration.search(
            key, sub_key, self._configuration, die=False)

        # Set default
        if intermediate is None:
            result = 10
        else:
            result = int(intermediate)
        return result

    def sqlalchemy_max_overflow(self):
        """Get sqlalchemy_max_overflow.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'sqlalchemy_max_overflow'
        intermediate = configuration.search(
            key, sub_key, self._configuration, die=False)

        # Set default
        if intermediate is None:
            result = 10
        else:
            result = int(intermediate)
        return result
