# Dockerfile for omero server
FROM debian:buster
# FROM ubuntu:bionic

# Following https://docs.openmicroscopy.org/omero/5.6.3/sysadmins/unix/server-debian10-ice36.html

RUN apt-get update
RUN apt-get install -y -q \
    unzip \
    wget \
    bc \
    default-jre \
    dumb-init \
    libhdf5-serial-dev \
    python3 \
    python3-venv \
    python3-dev \
    postgresql-client \
    ca-certificates-java

# install zeroc-ice
RUN apt-get install -y -q \
    build-essential \
    db5.3-util \
    libbz2-dev \
    libdb++-dev \
    libdb-dev \
    libexpat-dev \
    libmcpp-dev \
    libssl-dev \
    mcpp \
    zlib1g-dev \
    pkg-config

RUN cd /tmp
RUN wget -q https://github.com/ome/zeroc-ice-debian10/releases/download/0.1.0/ice-3.6.5-0.1.0-debian10-amd64.tar.gz
RUN tar xf ice-3.6.5-0.1.0-debian10-amd64.tar.gz
RUN mv ice-3.6.5-0.1.0 /opt

ADD omero-ice36.env .
RUN cat omero-ice36.env >> /etc/profile

# install python dependencies
RUN python3 -mvenv /opt/omero/server/server_venv
RUN /opt/omero/server/server_venv/bin/pip install --upgrade pip
RUN /opt/omero/server/server_venv/bin/pip install wheel setuptools
RUN /opt/omero/server/server_venv/bin/pip install https://github.com/ome/zeroc-ice-debian10/releases/download/0.1.0/zeroc_ice-3.6.5-cp37-cp37m-linux_x86_64.whl
RUN /opt/omero/server/server_venv/bin/pip install omero-server[default]
RUN /opt/omero/server/server_venv/bin/pip install "omero-py>=5.8.0"
RUN /opt/omero/server/server_venv/bin/pip install omego
RUN /opt/omero/server/server_venv/bin/pip install omero-certificates==0.2.0
RUN /opt/omero/server/server_venv/bin/pip install omero-cli-transfer>=0.2.0


#RUN mkdir -p /opt/omero/web/OMERO.web/etc/grid && \
#    chown -R omero-web /opt/omero/web/OMERO.web
RUN useradd -ms /bin/bash omero-server

WORKDIR /opt/omero/server
ENV SERVER=https://downloads.openmicroscopy.org/omero/5.6/server-ice36.zip
RUN wget -q $SERVER -O OMERO.server-ice36.zip
RUN unzip -q OMERO.server*
RUN chown -R omero-server OMERO.server-*
RUN ln -s OMERO.server-*/ OMERO.server
RUN chown -R omero-server /opt

# RUN mkdir -p /OMERO/certs 
#RUN chown -R omero-server /OMERO

# Startup scripts, from omero-server-docker
ADD entrypoint.sh /usr/local/bin/
COPY startup /startup/

USER omero-server
ENV OMERODIR /opt/omero/server/OMERO.server

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
