#!/usr/bin/env python3
"""Script to install patttoo."""

from inspect import ismethod
import textwrap
import argparse
import sys
import os
import getpass
import pwd

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

# Importing shared to install pattoo_shared if its not installed
from _pattoo import shared

# Attempt to import pattoo shared
default_path = '''\
{}/.local/lib/python3.6/site-packages'''.format(os.path.expanduser('~'))
try:
    import pattoo_shared
except ModuleNotFoundError:
    shared.run_script('pip3 install PattooShared -t {0}'.format(default_path))

# Import packages that depend on pattoo shared
from _pattoo import configure
from pattoo_shared.installation import packages, systemd, environment


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
        """CLI command to install all pattoo components.

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
            '--verbose',
            action='store_true',
            help='Enable verbose mode.')

    def database(self, width=80):
        """CLI command to create pattoo database tables.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'database',
            help=textwrap.fill('Install database', width=width)
        )
        # Add arguments
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose mode.')

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
            '--verbose',
            action='store_true',
            help='Enable verbose mode.')

    def systemd(self, width=80):
        """CLI command to install and start the system daemons.

        Args:
            width: Width of the help text string to STDIO before wrapping

        Returns:
            None
        """
        # Initialize key variables
        parser = self.subparsers.add_parser(
            'systemd',
            help=textwrap.fill('Install systemd service files', width=width)
        )

        # Add arguments
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose mode.')


def get_pattoo_home():
    """Retrieve home directory for pattoo user.

    Args:
        None

    Returns:
        The home directory for the pattoo user

    """
    try:
        # No exception will be thrown if the pattoo user exists
        pattoo_home = pwd.getpwnam('pattoo').pw_dir
    # Set defaults if pattoo user doesn't exist
    except KeyError:
        pattoo_home = '/home/pattoo'

    # Ensure that the pattoo home directory is not set to non-existent
    if pattoo_home == '/nonexistent':
        pattoo_home = '/home/pattoo'

    return pattoo_home


def installation_checks():
    """Validate conditions needed to start installation.

    Prevents installation if the script is not run as root and prevents
    installation if script is run in a home related directory

    Args:
        None

    Returns:
        True: If conditions for installation are satisfied

    """
    # Check user
    if getpass.getuser() != 'travis':
        if getpass.getuser() != 'root':
            shared.log('You are currently not running the script as root.\
Run as root to continue')
        # Check installation directory
        if os.getcwd().startswith('/home'):
            shared.log('''\
You cloned the repository in a home related directory, please clone in a\
 non-home directory to continue''')

        # Check if virtualenv is installed
        try:
            import virtualenv
        except ModuleNotFoundError:
            print('virtualenv is not installed. Installing virtualenv')
            shared.run_script('''\
pip3 install virtualenv -t {}'''.format(default_path))


def main():
    """Pattoo CLI script.

        None

    Returns:
        None

    """
    # Initialize key variables
    _help = 'This program is the CLI interface to configuring pattoo'
    daemon_list = [
        'pattoo_apid',
        'pattoo_api_agentd',
        'pattoo_ingesterd'
    ]
    template_dir = os.path.join(ROOT_DIR, 'setup/systemd/system')

    # Setup virtual environment
    if getpass.getuser() != 'travis':
        pattoo_home = get_pattoo_home()
        venv_dir = os.path.join(pattoo_home, 'pattoo-venv')
        environment.environment_setup(venv_dir)
        venv_interpreter = os.path.join(venv_dir, 'bin/python3')
        installation_dir = '{} {}'.format(venv_interpreter, ROOT_DIR)
    else:
        # Set default directories for travis
        pattoo_home = os.path.join(os.path.expanduser('~'), 'pattoo')
        venv_dir = default_path
        installation_dir = ROOT_DIR

    # Process the CLI
    _parser = Parser(additional_help=_help)
    (args, parser) = _parser.args()

    # Process CLI options
    if args.action == 'install':
        # Installs all pattoo components
        if args.qualifier == 'all':
            print('Installing everything')
            configure.install(pattoo_home)
            packages.install(ROOT_DIR, venv_dir, args.verbose)

            # Import db after pip3 packages are installed
            from _pattoo import db
            db.install()
            systemd.install(daemon_list=daemon_list,
                            template_dir=template_dir,
                            installation_dir=installation_dir,
                            verbose=args.verbose)

        # Configures pattoo and sets up database tables
        elif args.qualifier == 'database':
            print('Installing database tables')
            configure.install(pattoo_home)
            packages.install(ROOT_DIR, venv_dir)
            # Import db after pip3 packages are installed
            from _pattoo import db
            db.install()

        # Installs and starts system daemons
        elif args.qualifier == 'systemd':
            print('Installing systemd daemons')
            systemd.install(daemon_list=daemon_list,
                            template_dir=template_dir,
                            installation_dir=installation_dir,
                            verbose=True)

        elif args.qualifier == 'pip':
            # Installs additionally required pip3 packages
            packages.install(ROOT_DIR, venv_dir, args.verbose)

        # Sets up the configuration for pattoo
        elif args.qualifier == 'configuration':
            configure.install(pattoo_home)

        # Print help if no argument options were triggered
        else:
            parser.print_help(sys.stderr)
            sys.exit(1)

        # Done
        print('Done')


if __name__ == '__main__':
    # Ensure environment is okay
    installation_checks()
    # Execute main
    main()
