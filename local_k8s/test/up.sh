#!/bin/bash

kubectl apply -k test
sleep 60s
kubectl exec omero-server -- bash -c "/opt/omero/server/server_venv/bin/omero login -u root -w omero -s 127.0.0.1:4064"