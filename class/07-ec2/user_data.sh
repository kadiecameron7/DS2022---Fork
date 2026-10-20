#!/bin/bash
# EC2 user data: runs once, as root, the first time the instance boots.
# Used by 04-launch-ec2-user-data-cli.sh (--user-data file://user_data.sh)

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
