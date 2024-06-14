# Role for lambda
resource "aws_iam_role" "lambda_role" {
  name               = "lambda_role"
  assume_role_policy = var.aws_iam_policy_document_json
}

# Attach permissions for lambda role
# Attach ExecutionRole
resource "aws_iam_role_policy_attachment" "asic_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
# Attach logging policy
resource "aws_iam_role_policy_attachment" "logging_policy_attach" {
  policy_arn = var.lambda_logging_policy_arn
  role       = aws_iam_role.lambda_role.name
}
# Attach cross account policy
resource "aws_iam_role_policy_attachment" "cross_account_policy_attach" {
  policy_arn = var.cross_account_policy_attach_arn
  role       = aws_iam_role.lambda_role.name
}


#----- Lambda resource
#Create zip file with code to upload lambda
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../../code/users/lambda_function.py"
  output_path = "${path.module}/lambda.zip"
}
#Lambda function
resource "aws_lambda_function" "user_lambda_function" {
  function_name    = "user_lambda_function"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.11"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  filename         = data.archive_file.lambda_zip.output_path
  timeout          = 30

  environment {
    variables = {
      ACCOUNT_ID = var.account_id_env
    }
  }
}
#Cloudwatch log group to list created images role
resource "aws_cloudwatch_log_group" "user_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.user_lambda_function.function_name}"
  retention_in_days = 1
}
