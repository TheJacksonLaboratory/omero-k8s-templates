#!/usr/bin/dumb-init /bin/bash

set -e

# entrypoint.sh is not being called from a login shell:
source /etc/profile

source /opt/omero/server/server_venv/bin/activate

for f in /startup/*; do
    if [ -f "$f" -a -x "$f" ]; then
        echo "Running $f $@"
        "$f" "$@"
    fi
done
