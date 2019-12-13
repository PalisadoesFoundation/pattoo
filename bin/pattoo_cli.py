#!/usr/bin/env python3
"""Pattoo CLI script."""

# Standard libraries
import sys
import os


# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _BIN_DIRECTORY.endswith('/pattoo/bin') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)

# pattoo imports
from pattoo.cli.cli import Parser
from pattoo.cli import cli_show, cli_create, cli_set, cli_import


def main():
    """Ingest data."""
    # Initialize key variables
    _help = 'This program is the CLI interface to configuring pattoo'

    # Process the CLI
    _parser = Parser(additional_help=_help)
    (args, parser) = _parser.args()

    # Process CLI options
    if args.action == 'show':
        # Show DB contents
        cli_show.process(args)

    elif args.action == 'create':
        # "Add" directives
        cli_create.process(args)

    elif args.action == 'set':
        # "Set" directives
        cli_set.process(args)

    elif args.action == 'import':
        # "Set" directives
        cli_import.process(args)

    # Print help if no argument options were triggered
    parser.print_help(sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
