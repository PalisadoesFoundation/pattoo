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

Retrieving GraphQL data with Pattoo-Web
```````````````````````````````````````

You can use the `get` function in this file to get GraphQL data from the pattoo API server. https://github.com/PalisadoesFoundation/pattoo-web/blob/master/pattoo_web/phttp.py

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

        node = relay.Node.Field()

        # Results as a single entry filtered by 'id' and as a list
        agent_xlate = graphene.relay.Node.Field(AgentXlate)
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
      allAgent {
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

All Datapoints Polled by Agent where id = "X"
`````````````````````````````````````````````
You’ll notice that this query also gives you the following information that will be required for translations later on:
#. key-value pair `key` value for translating Datapoint metadata
#. `agentProgram` for translating the program name into something meaningful
#. `idxPairXlateGroup` for translating the key values

.. code-block:: text

    {
      agent(id: "QWdlbnQ6Mg==") {
        datapointAgent {
          edges {
            cursor
            node {
              id
              idxDatapoint
              idxAgent
              agent {
                agentProgram
                agentPolledTarget
                idxPairXlateGroup
                pairXlateGroup {
                  id
                }
              }
              glueDatapoint {
                edges {
                  node {
                    pair {
                      key
                      value
                    }
                  }
                }
              }
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
    }


All Charts in which Datapoints Polled by Agent appear. Where id = “X”
``````````````````````````````````````````````````````````````````````
This query will show:

#. All Datapoints for an Agent
#. The charts to which each datapoint belongs
#. The favorites to which the charts belong

.. code-block:: text

    {
      agent(id: "QWdlbnQ6MQ==") {
        datapointAgent {
          edges {
            cursor
            node {
              id
              idxDatapoint
              idxAgent
              chartDatapointDatapoint {
                edges {
                  node {
                    idxChartDatapoint
                    chart {
                      id
                      idxChart
                      name
                      checksum
                      favoriteChart {
                        edges {
                          node {
                            idxFavorite
                          }
                        }
                      }
                    }
                  }
                }
              }
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
    }



DataPoint Table Queries
------------------------

Here we have some representative queries you can do:

View All DataPoints
````````````````````

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
.............

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

Pair Table Queries
------------------
Here we have some representative queries you can do:

View All Key-Pair-Values
````````````````````````

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
.............

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

Glue Table Queries
------------------
Here we have some representative queries you can do:

View All GluePoints
```````````````````

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
.............

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

Data Table Queries
------------------
Here we have some representative queries you can do:

View All Numeric Timeseries Data for DataPoint id "x"
`````````````````````````````````````````````````````

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
.............

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

Language Table Queries
----------------------

This query provides all the configured languages. The `code` returned is the language code. In the results, a code of `en` is english. Make translation queries based on this code value.

.. code-block:: text

    {
      allLanguage {
        edges {
          node {
            id
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
      allAgentXlate {
        edges {
          node {
            id
            idxAgentXlate
            idxLanguage
            agentProgram
            translation
            enabled
            tsCreated
            tsModified
            language {
              id
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
      allAgentXlate(agentProgram: "pattoo_agent_snmp_ifmibd") {
        edges {
          node {
            id
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

Single Node from Agent Translation table filtered by an ID
``````````````````````````````````````````````````````````
In this case:

#. The ID is a `graphene.relay.node.GlobalID` string.
#. The translation for the `agentProgram` is in the “translation” field.

.. code-block:: text

    {
      agentXlate(id: "QWdlbnRYbGF0ZToy") {
        id
        idxAgentXlate
        idxLanguage
        agentProgram
        translation
        enabled
        tsCreated
        tsModified
      }
    }


Filtered Agent Translation table entry with Language where idxAgentXlate = “4”
``````````````````````````````````````````````````````````````````````````````

There are some things to note:

#. This will provide a list of translations for all configured languages. The translation for the agentProgram is in the “translation” field.
#. Normally you’d be able to filter by “id” with GraphQL. Unfortunately this capability was lost when we added the customized ability to filter by any database table column. Hopefully the Python Graphene (GraphQL) team will be able to fix this later as part of their standard build.

.. code-block:: text

    {
      allAgentXlate(idxAgentXlate: "4") {
        edges {
          node {
            id
            idxAgentXlate
            idxLanguage
            agentProgram
            translation
            enabled
            tsCreated
            tsModified
            language {
              id
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
      allPairXlate {
        edges {
          node {
            id
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
      allPairXlate (idxPairXlateGroup: "2"){
        edges {
          node {
            id
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
      allFavorite {
        edges {
          node {
            id
            idxFavorite
            order
            user {
              id
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
      allUser {
        edges {
          node {
            id
            username
            firstName
            lastName
            enabled
            favoriteUser {
              edges {
                node {
                  order
                  chart {
                    id
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
      allUser(username: "pattoo") {
        edges {
          node {
            id
            username
            favoriteUser {
              edges {
                node {
                  order
                  chart {
                    id
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


View all Favorites for a Specific User (by ID)
``````````````````````````````````````````````

This query will show:

#. The user
#. Its favorites
#. The charts associated with each favorite

.. code-block:: text

    {
      user(id: "VXNlcjox") {
        id
        username
        favoriteUser {
          edges {
            node {
              order
              chart {
                id
                idxChart
                name
              }
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
      allDatapoints {
        edges {
          node {
            idxDatapoint
            idxAgent
            id
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
      allDatapoints(first: x) {
        edges {
          node {
            idxDatapoint
            idxAgent
            id
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
      allDatapoints(last: x) {
        edges {
          node {
            idxDatapoint
            idxAgent
            id
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
      allDatapoints(first: X, after: "END_CURSOR_VALUE") {
        edges {
          node {
            idxDatapoint
            idxAgent
            id
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
      allDatapoints(last: X, before: "START_CURSOR_VALUE") {
        edges {
          node {
            idxDatapoint
            idxAgent
            id
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
      createChart(Input: {name: "Flying Fish"}) {
        chart {
          id
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
            "id": "Q2hhcnQ6MjM5",
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
      updateChart(Input: {idxChart: "239", name: "Teddy Bear"}) {
        chart {
          id
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
            "id": "Q2hhcnQ6MjM5",
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
      createChartDataPoint(Input: {idxDatapoint: "3", idxChart: "239"}) {
        chartDatapoint {
          id
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
            "id": "Q2hhcnREYXRhUG9pbnQ6MjQy",
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
      updateChartDataPoint(Input: {idxChartDatapoint: "242", enabled: "0"}) {
        chartDatapoint {
          id
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
            "id": "Q2hhcnREYXRhUG9pbnQ6MjQy",
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
      createUser(Input: {username: "foo@example.org", firstName: "Foo", lastName: "Fighter", password: "123456"}) {
        user {
          Id
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
            "id": "VXNlcjoz",
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
      updateUser(Input: {idxUser: "3", firstName: "Street"}) {
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
      createFavorite(Input: {idxUser: "3", idxChart: "149", order: "2"}) {
        favorite{
          id
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
            "id": "RmF2b3JpdGU6Mg==",
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
      updateFavorite(Input: {idxFavorite: "2", enabled: "0"}) {
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
