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


class Device(BASE):
    """Class defining the iset_device table of the database."""

    __tablename__ = 'iset_device'
    __table_args__ = (

        UniqueConstraint(
            'devicename'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_device = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    devicename = Column(VARBINARY(512), nullable=True, default=None)

    description = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class DeviceAgent(BASE):
    """Class defining the iset_deviceagent table of the database."""

    __tablename__ = 'iset_deviceagent'
    __table_args__ = (
        UniqueConstraint(
            'idx_device', 'idx_agent'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_deviceagent = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_device = Column(
        BIGINT(unsigned=True), ForeignKey('iset_device.idx_device'),
        nullable=False, server_default='1')

    idx_agent = Column(
        BIGINT(unsigned=True), ForeignKey('iset_agent.idx_agent'),
        nullable=False, server_default='1')

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    last_timestamp = Column(
        BIGINT(unsigned=True), nullable=False, server_default='0')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Data(BASE):
    """Class defining the iset_data table of the database."""

    __tablename__ = 'iset_data'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_datapoint', 'timestamp'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_datapoint = Column(
        BIGINT(unsigned=True), ForeignKey('iset_datapoint.idx_datapoint'),
        nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(NUMERIC(40, 10), default=None)


class Agent(BASE):
    """Class defining the iset_agent table of the database."""

    __tablename__ = 'iset_agent'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    idx_agent = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_agentname = Column(
        BIGINT(unsigned=True), ForeignKey('iset_agentname.idx_agentname'),
        nullable=False, server_default='1')

    id_agent = Column(VARBINARY(512), unique=True, nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class AgentName(BASE):
    """Class defining the iset_agentname table of the database."""

    __tablename__ = 'iset_agentname'
    __table_args__ = (
        UniqueConstraint(
            'name'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_agentname = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    name = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Datapoint(BASE):
    """Class defining the iset_datapoint table of the database."""

    __tablename__ = 'iset_datapoint'
    __table_args__ = (
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_datapoint = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_deviceagent = Column(
        BIGINT(unsigned=True), ForeignKey('iset_deviceagent.idx_deviceagent'),
        nullable=False, server_default='1')

    idx_department = Column(
        BIGINT(unsigned=True), ForeignKey('iset_department.idx_department'),
        nullable=False, server_default='1')

    idx_billcode = Column(
        BIGINT(unsigned=True), ForeignKey('iset_billcode.idx_billcode'),
        nullable=False, server_default='1')

    id_datapoint = Column(
        VARBINARY(512), unique=True, nullable=True, default=None)

    agent_label = Column(VARBINARY(512), nullable=True, default=None)

    agent_source = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    billable = Column(INTEGER(unsigned=True), server_default='0')

    timefixed_value = Column(VARBINARY(512), nullable=True, default=None)

    base_type = Column(INTEGER(unsigned=True), server_default='1')

    last_timestamp = Column(
        BIGINT(unsigned=True), nullable=False, server_default='0')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Department(BASE):
    """Class defining the iset_department table of the database."""

    __tablename__ = 'iset_department'
    __table_args__ = (
        UniqueConstraint(
            'code'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_department = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    code = Column(VARBINARY(512), nullable=True, default=None)

    name = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Billcode(BASE):
    """Class defining the iset_billcode table of the database."""

    __tablename__ = 'iset_billcode'
    __table_args__ = (
        UniqueConstraint(
            'code'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_billcode = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    code = Column(VARBINARY(512), nullable=True, default=None)

    name = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Configuration(BASE):
    """Class defining the iset_configuration table of the database."""

    __tablename__ = 'iset_configuration'
    __table_args__ = (
        UniqueConstraint(
            'config_key'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_configuration = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    config_key = Column(VARBINARY(512), nullable=True, default=None)

    config_value = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))
