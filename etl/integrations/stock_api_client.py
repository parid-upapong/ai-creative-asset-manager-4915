import requests
import backoff
from abc import ABC, abstractmethod
from ..schemas.metadata import OptimizedMetadata

class StockAPIClient(ABC):
    @abstractmethod
    def upload_metadata(self, metadata: OptimizedMetadata):
        pass

class AdobeStockClient(StockAPIClient):
    def __init__(self, access_token: str, api_key: str):
        self.base_url = "https://stock.adobe.io/api/v1"
        self.headers = {
            "x-api-key": api_key,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=3)
    def upload_metadata(self, metadata: OptimizedMetadata):
        payload = {
            "external_id": metadata.asset_id,
            "title": metadata.title,
            "keywords": [{"name": k} for k in metadata.keywords],
            "category_id": metadata.categories[0]
        }
        response = requests.post(f"{self.base_url}/media/metadata", json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

class ShutterstockClient(StockAPIClient):
    # Implementation for Shutterstock API
    def upload_metadata(self, metadata: OptimizedMetadata):
        # Specific implementation for SS JSON structure
        pass