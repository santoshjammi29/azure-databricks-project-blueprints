-- Production FinOps Queries on Databricks System Tables

-- 1. 30-Day DBU Spend and Cost by Job ID, SKU, and Cost Center
SELECT
  u.usage_date,
  u.sku_name,
  u.custom_tags['cost_center'] AS cost_center,
  u.usage_metadata.job_id,
  ROUND(SUM(u.usage_quantity), 2) AS total_dbus,
  ROUND(SUM(u.usage_quantity * lp.pricing.default), 2) AS estimated_usd
FROM system.billing.usage u
JOIN system.billing.list_prices lp
  ON u.cloud = lp.cloud
  AND u.sku_name = lp.sku_name
  AND u.usage_start_time >= lp.price_start_time
  AND (u.usage_end_time <= lp.price_end_time OR lp.price_end_time IS NULL)
WHERE u.usage_date >= CURRENT_DATE() - INTERVAL 30 DAYS
GROUP BY ALL
ORDER BY estimated_usd DESC;

-- 2. Identify High-Spill Queries in Databricks SQL Warehouses
SELECT
  statement_id,
  executed_by,
  warehouse_id,
  ROUND(total_duration_ms / 1000.0, 2) AS duration_sec,
  ROUND(spilled_local_bytes / (1024*1024*1024), 2) AS gb_spilled,
  statement_text
FROM system.query.history
WHERE start_time >= CURRENT_TIMESTAMP() - INTERVAL 7 DAYS
  AND spilled_local_bytes > 0
ORDER BY spilled_local_bytes DESC
LIMIT 20;
