.. Pattoo documentation master file, created by
   sphinx-quickstart on Tue Oct 22 22:23:00 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pattoo
======

``pattoo`` stores timeseries data in a database and makes it available for users via a GraphQL API.

Visit the `Pattoo GitHub site <https://github.com/PalisadoesFoundation/pattoo>`_ to see the code.

Introduction
------------

General information about the project, including the the prerequisite steps to get it operational on your system.

.. toctree::
   :maxdepth: 2
   :caption: Introduction:

   palisadoes
   introduction
   installation
   configuration

Daemon and Cron Setup
---------------------

How to get the daemons running to collect data.

.. toctree::
  :maxdepth: 2
  :caption: Daemon Setup:

  cron
  pattoo_apid
  pattoo_api_agentd

Testing GraphQL Queries
-----------------------

Developer testing tools.

.. toctree::
   :maxdepth: 2
   :caption: Developer Testing.

   graphql
   rest



Miscellaneous Information
-------------------------

Technical background information on the project.

.. toctree::
   :maxdepth: 2
   :caption: Miscellaneous Information:

   troubleshooting
   data
   glossary
