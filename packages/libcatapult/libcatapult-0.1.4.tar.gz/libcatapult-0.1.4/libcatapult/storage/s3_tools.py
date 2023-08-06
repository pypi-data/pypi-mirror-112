import logging

import boto3
from botocore.exceptions import ClientError


class S3Utils:
    """
    A simple interface around the S3 access commands.
    Only provides the tools that we need.
    """

    def __init__(self, access, secret, bucket, endpoint_url, region):
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=endpoint_url,
            verify=False,
            region_name=region,
            aws_access_key_id=access,
            aws_secret_access_key=secret,
        )

        self.bucket = bucket

    def count(self):
        """
        Count the number of objects in the bucket.

        :return: The number of objects in the bucket
        """
        return sum(1 for _ in self.s3.Bucket(self.bucket).objects.all())

    def list_files(self, prefix):
        """
        Create and return a list of all files in the bucket.

        :param: Prefix to search for, primarily a path but it's just a string match.
        :return: List of strings.
        """

        filenames = []
        for obj in self.s3.Bucket(self.bucket).objects.filter(Prefix=prefix):
            filenames.append(obj.key)

        return filenames

    def list_files_with_sizes(self, prefix):
        """
        Create and return a list of all files in the bucket along with their file sizes.

        :param: Prefix to search for, primarily a path but it's just a string match.
        :return: List of dictionaries with name and size keys.
        """
        results = []
        for obj in self.s3.Bucket(self.bucket).objects.filter(Prefix=prefix):
            results.append({"name": obj.key, "size": obj.size})
        return results

    def fetch_file(self, path, destination):
        """
        Download a file from S3 and put it in the destination

        :param path: location in S3 to get the file from.
        :param destination: where on the local file system to put the file
        :return: None
        """
        try:
            self.s3.Bucket(self.bucket).download_file(path, destination)
        except ClientError as ex:
            if ex.response['Error']['Code'] == '404':
                raise NoObjectError(f'Nothing found with {path} in {self.bucket} bucket')
            else:
                raise

    def put_file(self, source, destination):
        """
        put a file into S3 from the local file system.

        :param source: a path to a file on the local file system
        :param destination: where in S3 to put the file.
        :return: None
        """
        self.s3.Bucket(self.bucket).upload_file(source, destination)

    def get_object_body(self, path):
        try:
            obj = self.s3.Object(bucket_name=self.bucket, key=path).get()
            return obj.get('Body').read()
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                raise NoObjectError(f'Nothing found with {path} in {self.bucket} bucket')
            raise


class NoObjectError(Exception):
    pass
