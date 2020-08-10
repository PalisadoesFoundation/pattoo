#!/usr/bin/env python3
"""Testing pattoo/db/db.py."""

import os
import unittest
import sys
from random import random, randint
import multiprocessing
from collections import namedtuple

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}db'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


from tests.libraries.configuration import UnittestConfig
from pattoo_shared import data
from pattoo.db.table import language


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test_main(self):
        """Testing method / function main."""
        #
        # NOTE!
        #
        # This test is to verify that multiprocessing is supported without
        # hanging. We don't want database hanging if there is a large load of
        # connections to the database. This is a very important test. It MUST
        # pass for pattoo to be reliable.

        # Initialize key variables
        loops = 10
        process_count = 100
        timeout = 120
        code = data.hashstring(str(random()))
        name = data.hashstring(str(random()))
        Arguments = namedtuple('Arguments', 'loops process_count code')

        # Add an entry to the database
        language.insert_row(code, name)

        # Make sure it exists
        idx_language = language.exists(code)

        # Verify the index exists
        result = language.idx_exists(idx_language)
        self.assertTrue(result)

        # Create arguments
        arguments = Arguments(
            code=code,
            loops=loops,
            process_count=process_count
        )

        # Spawn a single process with a timeout
        process = multiprocessing.Process(target=run_, args=(arguments,))
        process.start()
        process.join(timeout)

        # Test if timing out
        if process.is_alive():
            # Multiprocessing is failing if this times out. I could be due to
            # the loops taking too long (unlikely, but should be checked), or
            # it could be a general failure in the database engine code in
            # pattoo.db.__init__.py.
            print('''\
Test for multiprocessing database update is hanging. Please check possible \
causes.''')
            sys.exit(2)


def run_(arguments):
    """Run multiprocessing database updates.

    Args:
        None

    Returns:
        None

    """
    # Create a list of arguments from a random list of names
    names = [
        data.hashstring(str(random())) for _ in range(5)
    ]
    args = [
        (arguments.code, names[randint(0, len(names) - 1)]) for _ in range(
            arguments.process_count)
    ]

    # Now spawn processes and update the table
    for loop in range(arguments.loops):
        print('Processing loop {}'.format(loop))
        with multiprocessing.get_context(
                'spawn').Pool(processes=arguments.process_count) as pool:
            pool.starmap(language.update_name, args)

        # Wait for all the processes to end and get results
        pool.join()


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
