import json
import boto3
from api.config import settings

class TaskOrchestrator:
    def __init__(self):
        # Using sync client for quick SQS dispatch, can be made async
        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1'
        )

    def trigger_ai_pipeline(self, asset_id: str, s3_path: str):
        """
        Dispatches a message to the SQS queue to trigger the 
        CV Engine (tagging) and ETL Engine (optimization).
        """
        payload = {
            "version": "1.0",
            "asset_id": asset_id,
            "s3_path": s3_path,
            "tasks": ["tagging", "metadata_generation", "stock_readiness_check"]
        }
        
        self.sqs.send_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            MessageBody=json.dumps(payload),
            MessageAttributes={
                'MessageType': {
                    'DataType': 'String',
                    'StringValue': 'AssetProcessingRequest'
                }
            }
        )

orchestrator = TaskOrchestrator()