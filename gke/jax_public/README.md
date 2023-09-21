# Replica of JAX public OMERO instance running at images.jax.org
Adds OMERO environment variables that are not required but are used in JAX public instance

# Create namespace first
```
kubectl create namespace example-omero
```

# Run OMERO via kustomize
```
cd omero-k8s-templates/gke/
kubectl apply -k jax_public
```

# Delete everything in namespace (to restart)
```
kubectl -n example-omero delete pod,deployment,svc,secret --all
```