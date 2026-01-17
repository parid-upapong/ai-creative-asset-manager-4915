import pytest
from etl.schemas.metadata import OptimizedMetadata

def test_metadata_validation_success():
    """Validates that correct metadata passes the Pydantic schema."""
    valid_data = {
        "asset_id": "uuid-123",
        "title": "Sunset over Himalayan Peaks",
        "description": "A beautiful cinematic shot of a mountain range at golden hour.",
        "keywords": ["mountain", "sunset", "nature", "snow", "landscape"],
        "categories": [1, 5],
        "language": "en"
    }
    metadata = OptimizedMetadata(**valid_data)
    assert metadata.asset_id == "uuid-123"
    assert len(metadata.keywords) == 5

def test_metadata_validation_failure_short_keywords():
    """Ensures validation fails if fewer than 5 keywords are provided (Stock Agency Requirement)."""
    invalid_data = {
        "asset_id": "uuid-124",
        "title": "Invalid Asset",
        "description": "Too few keywords.",
        "keywords": ["test", "only"],
        "categories": [1],
        "language": "en"
    }
    with pytest.raises(ValueError):
        OptimizedMetadata(**invalid_data)