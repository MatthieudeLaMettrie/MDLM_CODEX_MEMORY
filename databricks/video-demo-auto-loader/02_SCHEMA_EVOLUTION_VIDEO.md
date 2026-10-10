# Video 2 — Schema evolution: what happens when a file gets a new column

[Back to video 1](README.md) · [Next: video 3 — CDC](03_CDC_VIDEO.md) · [Lessons index](../README.md)

Written 10 October 2026. **Not run in a workspace.** Syntax and behaviour come from the sample data (checked locally) and Databricks documentation search results. Rehearse first; failure messages and menu names can differ by release.

## The story

Three days of sales files loaded cleanly in video 1. On day 4 the retailer's export adds a column, `discount_pct`. Will the pipeline break, silently drop the column, or adapt? Auto Loader's answer depends on its **schema evolution mode**.

## Prerequisite state

Video 1 finished: `landing/retail_sales` holds files 1–3, and Bronze/Silver/Gold show **21 rows, 582.80**.

## The new file

[`data/retail_sales_2026-10-04_new_column.csv`](data/retail_sales_2026-10-04_new_column.csv): same columns plus `discount_pct` at the end.

| New file | Rows | Gross revenue (qty × price) | Net revenue (after discount) |
|---|---:|---:|---:|
| `retail_sales_2026-10-04_new_column.csv` | 5 | 142.40 | 123.70 |

| After loading | Rows | Gross | Net (old rows count as 0% discount) |
|---|---:|---:|---:|
| Cumulative | 26 | 725.20 | 706.50 |

Discounts in the file: 10, 0, 25, 20, 0 percent for sales S1022–S1026.

## The four schema evolution modes (the core explanation)

Option: `cloudFiles.schemaEvolutionMode`.

| Mode | New column arrives, what happens | Use it when |
|---|---|---|
| **`addNewColumns`** (default when no schema is given) | The stream **fails once**, the new column is added to the stored schema, and the next run succeeds. Existing column types don't change | You want to adopt new columns, and your job restarts automatically |
| **`rescue`** | Never evolves, never fails. The new column's data goes into the `_rescued_data` column as JSON | You want zero breakage and will review rescued data later |
| **`failOnNewColumns`** | Fails and keeps failing until you update the schema or remove the file | A new column must be a human decision |
| **`none`** | New columns are ignored | You only want the agreed columns |
| `addNewColumnsWithTypeWidening` | Like `addNewColumns`, plus supported type widening. Documented as Public Preview on newer runtimes | Types may widen (for example int to bigint) |

Tell viewers: **Bronze should rarely lose data**, so the usual choices are `addNewColumns` or `rescue`.

## Part A — In a notebook (shows the failure clearly)

Use a new target so video 1's notebook table stays untouched. Reuse the checkpoint pattern, with new paths:

```python
from pyspark.sql.functions import col

base      = "/Volumes/mdlm_db_trial/dev/dev_volume"
landing   = f"{base}/landing/retail_sales"
schema_at = f"{base}/_checkpoints/evo_schema"
ckpt      = f"{base}/_checkpoints/evo_stream"
target    = "mdlm_db_trial.dev.bronze_retail_sales_evo"

def run_once():
    df = (spark.readStream.format("cloudFiles")
          .option("cloudFiles.format", "csv")
          .option("header", "true")
          .option("cloudFiles.schemaLocation", schema_at)
          .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
          .load(landing)
          .select("*", col("_metadata.file_name").alias("source_file")))
    (df.writeStream
       .option("checkpointLocation", ckpt)
       .option("mergeSchema", "true")            # lets the Delta table gain the new column
       .trigger(availableNow=True)
       .toTable(target))

run_once()   # loads files 1-3: 21 rows
```

1. Run it: expect **21 rows**.
2. Upload `retail_sales_2026-10-04_new_column.csv` to `landing/retail_sales`.
3. Run `run_once()` again. **Expect a failure** that mentions an unknown field or schema change: Auto Loader found `discount_pct`, wrote it into the schema location, and stopped.
4. Run `run_once()` again. It now succeeds.

```sql
SELECT source_file, COUNT(*) AS rows, COUNT(discount_pct) AS rows_with_discount
FROM mdlm_db_trial.dev.bronze_retail_sales_evo
GROUP BY 1 ORDER BY 1;
-- 8, 6, 7 rows with 0 discounts (NULL) and 5 rows with discounts: 26 rows in total
```

Old rows show `NULL` in the new column. That is expected: you never rewrite history.

**Rescue-mode variant** (optional, strong visual): change the mode to `"rescue"`, use fresh `_checkpoints/resc_*` paths and a new target, and also add `.option("rescuedDataColumn", "_rescued_data")`. The file loads without any failure, `discount_pct` is **not** a column, and `_rescued_data` holds JSON such as `{"discount_pct":"10","_file_path":"..."}` for the five new rows. Show how you could parse it later.

## Part B — In the pipeline from video 1

1. Reset to the video-1 state: files 1–3 loaded, file 4 not yet uploaded.
2. Upload file 4 and click **Run pipeline**.
3. Expect either an automatic retry that succeeds or a failed update that succeeds when you run it again. The behaviour is documented as "fails once, then works after restart". Say this plainly on camera, and show the update status and event-log message ([lesson 18](../18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md)).
4. Check Bronze. Because it is `SELECT *`, it should now include `discount_pct`.

```sql
DESCRIBE TABLE mdlm_db_trial.dev.bronze_retail_sales;
SELECT source_file, COUNT(*), COUNT(discount_pct) FROM mdlm_db_trial.dev.bronze_retail_sales GROUP BY 1 ORDER BY 1;
```

5. **Silver ignores the new column**, because its `SELECT` lists columns explicitly. That is the lesson: Bronze adapts, but downstream layers change only when you decide. Update Silver and Gold:

```sql
CREATE OR REFRESH MATERIALIZED VIEW silver_retail_sales (
  CONSTRAINT quantity_positive EXPECT (quantity > 0) ON VIOLATION DROP ROW,
  CONSTRAINT sale_id_present   EXPECT (sale_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT discount_valid    EXPECT (discount_pct BETWEEN 0 AND 100) ON VIOLATION DROP ROW
)
AS
SELECT
  sale_id,
  CAST(sale_date  AS DATE)          AS sale_date,
  store_id,
  product_id,
  product_name,
  CAST(quantity   AS INT)           AS quantity,
  CAST(unit_price AS DECIMAL(10,2)) AS unit_price,
  COALESCE(CAST(discount_pct AS DECIMAL(5,2)), 0) AS discount_pct,
  CAST(quantity AS INT) * CAST(unit_price AS DECIMAL(10,2))                         AS gross_revenue,
  CAST(quantity AS INT) * CAST(unit_price AS DECIMAL(10,2))
      * (1 - COALESCE(CAST(discount_pct AS DECIMAL(5,2)), 0) / 100)                 AS net_revenue,
  source_file
FROM bronze_retail_sales;

CREATE OR REFRESH MATERIALIZED VIEW gold_daily_store_sales AS
SELECT sale_date, store_id,
       SUM(quantity)      AS units_sold,
       SUM(gross_revenue) AS gross_revenue,
       SUM(net_revenue)   AS net_revenue
FROM silver_retail_sales
GROUP BY sale_date, store_id;
```

The `discount_valid` expectation also drops rows where `discount_pct` is NULL after the cast, so the `COALESCE` before it matters: it turns NULL into 0 first. If a rehearsal run drops rows you expect to keep, check this.

Run the pipeline. Expected: Silver **26 rows**, gross **725.20**, net **706.50**.

```sql
SELECT COUNT(*) AS rows, SUM(gross_revenue) AS gross, SUM(net_revenue) AS net
FROM mdlm_db_trial.dev.silver_retail_sales;
```

## What to tell viewers

- Schema evolution protects Bronze, and your business logic still needs a deliberate update.
- `addNewColumns` fails once by design. Run production streams as a job or pipeline that restarts automatically.
- Renamed or retyped columns are different problems: a type change like int to string goes to `_rescued_data` or fails, depending on the mode. Do not assume it will "just work".
- Keep the raw file, so you can replay if a schema decision was wrong.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| Failure never goes away | Stream is in `failOnNewColumns`, or schema location was deleted and recreated mid-run |
| New column missing from Bronze | Mode is `none`, a fixed schema was provided (without `schemaHints`), or `mergeSchema` is missing on the Delta sink |
| New column in `_rescued_data` instead | Mode is `rescue` |
| Silver lost rows after the change | A constraint such as `discount_valid` dropped rows with NULL: add `COALESCE` first |
| Numbers differ from the table above | Check old files were not re-ingested (checkpoint/schema location changed) |

Official references: [Auto Loader schema inference and evolution](https://learn.microsoft.com/azure/databricks/ingestion/auto-loader/schema) · [Type widening](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/type-widening)
