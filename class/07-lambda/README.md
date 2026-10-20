# AWS Lambda and Lab 07

> [!CAUTION]
> **Do NOT click Reset in the AWS Academy Learner Lab unless your instructor tells you to.**
> Reset permanently deletes everything in your lab account (S3 buckets, EC2 instances, Lambda functions, ...) and cannot be undone. To pause, click **End Lab**: your resources stay and are back with the next **Start Lab**.

Today you start **[Lab 07: Analyze Books on Amazon EC2 and AWS Lambda](https://github.com/ksiller/lab-07-ec2-lambda)**. Get as far as you can in class, and finish the lab as homework. This page explains how Lab 07 builds on Labs 05 and 06, introduces the new pieces (Lambda, Chalice, Parameter Store, Atlas network access), and collects the links you need.

> [!IMPORTANT]
> `mst3k` is a placeholder. Replace it everywhere with your UVA computing ID, for example `public-mst3k` → `public-abc2de`. If your Lab 06 bucket has a different name, use that name.



## Learning objectives

**Virtual machines (EC2)**

- Understand what a virtual machine (VM) is
- Provision a VM in AWS (EC2) from the command line
- Connect to an EC2 instance with `ssh`
- Customize an EC2 instance at launch: install software and your own code with a startup script
- Understand the life cycle of an EC2 instance: launch, run, stop, terminate

**Serverless computing (AWS Lambda)**

- Understand what serverless computing is
- Know the use cases for a server (EC2) vs. serverless compute (AWS Lambda)
- Write a Chalice app that deploys a Lambda function:
  - How to write a Lambda function
  - How to trigger its execution (here: an upload to S3)
  - How to deploy it to AWS



## In-class plan


| Part | Activity                                                                                                       | Time   |
| ---- | -------------------------------------------------------------------------------------------------------------- | ------ |
| --   | Lecture: from Lab 06 to Lab 07, EC2 vs Lambda                                                                   | 20 min |
| 1    | Lab 07 **Setup**: fork and clone, `uv sync`, Learner Lab credentials, Atlas access list, Parameter Store, test on your computer | 25 min |
| 2    | Lab 07 **Part 1**: launch the EC2 instance and analyze all books                                                | 30 min |
| --   | Homework: finish Part 1, do **Part 2** (Lambda), and submit                                                    |        |





## How Lab 07 builds on earlier labs and classes

Lab 07 builds on:

- [Lab 05: NoSQL with MongoDB](https://github.com/ksiller/lab-05-nosql): your Atlas cluster stores the results
- [Lab 06: Working with S3](https://github.com/ksiller/lab-06-s3): your bucket holds the books
- [class/07-ec2](../07-ec2/README.md): launching instances and connecting with `ssh`
- this page: Lambda and Chalice

The labs form one pipeline. Each lab adds one step, and the data stays where the previous lab put it:

```text
Project Gutenberg website
  │  Lab 06: download each book once and store it in S3
  ▼
S3 bucket public-mst3k: the books                                 INPUT
  │
  ├─▶ Lab 07 Part 1   EC2 instance   analyze all books, once      ─┐
  ├─▶ Lab 07 Part 2   AWS Lambda     analyze each new upload      ─┤  write results
  └─▶ Lab 08          UVA HPC        add summary, genre, date     ─┤
                                                                   ▼
MongoDB Atlas gutenberg.books: one document per book              OUTPUT
  │  (your cluster from Lab 05)
  ▼
Lab 10   web API (Chalice): look up any book's results
```

Lab 09 packages the analysis as a container, so it runs the same way anywhere.

- **What you reuse from Lab 06 (the input):** the bucket `public-mst3k` with the 100 books. Lab 07 only reads it, and in Part 2 adds one new book. S3 is the cache: no lab downloads the books from Project Gutenberg again.
- **What Lab 06 left open:** nothing happens when a new book arrives in the bucket.
- **What is new (the compute):** in Lab 06 your computer did all the work. In Lab 07 the work runs in AWS: Part 1 analyzes all books on a machine you launch (EC2); Part 2 analyzes each new book as soon as it arrives, with a function AWS runs for you (Lambda).
- **What you reuse from Lab 05 (the output):** your MongoDB Atlas cluster, the `MONGODB_ATLAS_*` environment variables, and PyMongo. Lab 07 creates the database `gutenberg` with one document per book; Lab 08 adds fields to the same documents.

**What the Lab 07 analysis computes.** The Lab 07 repository provides the analysis code (`analyze.py`); you deploy and run it. For each book it stores the title, author, language, and Project Gutenberg release date from the file's header, plus the number of words, the number of distinct words, and their ratio. Each document also records every run: where it happened (`ec2:i-...`, `lambda:...`, or your computer) and when.

> **Coming up in Lab 08:** more comprehensive analytics on UVA HPC. AI models will read every book and add a summary, its genre, and an estimate of when it was first published to the same documents.

You are ready to start [Lab 07](https://github.com/ksiller/lab-07-ec2-lambda): open it and follow its steps from the top. Use the rest of this page as background and reference while you work.

If you get stuck, ask. Errors in Setup are the most common ones, and they block everything after.



## EC2 vs Lambda

You launched EC2 instances in [class/07-ec2](../07-ec2/README.md). Lambda is the other end of the scale:


|             | EC2 (Lab 07 Part 1)                               | Lambda (Lab 07 Part 2)                                                     |
| ----------- | ------------------------------------------------- | -------------------------------------------------------------------------- |
| You provide | a machine image, then your code                   | one Python function (the **handler**)                                      |
| Runs        | until you stop or terminate it                    | once per **event**, at most 15 min                                         |
| Started by  | you (`aws ec2 run-instances`)                     | an event: an S3 upload, a schedule, an HTTP request, a test, ...           |
| Scales      | you launch more instances                         | AWS runs one copy per event, many in parallel                              |
| You pay for | every hour it runs, busy or idle                  | the milliseconds your code runs                                            |
| Credentials | instance profile `LabInstanceProfile` → `LabRole` | execution role `LabRole`                                                   |
| State       | its disk keeps files                              | none between events (except a small `/tmp`); keep data in S3 or a database |
| Good fit    | long batch jobs, big dependencies, debugging over SSH | small independent tasks that arrive one at a time                       |


In Lab 07 the **same** `analyze.py` runs in both places. Each run appends where it happened (`ec2:i-...` or `lambda:...`) to the book's document, which is how you prove you completed both parts.



## New concepts in Lab 07

### User data: automatic configuration at boot time

A new instance starts from a machine image (AMI) that contains only the standard operating system, Ubuntu in our case. Your analysis needs more: `git` to get the code, and `uv` with Python to run it. You could log in after every launch and install everything by hand. That's cumbersome and unreliable. Instead, you can hand EC2 a shell script with the installation steps, and EC2 runs it for you. In AWS this script is called **user data**; in Lab 07 it is the file [bootstrap.sh](https://github.com/ksiller/lab-07-ec2-lambda/blob/main/bootstrap.sh).

When you launch an instance with `--user-data file://bootstrap.sh`, EC2 runs that script once, as the administrator (root), the first time the instance boots. Lab 07's script installs `git` and `uv` and downloads the lab repository, so the instance is ready when you log in. The script's output goes to `/var/log/cloud-init-output.log`, and `cloud-init status --wait` waits until the script has finished.

### Roles instead of keys

On your computer, AWS knows who you are from the keys in `~/.aws/credentials`. A machine or function running inside AWS gets its permissions differently: you attach a **role** to it, like a badge that says what it is allowed to do. In the Learner Lab, that role is called `LabRole`. Your code then reaches S3 and the other services without any keys, so you never copy your keys to a machine in AWS.

### SSM Parameter Store: secrets outside your code

On your computer, the Atlas URL, user, and password come from the `MONGODB_ATLAS_*` environment variables you set in Lab 05. EC2 and Lambda need them too, but they must not be in your repository. **AWS Systems Manager Parameter Store** keeps them in your AWS account. In Lab 07 you copy them there once:

```bash
aws ssm put-parameter --name /lab07/mongodb --type SecureString \
  --value "{\"url\": \"$MONGODB_ATLAS_URL\", \"user\": \"$MONGODB_ATLAS_USER\", \"password\": \"$MONGODB_ATLAS_PWD\"}"
```

On EC2 and Lambda, the code reads the value at run time with `boto3.client("ssm").get_parameter(Name="/lab07/mongodb", WithDecryption=True)`, using `LabRole`. `SecureString` stores the value encrypted.

### Atlas network access: allow any address

In Lab 05 your Atlas cluster accepted connections only from UVA addresses. An EC2 instance gets a new public address every time it starts, and a Lambda function has no fixed address at all. In Lab 07 you therefore add `0.0.0.0/0` ("allow access from anywhere") to the cluster's **IP Access List**, and keep it for the rest of the semester: Lab 08 (HPC) and Lab 10 (an API built with Chalice) connect from changing addresses too. Your database user's password is then the only protection, so never commit it or share it.

### Lambda handlers: `event` and `context`

Every Python Lambda function has the same shape. Lambda calls it once per event:

```python
def handler(event, context):
    # event:   what happened, a dict parsed from JSON (for an S3 upload: bucket and key)
    # context: where it runs (request ID, time left before the timeout, ...)
    return {"message": "..."}   # sent back to the caller, if the caller waits
```

For an S3 upload, `event` looks like this (trimmed). The function only gets the bucket and the key; it downloads the book itself:

```json
{
  "Records": [
    {
      "eventName": "ObjectCreated:Put",
      "s3": {
        "bucket": {
          "name": "public-mst3k"
        },
        "object": {
          "key": "pg74.txt",
          "size": 421884
        }
      }
    }
  ]
}
```

`print` and logging output goes to **CloudWatch Logs**, one log group per function: `/aws/lambda/<function name>`. The first call of a new function is a **cold start**: Lambda starts an environment and imports your code. Later calls reuse it (**warm**) and are faster.

### S3 event notifications

An S3 bucket can notify a Lambda function when objects are created or deleted. The notification can be filtered by prefix and suffix, for example only keys ending in `.txt`. Lab 07's function only writes to MongoDB, never back to the bucket. A function that writes into the bucket it listens to can trigger itself in an endless loop, so such functions need a filter that excludes their own output.

The first notification on a bucket can take several minutes to become active. If your first upload does nothing, wait and upload again.

### Chalice and decorators

[AWS Chalice](https://aws.github.io/chalice/) is a Python framework that makes it extremely easy to write Lambda functions in Python that listen to S3 events, for example when a new file has been uploaded to a bucket or deleted from it. You write an ordinary Python function in `app.py` and mark it with a **decorator** that names the bucket and the events it listens to. `chalice deploy` then packages the code, creates the Lambda function, and sets up the S3 event notification for you.

**What is a decorator?** A line starting with `@` directly above a `def`. It wraps other code around your function, which can add behavior before or after your function runs. Think of a sticky note on a letter: the letter (your function) stays the same, and the note says what should happen to it ("mail this to Alice").

Chalice's decorators do not change what your function does. They **register** it: they note *when* the function should run, and `chalice deploy` turns that note into AWS setup. This is the whole Lambda part of Lab 07 ([book-analyzer/app.py](https://github.com/ksiller/lab-07-ec2-lambda/blob/main/book-analyzer/app.py)):

```python
@app.on_s3_event(bucket=BUCKET, events=["s3:ObjectCreated:*"], suffix=".txt")   # when: a .txt file is uploaded
def analyze_new_book(event):                                                    # what: ordinary Python
    analyze_book(event.bucket, event.key)
```

You do not need to write decorators yourself. Remember three things: the `@` line goes directly above `def`, the function underneath is normal Python, and the decorator says when it runs.


| Decorator                       | Creates                                                    | Started by                          |
| ------------------------------- | ---------------------------------------------------------- | ----------------------------------- |
| `@app.on_s3_event(bucket=...)`  | a function, the S3 permission, and the bucket notification | an object upload (Lab 07)           |
| `@app.lambda_function()`        | a plain Lambda function                                    | `chalice invoke`, the console, code |
| `@app.route("/path")`           | an HTTP API and a function that answers it                 | an HTTP request (Lab 10)            |
| `@app.schedule("rate(1 hour)")` | a function and a schedule rule                             | the clock (Lab 10)                  |


> **IAM in the Learner Lab.** Chalice normally creates an IAM role for each app, but the Learner Lab does not let you create roles. Lab 07's `.chalice/config.json` therefore sets `"manage_iam_role": false` and uses the existing `LabRole`.



## Resources

**Lab 07 and earlier labs**

- [Lab 07: Analyze Books on Amazon EC2 and AWS Lambda](https://github.com/ksiller/lab-07-ec2-lambda)
- [Lab 06: S3](https://github.com/ksiller/lab-06-s3) and [Lab 05: NoSQL with MongoDB](https://github.com/ksiller/lab-05-nosql)
- [MongoDB Atlas setup](../../setup/mongodb.md) and [class/05-nosql](../05-nosql/): PyMongo examples
- [Atlas IP access list](https://www.mongodb.com/docs/atlas/security/ip-access-list/)
- [PyMongo: `update_one` with `$set`, `$push`, and `upsert`](https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.update_one)
- [class/07-ec2](../07-ec2/README.md): launching instances, SSH, `vockey`, `launch-wizard-1`
- [class/06-s3](../06-s3/README.md): Learner Lab, AWS CLI credentials, `boto3`

**EC2**

- [Run commands on your Linux instance at launch (user data)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
- [IAM roles for Amazon EC2 (instance profiles)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
- [Instance metadata (IMDSv2)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html): how `analyze.py` finds its instance ID

**Lambda and Chalice**

- [What is AWS Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Define a Lambda function handler in Python](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
- [Process Amazon S3 event notifications with Lambda](https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html)
- [Lambda quotas (timeout, memory, payload size)](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [AWS Chalice documentation](https://aws.github.io/chalice/) and [Chalice events (S3, schedules)](https://aws.github.io/chalice/topics/events.html)
- [Chalice configuration file (`.chalice/config.json`)](https://aws.github.io/chalice/topics/configfile.html)
- [Using AWS Lambda layers with AWS Chalice](https://aws.amazon.com/blogs/developer/using-aws-lambda-layers-with-aws-chalice/)

**Parameter Store**

- [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [boto3: `get_parameter`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameter.html)



## Troubleshooting

See [Troubleshooting in Lab 07](https://github.com/ksiller/lab-07-ec2-lambda#troubleshooting). The most common problems in class:

- `ExpiredToken`: paste a fresh block from **AWS Details** → **AWS CLI** into `~/.aws/credentials`.
- `NoSuchBucket`: the bucket name is not your Lab 06 bucket. Did you replace `mst3k`? Check the name in the **AWS Console** under **S3** → **General purpose buckets**, or with `aws s3 ls`.
- `Cannot read SSM parameter /lab07/mongodb`: Setup step 5 of the lab is missing.
- `ServerSelectionTimeoutError` everywhere: your Atlas cluster is paused. In Atlas, open **Database** → **Clusters**, click **Resume**, and wait a few minutes.
- `ServerSelectionTimeoutError` on EC2 or in Lambda only: `0.0.0.0/0` is missing from the Atlas IP access list (Setup step 4).
- `Authentication failed`: the user or password in `/lab07/mongodb` does not match your Atlas database user.
- `ssh` hangs or `InvalidGroup.NotFound`: see [class/07-ec2 Troubleshooting](../07-ec2/README.md#troubleshooting).
