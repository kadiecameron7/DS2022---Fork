#!/bin/bash
# List all running EC2 instances in a table: name, instance ID, type and public IP.
# Run in the terminal on your computer: bash 02-list-running-ec2-cli.sh

set -euo pipefail

# --filters keeps only running instances (not pending, stopped or terminated)
# --query picks the fields to show; Tags[?Key==`Name`]|[0].Value is the instance name
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[Tags[?Key==`Name`]|[0].Value,InstanceId,InstanceType,PublicIpAddress]' \
  --output table
