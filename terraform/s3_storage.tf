# Secure Asset Storage with Transfer Acceleration for Creators
resource "aws_kms_key" "s3_key" {
  description             = "KMS key for CreatorNexus AI Assets"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_s3_bucket" "assets" {
  bucket = "creator-nexus-assets-${var.environment}"
}

# Security Hardening: Block Public Access
resource "aws_s3_bucket_public_access_block" "assets_block" {
  bucket = aws_s3_bucket.assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Encryption at Rest
resource "aws_s3_bucket_server_side_encryption_configuration" "assets_encryption" {
  bucket = aws_s3_bucket.assets.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.s3_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# S3 Transfer Acceleration for Global Speed
resource "aws_s3_bucket_accelerate_configuration" "assets_accel" {
  bucket = aws_s3_bucket.assets.id
  status = "Enabled"
}