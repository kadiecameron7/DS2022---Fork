# AWS IAM

This week you learn how access control works in AWS. **IAM** defines users, roles, and policies that control who can use which services. Without that model, you cannot safely launch EC2 virtual machines, attach storage, or invoke serverless functions later in the course.

**You will complete the AWS Academy IAM lab** and (optionally) dig into policies, STS temporary credentials, and named profiles.

These skills are the foundation for [S3](../06-s3/README.md), `Lab 6`, and the upcoming weeks on **EC2 virtual machines** and **serverless compute**.


## In-class exercises

### Step 1: Log into AWS Academy

1. You should have received an email to your UVA account with an invitation to the AWS Academy Cloud Foundations course.
2. If you haven't done so yet, follow the [AWS Academy account setup](../../setup/aws_academy.md) instructions to get your account ready.

### Step 2: Review AWS Academy lab instruction

1. On the AWS Academy Canvas page, navigate to the `DS2022 - AWS Cloud Foundations` course > `Modules` > `Introduction` and review the `How to complete lab exercises` instructions.

### Step 3: Complete **Lab: Introduction to AWS IAM**

1. On the AWS Academy Canvas page, navigate to `Modules` > `Module 4` > `Lab - 1 Introduction to AWS IAM`
2. Follow the lab instructions. When you click **Start Lab**, wait until the AWS indicator light turns green.
3. Click on the AWS link when the indicator turns green. A new browser tab should open with the `AWS Management Console`.
  ![AWS Management Console via AWS Academy](../../docs/images/aws-academy-console.png)
4. **Submit your work in AWS Academy.** This work contributes to this week's Lab 06 (see Canvas)
5. End the AWS Academy lab.


## Advanced Concepts (Optional)


### Policies

Example (bucket policy that allows read-only access to everything in a bucket):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
    }
  ]
}
```

Example (least-privilege IAM policy that only allows uploads to one prefix):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/book-analysis/*"
    }
  ]
}
```



### AWS STS + temporary credentials

Example (conceptual flow):

- Create a role with an S3 policy attached.
- Call `sts:AssumeRole` to get temporary credentials.
- Use those temporary credentials in the AWS CLI or `boto3` instead of long-lived access keys.

**AWS CLI (one-off)** `assume-role`

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/YOUR_ROLE_NAME \
  --role-session-name ds2022-session
```

The JSON output includes `AccessKeyId`, `SecretAccessKey`, and `SessionToken`. Export those as environment variables (or paste into a new shell) to run further `aws` commands as that role.

**AWS CLI (profile that assumes a role)** (recommended)

Add to `~/.aws/config` (use your real account ID and role name; `source_profile` is the profile whose user may call `sts:AssumeRole`):

```text
[profile my-assumed-role]
role_arn = arn:aws:iam::123456789012:role/YOUR_ROLE_NAME
source_profile = default
region = us-east-1
```

Then:

```bash
aws s3 ls --profile my-assumed-role
```

The CLI calls STS for you when you use that profile.

**boto3 (explicit)** `assume_role`

```python
import boto3

sts = boto3.client("sts")
resp = sts.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/YOUR_ROLE_NAME",
    RoleSessionName="ds2022-session",
)
creds = resp["Credentials"]

s3 = boto3.client(
    "s3",
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"],
)
print(s3.list_buckets())
```

**boto3 (same as the CLI profile)**

If you defined `my-assumed-role` in `~/.aws/config` as above:

```python
import boto3

session = boto3.Session(profile_name="my-assumed-role")
s3 = session.client("s3")
print(s3.list_buckets())
```



### Multiple AWS profiles

You can keep credentials for several AWS accounts and users side by side using named profiles in `~/.aws/credentials` and `~/.aws/config`.

Example (`~/.aws/credentials`):

```text
[default]
aws_access_key_id = YOUR_DEFAULT_ACCESS_KEY
aws_secret_access_key = YOUR_DEFAULT_SECRET_KEY

[ds2022]
aws_access_key_id = YOUR_DS2022_ACCESS_KEY
aws_secret_access_key = YOUR_DS2022_SECRET_KEY
```

Example (`~/.aws/config`):

```text
[default]
region = us-east-1

[profile ds2022]
region = us-east-1
```

Use a specific profile with the AWS CLI:

```bash
aws s3 ls --profile ds2022
```

And in `boto3`:

```python
import boto3

session = boto3.Session(profile_name="ds2022")
s3 = session.client("s3")
print(s3.list_buckets())
```



## Resources

- [Amazon IAM - Getting started](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html)
- [AWS STS](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html)
- [AWS CLI - Getting started](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
- [Boto3 Documentation](https://docs.aws.amazon.com/boto3/latest/)
