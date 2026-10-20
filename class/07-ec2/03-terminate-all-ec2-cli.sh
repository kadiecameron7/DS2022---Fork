#!/bin/bash
# Terminate all EC2 instances in your lab account.
# Terminating is permanent: each instance and its disk are deleted.
# Run in the terminal on your computer: bash 03-terminate-all-ec2-cli.sh

set -euo pipefail

# IDs of all instances that are not terminated yet
# --filters keeps only instances that are not terminated yet
# --query picks the fields to show; InstanceId is the instance ID
IIDS=$(aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=pending,running,stopping,stopped" \
  --query 'Reservations[].Instances[].InstanceId' --output text)

if [ -z "$IIDS" ]; then
  echo "No instances to terminate."
  exit 0
fi

echo "Terminating: $IIDS"
aws ec2 terminate-instances --instance-ids $IIDS > /dev/null
