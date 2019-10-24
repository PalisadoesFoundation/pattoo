
Basic Installation
==================

This section covers some key steps to get you started.

Installation
------------

Follow these steps.

#. Install `git` on your system.
#. Select the parent directory in which you want to install `pattoo`
#. Clone the repository to the parent directory using either the `git clone` command. You can also choose to downloading and unzip the file in the parent directory. The repository can be found at: https://github.com/PalisadoesFoundation/pattoo
#. Enter the directory with the `pattoo` files.
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
