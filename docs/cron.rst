Periodic Jobs
=============

The ``pattoo_ingester``
-----------------------

There are two options to ingesting (transferring) data posted by agents to the database:

#. Running the ``pattoo_ingesterd`` daemon which is a part of the installation process and should require no further action.
#. If you don't have root access to run the daemon then create a cron job to run the ``bin/pattoo_ingester.py`` script. Make it run at least every five minutes to process the data.
    #. Copy the the ``examples/cron.d/pattoo`` file to your crontab file.
    #. Edit the ``PATTOO_CONFIGDIR`` path accordingly.
    #. Edit the ``path/to/installation/`` path accordingly.

Logrotate Configuration
-----------------------

The default ``pattoo`` debug logging mode can quickly create large logging files. The logrotate utility can automatically compress and archive them.

#. Copy the the ``examples/logrotate.d/pattoo`` file to the ``/etc/logrotate.d`` directory.
#. Edit the file path accordingly.

Read up on the logrotate utility if you are not familiar with it. The documentation is easy to follow.
