# Build images
```
eval $(minikube docker-env)
cd containers
docker build omero-web -t omero-web
docker build omero-server -t omero-server
cd ../k8s_ymls
# NFS setup? docker container (because kub not privileged)
kubectl apply -f omero-secrets.yml
kubectl apply -f postgres.yml
kubectl apply -f omero-server.yml
kubectl apply -f nginx_conf_http.yml
kubectl apply -f nginx.sslsecret.yml
kubectl apply -f omero-rw-web.yml
kubectl port-forward svc/jax-omero-web 6080:4080 --address==0.0.0.0
```
