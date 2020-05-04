Testing Your Code
=================

Make sure you create your own unittests for all the classes, methods, and functions you have created or modified. Place them in the `tests/` directory in a subdirectory that matches the relative location of your production code under the `pattoo/` directory.

Database Setup
--------------

The unittests assume that a MySQL / MariaDB testing database has been created with the following parameters:

* `db_hostname`: localhost
* `db_username`: travis
* `db_password`: K2nJ8kFdthEbuwXE
* `db_name`: pattoo_unittest

Create a database and grant full privileges to the `travis` user.

.. code-block::

      # mysql
      MariaDB [(none)]> CREATE DATABASE pattoo_unittest;
      MariaDB [(none)]> GRANT ALL PRIVILEGES ON pattoo_unittest.* TO 'travis'@'localhost' identified by 'K2nJ8kFdthEbuwXE';
      MariaDB [(none)]> FLUSH PRIVILEGES;
      MariaDB [(none)]> exit;
      #

Setting up Syslog Error Codes
-----------------------------

`pattoo` uses unique error code numbers for syslog messages to make troubleshooting easier. Run the `tests/bin/error_code_report.py` script before the unittests to make there are no duplicates. The unittests will fail if there are duplicates.

.. code-block::

    $ tests/bin/error_code_report.py

    Pattoo Logging Error Code Summary Report
    ----------------------------------------
    Starting Code              : 20001
    Ending Code                : 20141
    Duplicate Codes to Resolve : []
    Available Codes            : [20141, 20142, 20143, 20144, 20145]
    $

Everything is OK if there are no `Duplicate Codes to Resolve`.

Running Tests
-------------

The `tests/bin/do_all_tests.py` script will recursively run all unittests in the `tests/` directory.
