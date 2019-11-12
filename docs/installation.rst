
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
#. Install the required packages using the ``pip_requirements`` document in the `pattoo` root directory

   .. code-block:: bash

      $ sudo pip3 install -r pip_requirements.txt

#. Populate the mandatory sections of the :doc:`configuration`
#. Create the `MySQL` or `MariaDB` database for `pattoo` with the correct authentication parameters provided in the :doc:`configuration`
#. Run the installation script

   .. code-block:: bash

      $ sudo setup/install.py

#. Start the `bin/pattoo-api-agentd.py` daemon to accept data sent by `pattoo` agents. :doc:`pattoo-api-agentd`
#. Start the `bin/pattoo-apid.py` daemon to provide `pattoo` agent data to web applications. :doc:`pattoo-apid`




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
