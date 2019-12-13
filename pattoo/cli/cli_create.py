#!/usr/bin/env python3
"""Process CLI arguments."""

import sys

# Import project libraries
from pattoo_shared import log
from pattoo.db import language, agent_group


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
    elif args.qualifier == 'agent_group':
        _process_agent_group(args)
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
        log_message = 'Language code "{}" already exists.'.format(args.code)
        log.log2die(20044, log_message)
    else:
        language.insert_row(args.code, args.description)


def _process_agent_group(args):
    """Process agent_group cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Initialize key variables
    if bool(agent_group.exists(args.description)) is True:
        log_message = ('''\
Agent group description "{}" already exists.'''.format(args.description))
        log.log2die(20057, log_message)
    else:
        agent_group.insert_row(args.description)
