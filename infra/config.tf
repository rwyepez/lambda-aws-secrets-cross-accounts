terraform {
  backend "s3" {
    bucket = "testlambdary"
    key    = "resources/terraform.state"
    region = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.11.0"
    }
  }
}
