# Dockerfile for a JAX-built omero web client
FROM debian:buster
# FROM ubuntu:bionic

# Following https://github.com/ome/omero-web-docker

RUN apt-get update
RUN apt-get install -y unzip python3 python3-venv dumb-init python3-dev zlib1g-dev libjpeg-dev build-essential

RUN useradd -ms /bin/bash omero-web
RUN mkdir -p /opt/omero/web/OMERO.web/etc/grid && \
    chown -R omero-web /opt/omero/web/OMERO.web

RUN python3 -m venv /opt/omero/web/venv3
RUN /opt/omero/web/venv3/bin/pip install --upgrade pip
RUN /opt/omero/web/venv3/bin/pip install wheel

# EP: As of 2120318 this is the most recent version with a wheel.  No idea why.
RUN /opt/omero/web/venv3/bin/pip install numpy==1.21.5
# TODO: Download & check hash function
RUN /opt/omero/web/venv3/bin/pip install --upgrade https://github.com/ome/zeroc-ice-debian10/releases/download/0.1.0/zeroc_ice-3.6.5-cp37-cp37m-linux_x86_64.whl
RUN /opt/omero/web/venv3/bin/pip install "omero-py==5.11.1"
RUN /opt/omero/web/venv3/bin/pip install "omero-web==5.14.0"

RUN /opt/omero/web/venv3/bin/pip install \
        omero-figure \
        omero-iviewer \
        whitenoise \
        omero-gallery \
        django-csp

# Startup
ADD entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/entrypoint.sh
COPY startup /startup/
ADD 01-default-webapps.omero /opt/omero/web/config/

USER omero-web

ENV OMERODIR=/opt/omero/web/OMERO.web/
ENV CONFIG_omero_web_application__server_host=0.0.0.0
# ENV CONFIG_omero_web_debug=true
# ENV CONFIG_omero_web_server__list='[["host.docker.internal", 6064, "host.docker.internal"]]'

EXPOSE 4080
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
