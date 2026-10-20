# AWS EC2 Compute

> [!CAUTION]
> **Do NOT click Reset in the AWS Academy Learner Lab unless your instructor tells you to.**
> Reset permanently deletes everything in your lab account (S3 buckets, EC2 instances, Lambda functions, ...) and cannot be undone. To pause, click **End Lab**: your resources stay and are back with the next **Start Lab**.

This session introduces **Amazon EC2**, virtual machines you rent by the hour. Building on [S3](../06-s3/README.md), you will:

- recap the `boto3` S3 scripts and see the same buckets in the AWS Console
- launch an EC2 instance in the AWS Console and connect to it with SSH
- launch a second instance from the command line with `aws ec2 run-instances`
- terminate both instances

> All exercises use the **AWS Academy Learner Lab** and the AWS CLI / `boto3` setup from [S3](../06-s3/README.md).

**Where you work.** Each step says where to do it:

- **Learner Lab page**: the AWS Academy page in your browser with **Start Lab**, **End Lab** and **AWS Details**.
- **AWS Console**: the AWS web interface in your browser, opened from the green **AWS** icon on the Learner Lab page.
- **Terminal on your computer**: your Mac Terminal or WSL shell. The `aws` CLI, the Python scripts and `ssh` run here.
- **Shell on the instance**: the remote Linux shell you get after `ssh` connects. The prompt changes to `ubuntu@ip-...`. Type `exit` to return to the terminal on your computer.



## In-class exercises


| Part | Activity                                        | Time   |
| ---- | ----------------------------------------------- | ------ |
| 1    | Recap: S3 from Python                           | 15 min |
| 2    | S3 in the AWS Console                           | 5 min  |
| --   | Lecture intro to EC2                            | 20 min |
| 3    | Launch an EC2 instance in the AWS Console + SSH | 15 min |
| 4    | Launch an EC2 instance from the CLI + clean up  | 20 min |




### Before you start

You need the `aws` CLI in the **terminal on your computer**. If `aws --version` fails, install it first: see [Environment (class/06-s3)](../06-s3/README.md#environment).

1. On the **Learner Lab page**, click **Start Lab** and wait for the green **AWS** icon. See [Start the AWS Academy Learner Lab (class/06-s3)](../06-s3/README.md#start-the-aws-academy-learner-lab).
2. On the **Learner Lab page**, click **AWS Details** (top right) → **AWS CLI** → **Show**. Copy the block into `~/.aws/credentials` on your computer (credentials change with every lab session).
   - **Quick tip:** In Cursor, open a chat window and enter this prompt: "open ~/.aws/credentials, create a new file if it doesn't exist". Paste your credentials. **Save the file!**
3. On the **Learner Lab page**, click **AWS Details** → **SSH key** → **Download PEM**. Your browser downloads `labsuser.pem`, the private key of the `vockey` key pair that already exists in your lab account. Next, move it into `~/.ssh` on your computer and use `chmod` to make it read-only for you (permission: 400).

   Open a **terminal on your computer**. Then,

   **Mac:**

   ```bash
   mkdir -p ~/.ssh
   mv ~/Downloads/labsuser.pem ~/.ssh/
   chmod 400 ~/.ssh/labsuser.pem
   ```

   **WSL:** the browser saves the file in your Windows `Downloads` folder, which WSL sees under `/mnt/c/Users/<windows-user>/`. Replace `<windows-user>` with your Windows user name:

   ```bash
   mkdir -p ~/.ssh
   mv /mnt/c/Users/<windows-user>/Downloads/labsuser.pem ~/.ssh/
   chmod 400 ~/.ssh/labsuser.pem
   ```

   The key must live inside WSL (`~/.ssh`): `chmod` has no effect on files under `/mnt/c`, and `ssh` refuses keys that other users can read.

   If `mv` reports `No such file or directory`, your browser saved the file somewhere else (for example a OneDrive folder) or under another name (for example `labsuser (1).pem`). Open the browser's downloads list, choose **Show in folder**, and use that path and file name instead. Put it in quotes if it contains spaces.



### 1. Recap: S3 from Python (15 min)

In the **terminal on your computer**, run two scripts from **[class/06-s3](../06-s3/)**. First go to that folder:

```bash
cd <path_to_your_cloned_fork_of_DS2022_repo>/class/06-s3
```

The folder should have the `.venv` with `boto3` from our last class session. If not, this command creates it:

```bash
uv venv && uv pip install boto3
```

Then run the scripts:

```bash
uv run python 00-check-aws-credentials.py   # same as: aws sts get-caller-identity
```

```bash
uv run python 01-make-bucket.py             # creates practice-$USER (no error if you already own it)
```

Python scripts, the `aws` command, and the AWS Console are three ways to do the same things in AWS.

### 2. S3 in the AWS Console (5 min)

1. On the **Learner Lab page**, click the green **AWS** icon to open the **AWS Console**.
2. In the **AWS Console**, search for **S3** in the top search bar and open it.
3. Find `practice-<your user name>` in the list of **General purpose buckets**. This is the bucket the script created (now or last session).
4. Open the bucket and check the tabs **Objects**, **Properties** (region, creation date) and **Permissions** (**Block public access** is on).
5. Optional: In the **AWS Console**, **Upload** a small file. Then list it from the **terminal on your computer**:

   ```bash
   aws s3 ls s3://practice-$USER/
   ```

---



### 3. Launch an EC2 instance in the AWS Console + SSH (15 min)

Steps 1–4 happen in the **AWS Console**. Make sure the region in the top right corner of the console is **N. Virginia (us-east-1)**, the same region as in `~/.aws/config` on your computer.

1. In the **AWS Console**, search for **EC2** and open it. Click **Launch instance**.
2. Fill in the form; leave everything else at its default:

   | Setting                       | Value                                                                      |
   | ----------------------------- | -------------------------------------------------------------------------- |
   | **Name**                      | `ec2-console`                                                              |
   | **Application and OS Images** | **Ubuntu**, *Ubuntu Server 26.04 LTS* (Free tier eligible)                 |
   | **Instance type**             | `t3.micro`                                                                 |
   | **Key pair (login)**          | `vockey`                                                                   |
   | **Network settings**          | **Create security group**, **Allow SSH traffic from** *Anywhere* (default) |
   | **Configure storage**         | 8 GiB gp3 (default)                                                        |
   | **File systems**              | None (default)                                                             |

3. Click **Launch instance**, then **View all instances** at the bottom of the screen.
4. Check the box in front of `ec2-console` (if you have more than one, pick the one you just launched). Wait until **Instance state** is *Running* (1-2 min); click the refresh button to update. On the **Details** tab, find the **Instance ID**, **Public IPv4 address** and **AMI ID**. On the **Security** tab, find the security group `launch-wizard-1`.
5. In the **AWS Console**, copy the **Public IPv4 address** to your clipboard. In the **terminal on your computer**, connect to the instance (replace `<public-ip>` with that address):

   ```bash
   ssh -i ~/.ssh/labsuser.pem ubuntu@<public-ip>
   ```

   Type `yes` to trust the host key on first connect. Ubuntu AMIs use the user name `ubuntu` (Amazon Linux uses `ec2-user`). Once connected, the prompt changes to `ubuntu@ip-...`: you are now in the **shell on the instance**.
6. In the **shell on the instance**, run the following commands to explore your instance:

   ```bash
   hostname
   whoami
   nproc          # number of CPUs
   free -h        # memory
   df -h /        # disk
   ```

   Then log out, which returns you to the **terminal on your computer**:

   ```bash
   exit
   ```

If `ssh` fails, see [Troubleshooting](#troubleshooting).

Leave the instance running; part 4 reuses its security group.

### 4. Launch an EC2 instance from the CLI + clean up (20 min)

Run all commands in this part in the **terminal on your computer**, except where a step says **shell on the instance**. The `aws` CLI on your computer has your lab credentials; the instance does not. Use one terminal window for the whole part: the shell variables `$IID` and `$IP` exist only in the terminal where you set them.

`aws ec2 run-instances` takes the same choices you made in the console form, as options:

- **AMI:** `ami-0b6d9d3d33ba97d99` is *Ubuntu Server 26.04 LTS* in us-east-1, the same image the console used in part 3. To confirm, in the **AWS Console** select `ec2-console` and compare its **AMI ID** on the **Details** tab.
- **Key pair:** `vockey` is the key pair that AWS Academy provides in your Learner Lab account. Its private key is the `labsuser.pem` you downloaded from **AWS Details**, so the same `ssh -i ~/.ssh/labsuser.pem` command works for every instance launched with `--key-name vockey`.
- **Security group:** `launch-wizard-1` is the security group the console created in part 3. When you launch more instances, reuse it: in the console form, choose **Select existing security group** → `launch-wizard-1`; on the CLI, pass `--security-groups launch-wizard-1`. Each time you pick **Create security group** instead, the console creates a new group with the next suffix (`launch-wizard-2`, `launch-wizard-3`, ...).

**Launch the instance**

```bash
IID=$(aws ec2 run-instances \
  --image-id ami-0b6d9d3d33ba97d99 \
  --instance-type t3.micro \
  --key-name vockey \
  --security-groups launch-wizard-1 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ec2-cli}]' \
  --query 'Instances[0].InstanceId' --output text)
echo "Instance ID: $IID"
```

`--tag-specifications` sets the instance name, `ec2-cli`, so you can tell it apart from `ec2-console`.
`--query` picks fields out of the JSON response (try the command without `--query` and `--output text` to see the full response).

| Option                 | Console field                     |
| ---------------------- | --------------------------------- |
| `--image-id`           | Application and OS Images (AMI)   |
| `--instance-type`      | Instance type                     |
| `--key-name`           | Key pair (login)                  |
| `--security-groups`    | Network settings → security group |
| `--tag-specifications` | Name                              |


Without `--subnet-id`, AWS picks a subnet in the default VPC, which is how the console launched `ec2-console` as well.

> **Optional:** [01-launch-ec2-cli.sh](01-launch-ec2-cli.sh) does the same launch, and also works if you skipped part 3: it reuses `launch-wizard-1`, or creates it with SSH allowed if it does not exist. It then waits for the instance and prints the `ssh` command. Run it in the **terminal on your computer** with `bash 01-launch-ec2-cli.sh`.

**Wait for it and connect**

```bash
aws ec2 wait instance-running --instance-ids $IID
IP=$(aws ec2 describe-instances --instance-ids $IID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo $IP
ssh -i ~/.ssh/labsuser.pem ubuntu@$IP
```

`wait instance-running` returns once the instance is running, but SSH may refuse connections for another 30 seconds while it boots. Retry if needed. In the **shell on the instance**, run `hostname`, then `exit` to return to the **terminal on your computer**.

In the **AWS Console**, refresh **EC2 → Instances**: `ec2-console` and `ec2-cli` are listed side by side.

Back in the **terminal on your computer**, list all your instances:

```bash
aws ec2 describe-instances
```

The output is a bit overwhelming.

Let's reduce this info to instance name, instance id, state, and public IP address, and format it as a table:

```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].[Tags[?Key==`Name`]|[0].Value,InstanceId,State.Name,PublicIpAddress]' \
  --output table
```

> **Optional:** [02-list-running-ec2-cli.sh](02-list-running-ec2-cli.sh) shows only the *running* instances (name, instance ID, type and public IP). Run it in the **terminal on your computer** with `bash 02-list-running-ec2-cli.sh`.

**Optional: set up an instance at boot with user data**

A new instance has only the plain Ubuntu operating system. Instead of logging in and installing software by hand, you can give EC2 a shell script, called **user data**. EC2 runs it once, as root, the first time the instance boots. [user_data.sh](user_data.sh) is a simple example:

```bash
#!/bin/bash

# 1. Update the package list
apt-get update -y

# 2. Install Git, cURL, and Python 3 without asking for confirmation
apt-get install -y git curl python3

# 3. Install uv
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# 4. Create a project directory and clone a repository into it
mkdir -p /home/ubuntu/code
git clone https://github.com/ksiller/DS2022.git /home/ubuntu/code/DS2022

# 5. Optional: Fix permissions so the 'ubuntu' user owns the cloned files
chown -R ubuntu:ubuntu /home/ubuntu/code
```

[04-launch-ec2-user-data-cli.sh](04-launch-ec2-user-data-cli.sh) launches `ec2-user-data` with the same options as above, plus `--user-data file://user_data.sh`. In the **terminal on your computer**, run:

```bash
cd <path_to_your_cloned_fork_of_DS2022_repo>/class/07-ec2
bash 04-launch-ec2-user-data-cli.sh
```

Connect with the `ssh` command the script prints. In the **shell on the instance**, wait for user data to finish, then check the result:

```bash
cloud-init status --wait     # prints status: done when user data has finished
ls ~/code/DS2022
uv --version
```

If the status is `error`, read the end of `/var/log/cloud-init-output.log`: it has the output of every command in `user_data.sh`. Type `exit` to return to the **terminal on your computer**.

**Clean up**

In the **terminal on your computer**, terminate both instances (and `ec2-user-data`, if you launched it). Terminating is permanent: the instance and its disk are deleted.

Copy the instance ID of `ec2-console` (starts with `i-`) from the table above and replace `<ec2-console-id>` with it. `$IID` still holds the ID of `ec2-cli`. If you launched `ec2-cli` with `01-launch-ec2-cli.sh`, `$IID` is empty in your terminal: replace `$IID` with the ID of `ec2-cli` from the table as well.

```bash
aws ec2 terminate-instances --instance-ids $IID <ec2-console-id>
```

> **Optional:** [03-terminate-all-ec2-cli.sh](03-terminate-all-ec2-cli.sh) terminates **all** instances in your lab account at once, without asking. Run it in the **terminal on your computer** with `bash 03-terminate-all-ec2-cli.sh`.

Wait a minute, then run the `describe-instances` table command again: both instances show `shutting-down`, then `terminated`, and disappear from the list after about an hour. The **AWS Console** shows the same states under **EC2 → Instances** after a refresh.

> When the Learner Lab session ends, running instances are **stopped**, not terminated, and start again with your next **Start Lab**. Stopped and running instances use up your lab budget, so terminate instances you no longer need.

> [!WARNING]
> **Before you leave class: terminate ALL your EC2 instances.**
> Running and stopped instances keep using up your lab budget. In the **terminal on your computer**, run:
>
> ```bash
> cd <path_to_your_cloned_fork_of_DS2022_repo>/class/07-ec2
> bash 03-terminate-all-ec2-cli.sh
> ```
>
> Then click **End Lab** on the **Learner Lab page**.



## Resources

- [Launch an EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/LaunchingAndUsingInstances.html)
- [Amazon EC2 instance types](https://aws.amazon.com/ec2/instance-types)
- [AWS CLI reference: `ec2 run-instances`](https://docs.aws.amazon.com/cli/latest/reference/ec2/run-instances.html)
- [Filter AWS CLI output with `--query`](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html)
- [Amazon EC2 security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
- [Instance lifecycle (stop, start, terminate)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)



## Troubleshooting

`ExpiredToken` **or** `InvalidClientTokenId` **(terminal on your computer).** Your lab credentials changed. On the **Learner Lab page**, copy the new block from **AWS Details** → **AWS CLI** → **Show** into `~/.aws/credentials` on your computer.

`01-make-bucket.py`**:** `BucketAlreadyExists`**.** Another AWS account owns `practice-$USER`. Bucket names are global, so pick a different suffix for this one command: `USER=$USER-1 uv run python 01-make-bucket.py` creates `practice-<your user name>-1`. Use that name in part 2.

`ssh`**:** `UNPROTECTED PRIVATE KEY FILE` **(terminal on your computer).** The key is readable by other users. Run `chmod 400 ~/.ssh/labsuser.pem`. On WSL, the key must be in `~/.ssh`, not under `/mnt/c`.

`ssh`**:** `Permission denied (publickey)` **(terminal on your computer).** Check the key path, run `chmod 400 ~/.ssh/labsuser.pem`, and log in as `ubuntu`.

`ssh`**:** `Connection refused` **right after launch (terminal on your computer).** The instance is still booting, even when the **AWS Console** already shows *Running*. Wait 30 seconds and retry.

`ssh` **hangs or times out.** In the **AWS Console** (EC2 → Instances → select the instance → **Security** tab), check that the security group allows inbound SSH (port 22). Also check that you use the instance's current **Public IPv4 address** (it changes when the instance is stopped and started).

`Unable to locate credentials` **(shell on the instance).** You ran an `aws` command on the instance. Type `exit` and run it in the **terminal on your computer**.

`run-instances`**:** `InvalidGroup.NotFound` **(terminal on your computer).** Your security group has a different name. In the **AWS Console**, select `ec2-console` and check the name on the **Security** tab (e.g. `launch-wizard-2`), then use that name with `--security-groups`.

`echo $IID` **or** `echo $IP` **prints nothing.** You opened a new terminal window or tab, so the shell variables are gone. Run the commands that set them again in the same terminal.