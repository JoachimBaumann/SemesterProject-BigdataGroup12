from minio import Minio
from minio.error import S3Error
import os

client = Minio(
    "minio.minio-operator.svc.cluster.local",
    access_key="BVM3WRSFPR9MUF7ELEFL",
    secret_key="hJ36jmiI9Sgw1HdXQAK6xBD2k0msVqy7wkQMHmMF",
    secure=False  # Set to True if using HTTPS
)


def download_objects(client = client, bucket_name='datasets', prefix=''):
    """
    Recursively download objects starting from the specified prefix.
    """
    try:
        objects = client.list_objects(bucket_name, prefix, recursive=True)

        for obj in objects:
            if obj.is_dir:
                # If the object is a directory, recursively download objects within it
                download_objects(client, bucket_name, prefix=obj.object_name)
            else:
                # Download the object
                file_path = obj.object_name
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                client.fget_object(bucket_name, obj.object_name, file_path)
                print(f"Downloaded {file_path}")
    except S3Error as err:
        print(f"Failed to download {bucket_name}: {err}")