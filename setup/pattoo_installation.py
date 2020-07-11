#!/usr/bin/env python3

from inspect import ismethod
import textwrap
import argparse
import sys
import os
import getpass


EXEC_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir))
_EXPECTED = '{0}pattoo{0}setup'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.append(ROOT_DIR)
    # Set pattoo config dir if it had not been set already
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
from _pattoo import shared





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

        # Header for the help menu of the application
        parser = _Parser(
            description=self._help,
            formatter_class=argparse.RawTextHelpFormatter)

        # Add subparser
        subparsers = parser.add_subparsers(dest='action')

        # Parse "install", return object used for parser
        _Install(subparsers, width=width)

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
            help=textwrap.fill('Install pattoo.', width=width)
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
        """CLI command to install all pattoo components

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'all',
            help=textwrap.fill('Install all pattoo components', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--prompt',
            action='store_true',
            help='Prompt for user input and enable verbose mode.')

    def database(self, width=80):
        """CLI command to create pattoo database tables.

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
        """CLI command to install the necessary pip3 packages.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'pip',
            help=textwrap.fill('Install PIP', width=width)
        )

        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose mode.')

    def configuration(self, width=80):
        """CLI command to configure pattoo.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'configuration',
            help=textwrap.fill('Install configuration', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--prompt',
            action='store_true',
            help='Prompt for user input')

    def systemd(self, width=80):
        """CLI command to install and start the system daemons.

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
        # Installs all pattoo components
        if args.qualifier == 'all':
            print('Install everything')
            if args.prompt is True:
                print('Prompt for input')
            else:
                print('Automatic installation')
            configure.configure_installation(args.prompt)
            packages.install_pip3(args.prompt, ROOT_DIR)
            # Import db after pip3 packages are installed
            from _pattoo import db
            db.create_pattoo_db_tables()
            systemd.install_systemd()
        # Configures pattoo and sets up database tables
        elif args.qualifier == 'database':
            # Assumes defaults unless the all qualifier is used
            configure.configure_installation(False)
            packages.install_pip3(False, ROOT_DIR)
            # Import db after pip3 packages are installed
            from _pattoo import db
            db.create_pattoo_db_tables()
        # Installs and starts system daemons
        elif args.qualifier == 'systemd':
            print('??: Installing systemd')
            configure.configure_installation(False)
            # Install pip3 packages, verbose mode is disabled by default
            packages.install_pip3(False, ROOT_DIR)
            systemd.install_systemd()
        # Only installs pip3 packages if they haven't been installed already
        elif args.qualifier == 'pip':
            print('Install pip')
            packages.install_pip3(args.verbose, ROOT_DIR)
        # Sets up the configuration for pattoo
        elif args.qualifier == 'configuration':
            print('Install configuration')
            configure.configure_installation(args.prompt)
        # Print help if no argument options were triggered
        else:
            parser.print_help(sys.stderr)
            sys.exit(1)


def installation_checks():
    """Validate conditions needed to start installation.

    Prevents installation if the script is not run as root

    Args:
        None

    Returns:
        True: If conditions for installation are satisfied
    """
    if getpass.getuser() != 'travis':
        if getpass.getuser() != 'root':
            shared._log('You are currently not running the script as root.\
Run as root to continue')
    return True


if __name__ == '__main__':
    installation_checks()
    # Try except to import pattoo libraries if pattoo shared isn't installed
    try:
        from _pattoo import packages, systemd, configure
    except ModuleNotFoundError:
        default_pip_dir = '/opt/pattoo-daemon/.python'
        print('Pattoo shared is missing. Installing pattoo shared')
        shared._run_script(
            'python3 -m pip install PattooShared -t {}'.format(default_pip_dir))
        sys.path.append(default_pip_dir)
        from _pattoo import packages, systemd, configure
    # Execute main
    main()
