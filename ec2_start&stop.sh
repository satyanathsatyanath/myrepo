#!/bin/bash
 


 
# Set the instance ID and region
INSTANCE_ID=""
REGION="ap-south-1"
 
# Check if the user provided a valid argument
if [ -z "$1" ]; then
  echo "Usage: $0 <start|stop>"
  exit 1
fi
 
ACTION=$1
 
# Python script for starting or stopping the instance
python3 <<EOF
import boto3
import sys
import time

# Configure boto3 to use the specified region
ec2 = boto3.client('ec2',aws_access_key_id = "", aws_secret_access_key = "" ,region_name="$REGION")
instance_id = "$INSTANCE_ID"
action = "$ACTION"
 
try:
    if action == "start":
        response = ec2.start_instances(InstanceIds=[instance_id])
        print(f"Starting instance {instance_id}: {response}")
        time.sleep(30)
        resp = ec2.describe_instances(InstanceIds=[instance_id])

        # Extract the public IP address
        public_ip = resp['Reservations'][0]['Instances'][0].get('PublicIpAddress')
        if public_ip:
            print(f"Public IP Address: {public_ip}")
        else:
            print("The instance does not have a public IP address.")
    elif action == "stop":
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping instance {instance_id}: {response}")
    else:
        print("Invalid action. Use 'start' or 'stop'.")
except Exception as e:
    print(f"Failed to {action} instance {instance_id}: {e}")
EOF
