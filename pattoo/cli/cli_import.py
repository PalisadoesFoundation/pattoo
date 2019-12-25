#!/usr/bin/env python3
"""Process CLI arguments."""

from __future__ import print_function
import sys
import os

# PIP3 imports
import pandas as pd

# Import project libraries
from pattoo_shared import log
from pattoo.db.table import pair_xlate


def process(args):
    """Process cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Process options
    if args.qualifier == 'key_pair_translation':
        _process_key_pair_translation(args)
        sys.exit(0)


def _process_key_pair_translation(args):
    """Process import cli arguments.

    Args:
        args: CLI argparse parser arguments

    Returns:
        None

    """
    # Check if file exists
    if os.path.isfile(args.filename) is False:
        log_message = 'File {} does not exist'.format(args.filename)
        log.log2die(20051, log_message)

    # Import CSV
    try:
        _df = pd.read_csv(args.filename)
    except:
        (etype, evalue, etraceback) = sys.exc_info()
        log_message = ('''File import failure: [{}, {}, {}]\
'''.format(etype, evalue, etraceback))
        log.log2die(20076, log_message)

    # Import the data
    pair_xlate.update(_df, args.idx_pair_xlate_group)
