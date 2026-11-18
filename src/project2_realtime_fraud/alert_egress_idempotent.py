# Project 2: Idempotent Alert Egress Handler
import json
from pyspark.sql import functions as F

def write_idempotent_alerts_to_event_hub(micro_batch_df, batch_id):
    if micro_batch_df.isEmpty():
        return

    # Generate deterministic deduplication key
    alerts = micro_batch_df.withColumn(
        "dedup_key",
        F.sha2(F.concat_ws("||", F.col("account_id"), F.col("event_time"), F.col("rule_name")), 256)
    ).select(
        F.col("dedup_key").alias("partitionKey"),
        F.to_json(F.struct("*")).alias("body")
    )

    # Publish to external Event Hub / queue
    (
        alerts.write
        .format("azureEventHubs")
        .options(**event_hubs_egress_conf)
        .save()
    )
