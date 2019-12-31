Using the CLI
=============

The command line interface allows you to interact with the database in a number of ways.

Location of the CLI Script
--------------------------

The CLI script is located in the ``bin/`` directory and is called ``bin/pattoo_cli.py``.

Running the CLI script without any parameters will display the usage options as seen below.

.. code-block:: text

  $ bin/pattoo_cli.py
  usage: pattoo_cli.py [-h] {show,create,set,import,assign} ...

  This program is the CLI interface to configuring pattoo

  positional arguments:
    {show,create,set,import,assign}
      show                Show contents of pattoo DB.
      create              Create entries in pattoo DB.
      set                 Show contents of pattoo DB.
      import              Import data into the pattoo DB.
      assign              Assign contents of pattoo DB.

  optional arguments:
    -h, --help            show this help message and exit

Viewing Agents
--------------

To view the agents posting data to the ``pattoo`` server use the

.. code-block:: text

  $ bin/pattoo_cli.py show agent
  idx_agent  agent_program                agent_target  enabled

  1          pattoo_agent_snmp_ifmibd     localhost     1
  2          pattoo_agent_snmpd           localhost     1
  3          pattoo_agent_os_autonomousd  nada          1
  4          pattoo_agent_os_spoked       nada          1
