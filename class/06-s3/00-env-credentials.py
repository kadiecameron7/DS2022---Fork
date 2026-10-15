#!/usr/bin/env python3
"""Build an S3 client from environment variables (optional alternative to ~/.aws)."""
import logging
import os

import boto3

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# Learner Lab AWS Details (session token required; expires ~4 hours):
#   export AWS_ACCESS_KEY_ID="YOUR_KEY"
#   export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
#   export AWS_SESSION_TOKEN="YOUR_SESSION_TOKEN"
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("MY_ACCESS_KEY")
SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") or os.getenv("MY_SECRET_ACCESS_KEY")
SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

if not ACCESS_KEY or not SECRET_ACCESS_KEY:
    log.error(
        "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY "
        "(and AWS_SESSION_TOKEN for Learner Lab)."
    )
    raise SystemExit(1)

kwargs = {
    "aws_access_key_id": ACCESS_KEY,
    "aws_secret_access_key": SECRET_ACCESS_KEY,
}
if SESSION_TOKEN:
    kwargs["aws_session_token"] = SESSION_TOKEN

s3 = boto3.client("s3", **kwargs)
log.info("S3 client created using environment credentials.")
