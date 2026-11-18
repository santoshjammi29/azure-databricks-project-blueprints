# Project 2: Real-Time Payments Fraud Streaming Engine
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def build_fraud_detection_stream(spark, event_hub_config, checkpoint_path, target_table):
    # Configure off-heap RocksDB state store
    spark.conf.set(
        "spark.sql.streaming.stateStore.providerClass",
        "com.databricks.sql.streaming.state.RocksDBStateStoreProvider"
    )
    spark.conf.set("spark.sql.streaming.stateStore.rocksdb.changelogCheckpointing.enabled", "true")

    stream_df = (
        spark.readStream.format("azureEventHubs")
        .options(**event_hub_config)
        .load()
        .select(F.from_json(F.col("body").cast("string"), "account_id STRING, amount DOUBLE, merchant_id STRING, event_time TIMESTAMP").alias("tx"))
        .select("tx.*")
        .withWatermark("event_time", "10 minutes")
    )

    # 15-minute sliding velocity window
    velocity_alerts = (
        stream_df.groupBy(
            F.window(F.col("event_time"), "15 minutes", "1 minute"),
            F.col("account_id")
        )
        .agg(
            F.count("amount").alias("transaction_count"),
            F.sum("amount").alias("total_velocity")
        )
        .filter((F.col("transaction_count") >= 5) | (F.col("total_velocity") > 10000))
    )

    query = (
        velocity_alerts.writeStream
        .format("delta")
        .outputMode("update")
        .option("checkpointLocation", checkpoint_path)
        .toTable(target_table)
    )
    return query
