#!/usr/bin/env python3
"""Process CLI arguments."""

import sys

# Import project libraries
from pattoo_shared import log
from pattoo.db import language


def process(args):
    """Process cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Do creations
    if args.qualifier == 'language':
        _process_language(args)
        sys.exit(0)


def _process_language(args):
    """Process language cli arguments.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    if bool(language.exists(args.code)) is True:
        log_message = 'Language code "{}" already exists.'.format(args.code)
        log.log2die(20044, log_message)
    else:
        language.insert_row(args.code, args.description)
