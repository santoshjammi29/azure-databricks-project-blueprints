-- Project 1: Delta Lake 3.x Table DDL with Liquid Clustering & Deletion Vectors

CREATE TABLE IF NOT EXISTS prod_retail.gold.fact_sales_line (
  order_id STRING NOT NULL,
  line_item_id INT NOT NULL,
  store_id STRING NOT NULL,
  product_sku STRING NOT NULL,
  customer_id STRING,
  order_ts TIMESTAMP NOT NULL,
  order_date DATE GENERATED ALWAYS AS (CAST(order_ts AS DATE)),
  quantity INT NOT NULL,
  unit_price DECIMAL(10, 2) NOT NULL,
  gross_amount DECIMAL(12, 2) NOT NULL,
  discount_amount DECIMAL(10, 2) DEFAULT 0.00,
  net_amount DECIMAL(12, 2) NOT NULL,
  currency STRING NOT NULL,
  original_order_id STRING
)
CLUSTER BY (store_id, order_date, product_sku)
TBLPROPERTIES (
  'delta.enableDeletionVectors' = true,
  'delta.enableChangeDataFeed' = true,
  'delta.autoOptimize.autoCompact' = true
);

CREATE TABLE IF NOT EXISTS prod_retail.gold.fact_inventory_daily (
  snapshot_date DATE NOT NULL,
  store_id STRING NOT NULL,
  product_sku STRING NOT NULL,
  opening_stock INT NOT NULL,
  units_sold INT NOT NULL,
  units_received INT NOT NULL,
  shrinkage_units INT DEFAULT 0,
  closing_stock INT NOT NULL
)
CLUSTER BY (store_id, snapshot_date)
TBLPROPERTIES (
  'delta.enableDeletionVectors' = true
);
