#!/usr/bin/env python3
"""List objects in an S3 bucket (optional prefix)."""
import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# practice-<USER>: bucket names must be globally unique across all of AWS
bucket_name = f"practice-{os.environ.get('USER', 'unknown')}"
prefix = ""  # e.g. "folder/in/bucket/"

try:
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    contents = response.get("Contents", [])
    if not contents:
        log.info("No objects found.")
    else:
        log.info(f"Objects in s3://{bucket_name}/{prefix}")
        for obj in contents:
            log.info(f"- {obj['Key']} ({obj['Size']} bytes)")
except ClientError as e:
    log.error(f"Error listing objects: {e}")
