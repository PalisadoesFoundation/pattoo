#!/usr/bin/env python3
"""CLI Assign testing"""

# Standard Python imports
import os
import unittest
import sys
import argparse
from unittest.mock import patch
from io import StringIO

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}cli'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from pattoo.cli.cli_import import (process, _process_key_translation,
                                   _process_agent_translation)
from pattoo_shared import log
from pattoo.db import db
from pattoo.cli.cli import _Import
from pattoo.db.models import (BASE, PairXlate, AgentXlate, PairXlateGroup,
                              Language)

# Pattoo unittest imports
from tests.bin.setup_db import (create_tables, teardown_tables, DB_URI)
from tests.libraries.configuration import UnittestConfig
