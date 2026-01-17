terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # Recommended: Use S3 + DynamoDB for state locking in production
  # backend "s3" { ... }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "CreatorNexusAI"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}