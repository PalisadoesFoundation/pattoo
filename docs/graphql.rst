Queries with GraphQL
====================

It's best to become familiar with GraphQL before trying these tests.

By default the ``pattoo`` server will run on port TCP 20202.

Non Interactive GraphQL
-----------------------

After completing this very brief tutorial you'll be able to do programmatic GraphQL queries.

If you are running it on your local machine go to the http://localhost:20202/pattoo/api/v1/web/graphql URL to get your results.

Interactive GraphQL
-------------------

If you are running it on your local machine go to the http://localhost:20202/pattoo/api/v1/web/igraphql to see the interactive query tool.

User Authentication via GraphQL
-------------------------------

It's necessarry to limit access to Pattoo resources through the use of limited
privilege controls. This is achieved through the use of `JSON Web Tokens(JWT)`.

Both an `access token` and `refresh token` is used to authenticate a given User.

To retrieve both an `access token` and `refresh token`:

.. code-block:: text

    mutation{
        authenticate(Input: {
            username: "pattoo",
            password: "associated pattoo user password"
        }){
            accessToken
            refreshToken
        }
    }

Sample Result
^^^^^^^^^^^^^

.. code-block:: text

    {
      "data": {
        "authenticate": {
          "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI",
          "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlhdCI6MTU5Nzg1OTI1NCwibmJmIjoxNTk3ODU5MjU0LCJqdGkiOiJjYWM3OWU0Yy1iNjAxLTQwNmQtYTFiNy1kYzgwOTdjNmYzMzUiLCJpZGVudGl0eSI6MywiZXhwIjoxNTk3OTQ1NjU0fQ.kjAWtIeK6n_Y8sDYbUzs4S9RRmTBdiQMNk4rFm8YN1w"
        }
      }
    }

All queries require a `token` input attribute when querying the GraphQL server.

.. code-block:: text

    {
        allUsers(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
            edges{
                nodes{
                    idxUser
                    username
                }
            }
        }
    }

View All DataPoints
-------------------

To see all DataPoints and their data enter this query on the left hand side of the viewer.

.. code-block:: text

    {
      allDatapoints {
        edges {
          node {
            id
    				idxDatapoint
            checksum
            dataType
            lastTimestamp
            pollingInterval
            enabled
          }
        }
      }
    }

Sample Result
^^^^^^^^^^^^^

Here is the result of all DataPoints. Take note of ``(id: "RGF0YVBvaW50OjE=")`` as we'll use it for querying timeseries data.

.. code-block:: json

    {
      "data": {
        "allDatapoints": {
          "edges": [
            {
              "node": {
                "id": "RGF0YVBvaW50OjE=",
                "idxDatapoint": "1",
                "checksum":  "ea5ee349b38fa7dc195b3689872c8487e7696201407ef27231b19be837fbc6da0847f5227f1813d893100802c70ffb18646e2097a848db0b7ea4ec15caced101",
                "dataType": 99,
                "lastTimestamp": 1575174588079,
                "pollingInterval": 10000,
                "enabled": "1"
              }
            },
            {
              "node": {
                "id": "RGF0YVBvaW50OjI=",
                "idxDatapoint": "2",
                "checksum":  "2b15d147330183c49a1672790bf09f54f8e849f9391c82385fd8758204e87940ab1ffef1bb67ac725de7cc0aa6aba9b6baeff34497ee494c38bee7f24eef65df",
                "dataType": 99,
                "lastTimestamp": 1575174588084,
                "pollingInterval": 10000,
                "enabled": "1"
              }
            }
          ]
        }
      }
    }

View All Key-Pair-Values
------------------------

To see all Key-Pair-Values enter this query on the left hand side of the viewer.

.. code-block:: text

    {
      allPairs {
        edges {
          node {
            id
            idxPair
            key
            value
          }
        }
      }
    }


Sample Result
^^^^^^^^^^^^^

Here is the result of all Key-Pair-Values.

.. code-block:: json

    {
      "data": {
        "allPairs": {
          "edges": [
            {
              "node": {
                "id": "UGFpcjox",
                "idxPair": "1",
                "key":  "pattoo_agent_hostname",
                "value":  "palisadoes"
              }
            },
            {
              "node": {
                "id": "UGFpcjoy",
                "idxPair": "2",
                "key":  "pattoo_agent_id",
                "value":  "23a224313e4aaa4678a81638025ab02b42cb8a5b7c47b3dd2efced06d1a13d39"
              }
            },
            {
              "node": {
                "id": "UGFpcjoz",
                "idxPair": "3",
                "key":  "pattoo_agent_polled_device",
                "value":  "device.example.com"
              }
            },
            {
              "node": {
                "id": "UGFpcjo0",
                "idxPair": "4",
                "key":  "pattoo_agent_program",
                "value":  "pattoo_agent_modbustcpd"
              }
            }
          ]
        }
      }
    }

View All GluePoints
-------------------

To see all GluePoints enter this query on the left hand side of the viewer. This table maps all the key-value pairs associated with an individual DataPoint

.. code-block:: text

    {
      allGlues {
        edges {
          node {
            id
            idxPair
            idxDatapoint
          }
        }
      }
    }

Sample Result
^^^^^^^^^^^^^

.. code-block:: json

    {
      "data": {
        "allGlues": {
          "edges": [
            {
              "node": {
                "id": "R2x1ZTooMSwgMSk=",
                "idxPair": "1",
                "idxDatapoint": "1"
              }
            },
            {
              "node": {
                "id": "R2x1ZTooMSwgMik=",
                "idxPair": "1",
                "idxDatapoint": "2"
              }
            },
            {
              "node": {
                "id": "R2x1ZTooMSwgMyk=",
                "idxPair": "1",
                "idxDatapoint": "3"
              }
            },
            {
              "node": {
                "id": "R2x1ZTooMSwgNCk=",
                "idxPair": "1",
                "idxDatapoint": "4"
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

    {
      datapoint(id: "RGF0YVBvaW50OjE=") {
        id
        idxDatapoint
        checksum
        dataType
        pollingInterval
        dataChecksum {
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
          "idxDatapoint": "1",
          "checksum":  "ea5ee349b38fa7dc195b3689872c8487e7696201407ef27231b19be837fbc6da0847f5227f1813d893100802c70ffb18646e2097a848db0b7ea4ec15caced101",
          "dataType": 99,
          "pollingInterval": 10000,
          "dataChecksum": {
            "edges": [
              {
                "node": {
                  "id": "RGF0YTooMSwgMTU3NTE3MjgzNTAyOCk=",
                  "timestamp": "1575172835028",
                  "value": "738.0000000000"
                }
              },
              {
                "node": {
                  "id": "RGF0YTooMSwgMTU3NTE3Mjg0NTIxOSk=",
                  "timestamp": "1575172845219",
                  "value": "738.0000000000"
                }
              },
              {
                "node": {
                  "id": "RGF0YTooMSwgMTU3NTE3Mjg1NTM2NCk=",
                  "timestamp": "1575172855364",
                  "value": "738.0000000000"
                }
              }
            ]
          }
        }
      }
    }
