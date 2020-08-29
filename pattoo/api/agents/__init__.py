"""Initialize the PATTOO_API_AGENT module."""

# Standard imports
import hashlib
import uuid

# Import PIP3 libraries
from flask import Flask
from flask_session import Session

# Define the global URL prefix
from pattoo_shared.constants import PATTOO_API_AGENT_PREFIX
from pattoo_shared import configuration
from pattoo_shared import files
from pattoo_shared import encrypt

# Import PATTOO_API_AGENT Blueprints
from pattoo.api.agents.post import POST
from pattoo.api.agents.status import STATUS
from pattoo.constants import PATTOO_API_AGENT_NAME

# Setup flask
PATTOO_API_AGENT = Flask(__name__)

# Add secret key to Flask for cookies
PATTOO_API_AGENT.config['SECRET_KEY'] = hashlib.sha256(
    str(uuid.uuid4()).encode()).hexdigest()

# Store the session cookies locally (for local session)
PATTOO_API_AGENT.config['SESSION_TYPE'] = 'filesystem'

# The maximum amount of session cookies to store (for local session)
PATTOO_API_AGENT.config['SESSION_FILE_THRESHOLD'] = 500

# Sign cookies (for local session)
PATTOO_API_AGENT.config['SESSION_USE_SIGNER'] = True

# Store cookies permanently (for local session)
PATTOO_API_AGENT.config['SESSION_PERMANENT'] = False

# Location to store cookies (for local session)
PATTOO_API_AGENT.config['SESSION_FILE_DIR'] = \
    files.get_session_cache_dir(configuration.BaseConfig())

# Initialize Session plugin (for local session)
sess = Session()
sess.init_app(PATTOO_API_AGENT)

# Register Blueprints
PATTOO_API_AGENT.register_blueprint(
    POST, url_prefix=PATTOO_API_AGENT_PREFIX)
PATTOO_API_AGENT.register_blueprint(
    STATUS, url_prefix=PATTOO_API_AGENT_PREFIX)
