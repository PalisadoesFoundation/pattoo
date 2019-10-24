Configuration
=============

After installation, you will need to edit a configuration file in the ``etc/`` directory. Pattoo will read any ``.yaml`` files found in this directory for configuration parameters.

For the sake of simplicity we will assume there is one file called ``etc/config.yaml``.

Make sure you have configured the ``main`` and ``remote_api`` sections of ``etc/config.yaml`` file before adding any sections for any data gathering `Pattoo Agents daemons <https://pattoo-agents.readthedocs.io/>`_  that you may also want to operate on the server.

Custom Directory Location
-------------------------

You can selectively set the location of the configuration directory by using the ``PATTOO_CONFIGDIR`` environmental variable.

This can be useful for:


#. Automated deployments
#. Software developer code testing

By default the ``etc/`` directory of the repository is used for all configuration file searches.

Mandatory Configuration Sections
--------------------------------

.. code-block:: yaml

   main:
       log_level: debug
       log_directory: ~/GitHub/pattoo-agents/log
       cache_directory: ~/GitHub/pattoo-agents/cache
       daemon_directory: ~/GitHub/pattoo-agents/daemon
       language: en
       polling_interval: 300

   remote_api:
       api_ip_address: 192.168.1.100
       api_ip_bind_port: 6000
       api_uses_https: False
       api_listen_address: 0.0.0.0

Configuration Explanation
^^^^^^^^^^^^^^^^^^^^^^^^^

This table outlines the purpose of each configuration parameter

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
     - Directory of unsuccessful data posts to ``pattoodb``
   * -
     - ``daemon_directory``
     - Directory used to store daemon related data that needs to be maintained between reboots
   * -
     - ``language``
     - Language  to be used in reporting statistics in JSON output. Language files can be found in the ``metadata/language/agents/`` directory.
   * -
     - ``polling_interval``
     - Interval of data collection and posting in seconds
   * - ``remote_api``
     -
     - **Note** The ``remote_api`` section is not required for ``patoo-os-spoked`` configurations
   * -
     - ``api_ip_address``
     - IP address of remote ``pattoodb`` server
   * -
     - ``api_ip_bind_port``
     - Port of remote ``pattoodb`` server
   * -
     - ``api_uses_https``
     - Use ``https`` when sending data  to remote ``pattoodb`` server
   * -
     - ``api_listen_address``
     - IP address on which the API server will listen. Setting this to ``0.0.0.0`` will make it listen on all IPv4 addresses. Setting to ``"0::"`` will make it listen on all IPv6 configured interfaces. It will not listen on IPv4 and IPv6 addresses simultaneously. You must **quote** all IPv6 addresses. The default is ``0.0.0.0``. This parameter is only used by the ``pattoo`` server.

Notes
-----

Here are some additional tips.

#. You can create a separate configuration file for each section. If you are doing this, make sure there is only one file per agent section. Keep the mandtatory configurations sections in a separate file for simplicity. Practice on a test system before doing this. *Start with a single file first to gain confidence.*
