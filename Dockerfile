# Use ubuntu as base image
FROM ubuntu:latest

# Metadata
LABEL version="1.0"
LABEL maintainers="Jason Gayle, Peter Harrison"

# Update packages
RUN apt-get update && apt-get upgrade -y

# Install 
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# Install sbin
ARG DEBIAN_FRONTEND=noninteractive

# Set working directorya
WORKDIR "/pattoo"

# Install systemd
RUN apt-get install -y systemd

# Copy repository contents
COPY . /pattoo

# Expose ports
EXPOSE 20202
EXPOSE 20201
EXPOSE 3306

# Set up mysql
RUN mkdir /var/run/mysqld

RUN setup/install.py install configuration

CMD ["/usr/bin/systemd"]
