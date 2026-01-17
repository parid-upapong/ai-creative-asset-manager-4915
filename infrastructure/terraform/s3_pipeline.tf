# Infrastructure as Code for Ingestion Pipeline

resource "aws_s3_bucket" "asset_storage" {
  bucket = "creatornexus-assets-prod"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.asset_storage.id

  queue {
    queue_arn     = aws_sqs_queue.ingestion_queue.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".jpg"
  }

  queue {
    queue_arn     = aws_sqs_queue.ingestion_queue.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".mp4"
  }
}

resource "aws_sqs_queue" "ingestion_queue" {
  name                      = "creatornexus-upload-queue"
  receive_wait_time_seconds = 20
  visibility_timeout_seconds = 300 # 5 mins for AI processing
}