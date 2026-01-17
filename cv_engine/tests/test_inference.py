import pytest
from PIL import Image
import torch
from models.tagging_engine import AutoTagger

def test_model_initialization():
    tagger = AutoTagger()
    assert tagger.model is not None
    assert tagger.device in ["cuda", "cpu"]

def test_tag_generation():
    tagger = AutoTagger()
    # Create a dummy white image
    img = Image.new('RGB', (224, 224), color = (255, 255, 255))
    tags = tagger.generate_tags(img)
    
    assert isinstance(tags, list)
    # Even a blank image should return low probability labels or empty list
    # but the function should not crash.