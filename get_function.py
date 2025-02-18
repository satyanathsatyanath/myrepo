import boto3

# Create a Lambda client
lambda_client = boto3.client('lambda',aws_access_key_id="",aws_secret_access_key="")


# List Lambda functions
response = lambda_client.list_functions()
c=0
for function in response['Functions']:
    # print(f"Function Name: {function['FunctionName']}")
    print(f"Function Name: {function['FunctionName']}")
    # Get Function URL (if configured)
    try:
        url_response = lambda_client.get_function_url_config(FunctionName=function['FunctionName'])
        # if url_response['FunctionUrl']=="https://cmcg5jiuceexlmavzmklw5z2ly0guuoi.lambda-url.ap-south-1.on.aws/":    
        # print(f"Function URL: {url_response['FunctionUrl']}")
        # print(f"Function Name: {function['FunctionName']}")
        c+=1
            # break
    except lambda_client.exceptions.ResourceNotFoundException:
        # print("Function URL: Not configured")
        pass
    print(c)
    # Access the Execution Role
    # execution_role = function['Role']
    # print(f"Execution Role ARN: {execution_role}")
    
    # print('-' * 60)
