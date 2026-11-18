-- Project 2: Real-Time Fraud Streaming Delta Table DDL

CREATE TABLE IF NOT EXISTS prod_fraud.gold.fraud_detection_alerts (
  alert_id STRING NOT NULL,
  account_id STRING NOT NULL,
  rule_name STRING NOT NULL,
  risk_score DOUBLE NOT NULL,
  velocity_count INT,
  velocity_sum DOUBLE,
  window_start TIMESTAMP NOT NULL,
  window_end TIMESTAMP NOT NULL,
  generated_ts TIMESTAMP NOT NULL
)
CLUSTER BY (rule_name, window_start)
TBLPROPERTIES (
  'delta.enableDeletionVectors' = true,
  'delta.enableChangeDataFeed' = true
);
