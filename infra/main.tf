module "policies" {
  source = "./policies"
}

module "lambda" {
  source                          = "./lambdas"
  lambda_logging_policy_arn       = module.policies.lambda_logging_policy_arn
  aws_iam_policy_document_json    = module.policies.aws_iam_policy_document_json
  cross_account_policy_attach_arn = module.policies.cross_account_policy_attach_arn
}
