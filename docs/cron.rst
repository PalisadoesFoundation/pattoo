Periodic Jobs
=============

The ``pattoo_ingester``
-----------------------

The ``bin/pattoo_ingester.py`` script reads cached agent data files and imports them into the database. Make it run at least every five minutes to process the data. Here is a sample crontab file.

#. Copy the the ``examples/cron.d/pattoo`` file to the ``/etc/cron.d`` directory.
#. Edit the ``PATTOO_CONFIGDIR`` path accordingly.
#. Edit the ``path/to/installation/`` path accordingly.

Logrotate Configuration
-----------------------

The default ``pattoo`` debug logging mode can quickly create large logging files. The logrotate utility can automatically compress and archive them.

#. Copy the the ``examples/logrotate.d/pattoo`` file to the ``/etc/logrotate.d`` directory.
#. Edit the file path accordingly.

Read up on the logrotate utility if you are not familiar with it. The documentation is easy to follow.
