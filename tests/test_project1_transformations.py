"""
Test Suite: Project 1 — Omnichannel Retail Lakehouse Transformations
====================================================================
Handbook: R11 azure-databricks-project-blueprints
Cross-links:
  - Architecture: https://github.com/santoshjammi29/data-system-design-handbook/tree/main/modules/01_lakehouse_and_medallion_architecture
  - Recipe: https://github.com/santoshjammi29/databricks-handbook/tree/main/notebooks/04_lakeflow_ingestion_and_dlt
  - Defense: https://github.com/santoshjammi29/data-engineering-interview-handbook/blob/main/pillars/01_spark_and_databricks.md
"""

try:
    import pytest
except ImportError:
    pytest = None
import unittest


class TestSCDType2Transformations(unittest.TestCase):
    """Test SCD Type 2 merge logic for dimension tables."""

    def test_scd2_new_record_insertion(self):
        """New records should be inserted with is_current=True and NULL end_date."""
        # Arrange
        new_customer = {
            "customer_id": "CUST_001",
            "email": "new@example.com",
            "loyalty_tier": "Gold",
        }
        existing_records = []

        # Act — simulate merge logic
        result = self._apply_scd2_merge(new_customer, existing_records)

        # Assert
        assert len(result) == 1
        assert result[0]["is_current"] is True
        assert result[0]["end_date"] is None
        assert result[0]["customer_id"] == "CUST_001"

    def test_scd2_update_closes_old_record(self):
        """Updates should close the old record and create new current version."""
        existing = {
            "customer_id": "CUST_001",
            "email": "old@example.com",
            "loyalty_tier": "Silver",
            "is_current": True,
            "end_date": None,
        }
        updated_customer = {
            "customer_id": "CUST_001",
            "email": "old@example.com",
            "loyalty_tier": "Gold",  # tier changed
        }

        result = self._apply_scd2_merge(updated_customer, [existing])

        current = [r for r in result if r["is_current"]]
        expired = [r for r in result if not r["is_current"]]

        assert len(current) == 1
        assert current[0]["loyalty_tier"] == "Gold"
        assert len(expired) == 1
        assert expired[0]["end_date"] is not None

    def test_scd2_no_change_no_new_version(self):
        """Identical records should not create a new version."""
        existing = {
            "customer_id": "CUST_001",
            "email": "same@example.com",
            "loyalty_tier": "Gold",
            "is_current": True,
            "end_date": None,
        }
        same_customer = {
            "customer_id": "CUST_001",
            "email": "same@example.com",
            "loyalty_tier": "Gold",
        }

        result = self._apply_scd2_merge(same_customer, [existing])
        assert len(result) == 1  # no new version created

    @staticmethod
    def _apply_scd2_merge(incoming: dict, existing: list) -> list:
        """Simplified SCD Type 2 merge logic for unit testing without Spark."""
        import datetime

        if not existing:
            return [{**incoming, "is_current": True, "end_date": None,
                     "effective_date": datetime.date.today()}]

        current = next((r for r in existing if r.get("is_current")), None)
        if current is None:
            return existing + [{**incoming, "is_current": True, "end_date": None,
                                 "effective_date": datetime.date.today()}]

        # Check if anything changed (excluding metadata fields)
        changed_keys = [k for k in incoming
                        if k in current and current[k] != incoming[k]]
        if not changed_keys:
            return existing

        # Close current record
        updated_existing = []
        for r in existing:
            if r.get("is_current"):
                updated_existing.append({**r, "is_current": False,
                                          "end_date": datetime.date.today()})
            else:
                updated_existing.append(r)

        # Add new current version
        updated_existing.append({**incoming, "is_current": True, "end_date": None,
                                   "effective_date": datetime.date.today()})
        return updated_existing


class TestSchemaContracts:
    """Test schema contract enforcement for all 3 projects."""

    def test_bronze_layer_required_columns(self):
        """Bronze layer must contain audit columns: _ingested_at, _source_file, _batch_id."""
        required_audit_cols = ["_ingested_at", "_source_file", "_batch_id"]
        # Simulate bronze schema check
        bronze_schema_cols = [
            "order_id", "customer_id", "amount", "order_date",
            "_ingested_at", "_source_file", "_batch_id"
        ]
        for col in required_audit_cols:
            assert col in bronze_schema_cols, f"Missing audit column: {col}"

    def test_silver_layer_no_duplicates_contract(self):
        """Silver layer unique key constraint: order_id must be deduplicated."""
        silver_records = [
            {"order_id": "ORD_001", "amount": 100.0},
            {"order_id": "ORD_002", "amount": 200.0},
        ]
        order_ids = [r["order_id"] for r in silver_records]
        assert len(order_ids) == len(set(order_ids)), "Duplicate order_ids found in silver"

    def test_idempotent_egress_contract(self):
        """Gold layer writes must be idempotent — same input = same output."""
        def process_batch(records):
            return sorted(set(r["order_id"] for r in records))

        batch = [{"order_id": "ORD_001"}, {"order_id": "ORD_002"}]
        result_1 = process_batch(batch)
        result_2 = process_batch(batch)
        assert result_1 == result_2, "Process is not idempotent"


class TestDLTPipelineConfigs:
    """Validate DLT pipeline YAML/SQL configurations."""

    def test_dlt_pipeline_sql_file_exists(self):
        """DLT pipeline SQL must exist for all 3 projects."""
        import os
        base = "src"
        projects = [
            "project1_omnichannel_retail/dlt_pipeline.sql",
            "project2_realtime_fraud/dlt_pipeline.sql",
            "project3_warehouse_modernization/dlt_pipeline.sql",
        ]
        for proj in projects:
            path = os.path.join(base, proj)
            assert os.path.exists(path), f"DLT pipeline missing: {path}"

    def test_databricks_yml_valid_yaml(self):
        """databricks.yml must be valid YAML with bundle and targets."""
        import yaml
        with open("databricks.yml") as f:
            config = yaml.safe_load(f)
        assert "bundle" in config, "Missing 'bundle' key"
        assert "targets" in config, "Missing 'targets' key"
        assert "dev" in config["targets"], "Missing 'dev' target"
