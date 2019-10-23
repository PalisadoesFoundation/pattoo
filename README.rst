

.. image:: https://user-images.githubusercontent.com/16875803/66711530-9bdbab80-ed42-11e9-913f-7a21ede86d8f.png
   :target: https://user-images.githubusercontent.com/16875803/66711530-9bdbab80-ed42-11e9-913f-7a21ede86d8f.png
   :alt: pattoo


Introduction
============

``pattoo`` stores timeseries data in a database and makes it available for users via a GraphQL API.

Data can be collected from a number of sources. The ``pattoo-agents`` repository provides a number standard data collection agents for:


* Linux
* SNMP
* Modbus

Documentation
=============

There are a number of sets of documents that cover the ``pattoo`` portfolio.

Pattoo
------
The data collection server that acts as the central repository of data provided by the ``pattoo`` agents.

* The `Pattoo Server documentation <https://pattoo.readthedocs.io/>`_ can be found here.
* Visit the `Pattoo Server GitHub site <https://github.com/PalisadoesFoundation/pattoo>`_ to see the code.

Pattoo-Agents
-------------
``pattoo`` agents collect data from a variety of sources and send them to the central ``pattoo`` server over HTTP. We provide a few standard agents, but you can create your own. (See Pattoo-Shared for details)

* The `Pattoo Agents documentation <https://pattoo-agents.readthedocs.io/>`_ can be found here.
* Visit the `Pattoo Agents GitHub site <https://github.com/PalisadoesFoundation/pattoo-agents>`_ to see the code.

Pattoo-Shared
-------------
Both the ``pattoo`` agents and server use a shared python library which must be pre-installed using ``pip3`` for them to work. 

You can use the ``pattoo-shared`` documentation to learn the basics of creating your own custom ``pattoo-agents`` to feed data to the ``pattoo`` server

* The `Pattoo Shared documentation <https://pattoo-shared.readthedocs.io/>`_ can be found here.
* Visit the `Pattoo Shared GitHub site <https://github.com/PalisadoesFoundation/pattoo-shared>`_ to see the code.

About Pattoo
============

``pattoo`` is based on the original ``infoset`` code created by the `Palisadoes Foundation <http://www.palisadoes.org>`_ as part of its annual Calico Challenge program. Calico provides paid summer internships for  Jamaican university students to work on selected open source projects. They are mentored by software professionals and receive stipends based on the completion of predefined milestones. Calico was started in 2015.
