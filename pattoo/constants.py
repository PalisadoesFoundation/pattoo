"""Module that defines universal constants used only by pattoo.

The aim is to have a single location for constants that may be used across
agents to prevent the risk of duplication.

"""
# Standard imports
import collections

###############################################################################
# Constants for pattoo Web API
###############################################################################

PATTOO_INGESTER_NAME = 'pattoo_ingester'
PATTOO_INGESTER_SCRIPT = '{}.py'.format(PATTOO_INGESTER_NAME)
PATTOO_INGESTERD_NAME = 'pattoo_ingesterd'
PATTOO_API_WEB_NAME = 'pattoo_apid'
PATTOO_API_WEB_PROXY = '{}-gunicorn'.format(
    PATTOO_API_WEB_NAME)
PATTOO_API_AGENT_NAME = 'pattoo_api_agentd'
PATTOO_API_AGENT_PROXY = '{}-gunicorn'.format(
    PATTOO_API_AGENT_NAME)

###############################################################################
# Constants for data ingestion
###############################################################################

IDXTimestampValue = collections.namedtuple(
    'IDXTimestampValue', 'idx_datapoint timestamp polling_interval value')

ChecksumLookup = collections.namedtuple(
    'ChecksumLookup', 'idx_datapoint last_timestamp polling_interval')
