# Video 3 — CDC with Auto Loader and AUTO CDC: inserts, updates, deletes and out-of-order events

[Back to video 1](README.md) · [Previous: video 2 — schema evolution](02_SCHEMA_EVOLUTION_VIDEO.md) · [Next: video 4 — file notifications](04_AZURE_FILE_NOTIFICATION_VIDEO.md) · [CDF and CDC explained](../17_CDF_AND_CDC_EXPLAINED.md)

Written 10 October 2026. **Not run in a workspace.** The sample data and the expected results were computed locally with a small simulation of "latest sequence wins". The `AUTO CDC` syntax is from memory of the documentation and must be rehearsed: the older spelling is `APPLY CHANGES INTO` (see the fallback below).

## The story

Videos 1–2 added new rows. Real systems also **correct** and **delete** rows. A source database exports its changes as CSV files: each line says what happened (`INSERT`, `UPDATE`, `DELETE`) and carries a **sequence number** saying in what order. Auto Loader ingests the files, and AUTO CDC turns the stream of changes into the right current table, even when an old event arrives late.

## The sample files

In [`data/cdc/`](data/cdc/). Columns: `sale_id, operation, sequence_num, sale_date, store_id, product_id, quantity, unit_price`.

**File 1: [`sales_cdc_001.csv`](data/cdc/sales_cdc_001.csv)**: five inserts.

| sale_id | operation | seq | qty | price |
|---|---|---:|---:|---:|
| S2001 | INSERT | 1 | 2 | 24.50 |
| S2002 | INSERT | 2 | 3 | 3.20 |
| S2003 | INSERT | 3 | 4 | 6.00 |
| S2004 | INSERT | 4 | 1 | 4.80 |
| S2005 | INSERT | 5 | 6 | 3.90 |

After file 1: **5 rows, revenue 110.80**.

**File 2: [`sales_cdc_002.csv`](data/cdc/sales_cdc_002.csv)**: an update, a delete, a new insert and a **stale** event.

| sale_id | operation | seq | what happens |
|---|---|---:|---|
| S2002 | UPDATE | 6 | quantity 3 → **5** |
| S2004 | DELETE | 7 | row removed |
| S2006 | INSERT | 8 | new row, qty 1 at 24.50 |
| S2005 | UPDATE | **3** | **stale**: sequence 3 is older than the insert at sequence 5, so it must be ignored |

After file 2 the current table should contain **5 rows** (S2001, S2002, S2003, S2005, S2006), revenue **136.90**:

| sale_id | qty | price | revenue |
|---|---:|---:|---:|
| S2001 | 2 | 24.50 | 49.00 |
| S2002 | 5 | 3.20 | 16.00 |
| S2003 | 4 | 6.00 | 24.00 |
| S2005 | 6 | 3.90 | 23.40 |
| S2006 | 1 | 24.50 | 24.50 |

S2004 is gone, S2002 shows the corrected quantity, and S2005 still shows 6, not 9.

## Setup

1. Create a folder `landing/sales_cdc` in `dev_volume` and upload **file 1 only**.
2. Create a **new pipeline**, `cdc_sales_demo`, with default catalog `mdlm_db_trial` and schema `dev`. Use a separate pipeline from video 1 so the two demos don't interfere.

## The pipeline code (SQL)

```sql
-- BRONZE: the raw change log, appended as files arrive
CREATE OR REFRESH STREAMING TABLE bronze_sales_cdc
COMMENT 'Raw CDC events from CSV files'
AS
SELECT
  sale_id,
  operation,
  try_cast(sequence_num AS INT)        AS sequence_num,
  try_cast(sale_date    AS DATE)       AS sale_date,
  store_id,
  product_id,
  try_cast(quantity     AS INT)        AS quantity,
  try_cast(unit_price   AS DECIMAL(10,2)) AS unit_price,
  _metadata.file_name                  AS source_file
FROM STREAM read_files(
  '/Volumes/mdlm_db_trial/dev/dev_volume/landing/sales_cdc/',
  format => 'csv',
  header => true
);

-- SILVER: current state, maintained by AUTO CDC (SCD type 1)
CREATE OR REFRESH STREAMING TABLE silver_sales_current;

CREATE FLOW sales_cdc_flow AS AUTO CDC INTO silver_sales_current
FROM STREAM(bronze_sales_cdc)
KEYS (sale_id)
APPLY AS DELETE WHEN operation = 'DELETE'
SEQUENCE BY sequence_num
COLUMNS * EXCEPT (operation, sequence_num, source_file)
STORED AS SCD TYPE 1;

-- GOLD: a simple revenue view on the current state
CREATE OR REFRESH MATERIALIZED VIEW gold_cdc_store_revenue AS
SELECT store_id, SUM(quantity) AS units, SUM(quantity * unit_price) AS revenue
FROM silver_sales_current
GROUP BY store_id;
```

The Bronze casts are a deliberate demo shortcut: `AUTO CDC` needs a sortable `sequence_num`. `try_cast` returns NULL instead of failing on the empty values in the DELETE row.

**If `AUTO CDC` isn't recognised in your workspace**, use the older form:

```sql
CREATE OR REFRESH STREAMING TABLE silver_sales_current;

APPLY CHANGES INTO silver_sales_current
FROM STREAM(bronze_sales_cdc)
KEYS (sale_id)
APPLY AS DELETE WHEN operation = 'DELETE'
SEQUENCE BY sequence_num
COLUMNS * EXCEPT (operation, sequence_num, source_file)
STORED AS SCD TYPE 1;
```

Check lesson 11 and the current docs for which spelling your runtime expects. AUTO CDC may need a supported pipeline edition or serverless pipeline.

## Run 1: file 1

Run the pipeline, then check:

```sql
SELECT COUNT(*) AS rows, SUM(quantity * unit_price) AS revenue FROM mdlm_db_trial.dev.silver_sales_current;
-- expected: 5 rows, 110.80
```

## Run 2: file 2

Upload `sales_cdc_002.csv` and run the pipeline again.

```sql
SELECT * FROM mdlm_db_trial.dev.silver_sales_current ORDER BY sale_id;
-- expected: S2001, S2002 (qty 5), S2003, S2005 (qty 6), S2006: 5 rows, revenue 136.90

SELECT sale_id, operation, sequence_num, source_file
FROM mdlm_db_trial.dev.bronze_sales_cdc ORDER BY sequence_num;
-- the change log keeps all 9 events: 5 + 4
```

Point out on screen:

- **S2002** was updated by seq 6.
- **S2004** has no row in Silver: the DELETE at seq 7 won, even though Bronze still holds its INSERT.
- **S2005** kept quantity 6: the arrival of the "UPDATE seq 3" was ignored because seq 5 is newer. That is why you need `SEQUENCE BY`.
- **Bronze never forgets:** it is your audit log and replay source.

## The experiment that sells the video

"What if we ordered by arrival time instead?" Explain that the file 2 stale event would then overwrite S2005 with quantity 9, and a replayed old insert could resurrect a deleted row. A correct sequence column is the whole contract.

## Optional: SCD type 2 (history)

Add a second target to keep history instead of just the latest version:

```sql
CREATE OR REFRESH STREAMING TABLE silver_sales_history;

CREATE FLOW sales_history_flow AS AUTO CDC INTO silver_sales_history
FROM STREAM(bronze_sales_cdc)
KEYS (sale_id)
APPLY AS DELETE WHEN operation = 'DELETE'
SEQUENCE BY sequence_num
COLUMNS * EXCEPT (operation, sequence_num, source_file)
STORED AS SCD TYPE 2;
```

Expect `__START_AT` / `__END_AT` columns. S2002 should have two versions (qty 3 then 5). I have **not** asserted row counts for this variant: how deletes and the out-of-order event appear in history should be verified on screen before you explain it.

## Optional: expose changes to others with CDF

Add `TBLPROPERTIES (delta.enableChangeDataFeed = true)` to the Silver table definition, then read `table_changes('mdlm_db_trial.dev.silver_sales_current', <from_version>)`. Support and behaviour for AUTO CDC targets have limits, so follow [lesson 12](../12_PIPELINES_CDF_CDC_AUTO_LOADER_EXAMPLES.md) and [lesson 16](../16_CDC_CDF_RETAIL_TABLE_WALKTHROUGH.md) and rehearse it first.

## What to tell viewers

- Auto Loader solves "which files are new". AUTO CDC solves "which rows are current". They compose.
- A CDC feed needs a **key**, an **operation** and a trustworthy **sequence**.
- Don't confuse this with ordinary `INSERT`-only files from video 1.
- CDC extraction from a real database needs a connector. This demo fakes the output as files.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| "not supported in a DLT pipeline" | A bare `SELECT` in the file; wrap it in a `CREATE` statement |
| `AUTO CDC` syntax error | Use `APPLY CHANGES INTO`, or check the pipeline edition/runtime |
| Delete row fails to load | Strict casting of empty fields: use `try_cast` as shown |
| S2005 shows quantity 9 | Sequence not used, or `SEQUENCE BY` ordered by the wrong column |
| Deleted row still present | The `APPLY AS DELETE WHEN` condition doesn't match the exact `operation` text (case, spaces) |
| Bronze has fewer rows than expected | Check `landing/sales_cdc` has both files and the pipeline was re-run |

Official references: [AUTO CDC](https://learn.microsoft.com/en-us/azure/databricks/ldp/cdc) · [Delta Change Data Feed](https://learn.microsoft.com/en-us/azure/databricks/tables/features/change-data-feed)
