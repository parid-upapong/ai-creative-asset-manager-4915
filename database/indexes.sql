-- Optimization for Analytics and High-Volume Lookups

-- Fast lookup for user assets sorted by date
CREATE INDEX idx_assets_user_id_created ON assets(user_id, created_at DESC);

-- GIN Index for JSONB metadata searching
CREATE INDEX idx_asset_metadata_raw_json ON asset_metadata USING GIN (raw_ai_output);

-- Fast lookup for tags by name
CREATE INDEX idx_tags_name_trgm ON tags USING gin (name gin_trgm_ops);

-- Index for distribution status tracking (useful for dashboard filters)
CREATE INDEX idx_distributions_status ON distributions(status);

-- Composite index for time-series analytics performance
CREATE INDEX idx_analytics_date_platform ON asset_analytics_daily(tracking_date, platform_id);

-- Checksum index to prevent duplicate file uploads at scale
CREATE INDEX idx_assets_checksum ON assets(checksum_md5) WHERE deleted_at IS NULL;