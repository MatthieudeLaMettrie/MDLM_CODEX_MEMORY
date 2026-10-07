# Databricks notebook source
# Original bounded teaching lab. Run only against a dedicated *_dev catalog.
# Databricks provides spark, dbutils, PySpark and the Delta Python API.
import re
from decimal import Decimal

from delta.tables import DeltaTable
from pyspark.sql import functions as F
from pyspark.sql import Window

dbutils.widgets.text("catalog", "training_dev")
dbutils.widgets.text("input_file", "/Volumes/training_dev/ops/lab_files/order_events.csv")
dbutils.widgets.dropdown("batch_id", "B1", ["B1", "B2", "B3"])
dbutils.widgets.dropdown("stage", "bronze", ["bronze", "silver", "gold", "validate"])

catalog = dbutils.widgets.get("catalog")
input_file = dbutils.widgets.get("input_file")
batch_id = dbutils.widgets.get("batch_id")
stage = dbutils.widgets.get("stage")
if not re.fullmatch(r"[a-z][a-z0-9_]*_dev", catalog):
    raise ValueError("Use a dedicated lowercase catalog ending in _dev.")
if not input_file.startswith(f"/Volumes/{catalog}/ops/lab_files/"):
    raise ValueError("Upload the fixture to this lab's dev volume.")
if batch_id not in {"B1", "B2", "B3"}:
    raise ValueError("Unknown fixture batch.")
if stage not in {"bronze", "silver", "gold", "validate"}:
    raise ValueError("Unknown stage.")
spark.conf.set("spark.sql.session.timeZone", "UTC")

bronze_name = f"{catalog}.bronze.order_events"
quarantine_name = f"{catalog}.silver.order_quarantine"
state_name = f"{catalog}.silver.orders_current"
gold_name = f"{catalog}.gold.daily_store_sales"
raw_columns = [
    "line_id", "batch_id", "source_system", "event_id", "order_id",
    "sequence_raw", "op", "store_id", "customer_id", "order_date_raw",
    "amount_raw", "event_ts_raw",
]


def reject_if_any(df, message):
    # Bound driver collection; diagnostic only. Do not collect full production data.
    sample = df.limit(5).collect()
    if sample:
        raise ValueError(f"{message}; bounded examples: {sample}")


def create_if_missing(name, df):
    # Never overwrite existing Bronze/Silver state on a retry.
    if not spark.catalog.tableExists(name):
        df.limit(0).write.format("delta").mode("errorifexists").saveAsTable(name)


def insert_lines_once(name, df):
    create_if_missing(name, df)
    target = spark.table(name)
    reject_if_any(
        df.alias("s").join(target.alias("t"), F.col("s.line_id") == F.col("t.line_id"))
        .filter(~F.col("s.raw_hash").eqNullSafe(F.col("t.raw_hash"))),
        "An existing source line ID has changed payload",
    )
    (DeltaTable.forName(spark, name).alias("t")
     .merge(df.alias("s"), "t.line_id = s.line_id")
     .whenNotMatchedInsertAll().execute())


if stage == "bronze":
    # Read all raw fields as strings. The baseline CSV uses empty fields for null.
    raw_schema = ", ".join(f"{name} STRING" for name in raw_columns)
    incoming = (spark.read.format("csv").schema(raw_schema)
                .option("header", "true").option("mode", "FAILFAST")
                .load(input_file).filter(F.col("batch_id") == batch_id))
    if incoming.limit(1).count() == 0:
        raise ValueError("The selected fixture batch is empty.")
    reject_if_any(incoming.filter(F.col("line_id").isNull()), "Missing source line ID")
    reject_if_any(incoming.groupBy("line_id").count().filter("count > 1"),
                  "Source line IDs must be unique within a delivered batch")
    observed = (incoming.withColumn("raw_hash", F.sha2(F.to_json(F.struct(*raw_columns)), 256))
                .withColumn("ingested_at", F.current_timestamp())
                .withColumn("source_path", F.lit(input_file)))
    insert_lines_once(bronze_name, observed)
    print(f"Bronze complete for {batch_id}")

# COMMAND ----------
if stage == "silver":
    raw = spark.table(bronze_name).filter(F.col("batch_id") == batch_id)
    if raw.limit(1).count() == 0:
        raise ValueError("Run this batch's Bronze stage first.")
    typed = (raw.withColumn("op", F.upper(F.trim("op")))
             .withColumn("amount", F.expr("try_cast(amount_raw AS DECIMAL(18,2))"))
             .withColumn("sequence", F.expr("try_cast(sequence_raw AS BIGINT)"))
             .withColumn("order_date", F.expr("try_cast(order_date_raw AS DATE)"))
             .withColumn("event_ts", F.expr("try_cast(event_ts_raw AS TIMESTAMP)")))

    def blank(name):
        return F.col(name).isNull() | (F.length(F.trim(F.col(name))) == 0)

    reasons = F.concat_ws(";", *[
        F.when(blank("source_system"), "missing_source"),
        F.when(blank("event_id"), "missing_event_id"),
        F.when(blank("order_id"), "missing_order_id"),
        F.when(F.col("sequence").isNull() | (F.col("sequence") < 0), "invalid_sequence"),
        F.when(F.col("op").isNull() | ~F.col("op").isin("UPSERT", "DELETE"), "invalid_op"),
        F.when(F.col("order_date").isNull(), "invalid_date"),
        F.when(F.col("event_ts").isNull(), "invalid_event_ts"),
        F.when((F.col("op") == "UPSERT") &
               (F.col("amount").isNull() | (F.col("amount") < 0)), "invalid_amount"),
        F.when((F.col("op") == "UPSERT") & blank("store_id"), "missing_store"),
        F.when((F.col("op") == "UPSERT") & blank("customer_id"), "missing_customer"),
    ])
    checked = typed.withColumn("reject_reason", reasons)
    rejected = checked.filter(F.col("reject_reason") != "")
    valid = checked.filter(F.col("reject_reason") == "")
    if raw.count() != rejected.count() + valid.count():
        raise AssertionError("Input classification failed")

    # Event ID conflicts must be checked across observed batches, not just this run.
    # The raw signature excludes line_id/batch_id, which describe delivery, not event.
    all_raw = spark.table(bronze_name).withColumn(
        "event_hash", F.sha2(F.to_json(F.struct(*raw_columns[2:])), 256))
    reject_if_any(
        all_raw.filter(F.col("event_id").isNotNull())
        .groupBy("source_system", "event_id").agg(F.countDistinct("event_hash").alias("n"))
        .filter("n > 1"), "Same event identity has contradictory payloads")

    # Canonical payload for equality at the same source sequence.
    payload_columns = ["source_system", "order_id", "op", "store_id",
                       "customer_id", "order_date", "amount"]
    canonical = valid.withColumn(
        "payload_hash", F.sha2(F.to_json(F.struct(*payload_columns)), 256))
    reject_if_any(
        canonical.groupBy("source_system", "order_id", "sequence")
        .agg(F.countDistinct("payload_hash").alias("n")).filter("n > 1"),
        "Different payloads have the same key and sequence")
    # Keep a deterministic representative of exact event re-delivery.
    event_window = Window.partitionBy("source_system", "event_id").orderBy("line_id")
    unique_events = (canonical.withColumn("_event_rank", F.row_number().over(event_window))
                     .filter("_event_rank = 1").drop("_event_rank"))
    latest_window = Window.partitionBy("source_system", "order_id").orderBy(
        F.col("sequence").desc(), F.col("event_id").desc())
    candidates = (unique_events.withColumn("_rank", F.row_number().over(latest_window))
                  .filter("_rank = 1")
                  .withColumn("is_deleted", F.col("op") == "DELETE")
                  .select("source_system", "order_id", "sequence", "op", "is_deleted",
                          "store_id", "customer_id", "order_date", "amount",
                          "event_ts", "event_id", "payload_hash"))
    create_if_missing(state_name, candidates)
    target = spark.table(state_name)
    reject_if_any(target.groupBy("source_system", "order_id").count().filter("count > 1"),
                  "Target business key is duplicated")
    # Compare every accepted sequence with current state, even if a newer event
    # for the same key is also in this batch and becomes the selected candidate.
    same_sequence = canonical.alias("s").join(target.alias("t"),
        (F.col("s.source_system") == F.col("t.source_system")) &
        (F.col("s.order_id") == F.col("t.order_id")) &
        (F.col("s.sequence") == F.col("t.sequence")))
    reject_if_any(same_sequence.filter(~F.col("s.payload_hash").eqNullSafe(F.col("t.payload_hash"))),
                  "Incoming payload contradicts current state at the same sequence")

    # Two separate table transactions: retry must safely complete both.
    insert_lines_once(quarantine_name, rejected)
    (DeltaTable.forName(spark, state_name).alias("t")
     .merge(candidates.alias("s"),
            "t.source_system = s.source_system AND t.order_id = s.order_id")
     .whenMatchedUpdateAll(condition="s.sequence > t.sequence")
     .whenNotMatchedInsertAll().execute())
    print(f"Silver complete for {batch_id}")

# COMMAND ----------
if stage == "gold":
    stores = spark.createDataFrame([("S01", "Sydney"), ("S02", "Newcastle")],
                                   "store_id STRING, store_name STRING")
    reject_if_any(stores.groupBy("store_id").count().filter("count > 1"),
                  "Store dimension is not unique")
    active = spark.table(state_name).filter(~F.col("is_deleted"))
    enriched = (active.join(stores, "store_id", "left")
                .withColumn("store_name", F.coalesce("store_name", F.lit("Unknown"))))
    gold = (enriched.groupBy("order_date", "store_id", "store_name")
            .agg(F.count("order_id").alias("order_count"),
                 F.sum("amount").alias("order_amount")))
    # Full recomputation is deliberate for this tiny development-only lab.
    gold.write.format("delta").mode("overwrite").saveAsTable(gold_name)
    print("Gold recomputed from current active state")

# COMMAND ----------
if stage == "validate":
    # Fixed expected values apply after B1, B1+B2, or B1+B2+B3 respectively.
    # They intentionally reject arbitrary partial/out-of-order fixture runs.
    expected = {
        "B1": (8, 3, 4, 4, Decimal("215.00")),
        "B2": (13, 3, 5, 4, Decimal("270.00")),
        "B3": (16, 3, 5, 4, Decimal("270.00")),
    }[batch_id]
    state = spark.table(state_name)
    active = state.filter(~F.col("is_deleted"))
    active_sum = active.agg(F.sum("amount")).first()[0]
    actual = (spark.table(bronze_name).count(), spark.table(quarantine_name).count(),
              state.count(), active.count(), active_sum)
    assert actual == expected, (actual, expected)
    reject_if_any(state.groupBy("source_system", "order_id").count().filter("count > 1"),
                  "Duplicate current-state key")
    gold = spark.table(gold_name)
    gold_stats = gold.agg(F.sum("order_count"), F.sum("order_amount")).first()
    assert gold_stats[0] == expected[3] and gold_stats[1] == expected[4]
    rows = [(str(r.order_date), r.store_id, r.store_name,
             r.order_count, r.order_amount)
            for r in gold.orderBy("order_date", "store_id").collect()]
    expected_gold = [
        ("2026-10-01", "S01", "Sydney", 2, Decimal("150.00")),
        ("2026-10-01", "S02", "Newcastle", 1, Decimal("40.00")),
        ("2026-10-01", "S99", "Unknown", 1, Decimal("25.00")),
    ] if batch_id == "B1" else [
        ("2026-10-01", "S01", "Sydney", 1, Decimal("120.00")),
        ("2026-10-01", "S02", "Newcastle", 1, Decimal("45.00")),
        ("2026-10-01", "S99", "Unknown", 1, Decimal("25.00")),
        ("2026-10-02", "S02", "Newcastle", 1, Decimal("80.00")),
    ]
    assert rows == expected_gold, (rows, expected_gold)
    if batch_id != "B1":
        deleted = state.filter("order_id = '1002'").first()
        assert deleted.is_deleted and deleted.sequence == 2
        assert state.filter("order_id = '1001'").first().amount == Decimal("120.00")
    print(f"All lab assertions passed for cumulative state through {batch_id}")
