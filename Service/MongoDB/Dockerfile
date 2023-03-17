# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/baseimage:0.11

LABEL maintainer="KycKyc"

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Update repo for mongo installation
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update && apt-get install -y --allow-unauthenticated \
    mongodb-org && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/

# Setup UTF-8
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN mkdir -p /data/db

# Copy production Configs
COPY configs/production/mongod.conf /etc/mongod.conf

EXPOSE 27017