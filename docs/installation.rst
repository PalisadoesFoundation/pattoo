
Basic Installation
==================

This section covers some key steps to get you started.

Prerequisites
-------------

There are some software components that need to be installed prior to starting.

#. ``pattoo`` requires the installation of a MySQL or MariaDB database. Make sure this software is installed beforehand.
#. ``pattoo`` only runs on Python 3.6 or higher

Let's install the software.

Installation
------------

Follow these steps.

#. Install ``git`` on your system.
#. Select and create the parent directory in which you want to install ``pattoo``.

    .. code-block:: bash

       $ mkdir -p /installation/parent/directory
       $ cd /installation/parent/directory

#. Clone the repository to the parent directory using the ``git clone`` command. You can also choose to downloading and unzip the file in the parent directory. The repository can be found at: https://github.com/PalisadoesFoundation/pattoo

    .. code-block:: bash

       $ cd /installation/parent/directory
       $ git clone https://github.com/PalisadoesFoundation/pattoo.git

#. Enter the ``/installation/parent/directory/pattoo`` directory with the ``pattoo`` files.
#. Install the required packages using the ``pip_requirements`` document in the ``pattoo`` root directory

   .. code-block:: bash

      $ pip3 install -r pip_requirements.txt

#. Create the ``MySQL`` or ``MariaDB`` database for ``pattoo`` with the correct authentication parameters provided in the :doc:`configuration` In this example adjust the name of your database and the password accordingly.

    .. code-block:: bash

       $ sudo mysql

    .. code-block:: sql

        CREATE DATABASE pattoo;
        GRANT ALL PRIVILEGES ON pattoo.* TO pattoo@"localhost" IDENTIFIED BY 'PATTOO_PASSWORD';
        FLUSH PRIVILEGES;
        exit;

#. Populate the mandatory sections of the :doc:`configuration`
#. Run the installation script

   .. code-block:: bash

      $ sudo setup/install.py

#. Configure the required ``cron`` jobs. :doc:`cron`
#. Start the ``bin/pattoo_api_agentd.py`` daemon to accept data sent by ``pattoo`` agents. :doc:`pattoo_api_agentd`
#. Start the ``bin/pattoo_apid.py`` daemon to provide ``pattoo`` agent data to web applications. :doc:`pattoo_apid`


Configuring systemd Daemons
---------------------------

You can also setup all the ``pattoo`` daemons as system daemons by executing the ``setup/systemd/bin/install_systemd.py`` script.

The script requires you to specify the following parameters. Make sure you have a username and group created for running your ``pattoo`` services.

.. code-block:: bash

    usage: install_systemd.py [-h] -f CONFIG_DIR -i INSTALLATION_DIR -u USERNAME
                              -g GROUP

    optional arguments:
      -h, --help            show this help message and exit
      -f CONFIG_DIR, --config_dir CONFIG_DIR
                            Directory where the pattoo configuration files will be
                            located
      -i INSTALLATION_DIR, --installation_dir INSTALLATION_DIR
                            Directory where the pattoo is installed. (Must end
                            with ``/pattoo``)
      -u USERNAME, --username USERNAME
                            Username that will run the daemon
      -g GROUP, --group GROUP
                            User group to which username belongs

**Note** The daemons are not enabled or started by default. You will have to do this separately using the ``systemctl`` command after running the script.


.. code-block:: bash

   $ sudo setup/systemd/bin/install_systemd.py --config_dir=~/GitHub/pattoo/etc --user pattoo --group pattoo --install ~/GitHub/pattoo

   SUCCESS! You are now able to start/stop and enable/disable the following systemd services:

   pattoo_api_agentd.service
   pattoo_apid.service

   $
