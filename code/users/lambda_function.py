import boto3
import json
import logging

# Define response headers for HTTP responses
responseHeaders = {
    'Content-Type': 'application/json'
}

# Main function that handles the Lambda function execution
def lambda_handler(event, context):
    # Get the HTTP method from the incoming event
    http_method = event['httpMethod']
    path = event['path'] if 'path' in event else '/'
    print('Method: ', http_method, 'Path', path)

    if path == '/users':
        if http_method == 'GET':
            return read_secrets(responseHeaders)

# Function to read secrets and return a response
def read_secrets(responseHeaders):
    account_id = "999555333444"
    role_name = "cross_role"
    secrets_manager_client = assume_role(account_id, role_name)
    secret_value = secrets_manager_client.get_secret_value(SecretId='your/secret/name')
    print(secret_value)
    return {
        'statusCode': 200,
        'headers': responseHeaders,
        'body': json.dumps('success')
    }


def assume_role(account_id, role_name):
  try:
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName="AssumeRoleSession"
    )
    credentials = response['Credentials']
    return boto3.client(
        'secretsmanager',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
  except Exception as e:
    logging.error(f"Error obtaining AWS credentials: {e}")
    raise