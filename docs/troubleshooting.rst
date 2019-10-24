Troubleshooting Pattoo Agents
=============================

You will need to have a ``log_directory`` entry in your ``pattoo`` agent configuration file. This will create a number of log files depending on the type of error. Sometimes ``pattoo`` agents will fail with no logging message to the console. Always check your log files to determine the potential causes of the issue.

.. list-table::
   :header-rows: 1

   * - Log File
     - Description
   * - ``log/pattoo.log``
     - General log file. 
   * - ``log/pattoo-api.log``
     - Logs for agents that passively provide data to remote devices that poll them.
   * - ``log/pattoo-daemon.log``
     - Logs for agent daemons.
