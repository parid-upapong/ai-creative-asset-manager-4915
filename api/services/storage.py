import aiobotocore.session
from fastapi import UploadFile
from api.config import settings

class StorageService:
    def __init__(self):
        self.session = aiobotocore.session.get_session()

    async def upload_asset(self, file: UploadFile, asset_id: str) -> str:
        """Uploads raw asset to S3 and returns the path."""
        path = f"raw/{asset_id}/{file.filename}"
        async with self.session.create_client(
            's3', 
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID
        ) as client:
            await client.put_object(
                Bucket=settings.S3_BUCKET_ASSETS,
                Key=path,
                Body=await file.read(),
                ContentType=file.content_type
            )
        return f"s3://{settings.S3_BUCKET_ASSETS}/{path}"

storage_service = StorageService()