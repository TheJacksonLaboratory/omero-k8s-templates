# Local Kubernetes OMERO deployment

## Current infrastructure
- `kubeadm` runs Kubernetes cluster on `Rocky 9`
- `postgres` baremetal database
- `calico` networking

Has also been tested with `minikube` on `Rocky 9` and `Centos 7`.

## Build images
If using minikube, you first need to access the minikube docker environment
```
eval $(minikube docker-env)
```

```
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
And put the base64 nginx.key and nginx.crt in nginx.sslsecret.yml

### Changes used for testing
- Temporary local nfs volume
- Temporary postgres database run as kubernetes pod

## CSRF trusted origins
When using Django 4 (required by OMERO.web 5.23.0+) with http or https, we need to set the CSRF_TRUSTED_ORIGINS environment variable. This can be set the OMERO config omero.web.csrf_trusted_origins (https://github.com/ome/omero-web/pull/477).

We've put this setting in the Nginx configmap ymls. In nginx_conf_http.yml or nginx_conf_https.yml, replace `http://web_url:port` with your web url and port.

## Run kubernetes deployments/pods
By using kustomize, we can just apply the whole folder at once:
```
kubectl apply -k test
```

## Forward a local port to an internal pod port, to access OMERO.web
If using minikube, `port-forward` is needed to expose port:
```
screen -S port-forward
kubectl port-forward svc/omero-web 8080:80 --address=0.0.0.0
```
Then access OMERO.web at `localhost:8080`

