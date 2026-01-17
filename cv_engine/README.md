# Computer Vision Model Development: Auto-Tagging

## Overview
This module serves as the visual intelligence core of **CreatorNexus AI**. It leverages the CLIP (Contrastive Language-Image Pretraining) architecture to bridge the gap between visual pixels and semantic stock keywords.

## Technical Choices
1.  **Model:** `CLIP (ViT-B/32)`. Chosen for its superior zero-shot capabilities. Unlike traditional ResNet classifiers, CLIP can identify niche stock photography concepts (e.g., "Sustainability," "Remote Work") without specific retraining.
2.  **API Framework:** `FastAPI`. Provides high-performance asynchronous processing, crucial for high-volume asset ingestion pipelines.
3.  **Output:** 
    *   **Tags:** Semantic labels for SEO optimization on platforms like Adobe Stock.
    *   **Embeddings:** 512-dimensional vectors saved to a Vector Database (Pinecone/Milvus) for visual search and duplicate detection.

## Implementation Roadmap
*   [x] Basic Inference Pipeline.
*   [ ] Multi-modal enhancement (Integrating BLIP-2 for caption generation).
*   [ ] Fine-tuning on proprietary stock metadata dataset (Shutterstock/Getty API data).
*   [ ] Color Palette Extraction for stylistic filtering.

## Execution