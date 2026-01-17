# CreatorNexus AI: High-Volume Asset Processing Architecture

## 1. System Design Philosophy
The architecture is built on an **Event-Driven, Microservices-based** model designed to handle asynchronous, compute-intensive tasks without blocking the user interface. It prioritizes scalability, resilience, and cost-efficiency (using Serverless where possible).

## 2. Core Components
*   **Edge Gateway:** Handles global uploads via S3 Transfer Acceleration.
*   **Asset Ingestion Pipeline:** Decouples file uploads from processing using message queues (AWS SQS/RabbitMQ).
*   **AI Processing Cluster:** A specialized fleet of workers that orchestrate Vision AI, LLMs for metadata, and Style Analysis.
*   **Metadata Engine:** A hybrid storage approach using PostgreSQL (Relational) and OpenSearch (Full-text/Vector Search).
*   **Distribution Bridge:** Managed workers that handle OAuth2 and SFTP/API connections to major stock platforms.

## 3. Data Flow
1. **Upload:** User uploads raw/high-res assets to S3 (Standard-IA).
2. **Trigger:** S3 Event Notification triggers an `Ingestion Lambda`.
3. **Queue:** Task is pushed to the `Processing Queue`.
4. **Worker:** `AssetWorker` downloads the file, generates low-res proxies, and calls the `AI Orchestrator`.
5. **AI Logic:** 
    - Vision API identifies objects.
    - LLM generates SEO-optimized titles/keywords.
    - Upscaling/Watermarking (if required).
6. **Persistence:** Metadata stored in DB; Assets indexed in Search.
7. **Delivery:** Scheduled tasks push optimized assets to Adobe Stock, Shutterstock, etc.