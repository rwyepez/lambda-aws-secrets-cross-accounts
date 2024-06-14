import boto3
import json
import logging
import os

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
    account_id = os.environ['ACCOUNT_ID']
    role_name = "cross_role"
    secrets_manager_client = assume_role(account_id, role_name, "secretsmanager")
    secret_response = secrets_manager_client.get_secret_value(SecretId='cpp/testry')
    print(secret_response)
    s3_client = assume_role(account_id, role_name, "s3")
    responseObjects = s3_client.list_objects_v2(Bucket="my_bucket", Prefix="any_prefix")
    print(responseObjects)
    return {
        'statusCode': 200,
        'headers': responseHeaders,
        'body': json.dumps('success')
    }

def assume_role(account_id, role_name, client_type):
    try:
        sts_client = boto3.client('sts')
        response = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
            RoleSessionName="AssumeRoleSession"
        )
        credentials = response['Credentials']

        if client_type not in ["s3", "secretsmanager"]:
            raise ValueError(f"Unsupported client type: {client_type}")

        return boto3.client(
            client_type,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    except Exception as e:
        logging.error(f"Error assuming role for account {account_id}, role {role_name}, client {client_type}: {e}")
        raise
