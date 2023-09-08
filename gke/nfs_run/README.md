# Create namespace first
```
kubectl create namespace example-omero
```

# Run OMERO via kustomize
```
cd omero-k8s-templates/gke/
kubectl apply -k nfs_run
```

# Delete everything in namespace (to restart)
```
kubectl -n example-omero delete pod,deployment,svc,secret --all
```