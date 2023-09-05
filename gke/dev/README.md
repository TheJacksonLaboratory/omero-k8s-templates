# Start or stop all
```
cd omero-k8s-templates/gke/
kubectl apply -k dev
```
```
kubectl -n test-omero delete pod,deployment,svc,secret --all
```