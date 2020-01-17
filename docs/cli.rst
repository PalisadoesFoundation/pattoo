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

Agents
------

As stated before, ``pattoo agents`` report data to the central ``pattoo`` server.

Viewing Agents
^^^^^^^^^^^^^^

To view the agents posting data to the ``pattoo`` server use the ``bin/pattoo_cli.py show agent`` command.

.. code-block:: text

  $ bin/pattoo_cli.py show agent

  idx_agent  agent_program                agent_target  enabled

  1          pattoo_agent_snmp_ifmibd     localhost     1
  2          pattoo_agent_snmpd           localhost     1
  3          pattoo_agent_os_autonomousd  nada          1
  4          pattoo_agent_os_spoked       nada          1

Viewing Agent Groups
^^^^^^^^^^^^^^^^^^^^

To view the groups to which the agents belong use the ``bin/pattoo_cli.py show agent_group`` command.

.. code-block:: text

    $ bin/pattoo_cli.py show agent_group

    idx_agent_group  description     idx_agent  agent_program                agent_target  enabled

    1                Pattoo Default                                                        1

    2                IfMIB Agents    2          pattoo_agent_snmpd           localhost     1
                                     3          pattoo_agent_snmp_ifmibd     localhost

    3                OS Agents       1          pattoo_agent_os_autonomousd  swim          1

Assigning Agents to Agent Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are some important things to know first.

1. Each agent has an ``idx_agent`` number that can be seen in the first column of the ``bin/pattoo_cli.py show agent`` command.
1. Each agent group has an ``idx_agent_group`` number that can be seen in the first column of the ``bin/pattoo_cli.py show agent_group`` command.

To assign an ``agent`` to an ``agent group`` use the ``bin/pattoo_cli.py assign agent`` command.

.. code-block:: text

    $ bin/pattoo_cli.py assign agent --idx_agent 2 --idx_agent_group 4

In this case we have assigned agent with an ``idx_agent`` agent number of ``2`` to the ``idx_agent_group`` group number ``4``

Key-Pair Translations
---------------------

Agents only post key-value pairs to the ``pattoo`` server. Translations are short descriptions of what each key means. The aim is for you to see these descriptions instead of the keys when you look at ``pattoo`` data with the ``pattoo-web`` UI.

When a translation for a key reported by an ``agent`` is installed, the translation is seen in ``pattoo-web`` instead of the key itself. This makes ``pattoo`` data more meaningful.

You don't have to install translations for every ``agent`` that reports data. You just have to assign ``agents`` to ``agent groups``, then you assign a single set of translations to the ``agent group``.

Viewing Agent Group Key-Pair Translation Assignments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can view these ``agent group`` to ``translation group`` assignments using the ``bin/pattoo_cli.py show key_pair_translation_group`` command.

.. code-block:: text

    $ bin/pattoo_cli.py show key_pair_translation_group

    idx_pair_xlate_group  translation_group_description  idx_agent_group  agent_group_description  enabled

    1                     Pattoo Default                 1                Pattoo Default           1

    2                     IfMIB Agents                   2                IfMIB Agents             1

    3                     OS Agents                      3                OS Agents                1


Viewing Agent Key-Pair Translation Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To view translation groups use the ``bin/pattoo_cli.py show key_pair_translation`` command.

.. code-block:: text

    $ bin/pattoo_cli.py show key_pair_translation

    idx_pair_xlate_group  description     language  key                                                     translation                                units                   enabled

    1                     Pattoo Default                                                                                                                                              1

    2                     IfMIB Agents    en        pattoo_agent_snmp_ifmibd_ifalias                        Interface Alias                                                    1
                                          en        pattoo_agent_snmp_ifmibd_ifdescr                        Interface Description
                                          en        pattoo_agent_snmp_ifmibd_ifhcinbroadcastpkts            Interface Broadcast Packets (HC inbound)   Packets / Second
                                          en        pattoo_agent_snmp_ifmibd_ifhcinmulticastpkts            Interface Multicast Packets (HC inbound)   Packets / Second
    ...
    ...
    ...

    3                     OS Agents       en        pattoo_agent_os_autonomousd_cpu_frequency               CPU Frequency                              Frequency               1
                                          en        pattoo_agent_os_autonomousd_cpu_stats_ctx_switches      CPU (Context Switches)                     Events / Second
                                          en        pattoo_agent_os_autonomousd_cpu_stats_interrupts        CPU (Context Switches)                     Events / Second
                                          en        pattoo_agent_os_autonomousd_cpu_stats_soft_interrupts   CPU (Soft Interrupts)                      Events / Second
                                          en        pattoo_agent_os_autonomousd_cpu_stats_syscalls          CPU (System Calls)                         Events / Second


Creating Agent Key-Pair Translation Group CSV Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating a CSV translation file is easy. Follow these steps.

1. Make sure the first row has the following headings separated by commas.

        .. code-block:: text

            language,key,description,units

1. Each subsequent row must have values that correspond to the headings. Each value must be separated by a comma.

    1. The ``language`` must correspond to the language configured in your ``pattoo.yaml`` configuration file. ``pattoo-web`` will only evaluate translation entries that match to the configured language.
    1. The ``key`` value must correspond to any expected keys from key-value pairs reported by an agent.
    1. The ``description`` must correspond to the brief text you want to use to describe the ``key``
    1. The ``units`` value is used to let users know the unit of measure to be used for the data being tracked by the ``key``

        .. code-block:: text

            language,key,description,units
            en,pattoo_agent_os_spoked_disk_io_write_bytes,Disk I/O (Bytes Written),Bytes / Second
            en,pattoo_agent_os_spoked_disk_io_write_count,Disk I/O (Write Count),Writes / Second
            en,pattoo_agent_os_spoked_disk_io_write_merged_count,Disk I/O (Write Merged Count),Writes / Second
            en,pattoo_agent_os_spoked_disk_io_write_time,Disk I/O (Write Time),
            en,pattoo_agent_os_spoked_disk_partition,Disk Partition,
            en,pattoo_agent_os_spoked_disk_partition_device,Disk Partition,

        Not all key-value pairs will need ``units``. For example, ``agent`` metadata won't have them. In this case don't put a value for ``units`` and end the line with a comma (``,``). The previous example shows three lines of translations including ``units`` followed by three without ``units``.

Importing Agent Key-Pair Translation Group Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are some important things to know first.

1. Each ``translation group`` has an ``idx_pair_xlate_group`` number that can be seen in the first column of the ``bin/pattoo_cli.py show key_pair_translation_group`` command.
1. The translations for the ``translation group`` must be in a CSV file formatted according to the guidelines mentioned previously.

To import a translation file's data and assign it to a ``translation group`` use the ``bin/pattoo_cli.py import key_pair_translation`` command.

.. code-block:: text

    $ bin/pattoo_cli.py import key_pair_translation --idx_pair_xlate_group 7 --filename agent_name_1_english.csv

In this case we have imported translations from a file named ``agent_name_1_english.csv`` and assigned it to a ``translation group``  with an ``idx_pair_xlate_group`` number of ``7``.

Agent Translations
------------------

Viewing Agent Translations
^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating Agent Translation CSV Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Importing Agent Translation Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
