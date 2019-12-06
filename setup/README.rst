Pattoo Installation and Setup
=============================

This page outlines the steps required to install the ``pattoo`` application suite.

Installation
------------

Run the ``install.py`` script in this directory. It will:

1. Let you know which ``python pip3`` packages you will need to install.
2. Do basic configuration checks to make sure ``pattoo`` will operate correctly.
3. Check connectivity to the ``pattoo`` database server and install all the correct tables.

When finished you will need to:

1. Start the ``pattoo_api_agentd.py`` script afterwards to start receiving agent data.
2. Configure and start the various ``pattoo`` agents so that they send data to the ``pattoo`` server.

Daemon Setup
------------

You can run the various ``pattoo`` processes as ``systemd`` daemons. Read the `Daemon Setup Documentation <systemd/>`_ in the 'setup/systemd' directory for more details.
