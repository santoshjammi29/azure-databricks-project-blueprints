# Azure Databricks Production Project Blueprints
> **Senior Data Engineer & Lakehouse Architect Design Portfolio**

This repository contains end-to-end design blueprints, code implementations, and operational playbooks for building enterprise data platforms on Azure Databricks.

## 🧠 Core Curriculum Concepts & Topics (35 Architectural Topics Covered)

> 💡 **Enterprise Knowledge Base Integration**: Production architectural topics and lakehouse engine primitives implemented across the 3 project blueprints, cross-linked with the [Modern Data Engineering Systems Encyclopedia (921 Topics)](https://moderndataengineer.uk/concepts).

### 📑 Project Topics Directory at a Glance

| Project Blueprint | Topic Count | Key Primitives Covered | Status |
|:---|:---:|:---|:---:|
| 🛒 **Scenario 1: Retail Sales & Inventory** | **12** | Auto Loader, Liquid Clustering, Deletion Vectors, SCD Type 2 | ✅ Documented |
| 💳 **Scenario 2: Payments Fraud & AML** | **12** | RocksDB State Store, Watermarks, Exactly-Once, Idempotent Egress | ✅ Documented |
| 🔄 **Scenario 3: Warehouse Modernization** | **11** | Expand/Contract Migration, Dual-Run Parity, DABs CI/CD | ✅ Documented |

<details open>
<summary><b>🛒 Scenario 1: Omnichannel Retail Sales & Inventory Lakehouse (12 Topics)</b> — <i>Click to collapse/expand</i></summary>

| # | Topic / Concept | Level | Architectural Definition & Core Principle |
|---|---|---|---|
| 1 | **Fact Table** | 🟢 Easy | A central table in a dimensional database model containing quantitative metrics and keys referencing dimension tables. |
| 2 | **Dimension Table** | 🟢 Easy | A table in a dimensional database model containing descriptive attributes used to filter, group, and slice facts. |
| 3 | **Databricks Auto Loader** | 🔴 Advanced | A Databricks-native structured streaming source that incrementally ingests new files from cloud storage (S3/ADLS/GCS) as they arrive, using directory listing or file notification events to detect new files efficiently at scale. |
| 4 | **Delta Lake Liquid Clustering & Space-Filling Curves** | 🟣 Architect | A dynamic layout optimization using Hilbert space-filling curves that replaces rigid Hive-style directory partitioning and manual Z-Ordering. |
| 5 | **Delta Lake Deletion Vectors (Merge-on-Read)** | 🟣 Architect | A storage optimization that shifts Delta Lake write operations from Copy-on-Write (CoW) to Merge-on-Read (MoR) using compact RoaringBitmap row tombstones. |
| 6 | **Slowly Changing Dimensions Type 2 (SCD Type 2)** | 🟡 Intermediate | A design pattern that tracks historical attribute changes by creating new records with effective start/end dates. |
| 7 | **Databricks Serverless Compute** | 🟡 Intermediate | A Databricks compute model where Databricks manages the cluster lifecycle entirely — provisioning, scaling, and terminating compute resources instantly — with per-second DBU billing and zero cluster configuration. |
| 8 | **Direct Lake Mode** | 🟡 Intermediate | A Power BI storage mode that reads Delta Parquet files directly from OneLake without importing or running SQL queries. |
| 9 | **Medallion Architecture Layer Invariants** | 🟢 Easy | The strict data quality, mutation, and schema rules that establish explicit technical boundaries between Bronze (Raw), Silver (Curated), and Gold (Aggregated) lakehouse layers. |
| 10 | **Delta Lake (Databricks)** | 🟢 Easy | Delta Lake is an open-source storage framework that brings ACID transactions, scalable metadata handling, and unified streaming and batch data processing to Apache Spark and data lakes. |
| 11 | **Clustered Columnstore Rowgroup Health** | 🟣 Architect | Columnstore rowgroup health measures the size, compaction state, and row count of columnar rowgroups, where the optimal target is exactly 1,048,576 rows per compressed rowgroup. |
| 12 | **Delta Lake Column Mapping** | 🟡 Intermediate | A Delta Lake metadata feature that decouples logical column names exposed to users from physical column identifiers stored inside Parquet files. |

</details>

<details open>
<summary><b>💳 Scenario 2: Real-Time Payments Fraud & AML Monitoring (12 Topics)</b> — <i>Click to collapse/expand</i></summary>

| # | Topic / Concept | Level | Architectural Definition & Core Principle |
|---|---|---|---|
| 1 | **Apache Kafka Architecture** | 🔴 Advanced | A distributed event streaming platform based on a distributed commit log, providing high-throughput, durable, and fault-tolerant publish-subscribe messaging with configurable delivery guarantees. |
| 2 | **Structured Streaming Fundamentals** | 🟡 Intermediate | How Structured Streaming on Databricks uses Delta Lake as both source and sink. |
| 3 | **RocksDB State Store in Structured Streaming** | 🟣 Architect | An embedded, disk-backed LSM-tree state store provider engineered to manage multi-gigabyte or multi-billion-key stateful streaming pipelines. |
| 4 | **Structured Streaming Watermarking & Allowed Lateness** | 🔴 Advanced | Threshold specifying how far event-time can lag behind maximum observed event-time before data is dropped. |
| 5 | **Stream-Stream Joins** | 🔴 Advanced | Joining two streaming DataFrames. |
| 6 | **Idempotent Pipeline Patterns & Replay Safety** | 🟣 Architect | A pipeline architectural design ensuring that executing a data transformation multiple times with identical inputs produces the exact same output without duplicates or data corruption. |
| 7 | **Dead-Letter Queue (DLQ) Quarantine Architecture** | 🟣 Architect | An isolation mechanism that routes malformed, corrupted, or non-conforming data records to a quarantined storage queue without halting primary pipeline execution. |
| 8 | **Unity Catalog** | 🟢 Easy | Unity Catalog is Databricks' centralized, multi-cloud governance solution providing unified access control, data auditing, lineage tracking, and discovery across all workspace assets. |
| 9 | **Debezium CDC & Analytical Stream Decoupling** | 🟣 Architect | Debezium CDC is a distributed transaction log mining engine that captures row-level database changes in real time, streaming events into Kafka to decouple OLTP from analytical lakehouses. |
| 10 | **Transactional Outbox Pattern for CDC** | 🟣 Architect | A distributed system design pattern that guarantees atomic database state changes and event publishing to a message broker without dual-write inconsistencies. |
| 11 | **Low-Latency Streaming Ingestion in Python via confluent-kafka (librdkafka)** | 🟣 Architect | High-performance Python Kafka client built on top of the native C library librdkafka, offering sub-millisecond message delivery, asynchronous batching, and exact-once semantics (EOS). |
| 12 | **Stream-Static Joins** | 🟡 Intermediate | Joining streaming DataFrames with batch DataFrames. |

</details>

<details open>
<summary><b>🔄 Scenario 3: Legacy Warehouse Modernization & Controlled Cutover (11 Topics)</b> — <i>Click to collapse/expand</i></summary>

| # | Topic / Concept | Level | Architectural Definition & Core Principle |
|---|---|---|---|
| 1 | **Zero-Downtime Expand/Contract Data Migration** | 🟣 Architect | A phased database and schema refactoring pattern that guarantees 100% continuous uptime and compatibility across active producers and consumers during major table schema evolutions. |
| 2 | **Data Contract Specification & Drift Prevention** | 🟣 Architect | An explicit, version-controlled agreement between data producers and consumers specifying schema definitions, business semantics, SLA guarantees, and change management protocols. |
| 3 | **Automated Source-to-Sink Ledger Reconciliation** | 🔴 Advanced | A mathematical verification pipeline that continuously compares financial or transactional source balances against downstream warehouse aggregations. |
| 4 | **Delta Lake Time Travel** | 🟡 Intermediate | Delta Lake's ability to query or restore a table to any previous version or timestamp by replaying the transaction log to reconstruct the historical table state. |
| 5 | **Databricks Asset Bundles (DABs) & Declarative DataOps Pipelines** | 🔴 Advanced | Infrastructure-as-Code for lakehouses defining jobs, pipelines, and permissions in version-controlled YAML. |
| 6 | **Data SLA, SLO & Error Budget Specification** | 🟣 Architect | A quantifiable framework translating business expectations into measurable pipeline metrics: Service Level Indicators (SLIs), Service Level Objectives (SLOs), and enforceable Service Level Agreements (SLAs). |
| 7 | **Production Readiness Review (PRR) for Data Products** | 🟣 Architect | A structured architectural review checklist conducted before promoting a data product to production, verifying operational readiness across security, reliability, observability, and support. |
| 8 | **Blameless Data Incident Postmortems & Cost of Downtime** | 🟣 Architect | A structured, blameless retrospective methodology for analyzing production data outages, identifying systemic root causes, quantifying financial impact, and implementing permanent safeguards. |
| 9 | **Cross-Engine Data Manipulation (Rosetta Stone)** | 🟡 Intermediate | The Cross-Engine Rosetta Stone is an architectural translation matrix mapping common data engineering operations across SQL, PySpark, Pandas, and Polars. |
| 10 | **Architectural Decision Records (ADRs) for Data Platforms** | 🟣 Architect | A lightweight, immutable document capturing significant technical architecture decisions, the historical context, explored alternatives, and accepted long-term trade-offs. |
| 11 | **Lakehouse Active-Passive Multi-Region Disaster Recovery** | 🟣 Architect | An enterprise disaster recovery pattern that replicates lakehouse table metadata and underlying object files to a secondary cloud region to meet strict RPO and RTO recovery mandates. |

</details>

---

## Master Project Index

### 1. Omnichannel Retail Sales & Inventory Lakehouse
- **Pattern**: Metadata-driven ingestion, Auto Loader schema evolution, Lakeflow Declarative Pipelines.
- **Key Techniques**:
  - Grain modeling: Order line item fact (`fact_sales_line`) and daily stock snapshot (`fact_inventory_daily`).
  - Liquid Clustering (`CLUSTER BY`) and Deletion Vectors (Merge-on-Read).
  - Out-of-order CDC processing into SCD Type 2 dimensions via `APPLY CHANGES INTO`.
  - Databricks SQL Serverless and Power BI Direct Lake delivery.

### 2. Real-Time Payments Fraud & AML Monitoring
- **Pattern**: Continuous streaming over Azure Event Hubs with low-latency alert generation.
- **Key Techniques**:
  - Structured Streaming with off-heap RocksDB state store provider.
  - Event-time watermarking bounding 15-minute and 1-hour sliding velocity windows.
  - Idempotent alert egress resolving dual-sink non-transactional delivery.
  - Unity Catalog dynamic column masking for PCI-DSS compliance.

### 3. Legacy Warehouse Modernization & Controlled Cutover
- **Pattern**: Phased migration from legacy SQL warehouse to governed Lakehouse.
- **Key Techniques**:
  - Dependency-graph phased migration across 4 topological waves.
  - Automated dual-run parity verification engine checking row counts, hash sums, and variance.
  - Declarative Automation Bundles (DABs) for GitOps and multi-target deployments.
  - Delta Time Travel rollback and recovery runbooks.

---

## Repository Structure
```text
├── databricks.yml              # Declarative Automation Bundles root definition
├── docs/                       # Architectural specifications and interview defense guides
├── resources/                  # Lakeflow workflow resource definitions
├── src/                        # PySpark pipelines, SQL DDL, and UDFs
└── tests/                      # Automated unit tests with Pytest
```

## License
MIT License
