#!/usr/bin/env python3
"""Upload a local file to S3."""
import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# practice-<USER>: bucket names must be globally unique across all of AWS
bucket_name = f"practice-{os.environ.get('USER', 'unknown')}"
local_file = "cloud.jpg"  # must exist in the current directory
key = "folder/in/bucket/cloud.jpg"

try:
    s3 = boto3.client("s3")
    with open(local_file, "rb") as f:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=f,
            ContentType="image/jpeg",  # so browsers can display, not download
        )
    log.info(f"Uploaded {local_file} to s3://{bucket_name}/{key}")
except FileNotFoundError:
    log.error(f"Local file not found: {local_file}")
except ClientError as e:
    log.error(f"Error uploading object: {e}")
