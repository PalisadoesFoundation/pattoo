#!/usr/bin/env python3
"""pattoo ORM Table classes.

Used to define the tables used in the database.

"""

# SQLobject stuff
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER
from sqlalchemy.dialects.mysql import NUMERIC, VARBINARY
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from pattoo.db import POOL
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH

###############################################################################
# Create Base SQLAlchemy class. This must be in the same file as the database
# definitions or else the database won't be created on install. Learned via
# trial and error.
BASE = declarative_base()

# GraphQL: Bind engine to metadata of the base class
BASE.metadata.bind = POOL

# GraphQL: Used by graphql to execute queries
BASE.query = POOL.query_property()
###############################################################################


class DataPoint(BASE):
    """Class defining the pt_datapoint table of the database."""

    __tablename__ = 'pt_datapoint'
    __table_args__ = (
        UniqueConstraint('checksum'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_datapoint = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    checksum = Column(VARBINARY(512), unique=True, nullable=True, default=None)

    data_type = Column(INTEGER(unsigned=True), nullable=False)

    last_timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    # Defaults to 5 minutes or 300000 milliseconds
    polling_interval = Column(
        INTEGER(unsigned=True), nullable=False, default='300000')

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Pair(BASE):
    """Class defining the pt_pair table of the database."""

    __tablename__ = 'pt_pair'
    __table_args__ = (
        UniqueConstraint('key', 'value'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_pair = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    key = Column(VARBINARY(MAX_KEYPAIR_LENGTH), nullable=True, default=None)

    value = Column(VARBINARY(MAX_KEYPAIR_LENGTH), nullable=True, default=None)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Glue(BASE):
    """Class defining the pt_glue table of the database."""

    __tablename__ = 'pt_glue'
    __table_args__ = (
        UniqueConstraint('idx_pair', 'idx_datapoint'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_pair = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_pair.idx_pair'),
        primary_key=True, nullable=False
    )

    idx_datapoint = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_datapoint.idx_datapoint'),
        primary_key=True, nullable=False)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a
    # DataPoint onto its Data
    datapoint = relationship(
        DataPoint,
        backref=backref(
            'glue_datapoint', uselist=True, cascade='delete,all'))

    # Use cascade='delete,all' to propagate the deletion of a
    # Pair onto its Data
    pair = relationship(
        Pair,
        backref=backref(
            'glue_pair', uselist=True, cascade='delete,all'))


class Data(BASE):
    """Class defining the pt_data table of the database."""

    __tablename__ = 'pt_data'
    __table_args__ = (
        PrimaryKeyConstraint('idx_datapoint', 'timestamp'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_datapoint = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_datapoint.idx_datapoint'),
        nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(NUMERIC(40, 10), nullable=False, default='1')

    # Use cascade='delete,all' to propagate the deletion of a
    # DataPoint onto its Data
    datapoint = relationship(
        DataPoint,
        backref=backref(
            'data_checksum', uselist=True, cascade='delete,all'))


class Language(BASE):
    """Class defining the pt_language table of the database."""

    __tablename__ = 'pt_language'
    __table_args__ = (
        UniqueConstraint('code'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_language = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    code = Column(VARBINARY(4), nullable=False, default=None)

    description = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class PairXlateGroup(BASE):
    """Class defining the pt_pair_xlate_group table of the database."""

    __tablename__ = 'pt_pair_xlate_group'
    __table_args__ = (
        UniqueConstraint('name'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_pair_xlate_group = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    name = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    description = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class PairXlate(BASE):
    """Class defining the pt_pair_xlate table of the database."""

    __tablename__ = 'pt_pair_xlate'
    __table_args__ = (
        PrimaryKeyConstraint('idx_language', 'key', 'idx_pair_xlate_group'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_pair_xlate_group = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_pair_xlate_group.idx_pair_xlate_group'),
        nullable=False, server_default='1')

    idx_language = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_language.idx_language'),
        nullable=False, server_default='1')

    key = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    description = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class AgentGroup(BASE):
    """Class defining the pt_agent_group table of the database."""

    __tablename__ = 'pt_agent_group'
    __table_args__ = (
        UniqueConstraint('name'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_agent_group = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_pair_xlate_group = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_pair_xlate_group.idx_pair_xlate_group'),
        nullable=False, server_default='1')

    name = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    description = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Agent(BASE):
    """Class defining the pt_agent table of the database."""

    __tablename__ = 'pt_agent'
    __table_args__ = (
        UniqueConstraint('pattoo_agent_id'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_agent = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_agent_group = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_agent_group.idx_agent_group'),
        nullable=False, server_default='1')

    pattoo_agent_id = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    pattoo_agent_program = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))
