# IAM Role for AI Workers to access S3 and Rekognition
resource "aws_iam_role" "ai_worker_role" {
  name = "CreatorNexusAIWorkerRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "asset_access" {
  name        = "CreatorNexusAssetAccess"
  description = "Allows AI workers to read/write to the asset bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "${aws_s3_bucket.assets.arn}",
          "${aws_s3_bucket.assets.arn}/*"
        ]
      },
      {
        Action = [
            "kms:Decrypt",
            "kms:GenerateDataKey"
        ]
        Effect = "Allow"
        Resource = "${aws_kms_key.s3_key.arn}"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ai_worker_s3_attach" {
  role       = aws_iam_role.ai_worker_role.name
  policy_arn = aws_iam_policy.asset_access.arn
}