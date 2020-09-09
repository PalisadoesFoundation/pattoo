===========
GraphQL API
===========

You can use the `pattoo` API to retrieve data using a GraphQL interface. It's best to become familiar with GraphQL before reading further.

After completing this tutorial you'll be able to do programmatic GraphQL queries.

Queries with GraphQL
====================

By default the ``pattoo`` server will run on port TCP 20202.

Interactive GraphQL
-------------------
Interactive GraphQL allows you to test your queries using your web browser.

If you are running it on your local machine go to the http://localhost:20202/pattoo/api/v1/web/igraphql to see the interactive query tool.

Non Interactive GraphQL
-----------------------

If you want to access GraphQL programmatically, without using your browser then you'll need to access the non-interactive GraphQL URL.

If you are running it on your local machine go to the http://localhost:20202/pattoo/api/v1/web/graphql URL to get your results.

How The Database Maps to GraphQL Queries
========================================

**Note** This section is very detailed, but it will help you with understanding how the GraphQL keywords required for your queries were created.

There are two important files in the repository's `pattoo/db <https://github.com/palisadoes/pattoo/tree/master/pattoo/db>`_ directory.

#. *models.py*: Defines the database structure using the python SQLAlchemy package
#. *schema.py*: Maps the database structure from SQLAlchemy to GraphQL queries using the graphene-sqlalchemy package.

Models.py
---------

This file defines the tables and columns in the database.

#. Each class defines a table
#. Each variable in the class defines the columns. The variable name is the column name

The python `graphene-sqlalchemy` package used to present GraphQL will convert column names into camelCase, removing any underscores. Therefore a column named `idx_datapoint` will be `idxDatapoint` in your GraphQL queries.

You will notice some tables will have foreign keys as part of the RDBMS structure. Here is an example in the AgentXlate table:

.. code-block:: text

      class AgentXlate(BASE):
          """Class defining the pt_agent_xlate table of the database."""

          __tablename__ = 'pt_agent_xlate'
          __table_args__ = (
              UniqueConstraint('idx_language', 'agent_program'),
              {'mysql_engine': 'InnoDB'}
          )

          idx_agent_xlate = Column(
              BIGINT(unsigned=True), primary_key=True,
              autoincrement=True, nullable=False)

          idx_language = Column(
              BIGINT(unsigned=True),
              ForeignKey('pt_language.idx_language'),
              index=True, nullable=False, server_default='1')


You will also notice that this class also has a backref relationship near the bottom. This is what `graphene-sqlalchemy` uses to track the relationships for queries. In this case, the backref has the name `Agent_xlate_language` which will be converted to `agentXlateLanguage` camelCase in your GraphQL queries

.. code-block:: text

    language = relationship(
        Language,
        backref=backref(
            'Agent_xlate_language', uselist=True,cascade='delete,all'))

Schemas.py
----------

This file contains the mappings from SQLAlchemy table definitions to GraphQL queries.

#. Database tables defined as SQLAlchemy classes in models.py are imported as `Model` classes in this file.
#. You’ll notice that if you manually type in your GraphQL queries in the `/igraphql` URL that you’ll see lists of each available table column with explanations. These explanations are defined in the `Attribute` classes in this file.
#. Attributes and models are tied together in the `SQLAlchemyObjectType` classes.

.. code-block:: text

    from pattoo.db.models import AgentXlate as AgentXlateModel

    class InstrumentedQuery(SQLAlchemyConnectionField):
        """Class to allow GraphQL filtering by SQlAlchemycolumn name."""

        def __init__(self, type_, **kwargs):
            ...
            ...
            ...


    class AgentXlateAttribute():
        """Descriptive attributes of the AgentXlate table.
        A generic class to mutualize description of attributes for both queries
        and mutations.
        """

        idx_agent_xlate = graphene.String(
            description='AgentXlate table index.')

        idx_language = graphene.String(
            description='Language table index (ForeignKey).')

        agent_program = graphene.String(
            resolver=resolve_agent_program,
            description=('Agent progam'))

        translation = graphene.String(
            resolver=resolve_translation,
            description='Translation of the agent program name.')

        enabled = graphene.String(
            description='"True" if enabled.')


    class AgentXlate(SQLAlchemyObjectType, AgentXlateAttribute):
        """AgentXlate node."""

        class Meta:
            """Define the metadata."""

            model = AgentXlateModel
            interfaces = (graphene.relay.Node,)

Next we'll discuss the `Query` class  you'll find further down the file. This class:

#. Uses the `InstrumentedQuery` class to filter queries by database column values. This `InstrumentedQuery` class makes things a lot easier. The `graphene-sqlalchemy` implementation of GraphQL has limited filtering capabilities. For example:
    #. Every row of every database table has a fixed unique automatically generated GraphQL ID which is a `graphene.relay.node.GlobalID` object. You can filter specifically on this ID.
    #. You also get lists of database row results containing the first X and last X rows.
    #. Lists of database row results can also be obtained for values before and/or after X GraphQL ID values retrieved from a database table.
    #. Custom filtering for specific values in a database column can be using resolvers, but you have to manually create a resolver for each table’s column. This per query customization is not ideal.
#. Has `Node` entries for single value GraphQL queries, or as a definition inside an "edges" section of a GraphQL query. You can filter Nodes by the GraphQL `graphene.relay.node.GlobalID` too. This will be shown later.

.. code-block:: text

    class Query(graphene.ObjectType):
        """Define GraphQL queries."""

        pair = InstrumentedQuery(Pair)
        all_agent_xlate = InstrumentedQuery(AgentXlate)


Query Examples
==============

Here are some query examples using the example database table we have been using. Run these queries in the /igraphql url.

**Note:**

#. In all the examples in this section the “id” represents the `graphene.relay.node.GlobalID` string. You can use this to get information on a specific row of a specific table.
#. The `InstrumentedQuery` related queries in the Query class can only filter on a database table value, not the `graphene.relay.node.GlobalID` string.

Agent Table Queries
-------------------
This section covers Agent table queries.

All Known Agents
````````````````

This will provide information on all the known polling agents.

The agentProgram value will be used later for getting a translation into a meaningful name.

.. code-block:: text

    {
      allAgent(token:
      'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImp0aSI6IjcyMzFmZjk5LTE0NDktNDRhMS04YzE2LTY4OTMzNjgwZTU4YSIsImlhdCI6MTU5OTQyMjk5MywiZXhwIjoxNTk5NDI2NTkzfQ.UP1FSU3hNOI6EiEt2sMJ4V5n2BN3ttICsJFhJXJTowU'){
        edges {
          node {
            id
            idxAgent
            agentPolledTarget
            agentProgram
          }
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
        }
      }
    }

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
          idxUser
        }
    }

Sample Result
^^^^^^^^^^^^^

.. code-block:: text

    {
      "data": {
        "authenticate": {
          "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI",
          "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlhdCI6MTU5Nzg1OTI1NCwibmJmIjoxNTk3ODU5MjU0LCJqdGkiOiJjYWM3OWU0Yy1iNjAxLTQwNmQtYTFiNy1kYzgwOTdjNmYzMzUiLCJpZGVudGl0eSI6MywiZXhwIjoxNTk3OTQ1NjU0fQ.kjAWtIeK6n_Y8sDYbUzs4S9RRmTBdiQMNk4rFm8YN1w",
          "idxUser": "1"
        }
      }
    }

All queries require a `token` input attribute when querying the GraphQL server.

.. code-block:: text

    {
      user(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges{
          nodes{
            idxUser
            username
          }
        }
      }
    }


Refreshing Access Token
```````````````````````

Access tokens usually have a short time of life, for the purposes of security.
If an access token is comprised it cannot be utilize once expired. The `default`
expiration period for an access token being about `15 mintues`. The purpose
of `refresh tokens` are to provide a client with the ability to obtain a new
access token.

`Note:` **Refresh Tokens cannot be used access resources from the GraphQL server**

To generate a new `access token`, utilizeing a `refresh token`:

.. code-block:: text

    mutation{
      authRefresh(refreshToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlhdCI6MTU5OTY2OTg5NywibmJmIjoxNTk5NjY5ODk3LCJqdGkiOiI0MzRjMDBkZi1hNmQ1LTQwOGUtOWQ1OS00OWYwMDY4OWM4YTYiLCJpZGVudGl0eSI6IkRldi1Eb21pbmljIiwiZXhwIjoxNTk5NzU2Mjk3fQ.9VVKdoUkKwFn8T0aKb5Be7Fgo-nI9S2y4-znLTaCYWE"){
        accessToken
      }
    }

The newly generate access token should then be stored as the new `access token`,
and the expired `access token` discarded.


Sample Result
^^^^^^^^^^^^^

.. code-block:: text

    {
      "data": {
        "authRefresh": {
          "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk5NjcwMzM0LCJuYmYiOjE1OTk2NzAzMzQsImp0aSI6Ijk3ZjhiZWFlLWM2OGYtNDAwZi05MDI3LWIwM2JmNmNmMjE3ZiIsImlkZW50aXR5IjoiRGV2LURvbWluaWMiLCJleHAiOjE1OTk2NzEyMzR9.GuZrvfcsjUoNuuadvHcZLeg9ftrCmmLHGLNVJX7rjr4"
        }
      }
    }


View All DataPoints
````````````````````

To see all DataPoints and their data enter this query on the left hand side of the viewer.

.. code-block:: text

    {
      datapoint(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges {
          node {
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
.. code-block:: json

    {
      "data": {
        "datapoint": {
          "edges": [
            {
              "node": {
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

Pair Table Queries
------------------
Here we have some representative queries you can do:

View All Key-Pair-Values
````````````````````````

To see all Key-Pair-Values enter this query on the left hand side of the viewer.

.. code-block:: text

    {
      pair(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
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
        "pair": {
          "edges": [
            {
              "node": {
                "idxPair": "1",
                "key":  "pattoo_agent_hostname",
                "value":  "palisadoes"
              }
            },
            {
              "node": {
                "idxPair": "2",
                "key":  "pattoo_agent_id",
                "value":  "23a224313e4aaa4678a81638025ab02b42cb8a5b7c47b3dd2efced06d1a13d39"
              }
            },
            {
              "node": {
                "idxPair": "3",
                "key":  "pattoo_agent_polled_device",
                "value":  "device.example.com"
              }
            },
            {
              "node": {
                "idxPair": "4",
                "key":  "pattoo_agent_program",
                "value":  "pattoo_agent_modbustcpd"
              }
            }
          ]
        }
      }
    }

Glue Table Queries
------------------
Here we have some representative queries you can do:

View All GluePoints
```````````````````

To see all GluePoints enter this query on the left hand side of the viewer. This table maps all the key-value pairs associated with an individual DataPoint

.. code-block:: text

    {
      glue(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
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
                "idxPair": "1",
                "idxDatapoint": "1"
              }
            },
            {
              "node": {
                "idxPair": "1",
                "idxDatapoint": "2"
              }
            },
            {
              "node": {
                "idxPair": "1",
                "idxDatapoint": "3"
              }
            },
            {
              "node": {
                "idxPair": "1",
                "idxDatapoint": "4"
              }
            }
          ]
        }
      }
    }

Data Table Queries
------------------
Here we have some representative queries you can do:

View All Numeric Timeseries Data for DataPoint idxDatapoint "x"
```````````````````````````````````````````````````````````````

To see all numeric data for a specific datapoint ``1``.

.. code-block:: text

    {
      datapoint(idxDatapoint: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        idxDatapoint
        checksum
        dataType
        pollingInterval
        dataChecksum {
          edges {
            node {
              timestamp
              value
            }
          }
        }
      }
    }


Sample Result
^^^^^^^^^^^^^

Here is all the timeseries data from idxDatapoint ```3```.

.. code-block:: json

    {
      "data": {
        "datapoint": {
          "idxDatapoint": "1",
          "checksum":  "ea5ee349b38fa7dc195b3689872c8487e7696201407ef27231b19be837fbc6da0847f5227f1813d893100802c70ffb18646e2097a848db0b7ea4ec15caced101",
          "dataType": 99,
          "pollingInterval": 10000,
          "dataChecksum": {
            "edges": [
              {
                "node": {
                  "timestamp": "1575172835028",
                  "value": "738.0000000000"
                }
              },
              {
                "node": {
                  "timestamp": "1575172845219",
                  "value": "738.0000000000"
                }
              },
              {
                "node": {
                  "timestamp": "1575172855364",
                  "value": "738.0000000000"
                }
              }
            ]
          }
        }
      }
    }

Language Table Queries
----------------------

This query provides all the configured languages. The `code` returned is the language code. In the results, a code of `en` is english. Make translation queries based on this code value.

.. code-block:: text

    {
      language(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            idxLanguage
            code
            name
          }
        }
      }
    }


Agent Translation Table Queries
-------------------------------

This section outlines how to view Agent translation data.

All Agent Translation Table Entries
```````````````````````````````````
You can use this query to get the translation for an agentProgram name for a specific language.This is useful for the home page.

.. code-block:: text

    {
      agentXlate(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges {
          node {
            idxAgentXlate
            idxLanguage
            agentProgram
            translation
            enabled
            tsCreated
            tsModified
            language {
              name
              code
              idxLanguage
            }
          }
        }
      }
    }

Translation for a Specific agentProgram (all Languages)
```````````````````````````````````````````````````````
In this case we get translations for the `agentProgram` named `pattoo_agent_snmp_ifmibd`.

.. code-block:: text

    {
      agentXlate(agentProgram: "pattoo_agent_snmp_ifmibd", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            idxAgentXlate
            idxLanguage
            agentProgram
            translation
            enabled
            tsCreated
            tsModified
          }
        }
      }
    }


Filtered Agent Translation table entry with Language where idxAgentXlate = “4”
``````````````````````````````````````````````````````````````````````````````

There are some things to note:

#. This will provide a list of translations for all configured languages. The translation for the agentProgram is in the “translation” field.
#. Normally you’d be able to filter by “id” with GraphQL. Unfortunately this capability was lost when we added the customized ability to filter by any database table column. Hopefully the Python Graphene (GraphQL) team will be able to fix this later as part of their standard build.

.. code-block:: text

    {
      allAgentXlate(idxAgentXlate: "4", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            idxAgentXlate
            idxLanguage
            agentProgram
            translation
            enabled
            tsCreated
            tsModified
            language {
              name
            }
          }
        }
      }
    }

Key-Pair Translation Queries
----------------------------
This section outlines how to view key-pair translation data.

View all key-pair Translations
``````````````````````````````
Here's the query you'll need to view all translations:

.. code-block:: text

    {
      pairXlate(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges {
          node {
            idxLanguage
            idxPairXlate
            idxPairXlateGroup
            key
            translation
          }
        }
      }
    }

View key-pair Translations for idxPairXlateGroup = “x”
``````````````````````````````````````````````````````
In this example, we filter by `idxPairXlateGroup`

.. code-block:: text

    {
      pairXlate (idxPairXlateGroup: "2", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges {
          node {
            idxLanguage
            idxPairXlate
            idxPairXlateGroup
            key
            translation
          }
        }
      }
    }

Favorites Table Queries
-----------------------

This section outlines how to view favorites data.

View all Favorites and Their Assigned Charts
````````````````````````````````````````````
This is the query string you'll need to see all the favorites in the database.

.. code-block:: text

    {
      favorite (token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges {
          node {
            idxFavorite
            order
            user {
              idxUser
              username
              firstName
              lastName
            }
            chart {
              name
              chartDatapointChart {
                edges {
                  node {
                    idxDatapoint
                  }
                }
              }
            }
          }
        }
      }
    }


User Table Queries
------------------

This section outlines how to view favorites data.

View all Favorites for All Users
````````````````````````````````
This query will show:

#. All users
#. Their favorites
#. The charts associated with each favorite

.. code-block:: text

    {
      user (token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges {
          node {
            username
            firstName
            lastName
            enabled
            favoriteUser {
              edges {
                node {
                  order
                  chart {
                    idxChart
                    name
                  }
                }
              }
            }
          }
        }
      }
    }

View all Favorites for a Specific User (by filter other than ID)
````````````````````````````````````````````````````````````````
This query will show:

#. The filtered username (“pattoo”)
#. Its favorites
#. The charts associated with each favorite

.. code-block:: text

    {
      user(username: "pattoo", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            username
            favoriteUser {
              edges {
                node {
                  order
                  chart {
                    idxChart
                    name
                  }
                }
              }
            }
          }
        }
      }
    }


View all Favorites for a Specific User (by idxUser)
``````````````````````````````````````````````

This query will show:

#. The user
#. Its favorites
#. The charts associated with each favorite

.. code-block:: text

    {
      favorite(idxUser: "4", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk5NDM0Mzc4LCJuYmYiOjE1OTk0MzQzNzgsImp0aSI6ImFjZWVlMWRlLWQ0YTctNDkyYi04N2MxLWQ4NDhkZWU1YjU5MSIsImlkZW50aXR5IjoiRGV2LURvbWluaWMiLCJleHAiOjE1OTk0MzUyNzh9.MGKMSeF8a_XFt6m1vCS40CSuVMMANblqMcZSxSS_nnM") {
        edges {
          node {
            order
            chart {
              idxChart
              name
            }
          }
        }
      }
    }

Pagination
----------

This section outlines how to do simple pagination

View all Datapoints
```````````````````

This query will return all Datapoint values.

.. code-block:: text

    {
      datapoints (token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI"){
        edges {
          node {
            idxDatapoint
            idxAgent
            tsCreated
            tsModified
          }
        }
      }
    }

View First X Datapoints
```````````````````````

It’s important to note the `startCursor` and `endCursor` values when wanting to paginate.  They are useful in subsequent queries where you may want ranges of values that are not relative to the very start and very end of database table rows.

.. code-block:: text

    {
      datapoint(first: x, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            idxDatapoint
            idxAgent
            tsCreated
            tsModified
          }
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
        }
      }
    }

View Last X Datapoints
``````````````````````

It’s important to note the `startCursor` and `endCursor` values when wanting to paginate.  They are useful in subsequent queries where you may want ranges of values that are not relative to the very start and very end of database table rows.

.. code-block:: text

    {
      datapoint(last: x, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            idxDatapoint
            idxAgent
            tsCreated
            tsModified
          }
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
        }
      }
    }

Next X Datapoints
`````````````````

**Note:**

#. It’s important to note the `endCursor` of the previous query.
#. The next X results would need a query like the one below, starting at the `endCursor` value of the previous query.

.. code-block:: text

    {
      datapoint(first: X, after: "END_CURSOR_VALUE", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            idxDatapoint
            idxAgent
            tsCreated
            tsModified
          }
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
        }
      }
    }



Previous X Datapoints
`````````````````````

**Note:**

#. It’s important to note the startCursor of the previous query.
#. The previous X results would need a query like the one below, starting at the `startCursor` value of the previous query.

.. code-block:: text

    {
      datapoint(last: X, before: "START_CURSOR_VALUE", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        edges {
          node {
            idxDatapoint
            idxAgent
            tsCreated
            tsModified
          }
        }
        pageInfo {
          startCursor
          endCursor
          hasNextPage
          hasPreviousPage
        }
      }
    }


Mutation Examples
=================

`Mutation` is the terminology that GraphQL uses for database updates. Here are some query examples using the example database table we have been using. Run these queries in the `/igraphql` url.

Chart Table Mutation
--------------------
This section outlines how to mutate chart data.

Add a New Chart
```````````````
This mutation will add the chart then return the resulting fields:

#. `id`
#. `name`
#. Enabled status

Mutation
........

.. code-block:: text

    mutation {
      createChart(Input: {name: "Flying Fish"}, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        chart {
          name
          enabled
        }
      }
    }

Result
......

.. code-block:: text

    {
      "data": {
        "createChart": {
          "chart": {
            "name": "Flying Fish",
            "enabled": "1"
          }
        }
      }
    }


Modify Chart Name
`````````````````
This mutation will change the chart `name` from “Flying Fish” to “Teddy Bear”:

Mutation
.........

.. code-block:: text

    mutation {
      updateChart(Input: {idxChart: "239", name: "Teddy Bear"}, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        chart {
          name
          enabled
        }
      }
    }



Result
......

.. code-block:: text

    {
      "data": {
        "updateChart": {
          "chart": {
            "name": "Teddy Bear",
            "enabled": "1"
          }
        }
      }
    }


ChartDataPoint Table Mutation
-----------------------------
This section outlines how to mutate ChartDataPoint data.

Add a New ChartDataPoint
````````````````````````
This mutation will add a `DataPoint` to an existing chart then return the resulting fields:

Mutation
........

.. code-block:: text

    mutation {
      createChartDataPoint(Input: {idxDatapoint: "3", idxChart: "239"}, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        chartDatapoint {
          idxChartDatapoint
          idxDatapoint
          idxChart
        }
      }
    }



Result
......

.. code-block:: text

    {
      "data": {
        "createChartDataPoint": {
          "chartDatapoint": {
            "idxChartDatapoint": "242",
            "idxDatapoint": "3",
            "idxChart": "239"
          }
        }
      }
    }


Modify ChartDataPoint Name
``````````````````````````

This mutation will remove a DataPoint from the ChartDataPoint entry (Disable the entry for the chart):

Mutation
........

.. code-block:: text

    mutation {
      updateChartDataPoint(Input: {idxChartDatapoint: "242", enabled: "0"},
      token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        chartDatapoint {
          idxChartDatapoint
          idxDatapoint
          idxChart
          enabled
        }
      }
    }



Result
......

.. code-block:: text

    {
      "data": {
        "updateChartDataPoint": {
          "chartDatapoint": {
            "idxChartDatapoint": "242",
            "idxDatapoint": "3",
            "idxChart": "239",
            "enabled": "0"
          }
        }
      }
   }


User Table Mutation
-------------------

This section outlines how to mutate user data.

Add a New User
``````````````
This mutation will add a User then return the resulting fields:

Mutation
........

.. code-block:: text

    mutation {
      createUser(Input: {username: "foo@example.org", firstName: "Foo", lastName: "Fighter", password: "123456"}, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        user {
          idxUser
          firstName
          lastName
          username
          enabled
        }
      }
    }

Result
......

.. code-block:: text

    {
      "data": {
        "createUser": {
          "user": {
            "idxUser": "3",
            "firstName": "Foo",
            "lastName": "Fighter",
            "username": "foo@example.org",
            "enabled": "1"
          }
        }
      }
    }


Modify User FirstName
`````````````````````
This mutation will remove a DataPoint from the ChartDataPoint entry (Disable the entry for the chart):

Mutation
........

.. code-block:: text

    mutation {
      updateUser(Input: {idxUser: "3", firstName: "Street"}, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        user {
          idxUser
          firstName
          lastName
          username
          enabled
        }
      }
    }



Result
......

.. code-block:: text

    {
      "data": {
        "updateUser": {
          "user": {
            "idxUser": "3",
            "firstName": "Street",
            "lastName": "Fighter",
            "username": "foo@example.org",
            "enabled": "1"
          }
        }
      }
    }


Favorite Table Mutation
-----------------------
This section outlines how to mutate favorite data.

Add a New Favorite
``````````````````
This mutation will add a Favorite then return the resulting fields:

Mutation
........

.. code-block:: text

    mutation {
      createFavorite(Input: {idxUser: "3", idxChart: "149", order: "2"}, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        favorite{
          idxFavorite
          idxChart
          idxUser
          enabled
        }
      }
    }



Result
......

.. code-block:: text

    {
      "data": {
        "createFavorite": {
          "favorite": {
            "idxFavorite": "2",
            "idxChart": "149",
            "idxUser": "3",
            "enabled": "1"
          }
        }
      }
    }


Modify Favorite
```````````````

This mutation will remove the `Favorite` entry (Disable the entry):

Mutation
........

.. code-block:: text

    mutation {
      updateFavorite(Input: {idxFavorite: "2", enabled: "0"}, token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNTk3ODU5MjU0LCJuYmYiOjE1OTc4NTkyNTQsImp0aSI6IjM5MTQzNzg1LTgyOWItNDAzZi05NGU4LTAwOTAxYTFmZjFhMiIsImlkZW50aXR5IjozLCJleHAiOjE1OTc4NjAxNTR9.MrPBtBTYj4aeX0ICRIEGyawbIWZTuOc7bYivud8MaSI") {
        favorite {
          idxFavorite
          idxChart
          idxUser
          enabled
        }
      }
    }

Result
......

.. code-block:: text

    {
      "data": {
        "updateFavorite": {
          "favorite": {
            "idxFavorite": "2",
            "idxChart": "149",
            "idxUser": "3",
            "enabled": "0"
          }
        }
      }
    }
