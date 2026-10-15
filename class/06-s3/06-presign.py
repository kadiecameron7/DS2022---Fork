#!/usr/bin/env python3
"""Generate a time-limited presigned URL for an S3 object."""
import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# practice-<USER>: bucket names must be globally unique across all of AWS
bucket_name = f"practice-{os.environ.get('USER', 'unknown')}"
key = "folder/in/bucket/cloud.jpg"  # must exist in the bucket
expiration = 600  # seconds

try:
    s3 = boto3.client("s3")
    # ResponseContent* override headers so the browser displays the image
    # instead of downloading (objects uploaded without ContentType are octet-stream).
    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket_name,
            "Key": key,
            "ResponseContentType": "image/jpeg",
            "ResponseContentDisposition": "inline",
        },
        ExpiresIn=expiration,
    )
    log.info(f"{url}")
except ClientError as e:
    log.error(f"Error generating presigned URL: {e}")
