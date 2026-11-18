-- Project 3: ADF Metadata-Driven Ingestion Control Table Schema

CREATE TABLE IF NOT EXISTS control.adf_pipeline_watermarks (
  pipeline_id INT IDENTITY(1,1) PRIMARY KEY,
  source_system VARCHAR(50) NOT NULL,
  source_table VARCHAR(100) NOT NULL,
  extraction_query VARCHAR(MAX) NOT NULL,
  watermark_column VARCHAR(50) NOT NULL,
  last_watermark_value VARCHAR(50) NOT NULL,
  adls_landing_path VARCHAR(255) NOT NULL,
  is_active BIT DEFAULT 1,
  last_run_status VARCHAR(20),
  last_run_timestamp DATETIME2 DEFAULT SYSUTCDATETIME()
);
