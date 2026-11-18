# Project 3: Automated Dual-Run Parity & Reconciliation Engine
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def reconcile_outputs(spark, legacy_table, lakehouse_table, join_keys, metric_columns, tolerance=0.0001):
    df_legacy = spark.table(legacy_table)
    df_lakehouse = spark.table(lakehouse_table)

    joined = df_legacy.alias("leg").join(
        df_lakehouse.alias("lkh"),
        on=join_keys,
        how="full_outer"
    )

    diff_exprs = []
    for col_name in metric_columns:
        diff_col = F.abs(F.coalesce(F.col(f"leg.{col_name}"), F.lit(0)) - F.coalesce(F.col(f"lkh.{col_name}"), F.lit(0)))
        diff_exprs.append((diff_col > tolerance).alias(f"{col_name}_has_variance"))

    reconciliation_results = joined.select(*join_keys, *diff_exprs)
    failures = reconciliation_results.filter(
        F.greatest(*[f"{col_name}_has_variance" for col_name in metric_columns]) == True
    )
    
    return failures
