Configuring systemd Daemons
===========================

You can also setup all the ``pattoo`` related daemons located in this GitHub repository as system daemons by executing the ``setup/systemd/bin/install_systemd.py`` script.

The script requires you to specify the following parameters. Make sure you have a username and group created for running your ``pattoo`` services.

.. code-block:: bash

    usage: install_systemd.py [-h] -f CONFIG_DIR -u USERNAME -g GROUP

    optional arguments:
      -h, --help            show this help message and exit
      -f CONFIG_DIR, --config_dir CONFIG_DIR
                            Directory where the pattoo configuration files will be located
      -u USERNAME, --username USERNAME
                            Username that will run the daemon
      -g GROUP, --group GROUP
                            User group to which username belongs


**Note** The daemons are not enabled or started by default. You will have to do this separately using the ``systemctl`` command after running the script.


.. code-block:: bash

   $ sudo setup/systemd/bin/install_systemd.py --user pattoo --group pattoo --config_dir /etc/pattoo

   SUCCESS! You are now able to start/stop and enable/disable the following systemd services:

   pattoo_api_agentd.service
   pattoo_apid.service
   pattoo_ingesterd.service

   $
