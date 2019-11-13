Queries with REST
=================

It's best to become familiar with REST before trying these tests.

Here are some things to remember.

#. By default the ``pattoo`` server will run on port TCP 7000.
#. If you are running it on your local machine the RESTful API URLs will all start with http://localhost:7000/pattoo/api/v1/rest. All the examples assume make reference to this fact. So if the uri ``/agent`` is mentioned then assume we are referring to the complete URL of http://localhost:7000/pattoo/api/v1/rest/agent

Let's begin.

Why a RESTful Interface?
------------------------

We provide a RESTful interface for ease of comparison with GraphQL for a limited set of functions. There will be no further development of the RESTful beyond what is listed here. Do not write any ``pattoo`` related code based on REST. This feature is deprecated and will soon be removed.

Using the RESTful Interface (Deprecated)
----------------------------------------

View All Agents
^^^^^^^^^^^^^^^

To see all Agents visit the ``/agent`` URI. The results will look like this:

.. code-block:: json

    [
       {
          "agent_program" : "pattoo-agent-os-autonomousd",
          "idx_agent" : 1,
          "agent_hostname" : "swim",
          "enabled" : 1,
          "polling_interval" : 300,
          "agent_id" : "adf1777380b07160c396dbc4bdcaa01be1201f2f8629fbc7c5c3219f78ac89c7"
       },
       {
          "idx_agent" : 2,
          "agent_program" : "pattoo-agent-snmpd",
          "agent_hostname" : "swim",
          "agent_id" : "0c9136e63849414c63310bc2da78fcbf7fd331c15c0e6f3133ff75ec653a18da",
          "enabled" : 1,
          "polling_interval" : 300
       },
       {
          "idx_agent" : 3,
          "agent_program" : "pattoo-agent-os-spoked",
          "agent_hostname" : "swim",
          "enabled" : 1,
          "polling_interval" : 300,
          "agent_id" : "24f1e1c41bda5d4474e28026e6a8142bded517c5bcfb88e62976e4963cbabf5d"
       }
    ]

View a Single Agent
^^^^^^^^^^^^^^^^^^^

Add the ``idx_agent`` value to see a specific agent. In this case we view ``idx_agent`` value 2 via URI ``/agent/2``.

.. code-block:: json

  [
    {
       "idx_agent" : 2,
       "agent_id" : "0c9136e63849414c63310bc2da78fcbf7fd331c15c0e6f3133ff75ec653a18da",
       "polling_interval" : 300,
       "enabled" : 1,
       "agent_program" : "pattoo-agent-snmpd",
       "agent_hostname" : "swim"
    }
  ]

View All DataSources
^^^^^^^^^^^^^^^^^^^^

To see all DataSources visit the ``/datasource`` URI. The results will look like this:

.. code-block:: json

    [
      {
          "idx_agent" : 1,
          "idx_datasource" : 1,
          "device" : "swim",
          "enabled" : 1,
          "gateway" : "swim"
      },
      {
          "gateway" : "swim",
          "enabled" : 1,
          "device" : "localhost",
          "idx_datasource" : 2,
          "idx_agent" : 2
      },
      {
          "gateway" : "swim",
          "idx_agent" : 3,
          "idx_datasource" : 3,
          "enabled" : 1,
          "device" : "swim"
      }
    ]


View a Single DataSource
^^^^^^^^^^^^^^^^^^^^^^^^

Add the ``idx_datasource`` value to see a specific agent. In this case we view ``idx_datasource`` value 3 via URI ``/datasource/3``.

.. code-block:: json

  [
    {
    "enabled" : 1,
    "idx_datasource" : 3,
    "device" : "swim",
    "idx_agent" : 3,
    "gateway" : "swim"
    }
  ]

View All DataPoints
^^^^^^^^^^^^^^^^^^^^

To see all DataPoints visit the ``/datapoint`` URI. The results will look like this:

.. code-block:: json

    [
      {
          "idx_datapoint" : 353,
          "data_type" : 0,
          "data_label" : "disk_usage_used",
          "enabled" : 1,
          "last_timestamp" : 1573525500,
          "checksum" : "9a413f2dec91a79b24718e0ee4004da0e12e53a0468998108127a2e1bdabeb1f",
          "data_index" : "/media/peter/9C1E-1403",
          "idx_datasource" : 1
      },
      {
          "idx_datapoint" : 355,
          "data_type" : 32,
          "data_label" : ".1.3.6.1.2.1.2.2.1.10",
          "enabled" : 1,
          "data_index" : "9",
          "checksum" : "102f9658500b7a04a41a170286693d6c823f73407bd2c63fd79e6e9e59a98465",
          "last_timestamp" : 1573525500,
          "idx_datasource" : 2
      },
      {
          "data_label" : ".1.3.6.1.2.1.2.2.1.16",
          "data_type" : 32,
          "idx_datapoint" : 356,
          "idx_datasource" : 2,
          "last_timestamp" : 1573525500,
          "checksum" : "a9ba70d230429284de9051ea7a8c1af83aad6f88b81fd9a96429125def7f2349",
          "data_index" : "9",
          "enabled" : 1
      }
    ]


View a Single DataPoint
^^^^^^^^^^^^^^^^^^^^^^^

Add the ``idx_datapoint`` value to see a specific agent. In this case we view ``idx_datapoint`` value 355 via URI ``/datapoint/355``.

.. code-block:: json

    [
      {
          "idx_datapoint" : 355,
          "data_type" : 32,
          "data_label" : ".1.3.6.1.2.1.2.2.1.10",
          "enabled" : 1,
          "data_index" : "9",
          "checksum" : "102f9658500b7a04a41a170286693d6c823f73407bd2c63fd79e6e9e59a98465",
          "last_timestamp" : 1573525500,
          "idx_datasource" : 2
      }
    ]

View DataPoint data
^^^^^^^^^^^^^^^^^^^^

To view data for generated by a specific DataPoint visit the ``/data`` URI. Add the ``idx_datapoint`` value to the end to get ``/data/1`` for  ``idx_datapoint`` value of 1.

#. By default a week's worth of data is returned.
#. There is no ability to get data for all DataPoints simultaneously.
#. You can use the ``?secondsago=X`` query string to get data starting ``X`` seconds ago to the most recently stored data.

In this case we have data from ``/data/1?secondsago=3600``

.. code-block:: json

    [
        {
            "1573619400" : 3878839847
        },
        {
            "1573619700" : 3879239629
        },
        {
            "1573620000" : 3879652192
        },
        {
            "1573620300" : 3880050372
        },
        {
            "1573620600" : 3880449410
        },
        {
            "1573620900" : 3880856015
        },
        {
            "1573621200" : 3881272430
        },
        {
            "1573621500" : 3881704477
        },
        {
            "1573621800" : 3882250116
        },
        {
            "1573622100" : 3882650025
        },
        {
            "1573622400" : 3883064936
        }
    ]
