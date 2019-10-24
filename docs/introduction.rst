Introduction
============

``pattoo`` stores timeseries data in a database and makes it available for users via a GraphQL API.

Data can be collected from a number of sources. The ``pattoo-agents`` repository provides a number standard data collection agents for:

* Linux
* SNMP
* Modbus

Data posted to the ``pattoo`` server's API automatically updates a specially designed database. Web applications can be created to access the database’s separate API for users to easily visualize and correlate the results.

Pattoo Server Objective
=======================

The ``pattoo`` server was created due to a real need where data from various DevOps, network, industrial PLC controllers, electro-mechanical and enterprise systems needed to be aggregated to help visualize how they affected each other.

It was designed to be modular so that custom data collection agents and web interfaces could be easily created by software developers.

Related Documentation
=====================

There are a number of sets of documents that cover the ``pattoo`` portfolio.

Pattoo
------
This is data collection server that acts as the central repository of data provided by the ``pattoo`` agents.

* The `Pattoo Server documentation <https://pattoo.readthedocs.io/>`_ can be found here.
* Visit the `Pattoo Server GitHub site <https://github.com/PalisadoesFoundation/pattoo>`_ to see the code.

Pattoo-Agents
-------------
The ``pattoo`` agents collect data from a variety of sources and send them to the central ``pattoo`` server over HTTP. We provide a few standard agents, but you can create your own. (See Pattoo-Shared for details)

* The `Pattoo Agents documentation <https://pattoo-agents.readthedocs.io/>`_ can be found here.
* Visit the `Pattoo Agents GitHub site <https://github.com/PalisadoesFoundation/pattoo-agents>`_ to see the code.

Pattoo-Shared
-------------
Both the ``pattoo`` agents and server use a shared python library which must be pre-installed using ``pip3`` for them to work.

You can use the ``pattoo-shared`` documentation to learn the basics of creating your own custom ``pattoo-agents`` to feed data to the ``pattoo`` server

* The `Pattoo Shared documentation <https://pattoo-shared.readthedocs.io/>`_ can be found here.
* Visit the `Pattoo Shared GitHub site <https://github.com/PalisadoesFoundation/pattoo-shared>`_ to see the code.
