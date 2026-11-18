# Unit tests for Dual-Run Parity Logic
import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").appName("unit-tests").getOrCreate()

def test_parity_tolerance_calculation(spark):
    data = [(100.0001, 100.0002)]
    df = spark.createDataFrame(data, ["legacy", "lakehouse"])
    diff = df.select(F.abs(F.col("legacy") - F.col("lakehouse"))).collect()[0][0]
    assert diff < 0.001
