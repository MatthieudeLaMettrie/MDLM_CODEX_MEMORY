# 15 — Field notes: reading volume files, dropping catalogs/schemas, pipeline SQL errors

[Learning path](README.md) · [10 — Unity Catalog volumes](10_UNITY_CATALOG_VOLUMES_GUIDE.md) · [11 — Lakeflow pipelines](11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md)

Practical answers from a hands-on session on 8 October 2026 in an Azure Databricks trial workspace (serverless, Unity Catalog). Names below come from that workspace: catalog `mdlm_db_trial`, schemas `dev`, `uat`, `prod`, `default`, volume `dev_volume`, file `fct_retail_sales_item_v.xlsx` (5.19 KB). **Syntax is from general Databricks knowledge and was not executed or re-checked against current docs in the session; verify in your workspace.**

## 1. Reading a file from a volume in a notebook

A volume is exposed as an ordinary path: `/Volumes/<catalog>/<schema>/<volume>/<file>`. Copy it from Catalog → the volume → Files → `⋮` on the file → **Copy volume path**. List contents with `display(dbutils.fs.ls("/Volumes/mdlm_db_trial/dev/dev_volume/"))`.

`spark.read` has **no built-in `.xlsx` reader** in the classic sense, so `df = spark.read.` alone cannot load an Excel file.

**Excel via pandas, then Spark (works on serverless):**

```python
import pandas as pd

path = "/Volumes/mdlm_db_trial/dev/dev_volume/fct_retail_sales_item_v.xlsx"
pdf = pd.read_excel(path, engine="openpyxl")   # sheet_name="Sheet1" if needed
df = spark.createDataFrame(pdf)
display(df)
```

If `openpyxl` is missing, run `%pip install openpyxl` first.

**Native Excel reader (newer runtimes; try it, fall back to pandas if the format is not recognised):**

```python
df = (spark.read.format("excel")
      .option("headerRows", 1)
      .load("/Volumes/mdlm_db_trial/dev/dev_volume/fct_retail_sales_item_v.xlsx"))
```

**CSV / Parquet:**

```python
df = spark.read.csv("/Volumes/.../file.csv", header=True, inferSchema=True)
df = spark.read.parquet("/Volumes/.../file.parquet")
```

## 2. Dropping a catalog

```sql
DROP CATALOG IF EXISTS mdlm_db_trial;          -- fails if schemas exist
DROP CATALOG IF EXISTS mdlm_db_trial CASCADE;  -- deletes everything inside
```

UI: Catalog → select catalog → `⋮` → **Delete** (tick the delete-contents option for CASCADE behaviour).

- Needs catalog owner or metastore admin.
- Cannot drop the catalog currently in use: `USE CATALOG` another first.
- `CASCADE` permanently removes schemas, tables **and volumes (including uploaded files)**. Managed data is removed too, recoverable only for a limited period.
- Built-in/legacy catalogs (`system`, `samples`, `hive_metastore`) are not droppable this way.
- Foreign and Delta Sharing catalogs: dropping removes the link, not the source data.

## 3. Dropping a schema only

```sql
DROP SCHEMA mdlm_db_trial.uat;                          -- fails if not empty
DROP SCHEMA IF EXISTS mdlm_db_trial.uat CASCADE;        -- deletes contents
```

UI: Catalog → catalog → schema → `⋮` → **Delete**.

- Needs ownership or sufficient privileges on the schema; `USE SCHEMA default` first if you are inside it.
- In the observed workspace `prod` and `uat` were empty, so a plain `DROP SCHEMA` works; `dev` held `dev_volume`, so it needs `CASCADE`, which deletes the volume and file.
- `information_schema` is system-managed and cannot be dropped.
- To remove only a volume: `DROP VOLUME mdlm_db_trial.dev.dev_volume;`

## 4. Pipeline error: statement "is not supported in a DLT pipeline"

Observed error (class `_LEGACY_ERROR_TEMP_54_UNSUPPORTED_SQL_COMMAND`, SQL state `0A000`):

> The following code at …/transformations/my_transformation.sql [cell: 0] [line: 0] is not supported in a DLT pipeline: `SELECT * FROM mdlm_db_trial.dev.fct_re...` Please correct your code and make sure you only have DLT statements. DLT currently accepts `CREATE MATERIALIZED VIEW`, `CREATE STREAMING TABLE`, `APPLY CHANGES INTO`, and `SET`.

**Cause:** a pipeline source file may only *define datasets*. A bare `SELECT` (also `DROP`, `INSERT`, `USE`, `DESCRIBE`) is rejected.

**Fix:** wrap the query in a dataset definition.

```sql
CREATE OR REFRESH MATERIALIZED VIEW fct_retail_sales_item_mv
AS
SELECT * FROM mdlm_db_trial.dev.fct_retail_sales_item_v;
```

For append-only streaming sources use `CREATE OR REFRESH STREAMING TABLE … AS SELECT * FROM STREAM(…)`.

- The dataset lands in the pipeline's configured target catalog/schema unless you fully qualify the name.
- To explore with plain `SELECT`, use the SQL Editor or a normal notebook, not a pipeline file. A notebook inside a pipeline folder showing an **Excluded** badge is not part of the pipeline's source set.
- An `.xlsx` in a volume cannot be queried from SQL directly. Load it (section 1), then `df.write.saveAsTable("mdlm_db_trial.dev.<table>")` and reference that table from the pipeline.

See [11 — Lakeflow pipelines](11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md) for the current Lakeflow Spark Declarative Pipelines naming and dataset types.
