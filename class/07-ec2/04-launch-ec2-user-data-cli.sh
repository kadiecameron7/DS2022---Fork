#!/bin/bash
# Launch the ec2-user-data instance: same as 01-launch-ec2-cli.sh, plus user data.
# At first boot the instance runs user_data.sh: installs git, curl, Python 3 and uv,
# and clones the DS2022 repository into /home/ubuntu/code/DS2022.
# Needs the security group launch-wizard-1 (part 3, or run 01-launch-ec2-cli.sh once).
# Run in the terminal on your computer: bash 04-launch-ec2-user-data-cli.sh

set -euo pipefail

# Ubuntu Server 26.04 LTS in us-east-1, the same AMI the console uses
AMI=ami-0b6d9d3d33ba97d99

# Run this script from class/07-ec2, where user_data.sh is
USER_DATA="user_data.sh"

# Launch ec2-user-data
# --user-data file://... reads the script from your computer and hands it to the instance
IID=$(aws ec2 run-instances \
  --image-id "$AMI" \
  --instance-type t3.micro \
  --key-name vockey \
  --security-groups launch-wizard-1 \
  --user-data "file://$USER_DATA" \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ec2-user-data}]' \
  --query 'Instances[0].InstanceId' --output text)
echo "Launched instance: $IID"

# Wait until it is running, then print its public IP
aws ec2 wait instance-running --instance-ids "$IID"
IP=$(aws ec2 describe-instances --instance-ids "$IID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "Running, public IP address: $IP. Connect with:"
echo "  ssh -i ~/.ssh/labsuser.pem ubuntu@$IP"
echo "On the instance, wait for user data to finish with:"
echo "  cloud-init status --wait"
echo "Terminate with:"
echo "  aws ec2 terminate-instances --instance-ids $IID"
