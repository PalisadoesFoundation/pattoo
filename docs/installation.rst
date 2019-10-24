
Basic Installation
==================

This section covers some key steps to get you started.

Installation
------------

Follow these steps.

#. Install the required packages using the ``pip_requirements`` document in the root directory

   .. code-block::

      $ sudo pip3 install -r pip_requirements.txt

#. Populate the mandatory sections of the :doc:`configuration`

Configuring Agents as systemd Daemons
-------------------------------------

You can also setup all the ``patoo`` daemons as system daemons by executing the ``setup/systemd/bin/install_systemd.py`` script.

You have to specify a ``--config_dir`` defining the configuration file directory.

**Note** The daemons are not enabled or started by default. You will have to do this separately using the ``systemctl`` command after running the script.

.. code-block:: bash

   $ sudo setup/systemd/bin/install_systemd.py --config_dir ~/GitHub/pattoo/etc

   SUCCESS! You are now able to start/stop and enable/disable the following systemd services:

   pattoo-api-agentd.service

   $
