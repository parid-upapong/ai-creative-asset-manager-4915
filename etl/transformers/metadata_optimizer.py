import openai
from typing import List
from ..schemas.metadata import AssetMetadata, OptimizedMetadata

class MetadataOptimizer:
    """
    Transforms raw AI-detected tags into SEO-optimized titles and descriptions
    tailored for global stock markets.
    """
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def generate_seo_metadata(self, metadata: AssetMetadata) -> OptimizedMetadata:
        tags_csv = ", ".join(metadata.raw_tags)
        
        prompt = f"""
        Act as a professional Stock Photography SEO Expert. 
        Analyze these tags: {tags_csv}.
        Create:
        1. A descriptive, commercial title (max 80 chars).
        2. A detailed description.
        3. 40 highly relevant keywords.
        
        Format as JSON.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        # In production, add error handling for JSON parsing
        refined = response.choices[0].message.content
        import json
        data = json.loads(refined)
        
        return OptimizedMetadata(
            asset_id=metadata.asset_id,
            title=data['title'],
            description=data['description'],
            keywords=data['keywords'],
            categories=[1, 7] # Mapping logic for stock categories
        )