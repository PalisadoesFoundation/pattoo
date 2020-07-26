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

Language
--------

``pattoo`` is meant to support multiple languages. The default language is English with a language code of ``en``. Agents do not post language specific data, but the keys used to define the data will need to be translated to descriptions that are meaningful to the end user.

Language translation files should be provided with any pattoo agent you install. You may have to create your own translation files for agents that poll data from non-standard data sources.

Viewing Languages
^^^^^^^^^^^^^^^^^

To view languages configured in the ``pattoo`` database use the ``bin/pattoo_cli.py show language`` command.

.. code-block:: text

  $ bin/pattoo_cli.py show language

  idx_language  code  name

  1             en    English

Upadating Language Names
^^^^^^^^^^^^^^^^^^^^^^^^

You can update the name of a language using the ``bin/pattoo_cli.py set language`` command. You must specify the language code and provide a name using the ``--name`` qualifier

.. code-block:: text

  $ bin/pattoo_cli.py set language --code 'en' --name 'English (Jamaican)'

In this example we have changed the name to 'English (Jamaican)'

Creating Languages
^^^^^^^^^^^^^^^^^^

To create a new language use the ``bin/pattoo_cli.py create language`` command.

.. code-block:: text

  $ bin/pattoo_cli.py create language --code 'es' --name 'Spanish'

In this case we create a new language with the name "Spanish" and identifying code "es"

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


Assigning Agents to Key-Pair Translations Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are some important things to know first.

1. Each agent has an ``idx_agent`` number that can be seen in the first column of the ``bin/pattoo_cli.py show agent`` command.
1. Each agent group has an ``idx_pair_xlate_group`` number that can be seen in the first column of the ``bin/pattoo_cli.py show key_translation`` command.

To assign an ``agent`` to an ``agent group`` use the ``bin/pattoo_cli.py assign agent`` command.

.. code-block:: text

    $ bin/pattoo_cli.py assign agent --idx_agent 2 --idx_pair_xlate_group 4

In this case we have assigned agent with an ``idx_agent`` agent number of ``2`` to the ``idx_pair_xlate_group`` group number ``4``

Key-Pair Translations
---------------------

Agents only post key-value pairs to the ``pattoo`` server. Translations are short descriptions of what each key means. The aim is for you to see these descriptions instead of the keys when you look at ``pattoo`` data with the ``pattoo-web`` UI.

When a translation for a key reported by an ``agent`` is installed, the translation is seen in ``pattoo-web`` instead of the key itself. This makes ``pattoo`` data more meaningful.

You don't have to install translations for every ``agent`` that reports data. You just have to assign ``agents`` to ``agent groups``, then you assign a single set of translations to the ``agent group``.

Viewing Agent Group Key-Pair Translation Assignments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can view these ``agent group`` to ``translation group`` assignments using the ``bin/pattoo_cli.py show key_translation_group`` command.

.. code-block:: text

    $ bin/pattoo_cli.py show key_translation_group

    idx_pair_xlate_group  translation_group_name         enabled

    1                     Pattoo Default                 1

    2                     IfMIB Agents                   1

    3                     OS Agents                      1

Creating Translation Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a new translation group use the ``bin/pattoo_cli.py create key_translation`` command.

.. code-block:: text

  $ bin/pattoo_cli.py create key_translation --name "Stock Market Symbol Translations"

In this case we create a new translation group with the name "Stock Market Symbol Translations"

Upadating Translation Group Names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can update the name of a translation group using the ``bin/pattoo_cli.py set key_translation_group`` command. You must specify the group's ``idx_pair_xlate_group`` value and a name.

.. code-block:: text

  $ bin/pattoo_cli.py set key_translation_group --idx_pair_xlate_group 20 --name 'New Translation Group Name'

In this example we have changed the name to 'New Translation Group Name' for ``idx_pair_xlate_group`` 20.

Viewing Agent Key-Pair Translation Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To view translation groups use the ``bin/pattoo_cli.py show key_translation`` command.

.. code-block:: text

    $ bin/pattoo_cli.py show key_translation

    idx_pair_xlate_group  name            language  key                                                     translation                                units                   enabled

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

Creating a CSV key-pair translation file is easy. Follow these steps.

1. Make sure the first row has the following headings separated by commas.

        .. code-block:: text

            language,key,translation,units

1. Each subsequent row must have values that correspond to the headings. Each value must be separated by a comma.

    1. The ``language`` must correspond to the language configured in your ``pattoo.yaml`` configuration file. ``pattoo-web`` will only evaluate translation entries that match to the configured language.
    1. The ``key`` value must correspond to any expected keys from key-value pairs reported by an agent.
    1. The ``translation`` must correspond to the brief text you want to use to describe the ``key``
    1. The ``units`` value is used to let users know the unit of measure to be used for the data being tracked by the ``key``

        .. code-block:: text

            language,key,translation,units
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

1. Each ``translation group`` has an ``idx_pair_xlate_group`` number that can be seen in the first column of the ``bin/pattoo_cli.py show key_translation_group`` command.
1. The translations for the ``translation group`` must be in a CSV file formatted according to the guidelines mentioned previously.

To import a translation file's data and assign it to a ``translation group`` use the ``bin/pattoo_cli.py import key_translation`` command.

.. code-block:: text

    $ bin/pattoo_cli.py import key_translation --idx_pair_xlate_group 7 --filename agent_name_1_english.csv

In this case we have imported translations from a file named ``agent_name_1_english.csv`` and assigned it to a ``translation group``  with an ``idx_pair_xlate_group`` number of ``7``.

You only need to import translations for the key-pairs you require. Any previously existing translation for an key-pair configured in the file will be updated. key-pairs not in the file will not be updated.

Agent Translations
------------------

Not only do an agent's key-pairs need translations, but the agents themselves need translations too. This is because an ``agent`` only reports its name when posting which, through translations, allows ``pattoo`` to be more flexible in supporting many different spoken languages.

Without translations, all references to a ``pattoo`` agent will just be by its name, which could be confusing.

Viewing Agent Translations
^^^^^^^^^^^^^^^^^^^^^^^^^^

To view agent translations use the ``bin/pattoo_cli.py show agent_translation`` command.

.. code-block:: text

  $ bin/pattoo_cli.py show agent_translation

  language  agent_program                translation                          enabled

  en        pattoo_agent_os_autonomousd  Pattoo Standard OS Autonomous Agent  1
            pattoo_agent_os_spoked       Pattoo Standard OS Spoked Agent
            pattoo_agent_snmpd           Pattoo Standard SNMP Agent
            pattoo_agent_snmp_ifmibd     Pattoo Standard IfMIB SNMP Agent
            pattoo_agent_modbustcpd      Pattoo Standard Modbus TCP Agent
            pattoo_agent_bacnetipd       Pattoo Standard BACnet IP Agent

Creating Agent Translation CSV Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating a CSV agent translation file is easy. Follow these steps.

1. Make sure the first row has the following headings separated by commas.

        .. code-block:: text

            language,key,translation

1. Each subsequent row must have values that correspond to the headings. Each value must be separated by a comma.

    1. The ``language`` must correspond to the language configured in your ``pattoo.yaml`` configuration file. ``pattoo-web`` will only evaluate translation entries that match to the configured language.
    1. The ``key`` value must correspond to the name of an agent.
    1. The ``translation`` must correspond to the brief text you want to use to describe the ``key``

.. code-block:: text

  language,key,translation
  en,pattoo_agent_os_autonomousd,Pattoo Standard OS Autonomous Agent
  en,pattoo_agent_os_spoked,Pattoo Standard OS Spoked Agent
  en,pattoo_agent_snmpd,Pattoo Standard SNMP Agent
  en,pattoo_agent_snmp_ifmibd,Pattoo Standard IfMIB SNMP Agent
  en,pattoo_agent_modbustcpd,Pattoo Standard Modbus TCP Agent
  en,pattoo_agent_bacnetipd,Pattoo Standard BACnet IP Agent

Importing Agent Translation Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To import an agent translation file's data use the ``bin/pattoo_cli.py import agent_translation`` command.

.. code-block:: text

    $ bin/pattoo_cli.py import agent_translation --filename agent_name_translation_english.csv

In this case we have imported translations from a file named ``agent_name_translation_english.csv``.

You only need to import translations for the ``agents`` you require. Any previously existing translation for an ``agent`` configured in the file will be updated. ``agents`` not in the file will not be updated.
