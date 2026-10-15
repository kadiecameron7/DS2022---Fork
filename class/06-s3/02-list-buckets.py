#!/usr/bin/env python3
"""List S3 buckets visible to the configured credentials."""
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

try:
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = response.get("Buckets", [])

    if not buckets:
        log.info("No buckets found.")
    else:
        log.info("Buckets:")
        for b in buckets:
            log.info(f"- {b['Name']}")
except ClientError as e:
    log.error(f"Error listing buckets: {e}")
