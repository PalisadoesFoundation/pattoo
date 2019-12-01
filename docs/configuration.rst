Configuration
=============

After installation, you will need to create a configuration file in a directory dedicated to ``pattoo``.

Set the  Configuration Directory Location
-----------------------------------------

You must set the location of the configuration directory by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this:

.. code-block:: bash

    $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo`` will read any ``.yaml`` files found in this directory for configuration parameters.

Beginners should use a single file. For the purposes of this document we will assume this file is called ``etc/config.yaml``.

Make sure that files in this directory are editable by the user that will be running ``pattoo`` daemons.

Copy the Template to Your Configuration Directory
-------------------------------------------------

Copy the template file in the ``examples/etc`` directory to the ``PATTOO_CONFIGDIR`` location.

.. code-block:: bash

    $ cp examples/etc/config.yaml.template \
      /path/to/configuration/directory/config.yaml

The next step is to edit the contents of ``config.yaml``

Edit Your Configuration
-----------------------

Take some time to read up on ``YAML`` formatted files if you are not familiar with them. A background knowledge is always helpful.

The ``config.yaml`` file created from the template will have sections that you will need to edit with custom values. Don't worry, these sections are easily identifiable as they all start with ``PATTOO_``

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items (if applicable).

.. code-block:: yaml

   main:
       log_level: debug
       log_directory: PATTOO_LOG_DIRECTORY
       cache_directory: PATTOO_CACHE_DIRECTORY
       daemon_directory: PATTOO_DAEMON_DIRECTORY
       language: en
       polling_interval: 300

   pattoo-api-agentd:

       api_ip_bind_port: 20201

   pattoo-apid:

       api_ip_bind_port: 20202

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
   * -
     - ``language``
     - Language  to be used in reporting statistics in JSON output. Language files can be found in the ``metadata/language/agents/`` directory.
   * -
     - ``polling_interval``
     - Interval of data collection and posting in seconds. This value should be the same for all ``pattoo`` configurations in your universe.
   * - ``pattoo-api-agentd``
     -
     -
   * -
     - ``api_ip_bind_port``
     - TCP port of used by the ``pattoo-api-agentd`` daemon for accepting data from remote ``pattoo`` agents. Default of 20201.
   * - ``pattoo-apid``
     -
     -
   * -
     - ``pattoo-apid``
     - TCP port of used by the ``pattoo-apid`` daemon when creating its API used by the ``pattoo`` web UI. Default of 20202. This port must be different from the one used by ``pattoo-api-agentd``.
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


Notes
-----

Here are some additional tips.

#. You can create a separate configuration file for each section. If you are doing this, make sure there is only one file per agent section. Keep the mandtatory configurations sections in a separate file for simplicity. Practice on a test system before doing this. *Start with a single file first to gain confidence.*
