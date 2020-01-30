Pattoo Ingester Daemon
======================

``pattoo_ingesterd`` batch processes agent data received by the ``pattoo`` agent API daemon.

Installation
------------

Follow these steps.

#. Follow the installation steps in the :doc:`installation` file.
#. Configure the main section of the configuration file following the steps in :doc:`configuration` file.
#. Start the desired daemons using the commands below. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Usage
-----

``pattoo_ingesterd`` has a simple command structure.

The daemon will require a configuration file in the ``etc/`` directory. See the configuration section for details.

.. code-block:: bash

   $ bin/pattoo_ingesterd.py --help
   usage: pattoo_ingesterd.py [-h] [--start] [--stop] [--status] [--restart]
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
#. Use the :doc:`troubleshooting` for further steps to take
