#!/usr/bin/env python3

from inspect import ismethod
import textwrap
import argparse
import sys
import os
import getpass
from shared import _run_script, _log

EXEC_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
PIP_DIR = '/opt/pattoo/daemon/.python'
_EXPECTED = '{0}pattoo{0}setup'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.append(ROOT_DIR)
    sys.path.append(PIP_DIR)
    # Try catch block to automatically set the config dir if it isn't already
    # set
    try:
        os.environ['PATTOO_CONFIGDIR']
    except KeyError:
        os.environ['PATTOO_CONFIGDIR'] = '/etc/pattoo'
else:
    print('''\
This script is not installed in the "{}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)
  
# Importing installation related packages
from installation_lib.install import install
from installation_lib.install import check_pip3
from installation_lib.configure import configure_installation

# Importing pattoo related packages
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


class Parser():
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
        #log_message = 'CLI: {}'.format(' '.join(sys.argv))
        #log.log2info(20043, log_message)

        # Header for the help menu of the application
        parser = _Parser(
            description=self._help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = parser.add_subparsers(dest='action')

        # Parse "install", return object used for parser
        _Install(subparsers, width=width)

        # Parse "set", return object used for parser
        _Set(subparsers, width=width)

        # Install help if no arguments
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        # Return the CLI arguments
        _args = parser.parse_args()

        # Return our parsed CLI arguments
        return (_args, parser)


class _Install():
    """Class gathers all CLI 'install' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'install',
            help=textwrap.fill('Set contents of pattoo DB.', width=width)
        )

        parser.add_argument(
            '--pip',
            action='store_true',
            help=textwrap.fill(
                'Install pip libraries.', width=width)
        )
        #
        parser.add_argument(
            '--database',
            action='store_true',
            help=textwrap.fill(
                'Install database.', width=width)
        )
        #
        parser.add_argument(
            '--systemd',
            action='store_true',
            help=textwrap.fill(
                'Install systemd.', width=width)
        )
        #
        parser.add_argument(
            '--all',
            action='store_true',
            help=textwrap.fill(
                'Install all.', width=width)
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

    def all(self, width=80):
        """
        CLI command to install all pattoo components

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'all',
            help=textwrap.fill('Install all components', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--prompt',
            action='store_true',
            help='Prompt for user input.')

    def database(self, width=80):
        """
        CLI command to create pattoo database tables.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        _ = self.subparsers.add_parser(
            'database',
            help=textwrap.fill('Install database', width=width)
        )

    def pip(self, width=80):
        """
        CLI command to install the necessary pip3 packages.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        _ = self.subparsers.add_parser(
            'pip',
            help=textwrap.fill('Install PIP', width=width)
        )

    def configuration(self, width=80):
        """
        CLI command to configure pattoo.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        _ = self.subparsers.add_parser(
            'configuration',
            help=textwrap.fill('Install configuration', width=width)
        )

    def systemd(self, width=80):
        """
        CLI command to install and start the system daemons.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        _ = self.subparsers.add_parser(
            'systemd',
            help=textwrap.fill('Install systemd service files', width=width)
        )


class _Set():
    """Class gathers all CLI 'set' information."""

    def __init__(self, subparsers, width=80):
        """Intialize the class."""
        # Initialize key variables
        parser = subparsers.add_parser(
            'set',
            help=textwrap.fill('Set contents of pattoo DB.', width=width)
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
            '--name',
            help='Language name',
            type=str,
            required=True)

    def pair_xlate_group(self, width=80):
        """Process set pair_xlate_group CLI commands.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None

        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'key_translation_group',
            help=textwrap.fill('''\
Set key-pair translation group information.''', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--idx_pair_xlate_group',
            help='Key-pair translation group index',
            type=int,
            required=True)

        parser.add_argument(
            '--name',
            help='Agent group name',
            type=str,
            required=True)


def main():
    """Pattoo CLI script.

        None

    Returns:
        None

    """
    # Initialize key variables
    _help = 'This program is the CLI interface to configuring pattoo'

    # Process the CLI
    _parser = Parser(additional_help=_help)
    (args, parser) = _parser.args()

    # Process CLI options
    if args.action == 'install':
        print('install', args)

        if args.qualifier == 'all':
            print('Install everything')
            if args.prompt is True:
                print('Prompt for input')
            else:
                print('Automatic installation')
            configure_installation(args.prompt)
            install(args.prompt)
        elif args.qualifier == 'database':
            print('??: Installing database')

        elif args.qualifier == 'systemd':
            print('Install systemd')
            # install_systemd()
        elif args.qualifier == 'pip':
            print('Install pip')
            check_pip3()
        elif args.qualifier == 'configuration':
            print('Install configuration')
            # Assume defaults unless the all qualifier is used
            configure_installation(False)
        sys.exit()
    # Print help if no argument options were triggered
    parser.print_help(sys.stderr)
    sys.exit(1)


def installation_checks():
    """
    Validate conditions needed to start installation.

    Prevents installation if pattoo is not being run in a venv and if the
    script is not run as root

    Args:
        None

    Returns:
        True: If conditions for installation are satisfied
    """
    if getpass.getuser() != 'travis':
        if getpass.getuser() != 'root':
            _log('You are currently not running the script as root.\
Run as root to continue')
    return True


if __name__ == '__main__':
    installation_checks()
    main()
