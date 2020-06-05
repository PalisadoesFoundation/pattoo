"""Set up pattoo database."""
import pymysql
import os
import yaml
import configure
from shared import _run_script


def get_db_config(file_path):
    """
    Get pattoo server config.

    Args:
        file_path: The file path for the server config yaml file

    Returns:
        A dictionary containing the server configuration
    """
    with open(os.path.join(file_path, 'pattoo_server.yaml')) as config_file:
        return yaml.load(config_file)


def get_connection_details(server_config):
    """
    Get connection details.

    Args:
        server_config: A dictionary containing the server configuration

    Returns:
        A tuple with the necessary attributes to create a database connection
    """
    db_host = server_config['pattoo_db']['db_hostname']
    db_name = server_config['pattoo_db']['db_name']
    db_password = server_config['pattoo_db']['db_password']

    return (db_host, db_name, db_password)


def create_connection(connection_details):
    """
    Create connection for MySQL database.

    Args:
        connection_details: A tuple of the attributes needed to configure the
        database
    Returns:
        The database connection
    """
    db_connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password="")
    return db_connection


def create_database(db_connection, connection_details):
    """
    Create MySQL database.

    Args:
        server_config: A dictionary of the server's configuration
        connection_details: A tuple of the attributes needed to configure the
        database

    Returns:
        True if the database is successfully created, and False if it already
        exists
    """
    print("Attempting to create database...\n")
    # Set password policy
    db_connection.cursor().execute('SET GLOBAL validate_password_policy=LOW')
    db_name = connection_details[1]
    no_schema = db_connection.cursor().execute(
        'select schema_name from \
information_schema.schemata where schema_name = "{}";'.format(db_name))
    if no_schema != 1:
        db_connection.cursor().execute('create database {}'.format(db_name))
        print("Database successfully created\n")
        return True
    else:
        print('Database already exists')
        return False


def initialize_privilages(db_connection, connection_details):
    """
    Grant privileges for the pattoo db to allow the pattoo user to log in.

    Args:
        server_config: A dictionary of the server's configuration
        connection_details: A tuple of the attributes needed to configure the
        database

    Returns:
        None
    """
    db_host = connection_details[0]
    db_name = connection_details[1]
    db_pass = connection_details[2]
    db_connection.cursor().execute(('grant all privileges on \
{0}.* to {0}@{1} identified by \'{2}\';').format(db_name, db_host, db_pass))
    db_connection.cursor().exceute('flush privileges')


def configure_database():
    """
    Configure MySQL database.

    Args:
        None

    Returns:
        True for a successful configuration
    """
    print("Configuring database")
    # Obtain configuration directory
    config_dir = os.environ['PATTOO_CONFIGDIR']
    db_config = get_db_config(config_dir)
    connection_details = get_connection_details(db_config)
    # Create database connection
    connection = create_connection(connection_details)
    # Create database
    create_database(connection, connection_details)
    initialize_privilages(connection, connection_details)
