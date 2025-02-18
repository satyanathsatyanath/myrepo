This Documentation is explanation of how the AWS Lambda function interacts with an S3 bucket to trigger synchronization with an Amazon Kendra index.

---

# **AWS Lambda Function for Amazon Kendra Data Source Sync**

## **Overview**

This AWS Lambda function script is designed to automatically trigger a synchronization job for an Amazon Kendra data source whenever a file is uploaded to a specific folder in an S3 bucket. The S3 bucket folder acts as a trigger for the Lambda function, which then initiates a sync job to update the Kendra index with the new data.

## **Dependencies**

- **boto3**: AWS SDK for Python, used to interact with AWS services.
- **botocore.exceptions.ClientError**: Exception class for handling errors from AWS service calls.
- **json**: Standard library for JSON manipulation.

## **Prerequisites**

- AWS credentials (configured in your Lambda environment or through AWS IAM roles).
- `boto3` library installed. In Lambda, it should be included by default.
- An Amazon Kendra index and data source already configured.
- An S3 bucket with a folder named `test` that will trigger the Lambda function.

## **Lambda Function Script**

```python
import json
import boto3
from botocore.exceptions import ClientError

# Initialize Kendra client
kendra = boto3.client('kendra')

def lambda_handler(event, context):
    # Environment variables
    index_id = '0f28ab41-69c3700565'  # Replace with your Kendra index ID
    data_source_id = '0542437fc6fd78d43f'  # Replace with your Kendra data source ID
    
    # Check if the event is from the S3 bucket and the specific folder
    if 'Records' in event:
        for record in event['Records']:
            # Extract the S3 bucket name and object key
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            folder_name = 'test/'

            # Verify if the file is uploaded to the 'test' folder
            if object_key.startswith(folder_name):
                print(f"File {object_key} uploaded to the {folder_name} folder in bucket {bucket_name}.")
                
                # Start a sync job for the data source
                try:
                    sync_response = kendra.start_data_source_sync_job(
                        Id=data_source_id,
                        IndexId=index_id
                    )
                    print("Sync job started:", sync_response)
                except ClientError as e:
                    print(f"Error starting sync job: {e}")
                    return {
                        'statusCode': 500,
                        'body': json.dumps('Error starting sync job')
                    }
                
                return {
                    'statusCode': 200,
                    'body': json.dumps('Sync job started successfully')
                }
    
    return {
        'statusCode': 400,
        'body': json.dumps('Invalid event data')
    }
```

## **Explanation**

### **Triggering the Lambda Function**

- **S3 Bucket Event Trigger**: The Lambda function is triggered by events from an S3 bucket. Specifically, the Lambda function is invoked whenever a file is uploaded to a folder named `test` within the S3 bucket.

- **S3 Event Structure**: The `event` parameter in the Lambda function contains information about the S3 event, including details about the bucket and the uploaded object.

### **Lambda Function Workflow**

1. **Initialize the Kendra Client**
   - Create a Kendra client using `boto3.client()`.

   ```python
   kendra = boto3.client('kendra')
   ```

2. **Define Environment Variables**
   - Set the Kendra index ID and data source ID.

   ```python
   index_id = '0f28ab41-69c3700565'  # Replace with your Kendra index ID
   data_source_id = '0542437fc6fd78d43f'  # Replace with your Kendra data source ID
   ```

3. **Process the S3 Event**
   - Check if the event contains records and process each record to extract the S3 bucket name and object key.
   - Verify if the uploaded file is in the `test` folder.

   ```python
   if 'Records' in event:
       for record in event['Records']:
           bucket_name = record['s3']['bucket']['name']
           object_key = record['s3']['object']['key']
           folder_name = 'test/'

           if object_key.startswith(folder_name):
               print(f"File {object_key} uploaded to the {folder_name} folder in bucket {bucket_name}.")
   ```

4. **Start the Sync Job**
   - If the file is in the `test` folder, initiate a sync job for the Kendra data source.

   ```python
   try:
       sync_response = kendra.start_data_source_sync_job(
           Id=data_source_id,
           IndexId=index_id
       )
       print("Sync job started:", sync_response)
   ```

5. **Handle Errors and Return Responses**
   - Catch and handle any errors that occur during the sync job initiation.
   - Return appropriate HTTP status codes and messages based on the result of the sync job.

   ```python
   except ClientError as e:
       print(f"Error starting sync job: {e}")
       return {
           'statusCode': 500,
           'body': json.dumps('Error starting sync job')
       }

   return {
       'statusCode': 200,
       'body': json.dumps('Sync job started successfully')
   }
   ```

### **Notes**

- **AWS Credentials**: Ensure that your Lambda function has the necessary IAM role and permissions to interact with both Amazon S3 and Amazon Kendra.
- **Folder Name**: The script is configured to trigger synchronization only for files uploaded to the `test` folder. Adjust the folder name as needed.
- **Event Data**: The Lambda function assumes a standard S3 event structure. Ensure your S3 bucket is configured to send the correct event notifications to Lambda.

This documentation outlines how to set up an AWS Lambda function that automatically synchronizes an Amazon Kendra data source whenever a file is uploaded to a specific folder in an S3 bucket. Let me know if you need further details or modifications!
