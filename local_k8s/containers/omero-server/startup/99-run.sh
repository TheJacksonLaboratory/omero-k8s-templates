#!/bin/bash

set -eu

omero=/opt/omero/server/server_venv/bin/omero
cd /opt/omero/server
echo "Starting OMERO.server"
exec $omero admin start --foreground
