import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np

class AutoTagger:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        """
        Initializes the CLIP-based tagging engine. 
        CLIP is ideal for stock photography because it understands semantic 
        concepts without being limited to a fixed set of classes.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
        # Pre-defined high-value stock categories for zero-shot classification
        self.stock_categories = [
            "lifestyle", "business", "nature", "technology", "architecture",
            "healthcare", "travel", "food and drink", "abstract", "portrait",
            "minimalist", "sustainable", "diversity", "innovation", "wellness"
        ]

    def generate_tags(self, image: Image.Image, threshold: float = 0.2, top_k: int = 15):
        """
        Generates a list of relevant keywords/tags for the input image.
        Uses a hybrid approach:
        1. Zero-shot classification against stock categories.
        2. Feature embedding extraction for similarity-based tagging (Future Scope).
        """
        inputs = self.processor(
            text=self.stock_categories, 
            images=image, 
            return_tensors="pt", 
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]

        # Filter categories by threshold
        tags = [
            self.stock_categories[i] 
            for i, prob in enumerate(probs) if prob > threshold
        ]
        
        return tags

    def get_image_features(self, image: Image.Image):
        """
        Extracts high-dimensional vector embeddings for visual similarity search.
        Used for the 'Similar Assets' recommendation engine.
        """
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        return image_features.cpu().numpy().tolist()