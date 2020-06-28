
Basic Installation
==================

This section covers some key steps to get you started.

Prerequisites
-------------

There are some software components that need to be installed prior to starting.

#. ``pattoo`` requires the installation of a MySQL or MariaDB database. Make sure this software is installed beforehand.
#. ``pattoo`` only runs on Python 3.6 or higher

Let's install the software.

Installation
------------

Follow these steps.

#. Install ``git`` on your system.
#. Select and create the parent directory in which you want to install ``pattoo``.

    .. code-block:: bash

       $ mkdir -p /installation/parent/directory
       $ cd /installation/parent/directory

#. Clone the repository to the parent directory using the ``git clone`` command. You can also choose to downloading and unzip the file in the parent directory. The repository can be found at: https://github.com/PalisadoesFoundation/pattoo

    .. code-block:: bash

       $ cd /installation/parent/directory
       $ git clone https://github.com/PalisadoesFoundation/pattoo.git

#. Enter the ``/installation/parent/directory/pattoo`` directory with the ``pattoo`` files.
#. Install the required packages using the ``pip_requirements`` document in the ``pattoo`` root directory

   .. code-block:: bash

      $ pip3 install -r pip_requirements.txt --target /opt/pattoo/daemon/.python

#. Create the ``MySQL`` or ``MariaDB`` database for ``pattoo`` with the correct authentication parameters provided in the :doc:`configuration` In this example adjust the name of your database and the password accordingly.

    .. code-block:: bash

       $ sudo mysql

    .. code-block:: sql

        CREATE DATABASE pattoo;
        GRANT ALL PRIVILEGES ON pattoo.* TO pattoo@"localhost" IDENTIFIED BY 'PATTOO_PASSWORD';
        FLUSH PRIVILEGES;
        exit;

#. Use the :doc:`configuration` to create a working configuration.
#. Run the installation script

   .. code-block:: bash

      $ sudo setup/pattoo_installation.py

#. Configure the required ``cron`` jobs. :doc:`cron`
