# CreatorNexus AI: Metadata ETL Pipeline

## Overview
This module handles the data transformation layer between our Computer Vision engine and external Stock Market APIs (Adobe Stock, Shutterstock).

## Workflow
1.  **Ingestion**: Receives JSON payloads from the `cv_engine` containing raw semantic tags.
2.  **Transformation (SEO Layer)**: Uses GPT-4o to contextualize tags into professional titles and descriptions that follow stock industry best practices (keyword density, commercial appeal).
3.  **Validation**: Ensures metadata meets strict platform constraints (e.g., keyword counts, character limits).
4.  **Distribution**: Dispatches metadata to third-party APIs via high-concurrency clients with built-in retry logic (exponential backoff).

## Environment Variables Required
- `OPENAI_API_KEY`: For metadata optimization.
- `ADOBE_STOCK_API_KEY`: API credentials for Adobe Stock.
- `ADOBE_STOCK_ACCESS_TOKEN`: OAuth2 token for asset management.
- `SHUTTERSTOCK_API_TOKEN`: API credentials for Shutterstock.

## Scalability
The pipeline is designed to be stateless, allowing it to be wrapped in a Celery worker or AWS Lambda function to process thousands of assets in parallel.