#!/usr/bin/env python3
"""Administer the PairXlate database table."""

from collections import namedtuple

# PIP3
from sqlalchemy import and_

# Pattoo PIP3 libraries
from pattoo_shared import log

# Import project libraries
from pattoo.db import db
from pattoo.db.models import PairXlate, Language, PairXlateGroup
from pattoo.db.table import language, pair_xlate_group


def pair_xlate_exists(idx_pair_xlate_group, idx_language, key):
    """Get the db PairXlate.idx_pair_xlate value for specific agent.

    Args:
        idx_pair_xlate_group: PairXlateGroup table primary key
        idx_language: Language table primary key
        key: Key for translation

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20081) as session:
        rows = session.query(PairXlate.description).filter(and_(
            PairXlate.idx_pair_xlate_group == idx_pair_xlate_group,
            PairXlate.idx_language == idx_language,
            PairXlate.key == key.encode()
        ))

    # Return
    for _ in rows:
        result = True
        break
    return result


def insert_row(key, description, units, idx_language, idx_pair_xlate_group):
    """Create a database PairXlate.agent row.

    Args:
        key: PairXlate key
        description: PairXlate description
        units: PairXlate units of measure
        idx_language: Language table index
        idx_pair_xlate_group: PairXlateGroup table index

    Returns:
        None

    """
    # Insert and get the new agent value
    with db.db_modify(20035, die=True) as session:
        session.add(
            PairXlate(
                key=key.encode(),
                description=str(description).strip().encode(),
                units=str(units).strip().encode(),
                idx_language=idx_language,
                idx_pair_xlate_group=idx_pair_xlate_group
            )
        )


def update_row(key, description, units, idx_language, idx_pair_xlate_group):
    """Update a database PairXlate.agent row.

    Args:
        key: PairXlate key
        description: PairXlate description
        units: PairXlate units of measure
        idx_language: Language table index
        idx_pair_xlate_group: PairXlateGroup table index

    Returns:
        None

    """
    # Insert and get the new agent value
    with db.db_modify(20080, die=False) as session:
        session.query(PairXlate).filter(and_(
            PairXlate.key == key.encode(),
            PairXlate.idx_language == idx_language,
            PairXlate.idx_pair_xlate_group == idx_pair_xlate_group)).update(
                {'description': description.strip().encode(),
                 'units': units.strip().encode()}
            )


def update(_df, idx_pair_xlate_group):
    """Import data into the .

    Args:
        _df: Pandas DataFrame with the following headings
            ['language', 'key', 'description', 'units']
        idx_pair_xlate_group: PairXlateGroup table index

    Returns:
        None

    """
    # Initialize key variables
    languages = {}
    headings_expected = [
        'language', 'key', 'description', 'units']
    headings_actual = []
    valid = True
    count = 0

    # Check if group exists
    if pair_xlate_group.idx_exists(idx_pair_xlate_group) is False:
        log_message = ('''\
idx_pair_xlate_group {} does not exist'''.format(idx_pair_xlate_group))
        log.log2die(20077, log_message)

    # Test columns
    for item in _df.columns:
        headings_actual.append(item)
    for item in headings_actual:
        if item not in headings_expected:
            valid = False
    if valid is False:
        log_message = ('''Imported data must have the following headings "{}"\
'''.format('", "'.join(headings_expected)))
        log.log2die(20053, log_message)

    # Process the DataFrame
    for _, row in _df.iterrows():
        # Initialize variables at the top of the loop
        count += 1
        code = row['language'].lower()
        key = str(row['key'])
        description = str(row['description'])
        units = str(row['units'])

        # Store the idx_language value in a dictionary to improve speed
        idx_language = languages.get(code)
        if bool(idx_language) is False:
            idx_language = language.exists(code)
            if bool(idx_language) is True:
                languages[code] = idx_language
            else:
                log_message = ('''\
Language code "{}" on line {} of imported translation file not found during \
key-pair data importation. Please correct and try again. All other valid \
entries have been imported.\
'''.format(code, count))
                log.log2see(20078, log_message)
                continue

        # Update the database
        if pair_xlate_exists(idx_pair_xlate_group, idx_language, key) is True:
            # Update the record
            update_row(
                key, description, units, idx_language, idx_pair_xlate_group)
        else:
            # Insert a new record
            insert_row(
                key, description, units, idx_language, idx_pair_xlate_group)


def cli_show_dump(idx=None):
    """Get entire content of the table.

    Args:
        idx: idx_pair_xlate_group to filter on

    Returns:
        result: List of NamedTuples

    """
    # Initialize key variables
    result = []
    rows = []
    Record = namedtuple(
        'Record',
        '''idx_pair_xlate_group description language key translation units \
enabled''')

    # Get the result
    if bool(idx) is False:
        with db.db_query(20122) as session:
            rows = session.query(PairXlateGroup)
    else:
        with db.db_query(20123) as session:
            rows = session.query(PairXlateGroup).filter(
                PairXlateGroup.idx_pair_xlate_group == idx)

    # Process
    for row in rows:
        first_agent = True

        # Get agents for group
        with db.db_query(20124) as session:
            line_items = session.query(
                Language.code,
                PairXlate.key,
                PairXlate.units,
                PairXlate.description).filter(and_(
                    PairXlate.idx_pair_xlate_group == row.idx_pair_xlate_group,
                    PairXlate.idx_language == Language.idx_language
                    ))

        if line_items.count() >= 1:
            # PairXlates assigned to the group
            for line_item in line_items:
                if first_agent is True:
                    # Format first row for agent group
                    result.append(
                        Record(
                            enabled=row.enabled,
                            idx_pair_xlate_group=row.idx_pair_xlate_group,
                            language=line_item.code.decode(),
                            key=line_item.key.decode(),
                            units=line_item.units.decode(),
                            translation=line_item.description.decode(),
                            description=row.description.decode()
                        )
                    )
                    first_agent = False
                else:
                    # Format subsequent rows
                    result.append(
                        Record(
                            enabled='',
                            idx_pair_xlate_group='',
                            language=line_item.code.decode(),
                            key=line_item.key.decode(),
                            units=line_item.units.decode(),
                            translation=line_item.description.decode(),
                            description=''
                        )
                    )

        else:
            # Format only row for agent group
            result.append(
                Record(
                    enabled=row.enabled,
                    idx_pair_xlate_group=row.idx_pair_xlate_group,
                    language='',
                    key='',
                    units='',
                    translation='',
                    description=row.description.decode()
                )
            )

        # Add a spacer between agent groups
        result.append(Record(
            enabled='', idx_pair_xlate_group='', language='', units='',
            key='', description='', translation=''))

    return result
