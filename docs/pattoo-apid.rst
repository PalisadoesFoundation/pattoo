Pattoo Web API
==============

``pattoo-apid`` serves ``pattoo`` agent data from the database via a web API.

Installation
------------

Follow these steps.

#. Follow the installation steps in the :doc:`installation` file.
#. Configure the main section of the configuration file following the steps in :doc:`configuration` file.
#. Start the desired daemons using the commands below. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Usage
-----

``pattoo-apid`` has a simple command structure.

The daemon will require a configuration file in the ``etc/`` directory. See the configuration section for details.

.. code-block:: bash

   $ bin/pattoo-apid.py --help
   usage: pattoo-apid.py [-h] [--start] [--stop] [--status] [--restart]
                            [--force]

   optional arguments:
     -h, --help  show this help message and exit
     --start     Start the agent daemon.
     --stop      Stop the agent daemon.
     --status    Get daemon daemon status.
     --restart   Restart the agent daemon.
     --force     Stops or restarts the agent daemon ungracefully when used with --stop or
                 --restart.
   $

Configuration
-------------

No additional configuration steps beyond that in the :doc:`configuration` file are required.

Testing
-------
There are a number of steps you can take to make sure everything is OK.

#. If you have setup the daemon for ``systemd`` then you can use the ``systemctl`` command to get the status of the daemon.
#. The daemon should be running on the port configured with the ``ip_bind_port`` parameter. Use the ``netstat`` command to verify this.
#. Visit the URL ``http://localhost:20202/pattoo/api/v1/web/status`` to get the status page.
#. Use the :doc:`troubleshooting` for further steps to take
