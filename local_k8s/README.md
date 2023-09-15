# Local Kubernetes OMERO deployment
Our local Kubernetes is solely used for testing currently. These templates are not as robust as the GCP ymls, and some things should probably be changed for a production environment:

1. Not running Postgres through Kubernetes, since the database needs to be persistent
2. Host a separate NFS server somewhere with lots of space for image data files, rather than as a Kubernetes persistent volume
3. Probably use something larger than minikube to run the Kubernetes cluster
4. More persistent port forwarding than `kubectl port-forward`

## Current tested setup:
`minikube` running Kubernetes cluster on `CentOS 7`

## Build images
```
eval $(minikube docker-env)
cd omero-k8s-templates/local_k8s/containers
docker build omero-web -t omero-web
docker build omero-server -t omero-server
```

## Run kubernetes deployments/pods
```
cd omero-k8s-templates/local_k8s/k8s_ymls
kubectl apply -f omero-secrets.yml
kubectl apply -f postgres.yml
kubectl apply -f omero-server.yml
kubectl apply -f omero-readonly-secrets.yml
kubectl apply -f omero-readonly-server.yml
kubectl apply -f nginx_conf_https.yml
kubectl apply -f nginx.sslsecret.yml
kubectl apply -f omero-web.yml
```

## Forward a local port to an internal pod port, to access OMERO.web
```
screen -S port-forward
kubectl port-forward svc/omero-web 6080:4080 --address==0.0.0.0
```
Then access OMERO.web at `localhost:6080`