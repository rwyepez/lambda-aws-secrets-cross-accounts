
# Setup for AWS Lambda to Read Secrets and List Objects from S3 in Another Account

This guide will help you set up a role in AWS account `999555333444` that allows a Lambda function in a different AWS account `123456789012` to assume this role and read secrets from AWS Secrets Manager, as well as list objects in an S3 bucket.

Replace the placeholder account numbers with your actual accounts:

| AWS Account      | Description                                |
|------------------|--------------------------------------------|
| `999555333444`   | AWS account where secrets and bucket are created |
| `123456789012`   | AWS account where Lambda is created        |

## Steps

### 1. Update and Deploy the lambda in account 123456789012

1. **Create an S3 Bucket**:
   - You'll need an S3 bucket to handle Terraform state.
   - Make sure to create the bucket in the region where you want to deploy your resources.
   - Update bucket name in config.tf file

### Configure AWS CLI with credentials for account 123456789012

- Ensure your AWS CLI is configured correctly by running:
  ```bash
  aws configure
  ```

2. **Update the `values.tfvars` file:**
   Ensure the `values.tfvars` file includes the correct Account ID for where the AWS Secrets Manager and S3 bucket are created:

   ```hcl
   variable "aws_resources_account_id" {
     type        = string
     description = "Account ID where aws secrets manager and bucket are created"
   }
   ```

3. **Navigate to the `infra` directory:**
   ```bash
   cd infra
   ```

4. **Initialize and deploy the Terraform configuration:**
   - Initialize Terraform:
     ```bash
     terraform init
     ```
   - Plan the deployment:
     ```bash
     terraform plan -var-file="values.tfvars"
     ```
   - Apply the configuration:
     ```bash
     terraform apply -var-file="values.tfvars"
     ```

### 2. Create a Role in Account `999555333444`

1. **Log in to the AWS Management Console in Account `999555333444`.**
2. **Navigate to the IAM (Identity and Access Management) Console.**
3. **Create a New Role:**
   - Click on "Roles" in the sidebar.
   - Click on "Create role".
   - Select "AWS account".
   - Choose "Another AWS account" as the type of trusted entity.
   - Enter the Account ID `123456789012` where your Lambda function is running.

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

   - Attach the `AmazonS3ReadOnlyAccess` policy to allow access to S3. You can also create a custom policy with more specific permissions if needed.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:Get*",
           "s3:List*",
           "s3:Describe*",
           "s3-object-lambda:Get*",
           "s3-object-lambda:List*"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

5. **Add Trust Relationship:**
   - After attaching policies, click "Next". Provide a role name, e.g., `cross_role`, and click "Create role".
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

### 3. Verify the Lambda Role to Assume the Role Created Previously

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

### Test Events for AWS Lambda

To test AWS Lambda functions from the AWS console, you can use the following test events:

1. **Get Information (GET)**:
   ```json
   {
     "httpMethod": "GET",
     "path": "/users"
   }
   ```

This setup will enable your Lambda function in account `123456789012` to assume a role in account `999555333444` and access the necessary resources for reading secrets from Secrets Manager and listing objects in an S3 bucket.
