#!/usr/bin/env python3
"""
Test Suite Runner for Azure Databricks Project Blueprints
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from tests.test_project1_transformations import TestSCDType2Transformations  # noqa: E402
from tests.test_project2_fraud import TestFraudAlertEgressIdempotency  # noqa: E402
from tests.test_project3_modernization import TestWarehouseDualRunReconciliation  # noqa: E402

def main():
    print("▶ Running Azure Databricks Project Blueprints Test Suite...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestSCDType2Transformations))
    suite.addTests(loader.loadTestsFromTestCase(TestFraudAlertEgressIdempotency))
    suite.addTests(loader.loadTestsFromTestCase(TestWarehouseDualRunReconciliation))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        print(f"\n❌ FAILURES: {len(result.failures)}, ERRORS: {len(result.errors)}")
        sys.exit(1)

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
