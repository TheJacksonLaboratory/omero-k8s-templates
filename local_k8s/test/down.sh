#!/bin/bash

kubectl delete pod database omero-server
kubectl delete deployment omero-web
kubectl delete pv pv-name
kubectl delete pvc pvc-name
kubectl delete secrets omero-secrets
kubectl delete service database omero-server omero-web
