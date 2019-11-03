#!/usr/bin/env python3
"""pattoo ORM classes.

Manages connection pooling among other things.

"""

# SQLobject stuff
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER
from sqlalchemy.dialects.mysql import NUMERIC, VARBINARY
from sqlalchemy import Column
from sqlalchemy import ForeignKey

BASE = declarative_base()


class Data(BASE):
    """Class defining the pt_data table of the database."""

    __tablename__ = 'pt_data'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_datavariable', 'timestamp'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_datavariable = Column(
        BIGINT(unsigned=True), ForeignKey('pt_datapoint.idx_datavariable'),
        nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(NUMERIC(40, 10), default=None)


class DataString(BASE):
    """Class defining the pt_data table of the database."""

    __tablename__ = 'pt_datastring'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_datavariable', 'timestamp'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_datavariable = Column(
        BIGINT(unsigned=True), ForeignKey('pt_datapoint.idx_datavariable'),
        nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(VARBINARY(512), nullable=True, default=None)


class DataVariable(BASE):
    """Class defining the pt_datapoint table of the database."""

    __tablename__ = 'pt_datapoint'
    __table_args__ = (
        UniqueConstraint(
            'idx_datasource', 'data_label', 'data_index', 'data_type'),
        {
            'mysql_engine': 'InnoDB'
        }
    )

    idx_datavariable = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_datasource = Column(
        BIGINT(unsigned=True), ForeignKey('pt_datasource.idx_datasource'),
        nullable=False, server_default='1')

    data_label = Column(VARBINARY(512), nullable=True, default=None)

    data_index = Column(VARBINARY(128), nullable=True, default=None)

    data_type = Column(INTEGER(unsigned=True), server_default='1')

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    last_timestamp = Column(
        BIGINT(unsigned=True), nullable=False, server_default='0')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class DataSource(BASE):
    """Class defining the pt_datasource table of the database."""

    __tablename__ = 'pt_datasource'
    __table_args__ = (
        UniqueConstraint('idx_agent', 'device', 'gateway'),
        {
            'mysql_engine': 'InnoDB'
        }
    )

    idx_datasource = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_agent = Column(
        BIGINT(unsigned=True), ForeignKey('pt_agent.idx_agent'),
        nullable=False, server_default='1')

    device = Column(VARBINARY(512), nullable=True, default=None)

    gateway = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Agent(BASE):
    """Class defining the pt_agent table of the database."""

    __tablename__ = 'pt_agent'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    idx_agent = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    agent_id = Column(VARBINARY(512), unique=True, nullable=True, default=None)

    agent_hostname = Column(
        VARBINARY(512), unique=True, nullable=True, default=None)

    agent_program = Column(
        VARBINARY(512), unique=True, nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))
