"""Count the words in a .txt file uploaded to S3.

Class 07 demo: a Lambda function built by hand in the AWS Console. Paste this file
into the console's code editor as lambda_function.py.
"""

import urllib.parse

import boto3

s3 = boto3.client("s3")


def lambda_handler(event, context):
    """Count the words in each uploaded file and log the result."""
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        # S3 sends the key URL-encoded: "my book.txt" arrives as "my+book.txt"
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        text = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8", errors="replace")
        # print output goes to CloudWatch Logs
        print(f"{key}: {len(text.split())} words")
