import boto3

# Initialize a session using your preferred region
ec2_client = boto3.client('ec2',aws_access_key_id = "", aws_secret_access_key =  ,region_name="ap-south-1")

# Specify your instance ID
instance_id = ''

# Retrieve instance information
response = ec2_client.describe_instances(InstanceIds=[instance_id])

# Extract the public IP address
public_ip = response['Reservations'][0]['Instances'][0].get('PublicIpAddress')

if public_ip:
    print(f"Public IP Address: {public_ip}")
else:
    print("The instance does not have a public IP address.")

