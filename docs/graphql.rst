Queries with GraphQL
====================

It's best to become familiar with GraphQL before trying these tests.

By default the ``pattoo`` server will run on port TCP 7000.

Non Interactive GraphQL
-----------------------

After completing this very brief tutorial you'll be able to do programmatic GraphQL queries.

If you are running it on your local machine go to the http://localhost:7000/pattoo/api/v1/graphql URL to get your results.

Interactive GraphQL
-------------------

If you are running it on your local machine go to the http://localhost:7000/pattoo/api/v1/igraphql to see the interactive query tool.

View All Agents
---------------

To see all Agents and their data enter this query on the left hand side of the viewer.

.. code-block:: text

    {
        allAgents {
          edges {
            node {
              id
              agentHostname
              agentProgram
              agentId
              idxAgent
            }
          }
        }
      }

Sample Result
^^^^^^^^^^^^^

Here is the result of all Agents.

.. code-block:: json

  {
    "data": {
      "allAgents": {
        "edges": [
          {
            "node": {
              "id": "QWdlbnQ6MQ==",
              "agentHostname": "b'swim'",
              "agentProgram": "b'pattoo-agent-os-autonomousd'",
              "agentId": "b'adf1777380b07160c396dbc4bdcaa01be1201f2f8629fbc7c5c3219f78ac89c7'",
              "idxAgent": "1"
            }
          },
          {
            "node": {
              "id": "QWdlbnQ6Mg==",
              "agentHostname": "b'swim'",
              "agentProgram": "b'pattoo-agent-snmpd'",
              "agentId": "b'0c9136e63849414c63310bc2da78fcbf7fd331c15c0e6f3133ff75ec653a18da'",
              "idxAgent": "2"
            }
          },
          {
            "node": {
              "id": "QWdlbnQ6Mw==",
              "agentHostname": "b'swim'",
              "agentProgram": "b'pattoo-agent-os-spoked'",
              "agentId": "b'24f1e1c41bda5d4474e28026e6a8142bded517c5bcfb88e62976e4963cbabf5d'",
              "idxAgent": "3"
            }
          }
        ]
      }
    }
  }

View All DataSources
--------------------

To see all DataSources enter this query on the left hand side of the viewer.

.. code-block:: text

      {
        allDatasources {
          edges {
            node {
              id
              idxAgent
              gateway
              device
              enabled
            }
          }
        }
      }


Sample Result
^^^^^^^^^^^^^

Here is the result of all DataSources.

.. code-block:: json

  {
    "data": {
      "allDatasources": {
        "edges": [
          {
            "node": {
              "id": "RGF0YVNvdXJjZTox",
              "idxAgent": "1",
              "gateway": "b'swim'",
              "device": "b'swim'",
              "enabled": "1"
            }
          },
          {
            "node": {
              "id": "RGF0YVNvdXJjZToy",
              "idxAgent": "2",
              "gateway": "b'swim'",
              "device": "b'localhost'",
              "enabled": "1"
            }
          },
          {
            "node": {
              "id": "RGF0YVNvdXJjZToz",
              "idxAgent": "3",
              "gateway": "b'swim'",
              "device": "b'swim'",
              "enabled": "1"
            }
          }
        ]
      }
    }
  }

View All DataPoints
-------------------

To see all DataPoints enter this query on the left hand side of the viewer.

.. code-block:: text

      {
        allDatapoints {
          edges {
            node {
              id
              idxDatapoint
              dataType
              dataLabel
              dataIndex
              idxDatapoint
              idxDatasource
            }
          }
        }
      }

Sample Result
^^^^^^^^^^^^^

Take note of ``(id: "RGF0YVBvaW50OjE=")`` as we'll use it for querying timeseries data.

.. code-block:: json

  {
    "data": {
      "allDatapoints": {
        "edges": [
          {
            "node": {
              "id": "RGF0YVBvaW50OjE=",
              "idxDatapoint": 1,
              "dataType": "32",
              "dataLabel": "b'.1.3.6.1.2.1.2.2.1.10'",
              "dataIndex": "b'1'",
              "idxDatasource": "2"
            }
          },
          {
            "node": {
              "id": "RGF0YVBvaW50OjI=",
              "idxDatapoint": 2,
              "dataType": "64",
              "dataLabel": "b'cpu_stats'",
              "dataIndex": "b'ctx_switches'",
              "idxDatasource": "1"
            }
          },
          {
            "node": {
              "id": "RGF0YVBvaW50OjM=",
              "idxDatapoint": 3,
              "dataType": "64",
              "dataLabel": "b'cpu_stats'",
              "dataIndex": "b'ctx_switches'",
              "idxDatasource": "3"
            }
          }
       ]
      }
    }
  }

View All Numeric Timeseries Data
--------------------------------

To see all numeric data for a specific datapoint ``(id: "RGF0YVBvaW50OjE=")``, enter this query on the left hand side of the viewer.

.. code-block:: text

      query {
        datapoint (id: "RGF0YVBvaW50OjE=")
        {
          id
          idxDatapoint
          dataType
          dataLabel
          dataIndex
          idxDatapoint
          idxDatasource
          numericDatapoints {
            edges {
              node {
                id
                timestamp
                value
              }
            }
          }
        }
      }


Sample Result
^^^^^^^^^^^^^

Here is all the timeseries data from ``(id: "RGF0YVBvaW50OjE=")``.

.. code-block:: json

  {
    "data": {
      "datapoint": {
        "id": "RGF0YVBvaW50OjE=",
        "idxDatapoint": 1,
        "dataType": "32",
        "dataLabel": "b'.1.3.6.1.2.1.2.2.1.10'",
        "dataIndex": "b'1'",
        "idxDatasource": "2",
        "numericDatapoints": {
          "edges": [
            {
              "node": {
                "id": "RGF0YTooMSwgMTU3MzUwNzgwMCk=",
                "timestamp": "1573507800",
                "value": "3723676230.0000000000"
              }
            },
            {
              "node": {
                "id": "RGF0YTooMSwgMTU3MzUwODEwMCk=",
                "timestamp": "1573508100",
                "value": "3724074803.0000000000"
              }
            },
            {
              "node": {
                "id": "RGF0YTooMSwgMTU3MzUwODQwMCk=",
                "timestamp": "1573508400",
                "value": "3724475744.0000000000"
              }
            },
            {
              "node": {
                "id": "RGF0YTooMSwgMTU3MzUwODcwMCk=",
                "timestamp": "1573508700",
                "value": "3724909864.0000000000"
              }
            },
            {
              "node": {
                "id": "RGF0YTooMSwgMTU3MzUwOTAwMCk=",
                "timestamp": "1573509000",
                "value": "3725315676.0000000000"
              }
            },
            {
              "node": {
                "id": "RGF0YTooMSwgMTU3MzUwOTMwMCk=",
                "timestamp": "1573509300",
                "value": "3725713877.0000000000"
              }
            }
         ]
        }
      }
    }
  }
