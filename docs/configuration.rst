Configuration
=============

After installation, you will need to create a configuration file in a directory dedicated to ``pattoo``.

Set the  Configuration Directory Location
-----------------------------------------

You must set the location of the configuration directory by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this:

.. code-block:: bash

    $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo`` will only read the configuration placed in a file named ``pattoo_server.yaml`` in this directory.

Make sure that files in this directory are readable by the user that will be running ``pattoo`` daemons or scripts.

Copy the Template to Your Configuration Directory
-------------------------------------------------

Copy the template file in the ``examples/etc`` directory to the ``PATTOO_CONFIGDIR`` location.

**NOTE:** If a ``/path/to/configuration/directory/pattoo_server.yaml`` file already exists in the directory then skip this step and edit the file according to the steps in following sections.

.. code-block:: bash

    $ cp examples/etc/pattoo_server.yaml.template \
      /path/to/configuration/directory/pattoo_server.yaml

The next step is to edit the contents of ``pattoo_server.yaml``

Edit Your Configuration
-----------------------

Take some time to read up on ``YAML`` formatted files if you are not familiar with them. A background knowledge is always helpful.

The ``pattoo_server.yaml`` file created from the template will have sections that you will need to edit with custom values. Don't worry, these sections are easily identifiable as they all start with ``PATTOO_``

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items (if applicable).

.. code-block:: yaml

   main:
       log_level: debug
       log_directory: PATTOO_LOG_DIRECTORY
       cache_directory: PATTOO_CACHE_DIRECTORY
       daemon_directory: PATTOO_DAEMON_DIRECTORY

   pattoo_api_agentd:

       ip_bind_port: 20201
       ip_listen_address: 127.0.0.1

   pattoo_apid:

       ip_bind_port: 20202
       ip_listen_address: 127.0.0.1

   pattoo_ingesterd:

       ingester_interval: 3600
       batch_size: 500

   db:
       db_pool_size: 10
       db_max_overflow: 10
       db_hostname: PATTOO_DB_HOSTNAME
       db_name: PATTOO_DB_NAME
       db_password: PATTOO_DB_PASSWORD
       db_username: PATTOO_DB_USERNAME

Configuration Explanation
^^^^^^^^^^^^^^^^^^^^^^^^^

This table outlines the purpose of each configuration parameter.

.. list-table::
   :header-rows: 1

   * - Section
     - Config Options
     - Description
   * - ``main``
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
   * - ``pattoo_api_agentd``
     -
     -
   * -
     - ``ip_listen_address``
     - IP address used by the ``pattoo_api_agentd`` daemon for accepting data from remote ``pattoo`` agents. Default of '0.0.0.0' which indicates listening on all available network interfaces.
   * -
     - ``ip_bind_port``
     - TCP port of used by the ``pattoo_api_agentd`` daemon for accepting data from remote ``pattoo`` agents. Default of 20201.
   * - ``pattoo_apid``
     -
     -
   * -
     - ``ip_listen_address``
     - IP address used by the ``pattoo_apid`` daemon for providing data to remote clients.
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
   * - ``db``
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
