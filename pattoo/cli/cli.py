#!/usr/bin/env python3
"""Classes to manage the pattoo cli."""

from inspect import ismethod
import textwrap
import argparse
import sys

# pattoo libraries
from pattoo_shared import log


class _Parser(argparse.ArgumentParser):
    """Class gathers all CLI information."""

    def error(self, message):
        """Override the default behavior of the error method.

        Will print the help message whenever the error method is triggered.
        For example, test.py --blah will print the help message too if --blah
        isn't a valid option

        Args:
            None

        Returns:
            _args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        sys.stderr.write('\nERROR: {}\n\n'.format(message))
        self.print_help()
        sys.exit(2)


class Parser(object):
    """Class gathers all CLI information."""

    def __init__(self, additional_help=None):
        """Intialize the class."""
        # Create a number of here-doc entries
        if additional_help is not None:
            self._help = additional_help
        else:
            self._help = ''

    def args(self):
        """Return all the CLI options.

        Args:
            None

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
        parser = _Parser(
            description=self._help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = parser.add_subparsers(dest='action')

        # Parse "show", return object used for parser
        _Show(subparsers, width=width)

        # Parse "create", return object used for parser
        _Create(subparsers, width=width)

        # Parse "set", return object used for parser
        _Set(subparsers, width=width)

        # Parse "import", return object used for parser
        _Import(subparsers, width=width)

        # Show help if no arguments
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        # Return the CLI arguments
        _args = parser.parse_args()

        # Return our parsed CLI arguments
        return (_args, parser)


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

    def agent_program(self, width=80):
        """Process show agent_program CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        self.subparsers.add_parser(
            'agent_program',
            help=textwrap.fill('Show agent_program.', width=width)
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

    def language(self, width=80):
        """Process create language CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'language',
            help=textwrap.fill('Create language.', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--code',
            help='Language code',
            type=str,
            required=True)

        parser.add_argument(
            '--description',
            help='Language description',
            type=str,
            required=True)


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

    def agent_program(self, width=80):
        """Process set agent_program CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'agent_program',
            help=textwrap.fill('Set agent_program information.', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--name',
            help='Agent program name',
            type=str,
            required=True)

        parser.add_argument(
            '--description',
            help='Agent program description',
            type=str,
            required=True)

    def language(self, width=80):
        """Process set language CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'language',
            help=textwrap.fill('Set language.', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--code',
            help='Language code',
            type=str,
            required=True)

        parser.add_argument(
            '--description',
            help='Language description',
            type=str,
            required=True)


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
