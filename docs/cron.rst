Periodic Jobs
=============

You will need to configure some jobs to improve ``pattoo`` performance and troubleshooting.

Logrotate Configuration
-----------------------

The default ``pattoo`` debug logging mode can quickly create large logging files. The logrotate utility can automatically compress and archive them.

#. Copy the the ``examples/logrotate.d/pattoo`` file to the ``/etc/logrotate.d`` directory.
#. Edit the file path accordingly.

Read up on the logrotate utility if you are not familiar with it. The documentation is easy to follow.
