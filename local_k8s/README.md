# Local Kubernetes OMERO deployment
Our local Kubernetes is solely used for testing currently. These templates are not as robust as the GCP ymls, and some things should probably be changed for a production environment:

1. Not running Postgres through Kubernetes, since the database needs to be persistent
2. Host a separate NFS server somewhere with lots of space for image data files, rather than as a Kubernetes persistent volume
3. Probably use something larger than minikube to run the Kubernetes cluster
4. More persistent port forwarding than `kubectl port-forward`

## Current tested setup:
`minikube` running Kubernetes cluster on `Rocky 9`

## Build images
```
eval $(minikube docker-env)
cd omero-k8s-templates/local_k8s/containers
docker build omero-web -t omero-web
docker build omero-server -t omero-server
```

## For testing purposes, create your own SSL certificate
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx.key -out nginx.crt
cat nginx.key | base64 -w 0
cat nginx.crt | base64 -w 0
```
And put base64 nginx.key and nginx.crt in nginx.sslsecret.yml

## CSRF trusted origins
When using Django 4 (required by OMERO.web 5.23.0+) with http or https, we need to set the CSRF_TRUSTED_ORIGINS environment variable. This can be set the OMERO config omero.web.csrf_trusted_origins (https://github.com/ome/omero-web/pull/477).

We've put this setting in the Nginx configmap ymls. In nginx_conf_http.yml or nginx_conf_https.yml, replace `http://web_url:port` with your web url and port.

## Run kubernetes deployments/pods
```
cd omero-k8s-templates/local_k8s/k8s_ymls
kubectl apply -f omero-secrets.yml
kubectl apply -f nfs_pv.yml
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
kubectl port-forward svc/omero-web 8080:80 --address=0.0.0.0
```
Then access OMERO.web at `localhost:8080`

