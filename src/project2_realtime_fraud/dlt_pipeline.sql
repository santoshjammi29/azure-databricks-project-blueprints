-- =============================================================================
-- Project 2: Real-Time Payments Fraud Detection — DLT Pipeline
-- Handbook: R11 azure-databricks-project-blueprints
-- Architecture: Kafka → Event Hubs → Databricks DLT → Delta Gold
-- =============================================================================

-- 🧭 Navigation:
-- Architecture: https://github.com/santoshjammi29/data-system-design-handbook/tree/main/modules/06_realtime_event_driven_lakehouse
-- Streaming: https://github.com/santoshjammi29/streaming-handbook/tree/main/modules/09_end_to_end_exactly_once
-- Interview: https://github.com/santoshjammi29/data-engineering-interview-handbook/blob/main/pillars/16_apache_flink_streaming.md

-- ── BRONZE: Raw Event Hub ingest ─────────────────────────────────────────────
CREATE OR REFRESH STREAMING TABLE bronze_raw_transactions
COMMENT "Raw payment transactions from Azure Event Hubs (Kafka protocol)"
TBLPROPERTIES (
  "quality" = "bronze",
  "pipelines.autoOptimize.zOrderCols" = "event_time"
)
AS SELECT
  body:transaction_id::STRING   AS transaction_id,
  body:account_id::STRING       AS account_id,
  body:merchant_id::STRING      AS merchant_id,
  body:amount::DOUBLE           AS amount,
  body:currency::STRING         AS currency,
  body:event_time::TIMESTAMP    AS event_time,
  body:ip_address::STRING       AS ip_address,
  body:device_fingerprint::STRING AS device_fingerprint,
  current_timestamp()           AS _ingested_at,
  _metadata.file_path           AS _source_file,
  _metadata.file_modification_time AS _batch_id
FROM cloud_files(
  "abfss://eventhub-capture@${storage_account}.dfs.core.windows.net/payments/",
  "avro",
  map("cloudFiles.inferColumnTypes", "true")
);

-- ── SILVER: Cleansed + Enriched Transactions ─────────────────────────────────
CREATE OR REFRESH STREAMING TABLE silver_transactions (
  CONSTRAINT valid_transaction_id EXPECT (transaction_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_amount         EXPECT (amount > 0)                  ON VIOLATION DROP ROW,
  CONSTRAINT valid_account        EXPECT (account_id IS NOT NULL)      ON VIOLATION DROP ROW
)
COMMENT "Cleansed and enriched transactions with velocity features"
TBLPROPERTIES (
  "quality" = "silver",
  "delta.enableChangeDataFeed" = "true"
)
AS SELECT
  t.transaction_id,
  t.account_id,
  t.merchant_id,
  t.amount,
  t.currency,
  t.event_time,
  t.ip_address,
  t.device_fingerprint,
  -- Velocity feature: 1-hour rolling transaction count per account
  count(*) OVER (
    PARTITION BY t.account_id
    ORDER BY t.event_time
    RANGE BETWEEN INTERVAL 1 HOUR PRECEDING AND CURRENT ROW
  ) AS txn_count_1h,
  -- Velocity feature: 1-hour rolling amount per account
  sum(t.amount) OVER (
    PARTITION BY t.account_id
    ORDER BY t.event_time
    RANGE BETWEEN INTERVAL 1 HOUR PRECEDING AND CURRENT ROW
  ) AS amount_sum_1h,
  t._ingested_at
FROM STREAM(LIVE.bronze_raw_transactions) t;

-- ── GOLD: Fraud Alerts (rule-based detection) ─────────────────────────────────
CREATE OR REFRESH STREAMING TABLE gold_fraud_alerts
COMMENT "High-confidence fraud alerts for real-time AML monitoring"
TBLPROPERTIES (
  "quality" = "gold",
  "pipelines.autoOptimize.zOrderCols" = "account_id,event_time"
)
AS SELECT
  transaction_id,
  account_id,
  merchant_id,
  amount,
  event_time,
  txn_count_1h,
  amount_sum_1h,
  CASE
    WHEN txn_count_1h > 20                    THEN 'HIGH_VELOCITY_COUNT'
    WHEN amount_sum_1h > 50000                THEN 'HIGH_VELOCITY_AMOUNT'
    WHEN amount > 10000 AND txn_count_1h > 5  THEN 'LARGE_AMOUNT_BURST'
    ELSE 'PATTERN_ANOMALY'
  END AS fraud_signal_type,
  current_timestamp() AS alert_generated_at
FROM STREAM(LIVE.silver_transactions)
WHERE
  txn_count_1h > 20
  OR amount_sum_1h > 50000
  OR (amount > 10000 AND txn_count_1h > 5);
