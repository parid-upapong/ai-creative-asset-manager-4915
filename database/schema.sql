-- CreatorNexus AI: Core Database Schema
-- Focus: Asset Tracking, AI Metadata Management, and Multi-Platform Analytics
-- Extension: uuid-ossp for secure, non-sequential identifiers

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USER & SUBSCRIPTION MANAGEMENT
CREATE TYPE subscription_tier AS ENUM ('free', 'pro', 'enterprise');

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    tier subscription_tier DEFAULT 'free',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. ASSET CORE DATA
CREATE TYPE asset_type AS ENUM ('image', 'video', 'illustration', 'vector');
CREATE TYPE processing_status AS ENUM ('queued', 'processing', 'completed', 'failed');

CREATE TABLE assets (
    asset_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_url TEXT NOT NULL, -- S3/Storage Link
    thumbnail_url TEXT,
    file_type asset_type NOT NULL,
    file_size_bytes BIGINT,
    dimensions_width INT,
    dimensions_height INT,
    processing_status processing_status DEFAULT 'queued',
    checksum_md5 VARCHAR(32), -- To prevent duplicate uploads
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE -- Soft delete for safety
);

-- 3. AI-GENERATED & OPTIMIZED METADATA
CREATE TABLE asset_metadata (
    metadata_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID UNIQUE NOT NULL REFERENCES assets(asset_id) ON DELETE CASCADE,
    ai_generated_title TEXT,
    ai_generated_description TEXT,
    optimized_title VARCHAR(200), -- Human-refined or final SEO title
    optimized_description TEXT,
    language_code VARCHAR(10) DEFAULT 'en',
    ai_confidence_score FLOAT, -- Average confidence across attributes
    raw_ai_output JSONB, -- Stores full response from CLIP/LLM for debugging
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. TAXONOMY & KEYWORDING
CREATE TABLE tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) -- e.g., 'nature', 'technology', 'people'
);

CREATE TABLE asset_tags (
    asset_id UUID REFERENCES assets(asset_id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(tag_id) ON DELETE CASCADE,
    confidence FLOAT DEFAULT 1.0, -- Confidence score from AI engine
    source VARCHAR(20) DEFAULT 'ai', -- 'ai' or 'manual'
    PRIMARY KEY (asset_id, tag_id)
);

-- 5. DISTRIBUTION TRACKING (STOCK PLATFORMS)
CREATE TABLE platforms (
    platform_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL, -- e.g., 'Adobe Stock', 'Shutterstock', 'Getty'
    api_endpoint TEXT,
    is_active BOOLEAN DEFAULT true
);

CREATE TYPE distribution_status AS ENUM ('pending', 'submitted', 'accepted', 'rejected', 'revision_required');

CREATE TABLE distributions (
    distribution_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES assets(asset_id) ON DELETE CASCADE,
    platform_id UUID REFERENCES platforms(platform_id) ON DELETE CASCADE,
    external_asset_id VARCHAR(255), -- ID assigned by the stock agency
    status distribution_status DEFAULT 'pending',
    rejection_reason TEXT,
    submission_date TIMESTAMP WITH TIME ZONE,
    last_sync_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(asset_id, platform_id)
);

-- 6. ANALYTICS & EARNINGS
CREATE TABLE asset_analytics_daily (
    analytics_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES assets(asset_id) ON DELETE CASCADE,
    platform_id UUID REFERENCES platforms(platform_id) ON DELETE CASCADE,
    tracking_date DATE NOT NULL,
    views_count INT DEFAULT 0,
    downloads_count INT DEFAULT 0,
    earnings_usd DECIMAL(12, 4) DEFAULT 0.0000,
    UNIQUE(asset_id, platform_id, tracking_date)
);

-- 7. AUDIT LOG FOR AI JOBS
CREATE TABLE ai_processing_jobs (
    job_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES assets(asset_id) ON DELETE CASCADE,
    job_type VARCHAR(50), -- 'tagging', 'upscaling', 'captioning'
    engine_version VARCHAR(50), -- e.g., 'clip-v2', 'gpt-4'
    execution_time_ms INT,
    log_output TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);