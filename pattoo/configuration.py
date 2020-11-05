#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

# Python imports
import os
import datetime
import stat

# Import project libraries
from pattoo_shared.configuration import ServerConfig
from pattoo_shared.configuration import search
from pattoo_shared import files
from pattoo_shared import log
from pattoo.constants import (
    PATTOO_API_WEB_NAME, PATTOO_API_AGENT_NAME,
    PATTOO_INGESTERD_NAME)


class ConfigAPId(ServerConfig):
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
        ServerConfig.__init__(self)

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
        result = search(
            key, sub_key, self._server_yaml_configuration)

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
        result = search(
            key, sub_key, self._server_yaml_configuration)

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
            result = search(
                key, sub_key, self._server_yaml_configuration)

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
        result = search(
            key, sub_key, self._server_yaml_configuration)

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
        intermediate = search(
            key, sub_key, self._server_yaml_configuration, die=False)

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
        intermediate = search(
            key, sub_key, self._server_yaml_configuration, die=False)

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
        result = search(
            key, sub_key, self._server_yaml_configuration, die=False)

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
        intermediate = search(
            key, sub_key, self._server_yaml_configuration, die=False)
        if intermediate is None:
            result = 20202
        else:
            result = int(intermediate)
        return result

    def jwt_secret_key(self):
        """Get jwt_secret_key.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = PATTOO_API_WEB_NAME
        sub_key = 'jwt_secret_key'

        # Process configuration
        result = search(key, sub_key, self._server_yaml_configuration)

        # Ensures that jwt_secret_key is set
        if bool(result is False):
            log_message = 'Parameter {} is not configured'.format(sub_key)
            log.log2die(20176, log_message)
        if isinstance(result, str):
            if bool(result.strip()) is False:
                log_message = 'Parameter {} is blank'.format(sub_key)
                log.log2die(20175, log_message)

        # Get result
        return result

    def access_token_exp(self):
        """Gets access_token_exp.

        Parsing config where:
        minutes: 'm', hours: 'h', days: 'D', weeks: 'W', months: 'M'

        Args:
            None

        Return:
           exp: access token expiration time using datetie.timedelta

        """
        # Initialize key variables
        key = PATTOO_API_WEB_NAME
        sub_key = 'access_token_exp'

        # Process configuration
        result = search(key, sub_key, self._server_yaml_configuration)

        # Setting timedelta for result
        # Sets a default value if accesss_token_exp not found
        exp = self.__exp(result)

        if exp is None:
            exp = datetime.timedelta(minutes=15)

        return exp

    def refresh_token_exp(self):
        """Gets refresh_token_exp.

        Parsing config where:
        minutes: 'm', hours: 'h', days: 'D', weeks: 'W', months: 'M'

        Args:
            None

        Return:
            exp: refresh token expiration time using datetie.timedelta

        """
        # Initialize key variables
        key = PATTOO_API_WEB_NAME
        sub_key = 'refresh_token_exp'

        # Process configuration
        result = search(key, sub_key, self._server_yaml_configuration)

        # Setting timedelta for result
        # Sets a default value if access_token_exp not found
        exp = self.__exp(result)

        if exp is None:
            exp = datetime.timedelta(minutes=15)

        return exp

    def __exp(self, time_string):
        """Parses string to create datetime.timedelta object

        Parsing config where:
        minutes: 'm', hours: 'h', days: 'D', weeks: 'W', months: 'M'

        Args:
            time_string: string to be parsed containing a time period

        Return:
            exp: datetime.timedelta object for a given expiration time

        """
        exp = None
        time_string = time_string.split('_')

        # Creating datetime.timedelta object
        if len(time_string) == 2:
            time_duration = int(time_string[0])
            time_stamp = time_string[-1]

            if time_stamp == 'm':
                exp = datetime.timedelta(minutes=time_duration)
            elif time_stamp == 'h':
                exp = datetime.timedelta(hours=time_duration)
            elif time_stamp == 'D':
                exp = datetime.timedelta(days=time_duration)
            elif time_stamp == 'W':
                exp = datetime.timedelta(weeks=time_duration)
            elif time_stamp == 'M':
                exp = datetime.timedelta(months=time_duration)

        return exp


class ConfigAgentAPId(ServerConfig):
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
        ServerConfig.__init__(self)

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
        result = search(
            key, sub_key, self._server_yaml_configuration, die=False)

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
        intermediate = search(
            key, sub_key, self._server_yaml_configuration, die=False)
        if intermediate is None:
            result = 20202
        else:
            result = int(intermediate)
        return result

    def session_directory(self):
        """Get directory for storing session infomation.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = '{}{}session'.format(self.cache_directory(), os.sep)

        # Create directory if it doesn't exist
        files.mkdir(result)

        # Change filemode to 700
        # Only allow the user to access the flash session folder
        os.chmod(result, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        return result


class ConfigIngester(ServerConfig):
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
        ServerConfig.__init__(self)

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
        result = search(
            key, sub_key, self._server_yaml_configuration, die=False)

        # Make sure we have an integer
        try:
            result = max(15, abs(int(result)))
        except:
            result = None

        # Default to 1 hour
        if result is None:
            result = 3600
        return result

    def graceful_timeout(self):
        """Get graceful_timeout.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_INGESTERD_NAME
        sub_key = 'graceful_timeout'
        result = search(
            key, sub_key, self._server_yaml_configuration, die=False)

        # Make sure we have an integer
        try:
            result = int(result)
        except:
            result = None

        # Default to 1 hour
        if result is None:
            result = 10
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
        _result = search(
            key, sub_key, self._server_yaml_configuration, die=False)

        # Return
        if _result is None:
            result = True
        else:
            result = bool(_result)
        return result

    def batch_size(self):
        """Get batch_size.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key varibles
        default = 500

        # Get result
        key = PATTOO_INGESTERD_NAME
        sub_key = 'batch_size'
        _result = search(
            key, sub_key, self._server_yaml_configuration, die=False)

        # Return
        if _result is None:
            result = default
        else:
            try:
                result = int(_result)
            except:
                result = default
        return result
