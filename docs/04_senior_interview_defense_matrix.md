# Senior Data Engineer Interview Defense Matrix

## Which Blueprint to Lead With?

| Interviewer Focus / Panel Persona | Best Project to Lead With | Core Theme to Emphasize |
| :--- | :--- | :--- |
| **Enterprise Architect / Director** | **Blueprint 3 (Warehouse Modernization)** | Migration strategy, business risk mitigation, dual-run parity, FinOps ROI, and cross-functional sign-offs. |
| **Distributed Systems / Streaming Lead** | **Blueprint 2 (Real-Time Payments & Fraud)** | Event-time watermarking, off-heap RocksDB state stores, low-latency micro-batching, and dual-sink idempotency. |
| **Data Modeling / Analytics Lead** | **Blueprint 1 (Omnichannel Retail & Inventory)** | Medallion grain design, Liquid Clustering vs. partitioning, SCD Type 2 CDC, and Power BI Direct Lake performance. |

---

## High-Frequency Architectural Defense Questions

### Q1: "Why choose Azure Data Factory (ADF) for ingestion if Databricks has Lakeflow Connect and Auto Loader?"
**Answer**: "ADF excels at cross-system orchestration, on-premises hybrid connectivity via Self-Hosted Integration Runtimes, and triggering workflows across disparate Azure services behind private networks. Lakeflow Connect is our preferred choice for integrated relational CDC where supported, and Auto Loader is our gold standard for cloud storage file discovery. We use ADF to land data securely in ADLS Gen2, and immediately hand off compute execution to Databricks Lakeflow Jobs and Pipelines to eliminate unnecessary ADF data flow compute overhead and benefit from Photon vectorization."

### Q2: "Why Liquid Clustering over Hive Partitioning and Z-Ordering?"
**Answer**: "Traditional Hive partitioning physically separates data into folder paths. On high-cardinality keys like `store_id` or `customer_id`, this causes the small-file problem and metadata explosion. Z-Ordering solved multi-dimensional sorting, but was non-incremental—requiring costly full-table rewrites on every compaction. Liquid Clustering uses Hilbert-curve space-filling algorithms to cluster incrementally, automatically balances file sizes to 256 MB–512 MB, and allows clustering keys to be redefined instantly via `ALTER TABLE` without rewriting historical Parquet data."

### Q3: "How do Deletion Vectors change the economics of `MERGE` and `DELETE`?"
**Answer**: "Historically, Delta Lake operated on Copy-on-Write (CoW). Modifying a single row inside a 512 MB Parquet file required reading the entire file and writing a brand-new 512 MB file. Deletion Vectors switch the write path to Merge-on-Read (MoR). Delta leaves the existing Parquet file untouched and writes a compact roaring bitmap recording tombstoned row offsets. Readers filter these invalid rows in memory during scan time. Invalidated rows are physically cleaned up asynchronously during scheduled `OPTIMIZE` or `VACUUM` runs. This speeds up DML by up to 10x and eliminates concurrent write lock conflicts."

### Q4: "How do you enforce security and prevent data exfiltration in a regulated enterprise?"
**Answer**: "We implement a defense-in-depth model across storage, network, and catalog. Storage uses Azure Managed Identities bound to Unity Catalog Storage Credentials—eliminating all static keys. Networking utilizes Azure Private Link, VNet Injection, and No Public IP (NPIP) clusters. Within the catalog, we enforce Attribute-Based Access Control (ABAC), Dynamic Column Masking for PII redaction, and Dynamic Row Filters for regional data isolation. All access, permissions, and query executions are continuously recorded in Databricks System Tables (`system.access.audit` and `system.access.table_lineage`) to guarantee end-to-end regulatory audit compliance."
