#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

import os

# Import project libraries
from pattoo_shared import configuration
from pattoo_shared.configuration import Config as ConfigShared
from pattoo_shared.configuration import search
from pattoo.constants import (
    PATTOO_API_WEB_NAME, PATTOO_API_AGENT_NAME,
    PATTOO_INGESTERD_NAME)


class ConfigPattoo(ConfigShared):
    """Class gathers all configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_API_WEB_NAME constant

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
        key = 'pattoo_db'
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
        key = 'pattoo_db'
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
        key = 'pattoo_db'
        sub_key = 'db_password'

        # Process configuration
        if 'PATTOO_TRAVIS' in os.environ:
            result = ''
        else:
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
        key = 'pattoo_db'
        sub_key = 'db_hostname'

        # Process configuration
        result = configuration.search(key, sub_key, self._configuration)

        # Get result
        return result

    def db_pool_size(self):
        """Get db_pool_size.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'pattoo_db'
        sub_key = 'db_pool_size'
        intermediate = configuration.search(
            key, sub_key, self._configuration, die=False)

        # Set default
        if intermediate is None:
            result = 10
        else:
            result = int(intermediate)
        return result

    def db_max_overflow(self):
        """Get db_max_overflow.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'pattoo_db'
        sub_key = 'db_max_overflow'
        intermediate = configuration.search(
            key, sub_key, self._configuration, die=False)

        # Set default
        if intermediate is None:
            result = 10
        else:
            result = int(intermediate)
        return result

    def ip_listen_address(self):
        """Get ip_listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_API_WEB_NAME
        sub_key = 'ip_listen_address'
        result = search(key, sub_key, self._configuration, die=False)

        # Default to 0.0.0.0
        if result is None:
            result = '0.0.0.0'
        return result

    def ip_bind_port(self):
        """Get ip_bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = PATTOO_API_WEB_NAME
        sub_key = 'ip_bind_port'

        # Get result
        intermediate = search(key, sub_key, self._configuration, die=False)
        if intermediate is None:
            result = 20202
        else:
            result = int(intermediate)
        return result


class ConfigAgent(ConfigShared):
    """Class gathers all configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_API_WEB_NAME constant

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

    def ip_listen_address(self):
        """Get ip_listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_API_AGENT_NAME
        sub_key = 'ip_listen_address'
        result = search(key, sub_key, self._configuration, die=False)

        # Default to 0.0.0.0
        if result is None:
            result = '0.0.0.0'
        return result

    def ip_bind_port(self):
        """Get ip_bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = PATTOO_API_AGENT_NAME
        sub_key = 'ip_bind_port'

        # Get result
        intermediate = search(key, sub_key, self._configuration, die=False)
        if intermediate is None:
            result = 20202
        else:
            result = int(intermediate)
        return result


class ConfigIngester(ConfigShared):
    """Class gathers all configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_INGESTERD_NAME constant

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

    def ingester_interval(self):
        """Get ingester_interval.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_INGESTERD_NAME
        sub_key = 'ingester_interval'
        result = search(key, sub_key, self._configuration, die=False)

        # Make sure we have an integer
        try:
            result = max(15, abs(int(result)))
        except:
            result = None

        # Default to 1 hour
        if result is None:
            result = 3600
        return result

    def multiprocessing(self):
        """Get multiprocessing.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_INGESTERD_NAME
        sub_key = 'multiprocessing'
        _result = search(key, sub_key, self._configuration, die=False)

        # Return
        if _result is None:
            result = True
        else:
            result = bool(_result)
        return result
