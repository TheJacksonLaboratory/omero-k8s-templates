:warning:
# Copied from jax-gcp-omero github with some changes
- jax-omero-server Dockerfile gives user more permissions to */opt* and */OMERO* folders
- added docker-compose yml 
- tag image in `docker build` command 

:warning:


# Docker containers for OMERO deployment

## Containers
*jax-omero-web* is our custom built OMERO.web container.

*jax-omero-server* is our custom built OMERO.server container.

You will need to initialize the submodule before building:
```bash
% git submodule update --init --recursive
```

## Local build

The containers can be built locally using docker.

```bash
docker build jax-omero-web -t jax-omero-web
docker build jax-omero-server -t jax-omero-server
```

```bash
docker compose -f docker-compose.test.yml up --renew-anon-volumes --force-recreate
```

## Google cloud build

[Google Cloud build](https://cloud.google.com/build) can be used to build the containers and push to a private repository for the project.

*TODO*: We should be using explicit version tags.
### Setup
Google Cloud build needs to be set up a single time per project.

First, enable the following Google APIs on the (Google Cloud Console)[https://console.developers.google.com/]:
* Cloud Build API
* Artifact Registry API

Next, create a repository to use:
```bash
gcloud artifacts repositories create jax-omero-repo --repository-format=docker \
    --location=us-east1 --description="Docker repository"
```

The region (`us-east1`) should match where the cluster will be run.
### Build containers in the cloud (by hand)

```bash
gcloud builds submit jax-omero-server --tag us-east1-docker.pkg.dev/jax-omero-pub/jax-omero-repo/jax-omero-server:latest
gcloud builds submit jax-omero-web --tag us-east1-docker.pkg.dev/jax-omero-pub/jax-omero-repo/jax-omero-web:latest

```

### Build using cloudbuild.yaml (recommended)

```bash
gcloud builds submit --config cloudbuild.yaml
```

### Tagging images for production

We will use the tag `:production` for the main k8 deployment.
```bash
gcloud artifacts docker tags add us-east1-docker.pkg.dev/jax-omero-pub/jax-omero-repo/jax-omero-web:latest us-east1-docker.pkg.dev/jax-omero-pub/jax-omero-repo/jax-omero-web:production
gcloud artifacts docker tags add us-east1-docker.pkg.dev/jax-omero-pub/jax-omero-repo/jax-omero-server:latest us-east1-docker.pkg.dev/jax-omero-pub/jax-omero-repo/jax-omero-server:production
```

## Repository queries
```bash
gcloud artifacts repositories list
gcloud artifacts docker images list us-east1-docker.pkg.dev/jax-omero-pub/jax-omero-repo
```
