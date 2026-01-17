# Database Architecture Documentation

## Overview
This schema is designed for **CreatorNexus AI**, prioritizing asset lifecycle management from ingestion through AI enhancement to global distribution and ROI tracking.

## Core Design Decisions

1.  **UUIDs Everywhere**: Uses `uuid-ossp` for all primary keys to ensure global uniqueness, which is critical for distributed systems and prevents ID enumeration in public APIs.
2.  **Asset Ingestion Pipeline**: The `assets` table includes a `checksum_md5`. Before processing, the system checks this to avoid redundant AI compute costs for duplicate files.
3.  **AI Metadata Storage**: 
    - `asset_metadata`: Separates core asset data from AI results.
    - `raw_ai_output (JSONB)`: Stores the complete model inference result. This allows us to re-parse data if we improve our parsing logic without re-running expensive AI models.
4.  **Tagging System**: A Many-to-Many relationship between `assets` and `tags` with a `confidence` score allows the UI to filter out "low-confidence" tags or highlight them for manual review.
5.  **Multi-Platform Distribution**: The `distributions` table acts as a state machine, tracking the lifecycle of an asset across Adobe Stock, Shutterstock, etc.
6.  **Analytics Granularity**: `asset_analytics_daily` allows for time-series reporting, enabling creators to see trends (e.g., "Which keywords are trending this month?").

## Setup Instructions
1. Enable the `pg_trgm` extension for fuzzy tag searching: