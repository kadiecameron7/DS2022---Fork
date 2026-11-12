#!/usr/bin/env python3
"""Create an S3 bucket named practice-<USER> in us-east-1."""
import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# practice-<USER>: bucket names must be globally unique across all of AWS
bucket_name = f"practice-khs3z-2"#{os.environ.get('USER', 'unknown')}"
log.info(f"{bucket_name}")

try:
    s3 = boto3.client("s3", region_name="us-east-1")
    # us-east-1: omit LocationConstraint or create_bucket fails
    s3.create_bucket(Bucket=bucket_name)
    log.info(f"Created bucket: {bucket_name}")
except ClientError as e:
    log.error(f"Error creating bucket {bucket_name}: {e}")
