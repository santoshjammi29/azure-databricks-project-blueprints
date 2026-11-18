-- Project 3: Conformed Gold Ledger Table DDL

CREATE TABLE IF NOT EXISTS prod_finance.gold.fact_general_ledger (
  ledger_entry_id STRING NOT NULL,
  transaction_id STRING NOT NULL,
  financial_month STRING NOT NULL,
  posting_date DATE NOT NULL,
  cost_center_id STRING NOT NULL,
  account_code STRING NOT NULL,
  posted_amount DECIMAL(18, 4) NOT NULL,
  currency STRING NOT NULL,
  source_system STRING NOT NULL
)
CLUSTER BY (financial_month, cost_center_id)
TBLPROPERTIES (
  'delta.enableDeletionVectors' = true,
  'delta.enableRowTracking' = true
);
