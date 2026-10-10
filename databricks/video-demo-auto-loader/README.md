# 19 — Video demo: Auto Loader and a Lakeflow pipeline, step by step

[Learning path](../README.md) · [10 — Volumes](../10_UNITY_CATALOG_VOLUMES_GUIDE.md) · [11 — Lakeflow pipelines](../11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md) · [12 — Auto Loader examples](../12_PIPELINES_CDF_CDC_AUTO_LOADER_EXAMPLES.md) · [18 — Monitoring runbook](../18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md)

Written 10 October 2026 for a YouTube walkthrough. **The sample files and arithmetic were checked locally. The Databricks steps and code were not run in a workspace**, and menu names change between releases, so rehearse the whole thing once before recording and adjust any label that differs.

## The video series

| # | Video | Guide | Sample data |
|---|---|---|---|
| 1 | Auto Loader and a Lakeflow pipeline (this file) | [README.md](README.md) | `data/retail_sales_2026-10-01..03.csv` |
| 2 | Schema evolution: a file arrives with a new column | [02_SCHEMA_EVOLUTION_VIDEO.md](02_SCHEMA_EVOLUTION_VIDEO.md) | `data/retail_sales_2026-10-04_new_column.csv` |
| 3 | CDC: inserts, updates, deletes and out-of-order events with AUTO CDC | [03_CDC_VIDEO.md](03_CDC_VIDEO.md) | `data/cdc/sales_cdc_001.csv`, `sales_cdc_002.csv` |
| 4 | Azure Blob with file-notification (file events) mode | [04_AZURE_FILE_NOTIFICATION_VIDEO.md](04_AZURE_FILE_NOTIFICATION_VIDEO.md) | reuses video 1 files |

## What you will show

"Auto Loader" is Databricks' incremental file ingestion feature (the "data loader" in your notes). You drop files in a folder, and it ingests **only the files it hasn't seen**, remembering progress in a checkpoint. You will:

1. Land one CSV in a Unity Catalog **Volume** and ingest it.
2. Drop two more CSVs later and watch Auto Loader pick them up on the next run, without re-reading the first one.
3. Do it twice: first in a plain **notebook** (the mechanics), then in a **Lakeflow pipeline** (the production style, with Bronze → Silver → Gold).

The story: a small retailer exports daily sales CSVs.

## The three sample files

In [`data/`](data/). Same schema in each.

| File | Rows | Dates | Revenue (quantity × unit_price) | Running rows | Running revenue |
|---|---:|---|---:|---:|---:|
| [`retail_sales_2026-10-01.csv`](data/retail_sales_2026-10-01.csv) | 8 | 2026-10-01 | 172.90 | 8 | 172.90 |
| [`retail_sales_2026-10-02.csv`](data/retail_sales_2026-10-02.csv) | 6 | 2026-10-02 | 202.60 | 14 | 375.50 |
| [`retail_sales_2026-10-03.csv`](data/retail_sales_2026-10-03.csv) | 7 | 2026-10-03 | 207.30 | 21 | 582.80 |

Columns: `sale_id, sale_date, store_id, product_id, product_name, quantity, unit_price`. Sale IDs run S1001–S1021 with no duplicates across files.

Expected revenue by store per day (for the Gold table):

| sale_date | ST01 | ST02 | ST03 |
|---|---:|---:|---:|
| 2026-10-01 | 82.00 | 60.50 | 30.40 |
| 2026-10-02 | 92.70 | 30.90 | 79.00 |
| 2026-10-03 | 43.80 | 112.40 | 51.10 |

## Part 0 — Choose the storage

| | **Unity Catalog Volume** (used here) | **Azure Blob / ADLS** |
|---|---|---|
| Setup | Seconds: it's already in your workspace | Needs a storage credential and external location first |
| Path | `/Volumes/mdlm_db_trial/dev/dev_volume/...` | `abfss://container@account.dfs.core.windows.net/...` |
| Best for | Demos, small files, simplest permissions | Data that already lives in Azure or is written by other systems |

Everything below works the same on Azure storage: only the path changes (see Part 7).

## Part 1 — Prepare the Volume folders

You already have the volume `/Volumes/mdlm_db_trial/dev/dev_volume`. Create folders in a notebook cell:

```python
base = "/Volumes/mdlm_db_trial/dev/dev_volume"
dbutils.fs.mkdirs(f"{base}/landing/retail_sales")      # where the CSVs arrive
dbutils.fs.mkdirs(f"{base}/_checkpoints")              # Auto Loader's memory
display(dbutils.fs.ls(base))
```

Keep checkpoints and schema folders **outside** the landing folder, so Auto Loader never tries to read its own bookkeeping files.

## Part 2 — Land file 1

1. **Catalog → mdlm_db_trial → dev → dev_volume.**
2. Open the `landing/retail_sales` folder, then **Upload to this volume**.
3. Upload `retail_sales_2026-10-01.csv` only. Keep files 2 and 3 on your desktop for later.
4. Check it landed:

```python
display(dbutils.fs.ls("/Volumes/mdlm_db_trial/dev/dev_volume/landing/retail_sales"))
```

## Part 3 — Auto Loader in a notebook (the mechanics)

Create a notebook, attach **serverless** compute, and run:

```python
base      = "/Volumes/mdlm_db_trial/dev/dev_volume"
landing   = f"{base}/landing/retail_sales"
schema_at = f"{base}/_checkpoints/nb_schema"
ckpt      = f"{base}/_checkpoints/nb_stream"
target    = "mdlm_db_trial.dev.bronze_retail_sales_nb"

from pyspark.sql.functions import col

df = (spark.readStream
      .format("cloudFiles")                          # <- this is Auto Loader
      .option("cloudFiles.format", "csv")
      .option("header", "true")
      .option("cloudFiles.schemaLocation", schema_at) # remembers the inferred schema
      .load(landing)
      .select("*", col("_metadata.file_name").alias("source_file")))  # keep the file name

(df.writeStream
   .option("checkpointLocation", ckpt)               # remembers which files are done
   .trigger(availableNow=True)                       # process what's new, then stop
   .toTable(target))
```

Check the result:

```sql
SELECT COUNT(*) AS rows, ROUND(SUM(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE)), 2) AS revenue
FROM mdlm_db_trial.dev.bronze_retail_sales_nb;
-- expected after file 1: 8 rows, 172.9
```

**Talking points:** `cloudFiles` is the Auto Loader format; the **checkpoint** records processed files; `availableNow` makes it a batch-style "catch up then stop" run, which works well on serverless. Columns arrive as text unless you cast them: Bronze keeps the raw shape, so casting happens in Silver.

**Add files 2 and 3.** Upload `retail_sales_2026-10-02.csv` to the same folder, then **re-run the same two cells**. Expected: 14 rows, 375.5. Repeat with file 3: 21 rows, 582.8. Prove it did not re-read old files:

```sql
SELECT source_file, COUNT(*) AS rows
FROM mdlm_db_trial.dev.bronze_retail_sales_nb
GROUP BY 1 ORDER BY 1;
-- 8, 6 and 7 rows: each file counted once
```

The `source_file` column comes from the `_metadata` column Auto Loader exposes; it isn't kept unless you select it, as in the read step above.

## Part 4 — The same thing as a Lakeflow pipeline (production style)

Reset first so the pipeline starts from file 1 only: move files 2 and 3 out of `landing/retail_sales` (delete them from the volume). Leave file 1.

### Create the pipeline

1. **Jobs & Pipelines → Create → ETL pipeline** (the name varies by release).
2. Name: `retail_sales_autoloader_demo`.
3. **Default catalog:** `mdlm_db_trial`. **Default schema:** `dev`.
4. Choose **start with an empty file** and **SQL** as the language (a Python option exists too).
5. Add a source file named `retail_pipeline.sql` and paste the code below.

Remember the rule from lesson 15: a pipeline SQL file may contain **only dataset definitions**, never a bare `SELECT`.

### The code (SQL)

```sql
-- BRONZE: raw files exactly as delivered, loaded incrementally by Auto Loader
CREATE OR REFRESH STREAMING TABLE bronze_retail_sales
COMMENT 'Raw daily sales CSVs, ingested incrementally'
AS
SELECT
  *,
  _metadata.file_name              AS source_file,
  _metadata.file_modification_time AS file_modified_at,
  current_timestamp()              AS ingested_at
FROM STREAM read_files(
  '/Volumes/mdlm_db_trial/dev/dev_volume/landing/retail_sales/',
  format => 'csv',
  header => true
);

-- SILVER: typed, validated rows
CREATE OR REFRESH MATERIALIZED VIEW silver_retail_sales (
  CONSTRAINT quantity_positive EXPECT (quantity > 0) ON VIOLATION DROP ROW,
  CONSTRAINT sale_id_present   EXPECT (sale_id IS NOT NULL) ON VIOLATION DROP ROW
)
COMMENT 'Typed and validated sales lines'
AS
SELECT
  sale_id,
  CAST(sale_date  AS DATE)          AS sale_date,
  store_id,
  product_id,
  product_name,
  CAST(quantity   AS INT)           AS quantity,
  CAST(unit_price AS DECIMAL(10,2)) AS unit_price,
  CAST(quantity AS INT) * CAST(unit_price AS DECIMAL(10,2)) AS line_revenue,
  source_file
FROM bronze_retail_sales;

-- GOLD: ready for a dashboard
CREATE OR REFRESH MATERIALIZED VIEW gold_daily_store_sales
COMMENT 'Revenue and units by store and day'
AS
SELECT
  sale_date,
  store_id,
  SUM(quantity)     AS units_sold,
  SUM(line_revenue) AS revenue
FROM silver_retail_sales
GROUP BY sale_date, store_id;
```

`read_files` with `STREAM` is Auto Loader inside a pipeline: you don't write checkpoints, because the pipeline manages them.

### Run and verify file 1

Click **Run pipeline**. Watch the graph show three datasets (Bronze → Silver → Gold). Then, in the SQL Editor or a notebook:

```sql
SELECT COUNT(*) AS rows, SUM(line_revenue) AS revenue FROM mdlm_db_trial.dev.silver_retail_sales;
-- expected: 8 rows, 172.90

SELECT * FROM mdlm_db_trial.dev.gold_daily_store_sales ORDER BY sale_date, store_id;
-- 2026-10-01: ST01 82.00, ST02 60.50, ST03 30.40
```

### Drop file 2, then file 3

1. Upload `retail_sales_2026-10-02.csv` to `landing/retail_sales`.
2. Click **Run pipeline** again. In the update details, the Bronze table should show about **6 rows written**, not 14: it only read the new file.
3. Expect 14 rows and 375.50 in Silver, and two days in Gold.
4. Repeat with file 3: 21 rows, 582.80.

```sql
SELECT source_file, COUNT(*) AS rows, SUM(line_revenue) AS revenue
FROM mdlm_db_trial.dev.silver_retail_sales
GROUP BY source_file ORDER BY source_file;
-- 8 / 172.90, 6 / 202.60, 7 / 207.30
```

### "Automatically": triggered vs continuous

- **Triggered** (default): the pipeline processes new files each time it runs. Put it on a **schedule** (pipeline or job) so file arrival becomes picked-up-automatically: in the pipeline, choose **Schedule** and set, say, every 15 minutes.
- **Continuous**: the pipeline stays running and ingests files as they arrive. This costs more because compute stays on.
- For a demo, a manual click per file shows the idea clearly. Then show the schedule as the "automatic" version.

## Part 5 — What to say about how Auto Loader knows

- It **lists the folder** (or, with file notifications at larger scale, listens to storage events) and compares against the **checkpoint**, which records files already processed.
- A file that is already processed is skipped even if it is still in the folder.
- It handles schema inference and can evolve when new columns appear (a good follow-up video: add a file with a new column and show the rescued-data column or schema evolution).
- It is built for large numbers of files, but it ingests files, not row-level updates: if a source row changes, you need CDC ([lesson 17](../17_CDF_AND_CDC_EXPLAINED.md)).

## Part 6 — Troubleshooting on camera

| Symptom | Likely cause and fix |
|---|---|
| "X is not supported in a DLT pipeline" | A bare `SELECT` in the pipeline file. Wrap it in a `CREATE OR REFRESH ...` statement |
| Pipeline succeeds but Bronze has 0 rows | Wrong path, or no files in the folder. Run `dbutils.fs.ls` on the path |
| New file not picked up | Pipeline wasn't re-run, the file is in a different folder, or the filename/extension isn't `.csv` |
| Permission denied | Your user lacks `READ VOLUME` / `WRITE VOLUME`, or `USE CATALOG`/`USE SCHEMA` |
| All columns are strings | Expected for raw Bronze; cast in Silver as shown |
| Notebook stream errors on serverless | Use `trigger(availableNow=True)`; the default continuous trigger isn't suited to serverless |
| Re-running re-reads everything | You changed the checkpoint path or reset the pipeline: a new checkpoint means "start over" |

Errors and event log: pipeline update page, then the event log (see [18](../18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md) and [15 §8](../15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md)).

## Part 7 — Using Azure Blob Storage instead

Use **ADLS Gen2** (a storage account with hierarchical namespace) for the cleanest Unity Catalog support.

1. Create a storage account and a container, for example `landing`, and a folder `retail_sales`.
2. In Databricks, **Catalog → External data → Credentials**: create a storage credential backed by an Azure managed identity or access connector. Grant that identity **Storage Blob Data Contributor** on the container in Azure.
3. **External locations → Create**: URL `abfss://landing@<account>.dfs.core.windows.net/`, using that credential. Test the connection.
4. Grant yourself `READ FILES` (and `WRITE FILES` to upload from Databricks) on the external location.
5. Upload the CSVs with the Azure portal, Storage Explorer or `azcopy`.
6. Change only the path:

```python
landing = "abfss://landing@<account>.dfs.core.windows.net/retail_sales"
```

and in SQL replace the `read_files('/Volumes/...')` path with the `abfss://` URL.

For a hands-off setup at scale, Auto Loader can use **file notification mode**, which needs extra Azure permissions and queue/Event Grid resources. For a first video, directory listing mode (the default) is simpler. Detail is in [lesson 13](../13_MANAGED_AND_EXTERNAL_STORAGE_GUIDE.md) and the official docs.

## Part 8 — Clean up after recording

```sql
DROP TABLE IF EXISTS mdlm_db_trial.dev.bronze_retail_sales_nb;
```

Delete the pipeline from **Jobs & Pipelines** (this also removes its tables unless you choose otherwise), then remove `landing/retail_sales` and `_checkpoints` from the volume if you want to start fresh. Dropping a pipeline or schema with `CASCADE` can delete data: check what's inside first.

## Suggested video outline (about 15–20 minutes)

| Time | Chapter | On screen |
|---|---|---|
| 0:00 | Hook: "Stop re-loading your whole data folder" | Folder of files and a counter |
| 0:45 | What Auto Loader is, in one diagram | Landing folder → checkpoint → table |
| 2:00 | Set up the Volume and landing folder | Catalog UI, `mkdirs` cell |
| 3:30 | Upload file 1 | Upload dialog, `ls` output |
| 4:30 | Notebook Auto Loader run | The `cloudFiles` cells; 8 rows, 172.90 |
| 7:00 | Drop files 2 and 3, re-run | 14 then 21 rows; per-file counts |
| 9:30 | Why not a plain `spark.read`? | Re-reads everything, no memory |
| 10:30 | Build the Lakeflow pipeline | Create pipeline, paste SQL, graph view |
| 13:00 | Drop file 2 and 3 into the pipeline | Rows written 6 then 7; Gold table |
| 15:30 | Make it automatic: schedule vs continuous | Schedule dialog |
| 16:30 | Common errors and monitoring | The DLT-statement error; event log |
| 18:00 | Recap and next video: schema evolution and CDC | Summary slide |

## Checks to run before you record

- [ ] Volume path and folder names exist and resolve (`dbutils.fs.ls`).
- [ ] File 1 only is in `landing/retail_sales`.
- [ ] Notebook run gives **8 rows, 172.90**, then 14/375.50 and 21/582.80 after files 2 and 3.
- [ ] Pipeline run gives the same numbers and Gold matches the per-store table above.
- [ ] You know where the event log and the update details are in your version of the UI.
- [ ] No tokens, workspace URLs or personal emails visible on screen. Blur the browser sidebar if needed.

Official references: [Auto Loader](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/) · [read_files](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/read_files) · [Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/) · [Unity Catalog volumes](https://learn.microsoft.com/en-us/azure/databricks/volumes/)
