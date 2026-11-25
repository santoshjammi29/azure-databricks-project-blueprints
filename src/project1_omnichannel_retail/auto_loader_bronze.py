# Project 1: Auto Loader Incremental File Ingestion
from pyspark.sql import functions as F

def run_auto_loader_bronze(spark, landing_path, schema_location, checkpoint_location, target_table):
    bronze_stream = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", schema_location)
        .option("cloudFiles.inferColumnTypes", "true")
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .option("cloudFiles.useNotifications", "true")
        .option("rescuedDataColumn", "_rescued_data")
        .load(landing_path)
        .select(
            "*",
            "_metadata.file_path",
            "_metadata.file_modification_time",
            F.current_timestamp().alias("_ingest_ts")
        )
    )

    query = (
        bronze_stream.writeStream
        .format("delta")
        .option("checkpointLocation", checkpoint_location)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)
        .toTable(target_table)
    )
    return query
