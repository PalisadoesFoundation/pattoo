"""Module that defines universal constants used only by pattoo.

The aim is to have a single location for constants that may be used across
agents to prevent the risk of duplication.

"""

from pattoo_shared.constants import PATTOO_API_SITE_PREFIX

###############################################################################
# Constants for pattoo Web API
###############################################################################

PATTOO_API_WEB_PREFIX = '{}/web'.format(PATTOO_API_SITE_PREFIX)
PATTOO_API_WEB_EXECUTABLE = 'pattoo-apid'
PATTOO_API_WEB_PROXY = '{}-gunicorn'.format(
    PATTOO_API_WEB_EXECUTABLE)
PATTOO_API_WEB_REST_PREFIX = '{}/rest'.format(PATTOO_API_WEB_PREFIX)
