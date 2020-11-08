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


class User(BASE):
    """Class defining the pt_user table of the database."""

    __tablename__ = 'pt_user'
    __table_args__ = (
        UniqueConstraint('username'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_user = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    first_name = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH),
        index=True, nullable=False, default=None)

    last_name = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH),
        index=True, nullable=False, default=None)

    username = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH),
        index=True, nullable=False, default=None)

    password = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH),
        nullable=False, default=None)

    role = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    password_expired = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class Chart(BASE):
    """Class defining the pt_chart table of the database."""

    __tablename__ = 'pt_chart'
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )

    idx_chart = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    name = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    checksum = Column(
        VARBINARY(512), unique=True, nullable=True, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


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

    code = Column(VARBINARY(MAX_KEYPAIR_LENGTH),
                  index=True, nullable=False, default=None)

    name = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH),
        index=True, nullable=False, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(self, code, name, enabled=1):
        """Language Constructor"""
        self.code = code
        self.name = name
        self.enabled = enabled


class Favorite(BASE):
    """Class defining the pt_favorite table of the database."""

    __tablename__ = 'pt_favorite'
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )

    idx_favorite = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_user = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_user.idx_user'),
        index=True, nullable=False, server_default='1')

    idx_chart = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_chart.idx_chart'),
        index=True, nullable=False, server_default='1')

    order = Column(
        BIGINT(unsigned=True), nullable=False, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    # Use cascade='delete,all' to propagate the deletion of a row
    # to rows in the tables used by foreign keys
    user = relationship(
        User,
        backref=backref(
            'favorite_user', uselist=True, cascade='delete,all'))

    chart = relationship(
        Chart,
        backref=backref(
            'favorite_chart', uselist=True, cascade='delete,all'))


class AgentXlate(BASE):
    """Class defining the pt_agent_xlate table of the database."""

    __tablename__ = 'pt_agent_xlate'
    __table_args__ = (
        UniqueConstraint('idx_language', 'agent_program'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_agent_xlate = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_language = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_language.idx_language'),
        index=True, nullable=False, server_default='1')

    agent_program = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    translation = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a row
    # to rows in the tables used by foreign keys
    language = relationship(
        Language,
        backref=backref(
            'agent_xlate_language', uselist=True, cascade='delete,all'))

    def __init__(self, idx_language, agent_program, translation, enabled=1):
        """PairXlate Constructor"""
        self.idx_language = idx_language
        self.agent_program = agent_program
        self.translation = translation
        self.enabled = enabled


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
        VARBINARY(MAX_KEYPAIR_LENGTH),
        index=True, nullable=False, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(self, name, enabled=1):
        """PairXlateGroup Constructor"""
        self.name = name
        self.enabled = enabled


class PairXlate(BASE):
    """Class defining the pt_pair_xlate table of the database."""

    __tablename__ = 'pt_pair_xlate'
    __table_args__ = (
        UniqueConstraint('idx_language', 'key', 'idx_pair_xlate_group'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_pair_xlate = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_pair_xlate_group = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_pair_xlate_group.idx_pair_xlate_group'),
        index=True, nullable=False, server_default='1')

    idx_language = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_language.idx_language'),
        index=True, nullable=False, server_default='1')

    key = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    translation = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    units = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH),
        index=True, nullable=False, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a
    # PairXlateGroup onto its PairXlate
    pair_xlate_group = relationship(
        PairXlateGroup,
        backref=backref(
            'pair_xlate_pair_xlate_group', uselist=True, cascade='delete,all'))

    # Use cascade='delete,all' to propagate the deletion of a
    # Language onto its PairXlate
    language = relationship(
        Language,
        backref=backref(
            'pair_xlate_language', uselist=True, cascade='delete,all'))

    def __init__(self, idx_pair_xlate_group, idx_language, key, translation,
                 units, enabled=1):
        """PairXlate Constructor"""
        self.idx_pair_xlate_group = idx_pair_xlate_group
        self.idx_language = idx_language
        self.key = key
        self.translation = translation
        self.units = units
        self.enabled = enabled


class Agent(BASE):
    """Class defining the pt_agent table of the database."""

    __tablename__ = 'pt_agent'
    __table_args__ = (
        UniqueConstraint('agent_id', 'agent_polled_target'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_agent = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_pair_xlate_group = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_pair_xlate_group.idx_pair_xlate_group'),
        index=True, nullable=False, server_default='1')

    agent_id = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    agent_polled_target = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    agent_program = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), nullable=False, default=None)

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a
    # PairXlateGroup onto its Agent
    pair_xlate_group = relationship(
        PairXlateGroup,
        backref=backref(
            'agent_pair_xlate_group', uselist=True, cascade='delete,all'))


class DataPoint(BASE):
    """Class defining the pt_datapoint table of the database."""

    __tablename__ = 'pt_datapoint'
    __table_args__ = (
        {'mysql_engine': 'InnoDB'}
    )

    idx_datapoint = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_agent = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_agent.idx_agent'),
        index=True, nullable=False, server_default='1')

    checksum = Column(
        VARBINARY(512), unique=True, nullable=True, default=None)

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

    # Use cascade='delete,all' to propagate the deletion of a
    # Agent onto its DataPoint
    agent = relationship(
        Agent,
        backref=backref(
            'datapoint_agent', uselist=True, cascade='delete,all'))


class ChartDataPoint(BASE):
    """Class defining the pt_chart_datapoint table of the database."""

    __tablename__ = 'pt_chart_datapoint'
    __table_args__ = (
        UniqueConstraint('idx_chart', 'idx_datapoint'),
        {'mysql_engine': 'InnoDB'}
    )

    idx_chart_datapoint = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_datapoint = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_datapoint.idx_datapoint'),
        index=True, nullable=False)

    idx_chart = Column(
        BIGINT(unsigned=True),
        ForeignKey('pt_chart.idx_chart'),
        index=True, nullable=False, server_default='1')

    enabled = Column(
        BIGINT(unsigned=True), nullable=False, server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a
    # Language onto its AgentXlate
    datapoint = relationship(
        DataPoint,
        backref=backref(
            'chart_datapoint_datapoint', uselist=True, cascade='delete,all'))

    chart = relationship(
        Chart,
        backref=backref(
            'chart_datapoint_chart', uselist=True, cascade='delete,all'))


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

    key = Column(
        VARBINARY(MAX_KEYPAIR_LENGTH), index=True, nullable=True, default=None)

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
    # DataPoint onto its Glue
    datapoint = relationship(
        DataPoint,
        backref=backref(
            'glue_datapoint', uselist=True, cascade='delete,all'))

    # Use cascade='delete,all' to propagate the deletion of a
    # Pair onto its Glue
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
        index=True, nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(NUMERIC(40, 10), nullable=False, default='1')

    # Use cascade='delete,all' to propagate the deletion of a
    # DataPoint onto its Data
    datapoint = relationship(
        DataPoint,
        backref=backref(
            'data_checksum', uselist=True, cascade='delete,all'))
