#!/bin/bash

kubectl delete pod database omero-server
kubectl delete deployment omero-readonly-server omero-web
kubectl delete pv pv-name
kubectl delete pvc pvc-name
kubectl delete secrets omero-secrets omero-readonly-secrets
kubectl delete service database omero-server omero-readonly-server omero-web
