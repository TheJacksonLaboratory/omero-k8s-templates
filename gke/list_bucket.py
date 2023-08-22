from google.cloud import storage
import time
import argparse


def list_buckets(project):
    """Lists all buckets."""

    storage_client = storage.Client(project=project)
    buckets = storage_client.list_buckets()

    return([bucket.name for bucket in buckets])


def list_blobs(bucket_name, project, prefix=None):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client(project=project)

    # Note: Client.list_blobs requires at least package version 1.17.0.
    if prefix is None:
        blobs = storage_client.list_blobs(bucket_name)
    else:
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

    # Note: The call returns a response only when the iterator is consumed.
    return([blob.name for blob in blobs])


def get_directories(bucket_name, project, prefix=None):
    """List all directories in bucket from file names, \
       return list that don't have corresponding object"""
    obj_list = list_blobs(bucket_name, project, prefix)
    directory_to_add = set()
    directory_exists = set()
    for obj_name in obj_list:
        if obj_name[-1] == "/":
            directory_exists.add(obj_name)
            # print(obj_name, "is already directory")
        else:
            obj_path_list = obj_name.split("/")
            for i in range(1, len(obj_path_list)):
                directory_to_add.add("/".join(obj_path_list[:i])+"/")
    total_dir_num = len(directory_to_add)
    directory_to_add.difference_update(directory_exists)
    return((total_dir_num, directory_to_add))


def make_dir_objects(directory_to_add, bucket_name, project):
    """Make empty objects representing directories in bucket"""
    # https://stackoverflow.com/questions/38416598/how-to-create-an-empty-folder-on-google-storage-with-google-api
    storage_client = storage.Client(project=project)
    bucket = storage_client.get_bucket(bucket_name)

    for dir_name in directory_to_add:
        blob = bucket.blob(dir_name)
        content_type = 'application/x-www-form-urlencoded;charset=UTF-8'
        blob.upload_from_string('', content_type=content_type)


def main(working_bucket, project, prefix=None):
    """List all directories, make objects for them if they don't exist. \
       Takes about 1 min per thousand folders."""
    start = time.time()
    dir_num, dir_to_add = get_directories(working_bucket, project, prefix)
    stop = time.time()
    print("Total directories in path:", dir_num)
    print("Directories to add:", len(dir_to_add))
    print("Listing took", stop - start, "seconds")
    start = time.time()
    make_dir_objects(dir_to_add, working_bucket, project)
    stop = time.time()
    print("Adding took", stop-start, "seconds for",
          len(dir_to_add), "directories")
    print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create empty object for each \
                                     nested folder in GCS bucket')
    parser.add_argument('working_bucket', metavar='bucket',
                        help='Name of GCS bucket')
    parser.add_argument('project',
                        help='GCP project with bucket')
    parser.add_argument("--prefix", default=None,
                        help="Folder path to create objects in")

    args = vars(parser.parse_args())
    main(args["working_bucket"], args["project"], args["prefix"])
