Installation Modes
===================

After running below command:
   .. code-block:: bash

      $ setup/install.py


You will be presented with two different installation options. The developer installation and the normal installation.

   .. code-block:: bash

      $ This program is the CLI interface to configuring pattoo

      positional arguments:
      {install,developer}
        install            Install pattoo. Type install --help to see additional 
                           arguments
        developer          Set up pattoo for unittesting. Type --help to see additional 
                           arguments

      optional arguments:
      -h, --help           show this help message and exit

**Note)** Both installation modes come with 5 installation options, however, only three are usable in the developer mode, that being ``all``, ``pip`` and ``configuration``. Due to the ``systemd`` and ``docker`` installation modes requiring ``sudo`` privileges to be run

**Installation Options**
^^^^^^^^^^^^^^^^^^^^^^^^

The code block below showcases all of the installation options available for installing pattoo.

   .. code-block:: bash

      $ sudo setup/install.py install --help

      positional arguments:
        {all,configuration,database,docker,pip,systemd}
          all                 Install all pattoo components
          configuration       Install configuration
          database            Install database
          docker              Install pattoo docker container.
          pip                 Install PIP
          systemd             Install systemd service files


**All** - This installation option is used for installing the configuration, pip packages, database tables and system daemons for pattoo

**Configuration** - This installation option is used for only installing the configuration files specified for pattoo in the ``PATTOO_CONFIGDIR`` location.


**Database** - This installation option is used for only setting up the database tables for pattoo.

**Docker** - This installation option is used for building the docker container for pattoo, based on the ``Dockerfile`` placed into the root directory of pattoo. A more in-depth overview of the docker installation option can be found at :doc:`docker`.


**Pip** - This installation option is used for only installing the python dependencies for pattoo.


**Systemd** - This installation option is used for only installing or reinstalling the pattoo system daemons, namely the ``pattoo_apid``, the ``pattoo_api_agentd``, and the ``pattoo_ingesterd``. 


**Normal Installation**
^^^^^^^^^^^^^^^^^^^^^^^

This installation mode is mainly for setting up your environment for unit testing, by populating the unit test database.

To bring up the installation options for the developer installation type the following command:
   .. code-block:: bash

      $ setup/install.py install --help


**Developer Installation**
^^^^^^^^^^^^^^^^^^^^^^^^^^

This installation mode is mainly for setting up your environment for unit testing, by populating the unit test database.

To bring up the installation options for the developer installation type the following command:
   .. code-block:: bash

      $ setup/install.py developer --help