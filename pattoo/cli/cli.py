#!/usr/bin/env python3
"""Classes to manage the pattoo cli."""

from inspect import ismethod
import textwrap
import argparse
import sys

# pattoo libraries
from pattoo_shared import log


class Parser(object):
    """Class gathers all CLI information."""

    def __init__(self, additional_help=None):
        """Intialize the class."""
        # Create a number of here-doc entries
        if additional_help is not None:
            self._help = additional_help
        else:
            self._help = ''

    def get_cli(self):
        """Return all the CLI options.

        Args:
            self:

        Returns:
            _args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        # Initialize key variables
        width = 80

        # Log the cli command
        log_message = 'CLI: {}'.format(' '.join(sys.argv))
        log.log2info(20043, log_message)

        # Header for the help menu of the application
        parser = argparse.ArgumentParser(
            description=self._help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = parser.add_subparsers(dest='action')

        # Parse "show", return object used for parser
        _Show(subparsers, width=width)

        # Parse "create", return object used for parser
        _Create(subparsers, width=width)

        # Parse "assign", return object used for parser
        _Assign(subparsers, width=width)

        # Parse "set", return object used for parser
        _Set(subparsers, width=width)

        # Parse "import", return object used for parser
        _Import(subparsers, width=width)

        # Return the CLI arguments
        _args = parser.parse_args()

        # Return our parsed CLI arguments
        return _args


class _Show(object):
    """Class gathers all CLI 'show' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'show',
            help=textwrap.fill('Show contents of pattoo DB.', width=width)
        )

        # Add subparser
        self.subparsers = parser.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def agent(self, width=80):
        """Process show agents CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'agent',
            help=textwrap.fill('Show agent.', width=width)
        )

    def agent_group(self, width=80):
        """Process show agent_group CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'agent_group',
            help=textwrap.fill('Show agent_group.', width=width)
        )

    def key_pair_translation(self, width=80):
        """Process show key_pair_translation CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'key_pair_translation',
            help=textwrap.fill(
                'Show agent key-pair translations.', width=width)
        )

    def language(self, width=80):
        """Process show language CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'language',
            help=textwrap.fill('Show language.', width=width)
        )


class _Create(object):
    """Class gathers all CLI 'create' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'create',
            help=textwrap.fill('Create entries in pattoo DB.', width=width)
        )

        # Add subparser
        self.subparsers = parser.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def agent_group(self, width=80):
        """Process create agent_group CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'agent_group',
            help=textwrap.fill('Create agent_group.', width=width)
        )

    def language(self, width=80):
        """Process create language CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'language',
            help=textwrap.fill('Create language.', width=width)
        )


class _Assign(object):
    """Class gathers all CLI 'assign' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'assign',
            help=textwrap.fill('Show contents of pattoo DB.', width=width)
        )

        # Add subparser
        self.subparsers = parser.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def agent(self, width=80):
        """Process assign agent CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'agent',
            help=textwrap.fill('Assign agent to an Agent Group.', width=width)
        )


class _Set(object):
    """Class gathers all CLI 'set' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'set',
            help=textwrap.fill('Show contents of pattoo DB.', width=width)
        )

        # Add subparser
        self.subparsers = parser.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def agent_group(self, width=80):
        """Process set agent_group CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'agent_group',
            help=textwrap.fill('Set agent_group information.', width=width)
        )

    def language(self, width=80):
        """Process set language CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'language',
            help=textwrap.fill('Set language.', width=width)
        )


class _Import(object):
    """Class gathers all CLI 'import' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'import',
            help=textwrap.fill('Import data into the pattoo DB.', width=width)
        )

        # Add subparser
        self.subparsers = parser.add_subparsers(dest='qualifier')

        # Execute all methods in this Class
        for name in dir(self):
            # Get all attributes of Class
            attribute = getattr(self, name)

            # Determine whether attribute is a method
            if ismethod(attribute):
                # Ignore if method name is reserved (eg. __Init__)
                if name.startswith('_'):
                    continue

                # Execute
                attribute(width=width)

    def key_pair_translation(self, width=80):
        """Process import key_pair_translation CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'key_pair_translation',
            help=textwrap.fill('Import key-pair translations.', width=width)
        )
