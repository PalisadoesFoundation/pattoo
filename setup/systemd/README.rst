Pattoo Daemon Setup
===================

This page outlines the steps required to install the necessary ``pattoo`` daemons on systems that support ``systemd``.

Installation
------------

Run the ``bin/install_systemd.py`` script. It will install the correct directories.

Run the script with the ``-f configuration_directory`` flag to ensure correct operation.

.. code-block::

 $ sudo bin/install_systemd.py -f /path/to/configuration/directory

Use the ``--help`` flag to get a complete list of supported options.

.. code-block::

 usage: install_systemd.py [-h] -f CONFIG_DIR

 optional arguments:
   -h, --help            show this help message and exit
   -f CONFIG_DIR, --config_dir CONFIG_DIR
                        Directory where the pattoo configuration files will be
                        located

Activation
----------

Use the ``systemctl`` commands listed in the script's output to enable, disable, start and stop the various daemons.
