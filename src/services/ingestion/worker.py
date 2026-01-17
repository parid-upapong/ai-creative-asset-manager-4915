import boto3
import json
import logging
from typing import Dict
from ai_orchestrator import ProcessManager
from database import db_session
from models import Asset

# Initialize AWS Clients
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

class AssetIngestionWorker:
    """
    Consumes messages from SQS to process newly uploaded assets.
    Responsible for thumbnail generation and triggering AI workflows.
    """
    
    def __init__(self, queue_url: str):
        self.queue_url = queue_url
        self.ai_manager = ProcessManager()

    def start_polling(self):
        logging.info("Starting Asset Ingestion Worker...")
        while True:
            messages = sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=20
            )

            if 'Messages' in messages:
                for msg in messages['Messages']:
                    self.process_message(msg)

    def process_message(self, message: Dict):
        body = json.loads(message['Body'])
        # Extract S3 bucket and key from the event
        bucket = body['Records'][0]['s3']['bucket']['name']
        key = body['Records'][0]['s3']['object']['key']
        
        logging.info(f"Processing asset: {key}")

        try:
            # 1. Create DB Record (Pending State)
            asset = Asset(original_path=f"s3://{bucket}/{key}", status="processing")
            db_session.add(asset)
            db_session.commit()

            # 2. Trigger AI Metadata Generation
            metadata = self.ai_manager.analyze_asset(bucket, key)
            
            # 3. Update Record with AI Insights
            asset.tags = metadata['tags']
            asset.title = metadata['suggested_title']
            asset.status = "completed"
            db_session.commit()

            # 4. Cleanup SQS
            sqs.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])
            
        except Exception as e:
            logging.error(f"Error processing {key}: {str(e)}")
            db_session.rollback()

if __name__ == "__main__":
    worker = AssetIngestionWorker(queue_url="https://sqs.us-east-1.amazonaws.com/123/CreatorNexus-Upload-Queue")
    worker.start_polling()