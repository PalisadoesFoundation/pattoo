#!/usr/bin/env python3
"""Process CLI arguments."""

from __future__ import print_function
import sys
import os

# PIP3 imports
import pandas as pd

# Import project libraries
from pattoo_shared import log
from pattoo.db import pair_xlate


def process(args):
    """Process cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Initialize key variables
    # Do creations
    if args.qualifier == 'key_pair_translation':
        _process_key_pair_translation(args)
        sys.exit(0)


def _process_key_pair_translation(args):
    """Process import cli arguments.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    headings_expected = ['landuage', 'agent_program', 'key', 'description']
    headings_actual = []
    valid = True

    # Check if file exists
    if os.path.isfile(args.filename) is False:
        log_message = 'File {} does not exist'.format(args.filename)
        log.log2die(20051, log_message)

    # Get data
    try:
        data = pd.read_csv(args.filename)
    except:
        pass

    # Test columns
    for item in data.columns:
        headings_actual.append(item)
    for item in headings_actual:
        if item not in headings_expected:
            valid = False
    if valid is False:
        log_message = ('''File {} must have the following headings "{}"\
'''.format(args.filename, '", "'.join(headings_expected)))
        log.log2die(20053, log_message)
