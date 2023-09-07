# Start or stop all
```
kubectl create namespace example-omero
```
```
cd omero-k8s-templates/gke/
kubectl apply -k gcs_run
```
```
kubectl -n example-gcs-omero delete pod,deployment,svc,secret --all
```