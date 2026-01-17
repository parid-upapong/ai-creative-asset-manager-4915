from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Core API Settings
    PROJECT_NAME: str = "CreatorNexus AI API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/creatornexus"
    
    # AWS / Storage
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_ASSETS: str
    SQS_QUEUE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week

    class Config:
        env_file = ".env"

settings = Settings()