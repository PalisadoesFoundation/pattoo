#!/usr/bin/env python3
"""Process CLI arguments."""

from __future__ import print_function
import sys

# Import project libraries
from pattoo_shared import log
from pattoo.db.table import agent, pair_xlate_group


def process(args):
    """Process cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Process options
    if args.qualifier == 'agent':
        _process_agent(args)
        sys.exit(0)


def _process_agent(args):
    """Process agent cli arguments.

    Args:
        args: CLI arguments

    Returns:
        None

    """
    # Validate parameters
    if bool(pair_xlate_group.idx_exists(args.idx_pair_xlate_group)) is False:
        log_message = ('''\
idx_pair_xlate_group "{}" not found.'''.format(args.idx_pair_xlate_group))
        log.log2die(20068, log_message)
    if bool(agent.idx_exists(args.idx_agent)) is False:
        log_message = (
            'idx_agent "{}" not found.'.format(args.idx_agent))
        log.log2die(20060, log_message)

    # Assign
    agent.assign(args.idx_agent, args.idx_pair_xlate_group)
