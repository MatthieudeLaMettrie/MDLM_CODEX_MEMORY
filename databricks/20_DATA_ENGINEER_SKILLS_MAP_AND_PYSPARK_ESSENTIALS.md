# Data engineer skills map and PySpark essentials

[Back to Databricks README](README.md) · [Auto Loader demo](video-demo-auto-loader/README.md) · [CDC and CDF explained](17_CDF_AND_CDC_EXPLAINED.md)

Written 12 October 2026. The skills map is a judgement from general data engineering practice, not a survey or a job-market analysis. The PySpark examples were **not run** in a live workspace. Check them in a notebook before you rely on them or record them.

## 1. Are Auto Loader and CDC/CDF the two main things?

No. They are two important pieces of one larger picture. Auto Loader is **how files arrive**. CDC/CDF is **how changes move**. A data engineer needs both, but they sit on top of a base of skills that matter more day to day.

| Layer | What to know | Why it comes first |
|---|---|---|
| 1. SQL | Joins, window functions, CTEs, aggregations, `MERGE` | Most transformation work is SQL, and every platform uses it |
| 2. Data modelling | Star schema, medallion (bronze/silver/gold), SCD1/SCD2, keys and grain | Decides whether the data is usable at all |
| 3. Python and PySpark | DataFrames, joins, aggregations, UDF pitfalls, reading and writing files | Needed whenever SQL is not enough, and for notebooks |
| 4. Storage and table formats | Delta tables, Parquet, partitioning, Unity Catalog, volumes | Where the data lives and how it is governed |
| 5. **Ingestion** | **Auto Loader**, schema evolution, batch vs streaming | Gets data in reliably and only once |
| 6. **Change handling** | **CDC, CDF, AUTO CDC / MERGE** | Keeps tables correct when rows are updated or deleted |
| 7. Orchestration and deployment | Jobs, Lakeflow pipelines, bundles, Git, CI/CD | Makes the work repeatable |
| 8. Quality and operations | Expectations, tests, monitoring, event logs, cost and performance | Keeps it running and trusted |
| 9. Cloud and security basics | Storage accounts, identities, permissions, secrets | Most real failures are access problems |

So the answer to "what are the main components?" is: SQL, modelling and PySpark first; Auto Loader and CDC/CDF are the two most **Databricks-specific** topics after that. That is a good reason to make them the first video series, because they are specific and searchable, but they do not replace the base.

## 2. Do you need PySpark?

Yes, at a working level. You do not need to be an expert on day one.

- **SQL covers** most transformations, and Lakeflow pipelines accept SQL.
- **PySpark is needed** for custom logic, reading odd file types, loops over many tables, notebooks, tests, and Auto Loader code in notebooks (`cloudFiles` is a PySpark reader option).
- Learn it **after** you are comfortable with SQL, not instead of it.

## 3. PySpark essentials (retail sales example)

Uses the same sample files as the Auto Loader demo. Replace the path with your own volume path.

```python
from pyspark.sql import functions as F
from pyspark.sql import Window

path = "/Volumes/mdlm_db_trial/dev/dev_volume/landing/retail_sales/"

# 1. Read a CSV with a header
df = (spark.read
      .option("header", True)
      .option("inferSchema", True)
      .csv(path))

# 2. Look at it
df.printSchema()
df.show(5, truncate=False)
print(df.count())

# 3. Select, rename, filter
clean = (df
         .select("sale_id", "store_id", "sale_date", "quantity", "unit_price")
         .withColumnRenamed("sale_date", "date")
         .filter(F.col("quantity") > 0))

# 4. Add a column
clean = clean.withColumn("revenue", F.col("quantity") * F.col("unit_price"))

# 5. Aggregate
daily = (clean
         .groupBy("store_id", "date")
         .agg(F.sum("revenue").alias("total_revenue"),
              F.count("*").alias("sales")))

# 6. Window function: rank stores within each day
w = Window.partitionBy("date").orderBy(F.desc("total_revenue"))
ranked = daily.withColumn("rank", F.row_number().over(w))

# 7. Join to a small lookup table
stores = spark.createDataFrame(
    [("ST01", "North"), ("ST02", "South"), ("ST03", "East")],
    ["store_id", "region"])
joined = daily.join(stores, on="store_id", how="left")

# 8. Write to a Delta table
(joined.write
       .format("delta")
       .mode("overwrite")
       .saveAsTable("mdlm_db_trial.dev.pyspark_daily_sales"))
```

Column names above are assumptions based on the demo files. Check the real header of your CSVs, and adjust.

### The ten ideas that cause most beginner problems

1. **Lazy evaluation.** `filter` and `select` do nothing until an action such as `show`, `count` or `write` runs.
2. **`inferSchema` guesses.** It reads the data twice and can guess wrong. Define the schema explicitly for anything important.
3. **`collect()` and `toPandas()`** bring everything to the driver. Use them only on small results.
4. **Python UDFs are slow** compared with built-in functions in `pyspark.sql.functions`. Look for a built-in first.
5. **Joins can be expensive.** A small table can be broadcast: `F.broadcast(stores)`.
6. **Shuffles** (groupBy, join, window) are where time and cost go. Watch them in the Spark UI.
7. **`overwrite` replaces the whole table.** For incremental loads use `MERGE` or `append`.
8. **Nulls** break comparisons. Use `F.col("x").isNull()`, `F.coalesce`, and be explicit.
9. **Small files** hurt performance. See the optimisation guide ([lesson 14](14_PIPELINE_OPERATIONS_AND_OPTIMISATION.md)).
10. **Streaming is the same API with `readStream` and `writeStream`**, plus a checkpoint. That is what Auto Loader uses ([lesson 19](video-demo-auto-loader/README.md)).

## 4. A learning order that fits this repo

1. SQL and Delta basics: [lesson 01](01_CORE_STUDY_GUIDE.md), [lesson 04](04_DELTA_AND_STREAMING.md)
2. PySpark essentials: this page
3. Unity Catalog and volumes: [lesson 10](10_UNITY_CATALOG_VOLUMES_GUIDE.md)
4. Auto Loader and pipelines: [lesson 11](11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md), [lesson 19](video-demo-auto-loader/README.md)
5. CDC and CDF: [lesson 17](17_CDF_AND_CDC_EXPLAINED.md), [lesson 16](16_CDC_CDF_RETAIL_TABLE_WALKTHROUGH.md)
6. Operations and troubleshooting: [lesson 18](18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md)
7. Bundles and deployment: [lesson 06](06_BUNDLES_AND_ORCHESTRATION.md)

## 5. Video outline: "What a data engineer must know (and the 3 Databricks topics to learn first)"

Target 8 to 9 minutes. Audience: **Beginner**. Do not claim a job outcome or guarantee anything. Present the map as your view.

| Time | Section | Content |
|---|---|---|
| 0:00 to 0:30 | Hook | "Everyone says learn Auto Loader and CDC. Here is where they fit, and what to learn before them." |
| 0:30 to 2:30 | The skills map | Show the nine layers from section 1 as one diagram, bottom to top |
| 2:30 to 3:30 | Where Auto Loader and CDC/CDF sit | Ingestion vs change handling, one sentence each |
| 3:30 to 7:00 | PySpark in 3 minutes | Live: read the CSV, filter, add a column, groupBy, write a Delta table |
| 7:00 to 8:00 | Common mistakes | Lazy evaluation, `collect()`, `overwrite` by accident |
| 8:00 to 9:00 | Recap and next video | Three bullets, then point to "Auto Loader explained in 10 minutes" |

Suggested title: **"Data Engineer Skills Map: What to Learn First (Databricks)"**. Place it **before** video 1 in Series 1 as an overview, or after video 3 if you prefer to start hands-on. Run the demand check first, because a generic "roadmap" topic has a lot of competition.

Rehearsal checklist:
- [ ] Run every PySpark cell above on your own CSVs and fix column names
- [ ] Note real row counts for the narration
- [ ] Keep the demo under 3.5 minutes
