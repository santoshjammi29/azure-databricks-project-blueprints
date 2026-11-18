# Unit tests for Retail Data Standardization
import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").appName("unit-tests").getOrCreate()

def test_sales_compensating_return_logic(spark):
    data = [("ORD-1", 1, 100.0), ("ORD-1-RET", -1, -100.0)]
    df = spark.createDataFrame(data, ["order_id", "qty", "amount"])
    net_sales = df.select(F.sum("amount")).collect()[0][0]
    assert net_sales == 0.0
