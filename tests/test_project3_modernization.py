"""
Test Suite: Project 3 — Legacy Warehouse Modernization & Cutover Verification
=============================================================================
Handbook: R11 azure-databricks-project-blueprints
Cross-links:
  - Architecture: https://github.com/santoshjammi29/data-system-design-handbook/tree/main/modules/01_lakehouse_and_medallion_architecture
  - DataOps: https://github.com/santoshjammi29/dataops-cicd-handbook/tree/main/modules/03_automated_testing_and_data_diff
  - Defense: https://github.com/santoshjammi29/data-engineering-interview-handbook/blob/main/playbooks/03_azure_databricks_125.md
"""

import unittest
try:
    import pytest
except ImportError:
    pytest = None


class TestWarehouseDualRunReconciliation(unittest.TestCase):
    """Tests dual-run parity evaluation logic and tolerance threshold gating."""

    def evaluate_metric_variance(self, legacy_val: float, lakehouse_val: float, tolerance: float = 0.0001) -> bool:
        """Returns True if variance exceeds tolerance (i.e. reconciliation fails)."""
        return abs(legacy_val - lakehouse_val) > tolerance

    def test_exact_parity_match(self):
        """Zero variance passes parity verification."""
        assert not self.evaluate_metric_variance(1250000.50, 1250000.50, tolerance=0.0001)

    def test_within_acceptable_tolerance(self):
        """Micro-rounding variance within epsilon passes parity verification."""
        assert not self.evaluate_metric_variance(100.00001, 100.00002, tolerance=0.0001)

    def test_variance_exceeding_tolerance_fails(self):
        """Material difference flags reconciliation failure."""
        assert self.evaluate_metric_variance(100.001, 100.003, tolerance=0.0001)

    def test_cutover_wave_gate_logic(self):
        """Cutover gate: all tables in wave must achieve 100% parity before traffic cutover."""
        tables_in_wave = [
            {"table": "dim_customer", "legacy_count": 50000, "lakehouse_count": 50000, "sum_variance": 0.0},
            {"table": "fct_orders", "legacy_count": 12000000, "lakehouse_count": 12000000, "sum_variance": 0.0},
            {"table": "dim_product", "legacy_count": 15000, "lakehouse_count": 15000, "sum_variance": 0.0},
        ]
        gate_passed = all(
            t["legacy_count"] == t["lakehouse_count"] and t["sum_variance"] <= 0.0001
            for t in tables_in_wave
        )
        assert gate_passed is True

    def test_cutover_wave_gate_blocks_on_drift(self):
        """A single drifted table blocks the entire wave cutover."""
        tables_in_wave = [
            {"table": "dim_customer", "legacy_count": 50000, "lakehouse_count": 50000, "sum_variance": 0.0},
            {"table": "fct_orders", "legacy_count": 12000000, "lakehouse_count": 11999990, "sum_variance": 500.0},
        ]
        gate_passed = all(
            t["legacy_count"] == t["lakehouse_count"] and t["sum_variance"] <= 0.0001
            for t in tables_in_wave
        )
        assert gate_passed is False
