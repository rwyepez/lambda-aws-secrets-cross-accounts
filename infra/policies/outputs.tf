output "aws_iam_policy_document_json" {
  value = data.aws_iam_policy_document.policy.json
}

output "lambda_logging_policy_arn" {
  value = aws_iam_policy.lambda_logging_policy.arn
}

output "cross_account_policy_attach_arn" {
  value = aws_iam_policy.cross_account_policy.arn
}
