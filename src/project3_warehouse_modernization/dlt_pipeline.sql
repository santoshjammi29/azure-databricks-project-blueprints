-- =============================================================================
-- Project 3: Legacy Warehouse Modernization — Controlled Cutover DLT Pipeline
-- Handbook: R11 azure-databricks-project-blueprints
-- Strategy: Dual-run parity verification → wave cutover → Delta Time Travel rollback
-- =============================================================================

-- ── BRONZE: SQL Server CDC via Debezium ──────────────────────────────────────
CREATE OR REFRESH STREAMING TABLE bronze_legacy_cdc
COMMENT "CDC events from legacy SQL Server via Debezium Kafka connector"
TBLPROPERTIES ("quality" = "bronze")
AS SELECT
  payload:before::STRING        AS before_state,
  payload:after::STRING         AS after_state,
  payload:op::STRING            AS cdc_operation,  -- c=create, u=update, d=delete
  payload:ts_ms::BIGINT         AS cdc_timestamp_ms,
  payload:source.table::STRING  AS source_table,
  current_timestamp()           AS _ingested_at
FROM cloud_files(
  "abfss://cdc-capture@${storage_account}.dfs.core.windows.net/debezium/",
  "json"
);

-- ── SILVER: Merged CDC events (UPSERT semantics) ─────────────────────────────
CREATE OR REFRESH MATERIALIZED VIEW silver_customers_current
COMMENT "Current state of customer dimension after CDC merge"
AS
WITH ranked_cdc AS (
  SELECT
    after_state:customer_id::STRING AS customer_id,
    after_state:name::STRING        AS name,
    after_state:email::STRING       AS email,
    after_state:segment::STRING     AS segment,
    after_state:credit_limit::DOUBLE AS credit_limit,
    cdc_operation,
    cdc_timestamp_ms,
    ROW_NUMBER() OVER (
      PARTITION BY after_state:customer_id::STRING
      ORDER BY cdc_timestamp_ms DESC
    ) AS rn
  FROM LIVE.bronze_legacy_cdc
  WHERE source_table = 'customers'
    AND cdc_operation != 'd'  -- exclude deletes for current-state view
)
SELECT customer_id, name, email, segment, credit_limit, cdc_timestamp_ms
FROM ranked_cdc
WHERE rn = 1;

-- ── GOLD: Parity validation metrics for dual-run verification ────────────────
CREATE OR REFRESH MATERIALIZED VIEW gold_parity_audit
COMMENT "Dual-run parity metrics: compare legacy vs new lakehouse row counts and checksums"
AS SELECT
  'customers'                           AS table_name,
  count(*)                              AS lakehouse_row_count,
  sum(hash(customer_id, email, segment)) AS lakehouse_checksum,
  current_timestamp()                   AS audit_timestamp
FROM LIVE.silver_customers_current;
