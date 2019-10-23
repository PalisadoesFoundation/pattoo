#!/usr/bin/env python3
"""Test all the pattoo modules."""

from __future__ import print_function
import os
import inspect
import re
import sys
import collections


# Import pattoo libraries
from pattoo_shared import log


def check(root):
    """Get all the error codes used in pattoo.

    Args:
        root: Root directory

    Returns:
        None

    """
    # Define min and max code values
    code_min_limit = 1000
    code_max_limit = 49999

    # Define where pattoo lives
    ignore_paths = [
        '/.git/', '/__pycache__/', '/_archive/', '/_deprecated/',
        '/pattoo/build/', '/pattoo/dist/', '.egg']
    error_functions = (
        'log2die_safe(', 'log2warning(',
        'log2debug(', 'log2live(', 'log2warn(', 'log2die(', 'log2quiet(',
        'log2info(', 'log2screen(', 'log2see(', r'.modify(', r'.query(',
        r'.replace(', '.add_all(')
    error_codes = []
    available_codes = []
    entries = 5

    # Get ready to ignore this script
    this_script = os.path.abspath(inspect.getfile(inspect.currentframe()))
    ignore_paths.append(this_script)

    # Compile regex to be used to find functions with error codes
    to_find = _wordlist_to_regex(error_functions)

    # Get a recursive listing of files
    python_files = _files(root, ignore_paths)

    # Read each file to find error codes
    for python_file in python_files:
        error_codes.extend(_codes(python_file, to_find))

    # Get duplicate codes
    _duplicates = [
        item for item, count in collections.Counter(
            error_codes).items() if count > 1]
    _duplicates.sort()
    if len(_duplicates) > entries:
        duplicates = '{} plus {} more...'.format(
            _duplicates[0:entries], len(_duplicates) - entries)
    else:
        duplicates = _duplicates

    # Get available codes
    code_max = max(error_codes)
    if int(code_max) >= code_max_limit:
        log_message = ('''\
Extremely large error code {} found. Must be less than {}. Please fix.\
'''.format(code_max, code_max_limit))
        log.log2die(1571, log_message)

    # Process error codes
    for next_code in range(min(error_codes), code_max):
        if next_code not in error_codes:
            available_codes.append(next_code)

    # Get available codes
    if bool(available_codes) is False:
        available_codes = list(
            range(max(error_codes), max(error_codes) + entries + 1))

    # Print report
    print('''
Pattoo Logging Error Code Summary Report
----------------------------------------
Starting Code              : {}
Ending Code                : {}
Duplicate Codes to Resolve : {}
Available Codes            : {}\
'''.format(min(error_codes),
           max(error_codes),
           duplicates,
           available_codes[0:entries]))

    # Exit with error if duplicate codes found
    if bool(duplicates) is True:
        print('''

ERROR: Duplicate error codes found. Please resolve.

''')
        sys.exit(1)

    # Exit with error if code values are out of range
    if (min(error_codes) < code_min_limit) or (max(error_codes) > code_max_limit):
        print('''

ERROR: Error codes values out of range {} to {}. Please resolve.

'''.format(code_min_limit, code_max_limit))
        sys.exit(1)



def _codes(filename, to_find):
    """Get a list of codes found in a file.

    Args:
        filename: Name of file
        to_find: Compiled list of functions to search for

    Returns:
        error_codes: List of error codes

    """
    # Initalize key variables
    digits = re.compile(r'^.*?(\d+).*?$')
    error_codes = []

    # Process file for codes
    with open(filename, 'r') as lines:
        # Read each line of the file
        for line in lines:
            # Ignore lines without a '(' in it
            if '(' not in line:
                continue

            # Ignore lines starting with comments
            if line.strip().startswith('#'):
                continue

            match_obj = to_find.search(line)
            if bool(match_obj) is True:
                # Search for digits in the arguments of the functions
                # in the error_functions
                components = line.split('(')
                arguments = ' '.join(components[1:])
                found = digits.match(arguments)
                if bool(found) is True:
                    # print('boo -', line)
                    error_codes.append(int(found.group(1)))

    # Exit with error if error codes are non numeric
    for _code in error_codes:
        if isinstance(_code, int) is False:
            print('''

ERROR: Non integer error code found. Please resolve.

'''.format(_code))
            sys.exit(1)

    # Return
    return error_codes


def _wordlist_to_regex(words):
    """Convert word list to a regex expression, escaping characters if needed.

    Args:
        words: List of words

    Returns:
        result: Compiled regex

    """
    escaped = map(re.escape, words)
    combined = '|'.join(sorted(escaped, key=len, reverse=True))
    result = re.compile(combined)
    return result


def _files(root, ignore_paths):
    """Get a recursive list of python files under a root directory.

    Args:
        root: Root directory
        ignore_paths: List of paths to ignore

    Returns:
        python_files: List of paths to python files

    """
    # Define where pattoo lives
    python_files = []

    # Get a recursive listing of files
    for directory, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(directory, filename)

            # Ignore pre-defined file extensions
            if file_path.endswith('.py') is False:
                continue

            # Ignore pre-defined paths
            ignored = False
            for ignore_path in ignore_paths:
                if ignore_path in file_path:
                    ignored = True
            if ignored is False:
                python_files.append(file_path)

    # Return
    return python_files
