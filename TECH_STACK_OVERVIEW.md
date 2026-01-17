# Suggested Tech Stack for CreatorNexus AI

*   **Frontend:** React.js / Next.js (SEO and Performance).
*   **State Management:** TanStack Query (React Query) for heavy data fetching.
*   **Backend:** Python (FastAPI) - Optimized for AI/ML library integration.
*   **AI/ML:** 
    *   Object Detection: PyTorch / TensorFlow.
    *   Metadata Generation: OpenAI GPT-4o API (Vision & Text).
    *   Vector Search: Pinecone (to find similar historical assets).
*   **Storage:** 
    *   Assets: AWS S3 with CloudFront CDN.
    *   Database: PostgreSQL (User data/Metadata).
    *   Caching: Redis.
*   **Infrastructure:** Docker / Kubernetes on AWS.
*   **Communication:** RabbitMQ / Celery for handling long-running background upload tasks.