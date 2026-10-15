#!/usr/bin/env python3
"""Optional: delete all objects (recursive empty). Run before 09-delete-bucket.py."""
import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# practice-<USER>: bucket names must be globally unique across all of AWS
bucket_name = f"practice-{os.environ.get('USER', 'unknown')}"

try:
    s3 = boto3.client("s3")
    # we use a paginator to handle large buckets with many objects
    # the paginator returns a generator of pages, each with a list of objects
    paginator = s3.get_paginator("list_objects_v2")
    deleted = 0
    for page in paginator.paginate(Bucket=bucket_name):
        contents = page.get("Contents", [])
        if not contents:
            continue
        s3.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": obj["Key"]} for obj in contents]},
        )
        deleted += len(contents)
        for obj in contents:
            log.info(f"Deleted s3://{bucket_name}/{obj['Key']}")
    if deleted == 0:
        log.info(f"Bucket s3://{bucket_name} is already empty.")
    else:
        log.info(f"Deleted {deleted} object(s) from s3://{bucket_name}")
except ClientError as e:
    log.error(f"Error emptying bucket {bucket_name}: {e}")
