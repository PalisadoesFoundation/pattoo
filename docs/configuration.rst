###################
Configuration Guide
###################

After installation, you will need to create a configuration file in a directory dedicated to ``pattoo``.

*********************************************
Setting the  Configuration Directory Location
*********************************************

Currently the configuration directory is automatically set when the installationscript is run


*********************
Configuration Options

*********************


There are two ways to configure ``pattoo``. These are the:

#. Quick Method
#. Expert Method

Quick Method
============

Use the quick method if you are new to ``pattoo``.

.. code-block:: bash
    $ sudo setup/pattoo_installation.py install configuration
    

The above command will set the most optimal defaults for your system for pattoo.

To guarantee success you will need to know the following beforehand.

#. ``db_name``: Database name
#. ``db_username``: Database username
#. ``db_password``: Database password
#. ``db_hostname``: Database hostname



Expert Method
=============

This section goes into configuration parameters in great detail.

Copy the Templates to Your Configuration Directory
--------------------------------------------------

Follow the steps in this section if you don't already have a valid configuration files in your ``PATTOO_CONFIGDIR`` directory.

Copy the template files in the ``examples/etc`` directory to the ``PATTOO_CONFIGDIR`` location.

**NOTE:** If a ``/path/to/configuration/directory/pattoo_server.yaml`` or ``/path/to/configuration/directory/pattoo.yaml`` file already exists in the directory then skip this step and edit the file according to the steps in following sections.

.. code-block:: bash

        $ cp examples/etc/pattoo_server.yaml.template \
            /path/to/configuration/directory/pattoo_server.yaml

        $ cp examples/etc/pattoo.yaml.template \
            /path/to/configuration/directory/pattoo.yaml

The next step is to edit the contents of both files.

Edit Your Configuration Files
-----------------------------

The ``pattoo`` server uses two configuration files:

#. ``pattoo.yaml``: Provides general configuration information for all ``pattoo`` related applications. ``pattoo.yaml`` also defines how ``pattoo`` agents should connect to the ``pattoo`` server APIs.
#. ``pattoo_server.yaml``: Provides configuration details for all the ``pattoo`` server's API daemons. These APIs accept data from ``pattoo`` agents and also provide data to ``pattoo`` related applications through your browser.

Take some time to read up on ``YAML`` formatted files if you are not familiar with them. A background knowledge is always helpful.

Server Configuration File
.........................

The ``pattoo_server.yaml`` file created from the template will have sections that you will need to edit with custom values. Don't worry, these sections are easily identifiable as they all start with ``PATTOO_``

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items (if applicable).

.. code-block:: yaml

   pattoo_api_agentd:

       ip_bind_port: 20201
       ip_listen_address: 0.0.0.0

   pattoo_apid:

       ip_bind_port: 20202
       ip_listen_address: 0.0.0.0

   pattoo_ingesterd:

       ingester_interval: 3600
       batch_size: 500

   pattoo_db:
       db_pool_size: 10
       db_max_overflow: 10
       db_hostname: PATTOO_DB_HOSTNAME
       db_name: PATTOO_DB_NAME
       db_password: PATTOO_DB_PASSWORD
       db_username: PATTOO_DB_USERNAME

Server Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter.

.. list-table::
   :header-rows: 1

   * - Section
     - Configuration Parameters
     - Description
   * - ``pattoo_api_agentd``
     -
     -
   * -
     - ``ip_listen_address``
     - IP address used by the ``pattoo_api_agentd`` daemon for accepting data from remote ``pattoo`` agents. Default of '0.0.0.0' which indicates listening on all available network interfaces. You can also use IPv6 nomenclature such as ``::``. The ``pattoo`` APIs don't support IPv6 and IPv4 at the same time.
   * -
     - ``ip_bind_port``
     - TCP port of used by the ``pattoo_api_agentd`` daemon for accepting data from remote ``pattoo`` agents. Default of 20201.
   * - ``pattoo_apid``
     -
     -
   * -
     - ``ip_listen_address``
     - IP address used by the ``pattoo_apid`` daemon for providing data to remote clients. Default of '0.0.0.0' which indicates listening on all available network interfaces. You can also use IPv6 nomenclature such as ``::``. The ``pattoo`` APIs don't support IPv6 and IPv4 at the same time.
   * -
     - ``ip_bind_port``
     - TCP port of used by the ``pattoo_apid`` daemon for providing data to remote clients. Default of 20202.
   * - ``pattoo_ingesterd``
     -
     -
   * -
     - ``ingester_interval``
     - The interval between checking for new agent files in the cache directory. Only valid if using the ``pattoo_ingesterd`` daemon.
   * -
     - ``batch_size``
     - The number of files to read per processing batch until all files are processed.
   * - ``pattoo_db``
     -
     -
   * -
     - ``db_hostname``
     - Hostname of the database server
   * -
     - ``db_username``
     - Username required for database access
   * -
     - ``db_password``
     - Password required for database access
   * -
     - ``db_name``
     - Name of database
   * -
     - ``db_pool_size``
     - This is the largest number of connections that will be keep persistently with the database
   * -
     - ``db_max_overflow``
     - Maximum overflow size. When the number of connections reaches the size set in ``db_pool_size``, additional connections will be returned up to this limit. This is the floating number of additional database connections to be made available.


Client Configuration File
.........................

The ``pattoo.yaml`` file created from the template will have sections that you will need to edit with custom values. Don't worry, these sections are easily identifiable as they all start with ``PATTOO_``

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items (if applicable).

.. code-block:: yaml

   pattoo:
       log_level: debug
       log_directory: PATTOO_LOG_DIRECTORY
       cache_directory: PATTOO_CACHE_DIRECTORY
       daemon_directory: PATTOO_DAEMON_DIRECTORY
       system_daemon_directory: PATTOO_SYSTEM_DAEMON_DIRECTORY


Client Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter.

.. list-table::
   :header-rows: 1

   * - Section
     - Configuration Parameters
     - Description
   * - ``pattoo``
     -
     -
   * -
     - ``log_directory``
     - Path to logging directory. Make sure the username running the daemons have RW access to files there.
   * -
     - ``log_level``
     - Default level of logging. ``debug`` is best for troubleshooting.
   * -
     - ``cache_directory``
     - Directory that will temporarily store data data from agents prior to be added to the ``pattoo`` database.
   * -
     - ``daemon_directory``
     - Directory used to store daemon related data that needs to be maintained between reboots
   * -
     - ``system_daemon_directory``
     - Directory used to store daemon related data that should be deleted between reboots. This should only be configured if you are running ``pattoo`` daemons as ``systemd`` daemons. The ``systemd`` daemon installation procedure automatically adjusts this configuration. This parameter defaults to the ``daemon_directory`` value if it is not configured. 
