Performance and Troubleshooting
===============================

Performance tuning and troubleshooting are related. So we created a page for both!

Troubleshooting
---------------
Troubleshooting steps can be found in the `PattooShared troubleshooting documentation <https://pattoo-shared.readthedocs.io/en/latest/troubleshooting.html>`_

``pattoo`` Performance Tuning
-----------------------------

There are a number of ways to improve ``pattoo`` performance.

Use RAM disks for Caching
^^^^^^^^^^^^^^^^^^^^^^^^^

We have seen a 10X improvement in the ``pattoo_ingester`` records / second performance when using a RAM disk versus SSDs. We recommend using RAM disks and SSDs for your cache directory over regular hard drives in production environments.

Run the ``pattoo_ingester`` More Frequently
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pattoo_ingester`` needs to run periodically to import agent data files into the database. You want to ensure that it can keep up with this task. Check your logs to make sure that the completion time of each ``pattoo_ingester`` run is less than the configured ``polling_interval``. Increase the ``crontab`` frequency if it isn't.

Database Performance Improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``pattoo_ingester`` makes many connections to the database. You have a number of options if it crashes. Check your logs for the cause of errors to help you choose the best corrective action.

#. If the errors state that you have too many connections, then increase ``max_connections`` value in the server configuration file. The default is 200. Try 300 and increase as needed.

   .. code-block:: text

      [mysqld]
      max_connections = 300

#. If the errors mention ``pool_size`` or ``max_overflow``, then edit your configuration file and adjust those values.

    .. code-block:: yaml

        db_pool_size: 10
        db_max_overflow: 10

Reduce Logging
^^^^^^^^^^^^^^
The default ``pattoo`` ``debug`` logging level can create large files. This is done to make it easier to troubleshoot the initial installation. Set the level to ``info`` for most scenarios.
