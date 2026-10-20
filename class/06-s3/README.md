# AWS S3 Storage

> [!CAUTION]
> **Do NOT click Reset in the AWS Academy Learner Lab unless your instructor tells you to.**
> Reset permanently deletes everything in your lab account (S3 buckets, EC2 instances, Lambda functions, ...) and cannot be undone. To pause, click **End Lab**: your resources stay and are back with the next **Start Lab**.

This session focuses on **S3**, object storage for datasets, backups, and pipeline I/O. Building on [IAM](../06-iam/README.md), you will:

- start an AWS Academy **Learner Lab** and inspect its pre-created IAM roles
- configure the AWS CLI with temporary credentials**
- create a bucket and move objects with `cp` / `sync` / `mv` / `presign`
- do the same from Python with `boto3` and the numbered scripts in this folder

`Lab 6` builds on this workflow, and you will reuse the same pattern of identity + storage with **Amazon EC2** and **AWS Lambda** in the coming weeks.

> Experiment with the commands and options. Errors are normal; ask for help and help each other when you can. Advanced topics (versioning, events, ACLs) are optional.


## In-class exercises


### Environment

Today you talk to AWS in two ways, and each needs its own tool:


| Tool            | What it is                                    | How you install it                                                                                                                                                 |
| --------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AWS CLI (`aws`) | A command line program you type commands into | Once, as a `uv` tool (below)                                                                                                                                       |
| `boto3`         | A Python library your scripts `import`        | Later, in a virtual environment for the Python scripts ([Access S3 using](#access-s3-using-boto3-in-python) `boto3` [in Python](#access-s3-using-boto3-in-python)) |


Install the AWS CLI now:

```bash
uv tool install awscli
```

`uv tool install` puts a command line program in its own isolated environment and adds the command to your `PATH`. The `aws` command then works in every terminal and every folder, independent of any project or `.venv`. You never `import` the CLI in Python, so it doesn't belong in a project's dependencies.

Confirm it works:

```bash
aws --version
```

You should see a line starting with `aws-cli/1.` (the version on PyPI is AWS CLI v1; it supports every command used in this course).

If the shell reports `aws: command not found`, run `uv tool update-shell`, then open a new terminal so the `uv` tool directory is on your `PATH`.

Create a working folder for the CLI exercises. The files you download and sync land here, outside the course repo:

```bash
mkdir -p ~/ds2022-fall-26/s3
cd ~/ds2022-fall-26/s3
```

Next, start the Learner Lab and configure credentials. You will set up the Python environment for `boto3` after the CLI exercises.

### Start the AWS Academy Learner Lab

Work in the **AWS Academy Learner Lab** (same Academy course as [IAM](../06-iam/README.md)).

1. Log in to **AWS Academy** with the account from your course invitation email.
2. Click **Start LMS**. This opens AWS Academy Canvas.
3. Click the **Learner Lab** course.
4. Go to **Modules** and, in the third section, click **Launch AWS Academy Learner Lab**.
5. Click **Start Lab** (top right corner).
6. Wait until the **AWS** icon in the top left corner turns green (a few minutes the first time).
7. Click the **AWS** icon, then **AWS Console**. The console opens in a new tab; allow pop-ups if nothing happens.

> **Do not click Reset.** A Learner Lab session lasts about 4 hours; when the timer runs out (or you click **End Lab**) the session stops, EC2 instances are stopped, and your credentials expire. Your S3 buckets and other resources stay in the account and are there again the next time you click **Start Lab**. **Reset** deletes everything in the lab account. You will reuse this setup later (EC2, serverless).

### AWS CLI configuration (temporary credentials)

The CLI credentials are not in the AWS Console. They are on the Learner Lab page where you clicked **Start Lab**:

1. Switch back from the AWS Console tab to the browser tab with the Learner Lab page (the one with the green **AWS** icon in the top left corner).
2. Click **AWS Details** in the top right corner, next to **Start Lab** and **End Lab**. A panel opens on the right.
3. Next to **AWS CLI**, click **Show**. A text block appears that starts with `[default]` and contains three lines: `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token`.
4. Select the whole block, from `[default]` through the end of the long `aws_session_token` line, and copy it. The block is already in the format the AWS CLI expects, so you paste it into the credentials file as is.

Create the credentials file and open it in Cursor:

```bash
mkdir -p ~/.aws
touch ~/.aws/credentials # creates empty ~/.aws/credentials
cursor ~/.aws/credentials
```

If the shell reports `cursor: command not found`, open the file from Cursor instead: **File** → **Open File...**, press `Cmd+Shift+.` (Mac) to show hidden folders, and go to `.aws/credentials` in your home folder. Alternatively, you can use other text editors like nano or vi.

Paste the whole block into the credentials file, replacing anything already in it, and save. It should look like this, with each value on a single line (the session token is very long):

```text
[default]
aws_access_key_id=ASIA...
aws_secret_access_key=...
aws_session_token=...
```

Set the default region and output format (this writes `~/.aws/config`):

```bash
aws configure set region us-east-1
aws configure set output json
```

> **Credentials expire when the lab session ends (about 4 hours).** When `aws` or `boto3` suddenly fail with expired-token errors, click **Start Lab** again if the session has ended, open **AWS Details** → **AWS CLI** → **Show**, copy the new block, and replace the contents of `~/.aws/credentials` with it. The region in `~/.aws/config` stays. Refreshing credentials does not affect your buckets.

Upon completion you will have `~/.aws/config` (region and output format) and `~/.aws/credentials` (the three values from AWS Details).

**Verify**

```bash
cat ~/.aws/config
cat ~/.aws/credentials
aws sts get-caller-identity
```

`get-caller-identity` should succeed and print something like this (your numbers and name will differ):

```json
{
    "UserId": "AROAZHRIMGJHAXBS5BBDQ:user5560460=Test_Student",
    "Account": "634666103374",
    "Arn": "arn:aws:sts::634666103374:assumed-role/voclabs/user5560460=Test_Student"
}
```

- **Account**: the 12-digit ID of your Learner Lab AWS account.
- **Arn**: `assumed-role/voclabs/...` means you are working as the `voclabs` role, not as an IAM user. The part after the last `/` is your lab session name.
- **UserId**: the role's unique ID, followed by the same session name.



### Access S3 using the AWS CLI

Now we can get busy!

#### `aws s3 ls` - List Buckets

```
aws s3 ls
```

You may see buckets you already created in this lab (for example `practice-mst3k`). The shared course materials live in `ds2022-fall26` in another account; that name may not appear in this list. Use the full `s3://ds2022-fall26/...` URIs below for download and sync.

#### `aws s3 mb` - Make a new bucket

```
echo $USER
aws s3 mb s3://practice-$USER
```

`$USER` expands to your computing id. Bucket names must be **globally unique** across all of AWS (a separate Learner Lab account does not give you a private name space). Prefixing your computing id with `practice-` makes a collision with someone else's bucket less likely. You should see:

```
make_bucket: practice-mst3k
```

If the bucket name is already taken, retry `practice-$USER-1`, `practice-$USER-2`, etc.

Check the list of buckets again:

```
aws s3 ls
```

Your bucket should be in the list now. 

If the output is too long, pipe it into grep, like `aws s3 ls | grep $USER`.

**Optional:** In the Academy console (from Start Lab), open **S3** → **General Purpose buckets** and confirm `practice-$USER` appears.

#### `aws s3 cp` - Copy files

The syntax is `aws s3 cp SOURCE DESTINATION`, similar to the regular `cp` command you're familiar with already. You can copy between any source/destination so long as at least one of them is S3:

- Copy from local environment to S3
- Copy from S3 to local environment
- Copy from S3 bucket to another S3 bucket

**Download**, try this:

```
aws s3 cp s3://ds2022-fall26/cloud.jpg . --no-sign-request
```

This downloads `cloud.jpg` from `ds2022-fall26` to your computer. Remember, `.` is the shorthand for your current directory.

**Why** `--no-sign-request`**?** Normally every AWS request is **signed** with your credentials, so AWS knows who you are. `ds2022-fall26` belongs to a different AWS account (the instructor's) and allows anyone to read its files. `--no-sign-request` sends the request anonymously, so it works without credentials and even after your lab credentials have expired. Your own `practice-$USER` bucket is private, so commands on it are signed and don't use this flag.

**Upload** (set content type so a later `presign` URL displays in the browser):

```
aws s3 cp cloud.jpg s3://practice-$USER/folder/in/bucket/cloud.jpg --content-type image/jpeg
```

Copies `cloud.jpg` into your bucket under the key `folder/in/bucket/cloud.jpg` (same path the Python scripts use). Confirm with `aws s3 ls s3://practice-$USER --recursive`.

Create another file on your computer, like `hello.txt`, add a message and save it. Then upload it into a new folder in S3.

**Another upload:**

```
aws s3 cp hello.txt s3://practice-$USER/new_folder/hello.txt
```

Notice that we don't have to create the `new_folder`.

**Folders in S3:** Contrary to how it appears, S3 is not a file system in the ordinary sense. It is object storage: each object has a **key** (name) and a **value** (the file contents). Keys can include `/`, which looks like folders (for example `folder/subfolder/filename.txt`), but those “folders” are only a naming convention (a mental convenience), not real directories you create ahead of time. The bucket name is not part of the key.

#### `aws s3 ls` - List the contents of a bucket

In the example below, replace `practice-mst3k` with your actual bucket name.

```bash
aws s3 ls s3://practice-mst3k/
```

Output may look like this:
```text
                           PRE folder/
                           PRE new_folder/
```

`PRE folder/` and `PRE new_folder/` are the CLI’s way of showing key prefixes (the “folders”) after your uploads. Use `aws s3 ls s3://practice-mst3k/ --recursive` to see full keys such as `folder/in/bucket/cloud.jpg`.

#### `aws s3 sync` - Synchronize a folder

`cp` copies one object. `sync` copies a whole prefix (folder) and **only transfers what is missing or changed**. The shared course bucket has a read-only `data/` folder you can pull from.

**1. Sync from the course bucket to your computer** (anonymous, as with `cp` above; see [Why](#aws-s3-cp---copy-files) `--no-sign-request`[?](#aws-s3-cp---copy-files))

```bash
mkdir -p data
aws s3 sync s3://ds2022-fall26/data/ ./data/ --no-sign-request
ls data
```

You should see eight files: three text files (`notes.txt`, `quotes.txt`, `todo.txt`), two JSON files (`books.json`, `stations.json`), and three CSV files (`sales.csv`, `sensors.csv`, `weather.csv`). Run the `sync` command a second time: nothing is transferred, because your local copies are already up to date.

**2. Sync that folder up into your own bucket**

```bash
aws s3 sync ./data/ s3://practice-$USER/data/
aws s3 ls s3://practice-$USER/data/
```

You can sync in any direction as long as at least one side is S3 (local ↔ S3, S3 ↔ local, or S3 ↔ S3).

#### `aws s3 mv` - Move (rename) an object in your bucket

`mv` renames or relocates an object. Practice on `notes.txt`, which you just synced into your bucket:

```bash
aws s3 mv s3://practice-$USER/data/notes.txt s3://practice-$USER/data/readme.txt
aws s3 ls s3://practice-$USER/data/
```

The listing now shows `readme.txt` instead of `notes.txt`.

#### `aws s3 presign` - Presign an S3 URL

In some cases you want to share a file for a limited time without creating access keys. `presign` creates a signed URL that expires after a set number of seconds (`--expires-in`).

```bash
aws s3 presign --expires-in 600 s3://practice-$USER/folder/in/bucket/cloud.jpg
```

You will receive a URL like this (yours will differ):

```text
https://practice-mst3k.s3.amazonaws.com/folder/in/bucket/cloud.jpg?AWSAccessKeyId=AKIA...&Signature=...&Expires=...
```

That URL works for 600 seconds (10 minutes). Open it in your web browser. After it expires, the link no longer grants access; the object is still in your bucket.

If the browser downloads the file instead of showing the image, the object was stored without a JPEG content type. Re-upload with `--content-type image/jpeg`, or use `06-presign.py`, which sets `ResponseContentType` / `ResponseContentDisposition` so the image opens inline.

#### `aws s3 rm` / `rb` - Optional cleanup

Keep the `practice-$USER` bucket for later weeks unless you intentionally want to delete it now. Deleting is an optional practice step.

**Delete one file**

```
aws s3 rm s3://practice-$USER/new_folder/hello.txt
```

**Empty the bucket, then you can delete it** (only if you are sure):

```
aws s3 rm --recursive s3://practice-$USER
aws s3 rb s3://practice-$USER
```

**Remember:** S3 buckets must be emptied before they can be removed. Once removed, the bucket name is available for other AWS customers.

### Access S3 using `boto3` in Python

The `boto3` package is the standard library enabling programmatic access to AWS using Python. `boto3` can access all AWS services and is helpful for creating, managing, or removing remote resources and infrastructure dynamically. The steps below refer to using `boto3` for working with files in S3.

#### Set up a Python environment for the scripts

The numbered scripts (`01-make-bucket.py` ... `09-delete-bucket.py`) are in the `class/06-s3` folder of your fork of the DS2022 course repo. You run them right there, inside a virtual environment that has `boto3` installed.

**1. Change into the** `06-s3` **folder of your fork**

```bash
cd <path_to_your_cloned_fork_of_DS2022_repo>/class/06-s3
ls
```

You should see the numbered `.py` scripts, `cloud.jpg`, and this `README.md`. If `class/06-s3` is missing, sync your fork with the course repo on GitHub (**Sync fork**), then `git pull`.

**2. Create a virtual environment**

```bash
uv venv
ls -la
```

This creates a `.venv/` folder in `class/06-s3` with its own Python interpreter and its own (still empty) set of packages. Anything you install goes into `.venv/`, not into your system Python or other projects.

> **Why** `uv venv` **and not** `uv init`**?** In [Lab 03](../03-scripting/README.md) you used `uv init` / `uv add`, which create a full project (`pyproject.toml`, `uv.lock`, `.venv/`). Here the scripts already belong to the course repo, so you only need the environment, not a new project. `.venv/` is listed in the repo's `.gitignore`, so it is never committed.

**3. Install** `boto3` **into the environment**

```bash
uv pip install boto3
```

`uv pip install` installs into the `.venv/` in the current folder. `boto3` pulls in its own dependencies, such as `botocore` (the low-level AWS client that the `aws` CLI uses too) and `s3transfer`.

**4. Check the environment**

```bash
uv pip list
uv run python -c "import boto3; print(boto3.__version__)"
```

`uv pip list` shows the packages in `.venv/`. `uv run` finds the `.venv/` in the current folder and runs Python inside it, so you don't need to activate the environment with `source .venv/bin/activate`. The second command should print a version number such as `1.43.113`.

Alternatively, you can run:

```bash
source .venv/bin/activate
python -c "import boto3; print(boto3.__version__)"
```

This puts the Python interpreter of this virtual environment on your PATH, and now you can drop the `uv run` and simply call `python ...`.

If you get `ModuleNotFoundError: No module named 'boto3'`, you are probably in a different folder: `cd` back into `class/06-s3`, where `.venv/` is, and run the command again.

#### Use `boto3` - 00-check-aws-credentials.py

Once `~/.aws/credentials` and `~/.aws/config` are set up, `boto3` looks up credentials in `~/.aws/credentials` (and region settings in `~/.aws/config`). You do **not** need to pass keys into your code:

```python
import boto3

s3 = boto3.client('s3')
```

Test that `boto3` is installed and finds your credentials. From `class/06-s3`, run:

```bash
uv run python 00-check-aws-credentials.py
```

The script prints the `boto3` version and your region, then makes the same call as `aws sts get-caller-identity`. You should see something like this (your account and session name will differ):

```text
boto3 version: 1.43.113
Region: us-east-1
Found credentials in shared credentials file: ~/.aws/credentials
Account: 634666103374
Arn: arn:aws:sts::634666103374:assumed-role/voclabs/user5560460=Test_Student
```

If it reports no region, no credentials, or invalid/expired credentials, fix `~/.aws/config` or refresh `~/.aws/credentials` from **AWS Details** (see [AWS CLI configuration](#aws-cli-configuration-temporary-credentials)) and run the script again.

#### Optional: credentials via environment variables - 00-env-credentials.py

If `~/.aws/credentials` is missing (or you prefer not to use it), you can set credentials in the shell as environment variables and read them in the script. That keeps secrets out of the source file; never hardcode keys in clear text (see [best practices](../../best-practices.md)).

In the shell:

```bash
export AWS_ACCESS_KEY_ID="YOUR_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
export AWS_SESSION_TOKEN="YOUR_SESSION_TOKEN"
```

In Python:

```python
import os
import boto3

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
)
```

For class, prefer putting the AWS Details values (including session token) in `~/.aws/credentials`, then use plain `boto3.client('s3')`. Refresh those values when the ~4 hour session expires.

#### Python scripts

| Script                        | Purpose                                                                |
| ----------------------------- | ---------------------------------------------------------------------- |
| `00-check-aws-credentials.py` | Check `boto3` version, region, and credentials (`get_caller_identity`) |
| `00-env-credentials.py`       | Build S3 client from env vars (optional; default is `~/.aws`)          |
| `01-make-bucket.py`           | Create `practice-$USER`                                                |
| `02-list-buckets.py`          | List buckets                                                           |
| `03-download-object.py`       | Download `cloud.jpg` from `s3://ds2022-fall26/` (public read)          |
| `04-upload-object.py`         | Upload to `folder/in/bucket/cloud.jpg` (`ContentType=image/jpeg`)      |
| `05-list-objects.py`          | List objects in a bucket                                               |
| `06-presign.py`               | Presign `folder/in/bucket/cloud.jpg` (inline display)                  |
| `07-delete-object.py`         | Delete `folder/in/bucket/cloud.jpg`                                    |
| `08-delete-all-objects.py`    | Empty a bucket (recursive; optional cleanup)                           |
| `09-delete-bucket.py`         | Delete the bucket (optional; must be empty)                            |

The scripts are short top-to-bottom demos with no helper functions or `if __name__ == "__main__"` guards, so each file is easy to read in one pass. Prefer keeping `practice-$USER` for later weeks; treat `08` / `09` as optional cleanup. For labs and production code, follow the course [best practices](../../best-practices.md).

Inspect and run the scripts in numerical order. The following sections explain the key principles for the most used S3 operations.

#### Create a bucket - 01-make-bucket.py

```python
import boto3

bucket_name = "practice-mst3k"  # replace with your bucket name
s3 = boto3.client("s3", region_name="us-east-1")
# For most regions you pass CreateBucketConfiguration={"LocationConstraint": "region-name"}.
# us-east-1 is special: omit LocationConstraint or create_bucket will fail.
s3.create_bucket(Bucket=bucket_name)
```

#### List buckets - 02-list-buckets.py

```python
import boto3

s3 = boto3.client("s3")
response = s3.list_buckets()
for b in response.get("Buckets", []):
    print(b["Name"])
```

#### Download a file from S3 - 03-download-object.py

Download the shared `cloud.jpg` image from the public course bucket:

```python
import boto3
from botocore import UNSIGNED
from botocore.client import Config

bucket_name = "ds2022-fall26"
key = "cloud.jpg"
local_file = "cloud.jpg"
# Anonymous client: the boto3 version of --no-sign-request (ds2022-fall26 is public)
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

obj = s3.get_object(Bucket=bucket_name, Key=key)
# save the object, "wb" stands for write binary
with open(local_file, "wb") as f:
    f.write(obj["Body"].read())
```

#### Upload a file to S3 - 04-upload-object.py

```python
import boto3

bucket_name = "practice-mst3k"  # replace with your bucket name
local_file = "cloud.jpg"
key = "folder/in/bucket/cloud.jpg"  # 06-presign.py uses the same key

s3 = boto3.client("s3")
with open(local_file, "rb") as f:
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=f,
        ContentType="image/jpeg",
    )
```

#### List objects in a bucket - 05-list-objects.py

`Prefix` limits the listing to keys that start with a "folder" path; use `""` to list everything.

```python
import boto3

bucket_name = "practice-mst3k"  # replace with your bucket name
s3 = boto3.client("s3")
response = s3.list_objects_v2(Bucket=bucket_name, Prefix="folder/in/bucket/")
for obj in response.get("Contents", []):
    print(obj["Key"], obj["Size"])
```

`list_objects_v2` returns at most 1,000 keys per call. For larger buckets, use a paginator (see `08-delete-all-objects.py`).

#### Presign a URL - 06-presign.py

A presigned URL gives anyone who has the link temporary read access to a private object, without AWS credentials. The `ResponseContent*` parameters make the browser display the image instead of downloading it.

```python
import boto3

bucket_name = "practice-mst3k"  # replace with your bucket name
key = "folder/in/bucket/cloud.jpg"  # must exist in the bucket

s3 = boto3.client("s3")
url = s3.generate_presigned_url(
    "get_object",
    Params={
        "Bucket": bucket_name,
        "Key": key,
        "ResponseContentType": "image/jpeg",
        "ResponseContentDisposition": "inline",
    },
    ExpiresIn=600,  # seconds
)
print(url)
```

#### Delete files in S3 - 07-delete-object.py , 08-delete-all-objects.py

```python
import boto3

s3 = boto3.client("s3")
bucket_name = "practice-mst3k"  # replace with your bucket name
key = "folder/in/bucket/cloud.jpg"

s3.delete_object(Bucket=bucket_name, Key=key)
```

To remove every object (empty the bucket), page through the listing and delete each page in one `delete_objects` call (up to 1,000 keys per call):

```python
import boto3

bucket_name = "practice-mst3k"  # replace with your bucket name
s3 = boto3.client("s3")
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket=bucket_name):
    contents = page.get("Contents", [])
    if contents:
        s3.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": [{"Key": obj["Key"]} for obj in contents]},
        )
```

#### Delete a bucket - 09-delete-bucket.py

```python
import boto3

bucket_name = "practice-mst3k"  # replace with your bucket name
s3 = boto3.client("s3")
s3.delete_bucket(Bucket=bucket_name)
```

> **Note:** Optional cleanup only. Buckets must be empty before delete (`08-delete-all-objects.py`, then `09-delete-bucket.py`). Keep `practice-$USER` if you will reuse it later.

#### Catching boto exceptions

Most S3 errors show up as a `botocore.exceptions.ClientError`. For the simplest demos above, we omit error handling so you can focus on the API calls.

See the numbered scripts in this folder (listed under [Python scripts](#python-scripts)) for runnable examples, including `try` / `except ClientError` patterns.

### Instructor note: shared bucket `ds2022-fall26`

On the account that owns `ds2022-fall26`, teaching objects are **publicly readable** (not cross-account IAM):

- Allow `s3:GetObject` for `Principal: "*"` on `arn:aws:s3:::ds2022-fall26/*` (or only `cloud.jpg` and `data/*`).
- For `aws s3 sync .../data/`, also allow `s3:ListBucket` on the bucket with a prefix condition on `data/`.
- Adjust Block Public Access only as needed for this teaching bucket.
- Students must not have write access to `ds2022-fall26`.



## Advanced Concepts (Optional)



### Versioning + lifecycle policies

Example (lifecycle rules are configured as bucket lifecycle JSON). Common patterns:

- Delete incomplete multipart uploads after N days.
- Expire objects in a prefix after N days.
- Transition objects to cheaper storage classes after N days.



### S3 event notifications

Example (typical event-driven pipeline):

- S3 `ObjectCreated` event on a prefix (e.g., `book-analysis/`)
- Triggers one of: **Lambda**, **SQS**, or **SNS**
- Your handler reads the new object and runs processing



### Access logging & auditing

Examples:

- **CloudTrail data events** for S3: see who accessed which objects (read/write).
- **S3 server access logs**: deliver access logs to a separate logging bucket for analysis.



### Access control lists (ACLs)

An ACL is a per-object (or per-bucket) permission list: who can read or write that object. Newer accounts often have **Block Public Access** turned on, so public ACLs may be rejected until you change that setting (in class, prefer private objects + `presign` unless the lab asks for public access).

Upload with a canned ACL (example: public read):

```python
import boto3

bucket_name = "practice-mst3k"  # replace with your bucket name
s3 = boto3.client("s3")

with open("cloud.jpg", "rb") as f:
    s3.put_object(
        Bucket=bucket_name,
        Key="folder/in/bucket/cloud.jpg",
        Body=f,
        ContentType="image/jpeg",
        ACL="public-read",
    )
```

Change the ACL on an existing object:

```python
s3.put_object_acl(
    Bucket=bucket_name,
    Key="folder/in/bucket/cloud.jpg",
    ACL="private",
)
```

Common canned ACLs: `private`, `public-read`. For broader rules (whole prefix, many principals), use a **bucket policy** instead (see [IAM policies](../06-iam/README.md#policies)).

## Resources

- [AWS CLI - Getting started](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
- [Amazon S3 - Getting started](https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html)
- [Boto3 Documentation](https://docs.aws.amazon.com/boto3/latest/)
- [Boto3 and S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [IAM](../06-iam/README.md)

