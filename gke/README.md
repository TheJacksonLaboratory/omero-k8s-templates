# Google Cloud Project (GCP) Setup

## VPC
## Google Kubernetes Engine (GKE)
CLI command 
```bash
gcloud container --project <PROJECT NAME> \
	clusters create <GKE CLUSTER NAME> --region "us-east1" \
	--machine-type "e2-custom-8-10240" \
	--image-type "COS_CONTAINERD" \
	--disk-type "pd-balanced" --disk-size "100" \
	--num-nodes "1" \
	--enable-private-nodes --master-ipv4-cidr "172.16.0.0/28" --enable-ip-alias \
	--enable-private-endpoint \
	--network "projects/<PROJECT NAME>/global/networks/<VPC NAME>" --subnetwork "projects/<PROJECT NAME>/regions/us-east1/subnetworks/<SUBNETWORK NAME>" \
	--cluster-ipv4-cidr "/17" --services-ipv4-cidr "/22" \
	--enable-autoscaling --min-nodes "0" --max-nodes "3" --location-policy "BALANCED" \
	--enable-master-authorized-networks --master-authorized-networks <ALLOWED IPS FOR KUBECTL> \
	--enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0
```

Notes:
- Must be a standard cluster, not autopilot, if will be connecting to object storage. OMERO.server pods that read from object storage currently need to be privileged, which is only allowed on a standard cluster.
- `--enable-master-authorized-networks --master-authorized-networks <ALLOWED IPS FOR KUBECTL>` is optional whitelisting IPs that can connect to the GKE control plane node

## Postgres SQL instance
- JAX currently running PostgreSQL 13, 2vCPU, 7.5 GB memory, 25 HDD storage
- Probably set a Private IP on the OMERO VPC
- Keep track of the admin password on set up - username for that is usually "postgres"

### Creating Postgres users and database for OMERO
Need a psql client matching Postgres version: https://www.postgresql.org/download/linux/debian/
```
apt-get install wget gnupg2
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-client-13 
```

Create users and database (Here OMERO.server user is omero_rw and readonly OMERO.server user is omero_ro, feel free to change. Definitely change password of omero_ro.)
```
createuser -h <DATABASE IP> -U postgres -P -D -R -S omero_rw
psql -h <DATABASE IP> -U postgres
GRANT omero_rw to postgres;
exit
createdb -h <DATABASE IP> -U postgres -E UTF8 -O omero_rw omero_database
psql -h <DATABASE IP> -U postgres
CREATE USER omero_ro;
\c omero_database omero_rw
GRANT CONNECT ON DATABASE omero_database TO omero_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO omero_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO omero_ro;
\c postgres postgres
ALTER USER omero_ro WITH PASSWORD 'password';
```

## Filestore
If using object storage, this only needs to be 1Tb (minimum possible size) to accommodate OMERO server files. If storing data on Filestore, this needs to be at least as large as the data to store, plus some for OMERO server files. Size can be increased later.

## Google Cloud Storage (GCS) - optional
We use gcsfuse to mount object storage such that OMERO sees it as a filesystem and can read data files. The object storage bucket will be mounted read-only to the OMERO.server pod, useful for OMERO in-place imports with the `--transfer ln_s` flag.

## Artifact Registry container image repository
We build container images and push them to the project's Google Artifact Registry for the kubernetes pods to reference. Any other image repository would also work.

## Google Compute Engine (GCE) - optional
Useful to have an extra VM to mount Filestore for data transfers, also possibly as the single authorized IP to access the GKE control plane (e.g. via kubectl)

# Params to configure in yml
OMERO.server (omero-server.yml, omero-readonly-server.yml, omero-server-nfs.yml, omero-readonly-server-nfs.yml)
- CONTAINER IMAGE
    - Likely the URL to the Google artifact registry repository where you pushed the container image
- DB NAME
    - Database name within the SQL instance (click on SQL name and go to "Databases" on the left side)
- CLOUD SQL IP
    - IP of the SQL instance on GCP
- FILESTORE IP
    - IP of the NFS server, likely run as a Filestore instance but also possible as a small VM
- MOUNT PATH / DATA MOUNT PATH
    - path of the directory to be mounted within NFS server
- GCS BUCKET NAME
    - Only for object-storage OMERO.server yamls
    - Name of Google Storage bucket

OMERO.server container image
- data_mount
	- the Dockerfile in `omero-k8s-templates/gke/containers/omero-server` sets permissions such that Filestore or gcsfuse can mount to `/data_mount`
	- the lines ```RUN mkdir -p /data_mount; RUN chown -R omero-server /data_mount``` can be changed to a different mount path if desired (the mount path in the OMERO.server ymls would have to be changed accordingly)

OMERO.web
- CONTAINER IMAGE
    - Likely the URL to the Google artifact registry repository where you pushed the container image

OMERO.web container image
- logo.png
	- this OMERO.web setup (container image and deployment .yml) currently switch out the OMERO logo in the top left of the webpage with the logo saved at logo.png in `omero-k8s-templates/gke/containers/omero-web`

# Secrets
All secrets are base64. `echo -n key | base64`
- nginx.sslsecret.yml
    - SSL cert and key
- omero-secrets.yml
    - database user and password
- omero-readonly-secrets.yml
    - read-only database user and password

# kustomize
- `nfs_base`: base folder of templates
	- This runs if you replace every <ALL CAPS> parameter in the ymls, as described above
	- OMERO.server read-write, OMERO.server read-only, OMERO.web connected to read-only OMERO.server
	- Both OMERO files and image data files are hosted on Filestore (NFS)
- `nfs_run`: use kustomize to enter all parameters for `nfs_base`
	- Currently runs exactly the same pods as `nfs_base`
	- This is just another way for you to enter all the abstracted <ALL CAPS> parameters from `nfs_base` in one file (`nfs_changes.yml`)
	- As an example, where possible, most of the abstracted parameters have been filled in
- `gcs_run`: use kustomize to change OMERO.server pods to mount object storage (GCS)
	- OMERO files are hosted on Filestore still, image data files can be hosted on object storage (GCS)
	- requires running on a standard GKE cluster
	- Enter all abstracted <ALL CAPS> parameters from `nfs_base` in `gcs_changes.yml`
	- As an example, where possible, most of the abstracted parameters have been filled in