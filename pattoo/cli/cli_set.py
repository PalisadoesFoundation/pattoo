#!/usr/bin/env python3
"""Process CLI arguments."""

import sys

# Import project libraries
from pattoo_shared import log
from pattoo.db.table import language, pair_xlate_group


def process(args):
    """Process cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Process options
    if args.qualifier == 'language':
        _process_language(args)
        sys.exit(0)
    elif args.qualifier == 'key_translation_group':
        _process_pair_xlate_group(args)
        sys.exit(0)


def _process_language(args):
    """Process language cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Initialize key variables
    if bool(language.exists(args.code)) is True:
        language.update_name(args.code, args.name)
    else:
        log_message = 'Language code "{}" not found.'.format(args.code)
        log.log2die(20005, log_message)


def _process_pair_xlate_group(args):
    """Process pair_xlate_group cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Initialize key variables
    exists = pair_xlate_group.idx_exists(args.idx_pair_xlate_group)
    if bool(exists) is True:
        # Check for duplicates
        duplicate = pair_xlate_group.exists(args.name)
        if bool(duplicate) is True:
            log_message = ('''\
Translation group  "{}" already exists.'''.format(args.name))
            log.log2die(20075, log_message)

        # Update
        if args.idx_pair_xlate_group != 1:
            pair_xlate_group.update_name(
                args.idx_pair_xlate_group, args.name)
        else:
            log_message = 'Cannot change Translation group "1".'
            log.log2die(20072, log_message)
    else:
        log_message = ('''\
Translation group  "{}" not found.'''.format(args.idx_pair_xlate_group))
        log.log2die(20074, log_message)
