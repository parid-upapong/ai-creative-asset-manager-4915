from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class AssetBase(BaseModel):
    file_name: str
    file_type: str

class AssetCreate(AssetBase):
    user_id: UUID4

class AssetResponse(AssetBase):
    asset_id: UUID4
    status: str
    storage_path: str
    created_at: datetime

    class Config:
        from_attributes = True

class TaskStatus(BaseModel):
    asset_id: UUID4
    stage: str # 'ingesting', 'tagging', 'optimizing', 'ready'
    progress: float
    message: Optional[str] = None