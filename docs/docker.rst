Docker installation option
==========================

The docker installation utilizes the ``Dockerfile`` located in the root directory of ``pattoo``. The code that handles the docker installation can be found in 
the  ``setup/_pattoo/docker.py`` folder.

However, if you desire to run the docker installation outside of the pattoo installation script it can be achieved by doing the following:


#. The docker container is built using the following command:

    .. code-block:: bash

       $ docker build -t pattoo .

#. Run the container in detached mode with the ``--privileged`` tag and the ``--network`` tag set to ``host``.


    .. code-block:: bash

       $ docker run --privileged -d --network=host --name=pattoo pattoo


**Note)** The container is run in detached mode, with the network set to host, to allow the pattoo container to communicate with the host machine's MySQL or MariaDB database for ``pattoo``. Additionally, the container is run in privileged mode to allow the system daemons to be run in the docker container.


#. Run the pattoo installation in the container

    .. code-block:: bash

       $ docker exec -i pattoo setup/install.py install all



Dockerfile Breakdown
^^^^^^^^^^^^^^^^^^^^

**Pulling the base image**

This sets the base image for the pattoo container to the latest version of ubuntu.


    .. code-block:: bash

       FROM ubuntu:latest

**Installing python to container**

Since the Ubuntu image doesn't have python or installed by default, it has to be installed via ``apt``

    .. code-block:: bash

       RUN apt-get update \
        && apt-get install -y python3-pip python3-dev \
        && cd /usr/local/bin \
        && ln -s /usr/bin/python3 python \
        && pip3 install --upgrade pip

**Disabling the interactive mode for the Debian frontend**

This sets the ``DEBIAN_FRONTEND`` variable to its non-interactive mode to prevent the build from failing due to user input being required.


    .. code-block:: bash

       ARG DEBIAN_FRONTEND=noninteractive

**Set working directory to pattoo**

    .. code-block:: bash

       WORKDIR "/pattoo"

**Install systemd package**


Since the base image for ubuntu does not have systemd installed by default, it has to be installed via ``apt``

    .. code-block:: bash

       RUN apt-get install -y systemd

**Copy repository contents**

This copies all of the contents in the directory with the ``Dockerfile``, excluding files and directories listed in the ``.dockerignore`` file.


    .. code-block:: bash

       COPY . /pattoo

**Expose the respective ports**

To allow the daemons to communicate outside of the docker container, the respective ports will have to be exposed in the Dockerfile. Fortunately, if the installation is run with the installation script, all ports listed in the ``pattoo_server.yaml`` file will be automatically inserted in the ``Dcokerfile``.

    .. code-block:: bash

       EXPOSE 20203
       EXPOSE 20202
       EXPOSE 20201
       EXPOSE 3306

**Start systemd**

By default the systemd service will not be activated in a docker container. So the ``/usr/bin/systemd`` file has to be executed to allow daemons to run in the docker container.

    .. code-block:: bash

       CMD ["/usr/bin/systemd"]





