import logging
from .transformers.metadata_optimizer import MetadataOptimizer
from .integrations.stock_api_client import AdobeStockClient
from .schemas.metadata import AssetMetadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetadataPipeline:
    def __init__(self, openai_key: str, adobe_creds: dict):
        self.optimizer = MetadataOptimizer(openai_key)
        self.adobe_client = AdobeStockClient(**adobe_creds)

    def process_asset(self, raw_data: dict):
        """
        Main ETL Workflow:
        1. Extract: Load raw tags from CV engine
        2. Transform: Use LLM to optimize for SEO
        3. Load: Push to Stock Platforms
        """
        try:
            # 1. Validation & Extraction
            asset_meta = AssetMetadata(**raw_data)
            logger.info(f"Starting ETL for Asset: {asset_meta.asset_id}")

            # 2. Transformation
            optimized = self.optimizer.generate_seo_metadata(asset_meta)
            logger.info(f"Metadata optimized for {asset_meta.asset_id}")

            # 3. Loading (Distribution)
            result = self.adobe_client.upload_metadata(optimized)
            logger.info(f"Successfully synced with Adobe Stock: {result.get('id')}")
            
            return {"status": "success", "asset_id": asset_meta.asset_id}

        except Exception as e:
            logger.error(f"Pipeline failed for asset {raw_data.get('asset_id')}: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage (simulating a message from SQS)
    mock_payload = {
        "asset_id": "nexus_9901",
        "raw_tags": ["mountain", "sunset", "lake", "reflection", "nature"],
        "confidence_scores": [0.98, 0.95, 0.88, 0.85, 0.99],
        "file_path": "s3://creator-nexus-assets/user_1/mountain.jpg",
        "file_type": "image/jpeg"
    }
    
    pipeline = MetadataPipeline(
        openai_key="sk-...", 
        adobe_creds={"access_token": "...", "api_key": "..."}
    )
    pipeline.process_asset(mock_payload)