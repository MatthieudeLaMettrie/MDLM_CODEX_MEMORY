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

## 7. Using Genie Code to build, fix and review pipelines

Researched 8 October 2026 from Databricks documentation search results. **Nothing was run or tried in a workspace.** Agent mode for pipelines is documented as **Public Preview** and needs partner-powered AI features enabled for the account and workspace; check the full requirements page.

**Two similarly named tools:**

| Tool | Where | Purpose |
|---|---|---|
| **Genie Agents** (formerly Genie spaces) | Left sidebar | Business users ask data questions in plain English and get SQL answers/charts. Does not build or fix pipelines |
| **Genie Code** | Pipeline editor, notebooks, SQL Editor | AI coding assistant; **Agent mode** plans, writes, runs and fixes code |

A third-party blog says Genie Code replaced Databricks Assistant in March 2026. This was not confirmed on Databricks' own pages, so treat it as unverified.

**What Agent mode can do (Lakeflow Spark Declarative Pipelines / Lakeflow Pipelines Editor):**
- Create a pipeline: explore data, generate code, run updates and iterate from one prompt.
- Fix a failing pipeline: diagnose errors and work through multiple files until resolved.
- Change an existing pipeline: add tables, transformations or expectations.
- Migrate dbt and Informatica projects into a pipeline (Beta). Other SQL dialects use a separate code-converter tool.
- In notebooks and the SQL Editor: data exploration and analysis.

**How:** open the pipeline in the Lakeflow Pipelines Editor, open the Genie Code panel, switch to **Agent mode**, give a specific prompt, review and approve its plan, let it run an update, then check the diff.

Example prompts:
- "Create a pipeline that reads `mdlm_db_trial.dev.fct_retail_sales_item_v`, cleans it into a Silver materialized view, and adds a Gold daily sales summary."
- "The last update failed. Diagnose the error and fix it."
- "Add expectations that fail the update if `order_id` is null or `amount` is negative."

**Monitoring and optimisation:** no dedicated feature was found in the sources. It can still be asked in chat (for example to write an event-log query or suggest query changes), but treat answers as suggestions and verify them with the Spark UI and your own measurements ([14](14_PIPELINE_OPERATIONS_AND_OPTIMISATION.md)).

**Safety:** it only acts within your permissions; use dev first; read generated code before running (watch `DROP`, full refresh, deletes); do not paste secrets; verify data with counts and reconciliation rather than "no errors".

Sources: [Use Genie Code for pipeline development](https://docs.databricks.com/aws/en/ldp/de-agent) · [Genie Code overview](https://docs.databricks.com/genie-code)

## 8. Where to see errors: the event log, notebook output and job runs

Where you look depends on what ran. UI labels change between releases and this was **not verified in a workspace**, so confirm the names in yours.

| What ran | Where to see the error |
|---|---|
| **Pipeline (Lakeflow / DLT)** | Open the pipeline in **Jobs & Pipelines**. Select an update to see its state and error message, click a failed table in the pipeline graph for its details, and use the **event log / logs** panel for the full list of events. The Lakeflow Pipelines Editor shows errors for the latest run beside the code |
| **Pipeline event log as a table** | Query it with SQL (below). It can be published to a Unity Catalog table through the pipeline's settings so it can be queried and alerted on long term |
| **Notebook run interactively** | There is no event log. The error appears in the failing cell's output, which shows the first error and the Python/Spark stack trace. Use the **Spark UI** and **driver logs** on the compute for lower-level detail |
| **Notebook or task run by a job** | **Jobs & Pipelines → Jobs → the job → Runs → the run**. The task output shows the error and the executed notebook with its cell output |
| **Notebook that is a pipeline source file** | Its errors appear in the **pipeline** update and event log, not as ordinary cell output. A bare `SELECT` there gives the "not supported in a DLT pipeline" error (see section 4 above) |
| **SQL query** | **Query History** shows the failed statement, error message and duration |
| **Delta table changes** | `DESCRIBE HISTORY <table>` or Catalog → table → **History** |

**Querying a pipeline's event log:**

```sql
-- by pipeline ID (copy it from the pipeline's settings or URL)
SELECT timestamp, event_type, level, message
FROM event_log("<pipeline_id>")
WHERE level IN ('ERROR', 'WARN')
ORDER BY timestamp DESC
LIMIT 50;

-- by table, where the event log is published or the table is owned by the pipeline
SELECT * FROM event_log(TABLE(mdlm_db_trial.dev.my_materialized_view)) ORDER BY timestamp DESC LIMIT 20;
```

Run `SELECT * ... LIMIT 5` first to confirm field names in your version. Further queries and a troubleshooting sequence are in [18 — Monitoring and troubleshooting runbook](18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md).

**Practical order:** read the first ERROR in the pipeline update, then look at the failing table's details, then query the event log for the full chain. Read the *earliest* error: later errors are usually consequences.
