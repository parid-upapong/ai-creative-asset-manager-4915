variable "aws_region" {
  description = "AWS deployment region"
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (prod/staging/dev)"
  default     = "production"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}