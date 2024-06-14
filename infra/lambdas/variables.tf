variable "lambda_logging_policy_arn" {
  type        = string
  description = "lambda logging policy arn"
}

variable "aws_iam_policy_document_json" {
  type        = string
  description = "policy json"
}

variable "cross_account_policy_attach_arn" {
  type        = string
  description = "cross account policy arn"
}

variable "account_id_env" {
  type        = string
  description = "Account id environment variable"
}
