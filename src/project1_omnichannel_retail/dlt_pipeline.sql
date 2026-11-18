-- Project 1: Omnichannel Retail Lakeflow Declarative Pipeline

CREATE OR REFRESH STREAMING TABLE bronze_sales_raw
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingest_ts
FROM STREAM read_files(
  '/Volumes/retail_catalog/landing/pos_sales/',
  format => 'json'
);

CREATE OR REFRESH STREAMING TABLE silver_sales_conformed (
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
  CONSTRAINT positive_quantity EXPECT (quantity > 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_currency EXPECT (currency IN ('EUR', 'USD', 'GBP')) ON VIOLATION DROP ROW
)
CLUSTER BY (store_id, order_date)
TBLPROPERTIES (
  'delta.enableDeletionVectors' = true,
  'delta.enableChangeDataFeed' = true
);

APPLY CHANGES INTO LIVE.silver_sales_conformed
FROM STREAM(LIVE.bronze_sales_raw)
KEYS (order_id, line_item_id)
APPLY AS DELETE WHEN operation = 'CANCEL'
SEQUENCE BY event_timestamp
COLUMNS * EXCEPT (operation, source_file);
