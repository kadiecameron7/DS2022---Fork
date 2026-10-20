#!/bin/bash
# Launch the ec2-cli instance without hard-coding the security group ID.
# No other instance needs to exist: the security group is looked up by name
# (created if missing).
# Run in the terminal on your computer: bash 01-launch-ec2-cli.sh

set -euo pipefail

# Ubuntu Server 26.04 LTS in us-east-1, the same AMI the console uses
AMI=ami-0b6d9d3d33ba97d99

# Reuse the security group by name; --output text prints "None" if it does not exist
SG_NAME=launch-wizard-1
SG=$(aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=$SG_NAME" \
  --query 'SecurityGroups[0].GroupId' --output text)
if [ "$SG" = "None" ]; then
  # create a new security group "launch-wizard-1", same as console example
  SG=$(aws ec2 create-security-group \
    --group-name "$SG_NAME" \
    --description "SSH from anywhere" \
    --query 'GroupId' --output text)
  # allow SSH from anywhere
  aws ec2 authorize-security-group-ingress \
    --group-id "$SG" --protocol tcp --port 22 --cidr 0.0.0.0/0 > /dev/null
  echo "Created security group $SG_NAME"
fi
echo "AMI: $AMI"
echo "Security group: $SG  with name $SG_NAME"

# Launch ec2-cli
# aws ec2 run-instances returns information about the instance in JSON format
# --query 'Instances[0].InstanceId' picks the InstanceId field from the first instance in the response
IID=$(aws ec2 run-instances \
  --image-id "$AMI" \
  --instance-type t3.micro \
  --key-name vockey \
  --security-group-ids "$SG" \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ec2-cli}]' \
  --query 'Instances[0].InstanceId' --output text)
echo "Launched instance: $IID"

# Wait until it is running, then print its public IP
aws ec2 wait instance-running --instance-ids "$IID"
IP=$(aws ec2 describe-instances --instance-ids "$IID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "Running, public IP address: $IP. Connect with:"
echo "  ssh -i ~/.ssh/labsuser.pem ubuntu@$IP"
echo "Terminate with:"
echo "  aws ec2 terminate-instances --instance-ids $IID"
