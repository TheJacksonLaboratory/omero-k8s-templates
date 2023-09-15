## Google cloud build

[Google Cloud build](https://cloud.google.com/build) can be used to build the containers and push to a private repository for the project.

### Setup
Google Cloud build needs to be set up a single time per project.

First, enable the following Google APIs on the (Google Cloud Console)[https://console.developers.google.com/]:
* Cloud Build API
* Artifact Registry API

Next, create a repository to use:
```bash
gcloud artifacts repositories create omero-repo --repository-format=docker \
    --location=us-east1 --description="Docker repository"
```

The region (`us-east1`) should match where the cluster will be run.
### Build containers in the cloud (by hand)

```bash
gcloud builds submit omero-server --tag us-east1-docker.pkg.dev/<GCP PROJECT NAME>/omero-repo/omero-server:latest
gcloud builds submit omero-web --tag us-east1-docker.pkg.dev/<GCP PROJECT NAME>/omero-repo/omero-web:latest

```