#!/usr/bin/env python3
"""Process CLI arguments."""

from __future__ import print_function
import sys

# Import project libraries
from pattoo.db.table import (
    agent, agent_group, language, pair_xlate_group, pair_xlate, agent_xlate)


def process(args):
    """Process cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Process options
    if args.qualifier == 'agent':
        _process_agent()
        sys.exit(0)
    elif args.qualifier == 'agent_group':
        _process_agent_group()
        sys.exit(0)
    elif args.qualifier == 'language':
        _process_language()
        sys.exit(0)
    elif args.qualifier == 'key_translation_group':
        _process_pair_xlate_group(args)
        sys.exit(0)
    elif args.qualifier == 'key_translation':
        _process_pair_xlate(args)
        sys.exit(0)
    elif args.qualifier == 'agent_translation':
        _process_agent_xlate()
        sys.exit(0)

def _process_agent():
    """Process agent cli arguments.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    data = agent.cli_show_dump()
    _printer(data)


def _process_agent_group():
    """Process agent_group cli arguments.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    data = agent_group.cli_show_dump()
    _printer(data)


def _process_language():
    """Process language cli arguments.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    data = language.cli_show_dump()
    _printer(data)


def _process_pair_xlate_group(args):
    """Process pair_xlate_group cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Initialize key variables
    data = pair_xlate_group.cli_show_dump()
    _printer(data)


def _process_pair_xlate(args):
    """Process pair_xlate cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Initialize key variables
    data = pair_xlate.cli_show_dump(args.idx_pair_xlate_group)
    _printer(data)


def _process_agent_xlate():
    """Process agent_xlate cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Initialize key variables
    data = agent_xlate.cli_show_dump()
    _printer(data)


def _printer(data):
    """Print results to the screen.

    The order is the same as the ordering when the initial
    collections.namedtuple definitions in data

    Args:
        data: List of NamedTuples

    Returns:
        None

    """
    # Initialize key variables
    max_width = {}
    column_formatter = '{{:<{}}}'
    keys = []

    # Get headings. Initialize the values of max_width
    for item in data:
        keys = list(item._asdict().keys())
        break
    for key in keys:
        max_width[key] = len(str(key))

    # Get the maximum width each value in the data
    for item in data:
        for key, value in item._asdict().items():
            len_value = len(str(value))
            max_key = max_width[key]
            max_width[key] = max(max_key, len_value)

    # Print heading
    segments = []
    for key in keys:
        segment_formatter = column_formatter.format(max_width[key])
        segment = segment_formatter.format(key)
        segments.append(segment)
    print('{}\n'.format('  '.join(segments)))

    # Print lines
    for item in data:
        segments = []
        for key, value in item._asdict().items():
            segment_formatter = column_formatter.format(max_width[key])
            segment = segment_formatter.format(value)
            segments.append(segment)
        print('{}'.format('  '.join(segments)))
