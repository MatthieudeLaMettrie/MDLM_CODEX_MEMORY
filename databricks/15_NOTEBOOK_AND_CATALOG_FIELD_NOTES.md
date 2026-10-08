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

## 5. Seeing the operations on a table

"Operation" can mean two things.

**Which operations were run on the table (Delta history):**

```sql
DESCRIBE HISTORY mdlm_db_trial.dev.fct_retail_sales_item_v LIMIT 5;
```

One row per commit: `version`, `timestamp`, `userName`, `operation` (`CREATE TABLE`, `WRITE`, `MERGE`, `UPDATE`, `DELETE`, `OPTIMIZE`, `VACUUM`…), `operationParameters`, `operationMetrics` (rows inserted/updated/deleted, files written). UI: Catalog → table → **History** tab. Delta tables only: a view has no history, so run it on the underlying table. Check what an object is with `DESCRIBE EXTENDED <name>`.

**Which rows were inserted, updated or deleted (Change Data Feed):** must be enabled *before* the changes you want to see.

```sql
SHOW TBLPROPERTIES mdlm_db_trial.dev.fct_retail_sales_item_v;
ALTER TABLE mdlm_db_trial.dev.fct_retail_sales_item_v
  SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
SELECT * FROM table_changes('mdlm_db_trial.dev.fct_retail_sales_item_v', 1, 5);
```

`_change_type` holds `insert`, `update_preimage`, `update_postimage` or `delete`. If you land your own CDC feed with an `operation` column, it is an ordinary column: `SELECT operation, COUNT(*) FROM feed GROUP BY operation`. See [17 — CDF and CDC explained](17_CDF_AND_CDC_EXPLAINED.md).

## 6. Publishing an AI/BI dashboard beyond Databricks

Researched 8 October 2026 from Databricks documentation search results; **no dashboard was published or embedded in this session**, so verify the steps in your workspace and with your admin.

| Option | What it does | Notes |
|---|---|---|
| **Publish and share inside Databricks** | Viewers open the published dashboard in the workspace | Publish with *shared data permissions* (queries run with the publisher's credentials) or *individual permissions* (each viewer needs access to the underlying data) |
| **Embed with an iframe** | Puts the published dashboard in an external website or application | Only **published** dashboards can be embedded. A workspace admin must first define the allowed embedding surfaces. Users with at least CAN EDIT generate the iframe code from the **Share** dialog (an `/embed/dashboardsv3/` URL on your workspace host). Sharing settings still apply: viewers need explicit access, and basic embedding means viewers sign in with their Databricks credentials |
| **Scheduled email subscriptions** | Emails a PDF/image snapshot of the dashboard on a schedule | Controlled by a workspace setting (dashboard email subscriptions). Subscriber limits apply (a Databricks reply mentioned 100). Scheduled subscriptions cannot set per-recipient filters, so use row-level security on the dataset for per-person views |
| **Download PDF** | Manual export from the dashboard UI | At the time of the source thread there was no PDF export API; check current docs |
| **Link or screenshot** | Share the workspace URL | Recipients still need workspace access |

**SharePoint:** the likely route is the iframe/embed approach, with SharePoint's embed web part, which typically requires the host domain to be approved. This part is *unverified*: confirm with your SharePoint and Databricks admins, and expect viewers to need Databricks access. **Public anonymous viewing** is not the default: the documented model requires explicit access or a separately configured OAuth/service-principal pattern (described in a third-party article, not official docs).

Dashboards are separate from Power BI: to publish in Power BI, connect Power BI to the tables instead, or embed the Databricks dashboard link or iframe.

Sources: [Embed a dashboard (Microsoft Learn)](https://learn.microsoft.com/en-ca/azure/databricks/dashboards/embed) · [Embed a dashboard (Databricks docs)](https://docs.databricks.com/aws/en/dashboards/embedding/) · [Dashboard email subscriptions setting (SDK docs)](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/settings/dashboard_email_subscriptions.html)
