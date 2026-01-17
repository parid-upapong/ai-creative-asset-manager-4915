-- Comprehensive views for the Creator Dashboard

-- View: Asset Performance Overview
CREATE OR REPLACE VIEW view_asset_performance AS
SELECT 
    a.asset_id,
    a.filename,
    a.user_id,
    p.name as platform_name,
    SUM(ad.downloads_count) as total_downloads,
    SUM(ad.earnings_usd) as total_earnings,
    MAX(ad.tracking_date) as last_activity
FROM assets a
JOIN distributions d ON a.asset_id = d.asset_id
JOIN platforms p ON d.platform_id = p.platform_id
LEFT JOIN asset_analytics_daily ad ON a.asset_id = ad.asset_id AND p.platform_id = ad.platform_id
GROUP BY a.asset_id, a.filename, a.user_id, p.name;

-- View: User Portfolio Statistics
CREATE OR REPLACE VIEW view_user_stats AS
SELECT 
    user_id,
    COUNT(DISTINCT asset_id) as total_assets,
    COUNT(DISTINCT CASE WHEN processing_status = 'completed' THEN asset_id END) as processed_assets,
    (SELECT SUM(earnings_usd) FROM asset_analytics_daily ad 
     JOIN assets a2 ON ad.asset_id = a2.asset_id 
     WHERE a2.user_id = u.user_id) as lifetime_earnings
FROM users u
GROUP BY user_id;