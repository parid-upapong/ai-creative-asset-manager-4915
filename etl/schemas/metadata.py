from pydantic import BaseModel, Field, validator
from typing import List, Optional

class AssetMetadata(BaseModel):
    asset_id: str
    raw_tags: List[str]
    confidence_scores: List[float]
    file_path: str
    file_type: str
    
class OptimizedMetadata(BaseModel):
    asset_id: str
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=2000)
    keywords: List[str] = Field(..., min_items=5, max_items=50)
    categories: List[int]
    language: str = "en"

    @validator('keywords')
    def validate_keywords(cls, v):
        # Stock agencies usually don't allow special characters in keywords
        return [k.lower().strip() for k in v if k.isalnum() or ' ' in k]

class StockPlatformConfig(BaseModel):
    platform_name: str
    api_key: str
    api_secret: Optional[str]
    upload_endpoint: str