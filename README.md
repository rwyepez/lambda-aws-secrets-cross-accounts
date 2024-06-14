
# Setup for AWS Lambda to Read Secrets from Another Account

This guide will help you create a role in the AWS account `999555333444` that allows a Lambda function in a different AWS account `123456789012` to assume this role and read secrets from AWS Secrets Manager.

For this example, replace with account numbers by your correct accounts:

| AWS Account      | Description                           |
|------------------|---------------------------------------|
| `999555333444`   | AWS account where secrets are created |
| `123456789012`   | AWS account where Lambda is created   |


## Steps

### 1. Create a Role in Account `999555333444`

1. **Login to the AWS Management Console in Account `999555333444`.**
2. **Navigate to the IAM (Identity and Access Management) Console.**
3. **Create a New Role:**
   - Click on "Roles" in the sidebar.
   - Click on "Create role".
   - Click "AWS account".
   - Choose "Another AWS account" as the type of trusted entity.
   - Enter the Account ID of the AWS account where your Lambda function is running.

4. **Attach Policies to the Role:**
   - Click "Next: Permissions".
   - Attach the `SecretsManagerReadWrite` policy to allow access to Secrets Manager. You can also create a custom policy with more specific permissions if needed.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "secretsmanager:GetSecretValue",
           "secretsmanager:DescribeSecret"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

5. **Add Trust Relationship:**
   - After attaching policies, click "Next: Tags", add tags if necessary, and then "Next: Review".
   - Provide a role name, e.g., `cross_role`, and click "Create role".
   - Go to the "Trust relationships" tab of the newly created role and click "Edit trust relationship".
   - Ensure the following trust policy is in place, replacing `123456789012` with the Account ID of the account where your Lambda function is running and `lambda_role` with Lambda's role:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::123456789012:role/lambda_role"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```

### 2. Verify the Lambda Role to Assume the Role Created Previously and Update the Account or Lambda Role if Necessary

- **Lambda Function IAM Role:**
  The IAM role associated with your Lambda function must have the `sts:AssumeRole` permission to assume the `cross_role` created in the other account. 

  Example policy to attach to the Lambda execution role:

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Resource": "arn:aws:iam::999555333444:role/cross_role"
      }
    ]
  }
  ```

