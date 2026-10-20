#!/usr/bin/env python3
"""Check that boto3 is installed and finds your Learner Lab credentials."""
import logging

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logging.basicConfig(format="%(message)s")
# logging.basicConfig(level=logging.INFO, format="%(levelname)s %(asctime)s %(message)s")
log = logging.getLogger(__name__)

log.info(f"boto3 version: {boto3.__version__}")

session = boto3.session.Session()
log.info(f"Region: {session.region_name}")  # from ~/.aws/config
if session.region_name is None:
    log.warning("No region set. Run: aws configure set region us-east-1")

try:
    # Same check as `aws sts get-caller-identity`
    sts = session.client("sts")
    identity = sts.get_caller_identity()
    log.info(f"Account: {identity['Account']}")
    log.info(f"Arn: {identity['Arn']}")
except NoCredentialsError:
    log.error("No credentials found. Paste the AWS Details block into ~/.aws/credentials.")
except ClientError as e:
    log.error(f"Credentials invalid or expired. Copy a fresh block from AWS Details (in AWS Academy Learner Lab): {e}")
