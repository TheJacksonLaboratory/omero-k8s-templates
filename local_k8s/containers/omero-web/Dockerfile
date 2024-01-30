# Dockerfile for an omero web client
FROM debian:bullseye

# Following https://github.com/ome/omero-web-docker

RUN apt-get update
RUN apt-get install -y unzip python3 python3-venv dumb-init python3-dev zlib1g-dev libjpeg-dev build-essential

RUN useradd -ms /bin/bash omero-web
RUN mkdir -p /opt/omero/web/OMERO.web/etc/grid && \
    chown -R omero-web /opt/omero/web/OMERO.web

RUN python3 -m venv /opt/omero/web/venv3
RUN /opt/omero/web/venv3/bin/pip install --upgrade pip
RUN /opt/omero/web/venv3/bin/pip install wheel

RUN /opt/omero/web/venv3/bin/pip install numpy
# TODO: Download & check hash function
RUN /opt/omero/web/venv3/bin/pip install --upgrade https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20231130/zeroc_ice-3.6.5-cp39-cp39-manylinux_2_28_x86_64.whl
RUN /opt/omero/web/venv3/bin/pip install omero-py==5.17.0
RUN /opt/omero/web/venv3/bin/pip install omero-web==5.23.0

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
