"""Count the words in a .txt file uploaded to S3, deployed with Chalice.

Class 07 demo: the console demo's lambda_handler, rewritten as a Chalice S3 event handler.
Paste this file over the app.py that chalice new-project created.
"""

import boto3
from chalice import Chalice

# Update the bucket name to your bucket
BUCKET = "demo-mst3k"

app = Chalice(app_name="textapp")
s3 = boto3.client("s3")


@app.on_s3_event(bucket=BUCKET, events=["s3:ObjectCreated:*"], suffix=".txt")
def count_words(event):
    """Count the words in the uploaded file and log the result."""
    # Chalice hands over the bucket and the decoded key: no Records loop, no unquote_plus
    text = s3.get_object(Bucket=event.bucket, Key=event.key)["Body"].read().decode("utf-8", errors="replace")
    # print output goes to CloudWatch Logs
    print(f"{event.key}: {len(text.split())} words")
