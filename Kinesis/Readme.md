`README.md` file for creating, producing to, consuming from, and deleting an Amazon Kinesis Data Stream using `boto3`.

---

# **Amazon Kinesis Data Stream Operations with Boto3**

## **Overview**

This document provides a set of Python scripts to manage Amazon Kinesis Data Streams using the `boto3` library. The operations include creating a data stream, sending records to it, consuming records from it, and deleting it.

## **Dependencies**

- **boto3**: AWS SDK for Python, used to interact with AWS services.
- **json**: Standard library for JSON manipulation.

## **Prerequisites**

- AWS credentials (access key ID and secret access key).
- `boto3` library installed. Install it using `pip install boto3`.

## **1. Creating a Kinesis Data Stream**

```python
import boto3
import time

# Initialize the Kinesis client
aws_access_key_id = ''  # Replace with your AWS access key ID
aws_secret_access_key = ''  # Replace with your AWS secret access key
kinesis = boto3.client('kinesis',
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key,
                       region_name="us-east-1")

# Define the stream name
stream_name = 'test'

# Define the number of shards
shard_count = 1  # Adjust the number of shards based on your throughput needs

# Create the Kinesis Data Stream
response = kinesis.create_stream(
    StreamName=stream_name,
    ShardCount=shard_count
)

# Print the response from the create_stream call
print(f"Stream {stream_name} is being created.")

# Wait until the stream is active
while True:
    response = kinesis.describe_stream(StreamName=stream_name)
    stream_status = response['StreamDescription']['StreamStatus']
    print(f"Stream status: {stream_status}")

    if stream_status == 'ACTIVE':
        print(f"Stream {stream_name} is now active.")
        break
    time.sleep(5)
```

### **Explanation**

- Initializes a Kinesis client.
- Creates a Kinesis Data Stream with a specified number of shards.
- Waits until the stream is in the `ACTIVE` state.

## **2. Producing Records to a Kinesis Data Stream**

```python
import boto3
import json

# Initialize the Kinesis client
aws_access_key_id = ''  # Replace with your AWS access key ID
aws_secret_access_key = ''  # Replace with your AWS secret access key
kinesis = boto3.client('kinesis',
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key,
                       region_name="us-east-1")

# Define the stream name
stream_name = 'test'

# Prepare the data to send
metadata = {
    'key1': 'value1',
    'key2': 'value2'
}

# Send the data record to the stream
response = kinesis.put_record(
    StreamName=stream_name,
    Data=json.dumps(metadata).encode('utf-8'),
    PartitionKey='partitionkey'
)

# Print the response from the put_record call
print(response)
```

### **Explanation**

- Initializes a Kinesis client.
- Sends a record to the specified Kinesis Data Stream.
- Prints the response from the `put_record` call.

## **3. Consuming Records from a Kinesis Data Stream**

```python
import boto3

# Initialize the Kinesis client
aws_access_key_id = ''  # Replace with your AWS access key ID
aws_secret_access_key = ''  # Replace with your AWS secret access key
kinesis = boto3.client('kinesis',
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key,
                       region_name="us-east-1")

# Define the stream name
stream_name = 'test'

# Describe the stream to get shard information
response = kinesis.describe_stream(StreamName=stream_name)

# Print shard information
shards = response['StreamDescription']['Shards']
for shard in shards:
    print(f"Shard ID: {shard['ShardId']}")

# Get the Shard ID from the previous response
shard_id = shards[0]['ShardId']  # Example: selecting the first shard

# Get a shard iterator for the selected shard
shard_iterator_response = kinesis.get_shard_iterator(
    StreamName=stream_name,
    ShardId=shard_id,
    ShardIteratorType='TRIM_HORIZON'  # Options: 'LATEST', 'TRIM_HORIZON', 'AT_SEQUENCE_NUMBER', etc.
)

# Retrieve the shard iterator
shard_iterator = shard_iterator_response['ShardIterator']

# Get records using the shard iterator
records_response = kinesis.get_records(ShardIterator=shard_iterator, Limit=10)

# Print the retrieved records
for record in records_response['Records']:
    print(f"Partition Key: {record['PartitionKey']}")
    print(f"Data: {record['Data'].decode('utf-8')}")
    print(f"Sequence Number: {record['SequenceNumber']}\n")
```

### **Explanation**

- Initializes a Kinesis client.
- Retrieves shard information from the stream.
- Obtains a shard iterator for the selected shard.
- Retrieves and prints records from the stream.

## **4. Deleting a Kinesis Data Stream**

```python
import boto3

# Initialize the Kinesis client
aws_access_key_id = ''  # Replace with your AWS access key ID
aws_secret_access_key = ''  # Replace with your AWS secret access key
kinesis = boto3.client('kinesis',
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key,
                       region_name="us-east-1")

# Define the stream name
stream_name = 'test'

# Delete the Kinesis Data Stream
response = kinesis.delete_stream(StreamName=stream_name)
print(f"Stream {stream_name} is being deleted.")
```

### **Explanation**

- Initializes a Kinesis client.
- Deletes the specified Kinesis Data Stream.
- Prints a message indicating that the stream is being deleted.

---

This `README.md` file provides a comprehensive guide to managing Amazon Kinesis Data Streams with `boto3`. Adjust the placeholder values for AWS credentials and stream names as needed for your environment. Let me know if you need any further modifications!
