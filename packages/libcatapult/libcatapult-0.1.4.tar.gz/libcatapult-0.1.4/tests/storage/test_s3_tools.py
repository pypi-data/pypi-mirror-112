

import os
from pathlib import Path

import boto3
import pytest
from moto import mock_s3
from libcatapult.storage.s3_tools import S3Utils, NoObjectError

BUCKET = 'test'


def initialise_bucket(bucket_name):
    conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket=bucket_name)

    for file in Path('tests/data/bucket').glob('**/*.txt'):
        conn.Bucket(bucket_name).upload_file(
            Filename=str(file),
            Key=f"tests/data/bucket/{file.parent.stem}/{file.name}"
        )


@mock_s3
def test_count():
    initialise_bucket(BUCKET)
    s3 = S3Utils(access=None, secret=None, bucket=BUCKET, endpoint_url=None, region='us-east-1')
    result = s3.count()
    assert result == 2


@mock_s3
def test_list():
    initialise_bucket(BUCKET)
    s3 = S3Utils(access=None, secret=None, bucket=BUCKET, endpoint_url=None, region='us-east-1')
    result = s3.list_files("")
    assert len(result) == 2

    assert result[0] == "tests/data/bucket/bucket/test_1.txt"
    assert result[1] == "tests/data/bucket/bucket/test_2.txt"


@mock_s3
def test_list_with_size():
    initialise_bucket(BUCKET)
    s3 = S3Utils(access=None, secret=None, bucket=BUCKET, endpoint_url=None, region='us-east-1')
    result = s3.list_files_with_sizes("")
    assert len(result) == 2

    assert result[0]["name"] == "tests/data/bucket/bucket/test_1.txt"
    assert result[1]["name"] == "tests/data/bucket/bucket/test_2.txt"

    assert result[0]["size"] == 11
    assert result[1]["size"] == 7


@mock_s3
def test_fetch_file():
    initialise_bucket(BUCKET)
    s3 = S3Utils(access=None, secret=None, bucket=BUCKET, endpoint_url=None, region='us-east-1')
    s3.fetch_file("tests/data/bucket/bucket/test_1.txt", "/tmp/test_fetch.txt")

    assert os.path.exists("/tmp/test_fetch.txt")
    assert [row for row in open("/tmp/test_fetch.txt")] == [row for row in open("tests/data/bucket/test_1.txt")]


@mock_s3
def test_fetch_non_existent_file():
    initialise_bucket(BUCKET)
    s3 = S3Utils(access=None, secret=None, bucket=BUCKET, endpoint_url=None, region='us-east-1')
    with pytest.raises(NoObjectError):
        s3.fetch_file("this_doesnt_exist.txt", "/tmp/test_fetch.txt")


@mock_s3
def test_put_file():
    initialise_bucket(BUCKET)
    s3 = S3Utils(access=None, secret=None, bucket=BUCKET, endpoint_url=None, region='us-east-1')
    s3.put_file("tests/data/bucket/test_1.txt", "tests/result/test_1.txt")
    s3.fetch_file("tests/result/test_1.txt", "/tmp/test_put.txt")

    assert os.path.exists("/tmp/test_put.txt")
    assert [row for row in open("/tmp/test_put.txt")] == [row for row in open("tests/data/bucket/test_1.txt")]
