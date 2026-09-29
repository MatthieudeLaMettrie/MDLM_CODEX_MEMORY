# dbt Cloud with BigQuery: setup and deployment field guide

Updated: 2026-09-29. This is a living guide; add later findings and verified fixes below.

## The four names that matter

| Layer | This project | Meaning |
| --- | --- | --- |
| Google Cloud project | `fei-website-f16b0` | BigQuery billing, jobs, and datasets |
| dbt Cloud project | `TEST_ANALYTICS` | Repository, connections, and environments |
| dbt project name | `fei_dbt` | `name:` in `dbt_project.yml`; also the key under `models:` |
| BigQuery dataset | `FEI_ADMIN_PORTAL`, `dbt_fei_mdelamettrie`, `DBT_FEI_PROD` | A dataset is what dbt calls a schema |

These names are examples from the 2026-09-29 setup. Check current values before copying them into another project.

## Architecture

```mermaid
flowchart LR
  G[Git repository main branch] --> P[dbt Cloud project TEST_ANALYTICS]
  P --> D[Development environment / Studio]
  P --> J[Production deployment job]
  S[BigQuery source dataset FEI_ADMIN_PORTAL] --> D
  S --> J
  D --> DV[Development dataset dbt_fei_mdelamettrie]
  J --> PR[Production dataset DBT_FEI_PROD]
```

Studio commands use development credentials. A production job clones a committed Git branch and uses its deployment environment credentials. A successful Studio run alone does not publish code or build production objects.

## 1. Prepare BigQuery and identity

1. Confirm the source dataset and table, here `fei-website-f16b0.FEI_ADMIN_PORTAL.FEI_TRAFFIC_NAMED`.
2. In BigQuery, open the source dataset **Details** and record its exact **Data location**. Here it is `australia-southeast1`.
3. Create or select separate development and production output datasets in that same location. Here the development dataset is `dbt_fei_mdelamettrie`; production is `DBT_FEI_PROD`. A BigQuery project cannot contain two datasets with the same ID in different locations.
4. An existing dedicated service account can be reused. The example account is `dbt-fei-sa@fei-website-f16b0.iam.gserviceaccount.com`. It needs permission to create BigQuery jobs, read the source, and write to the output datasets. A typical starting point is **BigQuery Job User** on the project and **BigQuery Data Editor** on the output datasets, with appropriate read access to sources. Scope permissions to the actual datasets where possible.
5. For **Service Account JSON** authentication, create a JSON key for that service account only if organizational policy permits it. Upload it to dbt Cloud credentials. Keep keys out of Git, screenshots, chat, and `profiles.yml`. Workload Identity Federation is an alternative enterprise setup involving an identity provider and Google workload identity pool; it is not interchangeable with simply selecting the dropdown option.

## 2. Configure dbt Cloud

1. Under **Settings → Connections**, create a **BigQuery** connection, choose **Service Account JSON** for deployment authentication, set project ID `fei-website-f16b0`, and upload the key. Set **Location** to the source dataset location where the connection or credential offers that field.
2. Under **Settings → Projects**, connect the Git repository and BigQuery connection.
3. Set **Project subdirectory** based on the Git repository layout, **not its repository name or how Studio labels its top folder**:

   | Path on the deployment branch | Project subdirectory |
   | --- | --- |
   | `dbt_project.yml` | Leave blank |
   | `dbt_cert/dbt_project.yml` | `dbt_cert` |

   In this case the private `dbt_cert` repository's `main` branch has `dbt_project.yml` at the root, so the field must be **blank**. Setting it to `dbt_cert` caused the deployment job's “valid dbt project was not found” error.
4. Under **Your profile → Credentials**, edit the development credentials for `TEST_ANALYTICS`. Use **Service Account JSON** and set **Dataset** to `dbt_fei_mdelamettrie`. Save and test the connection. Creating a dataset in BigQuery does not update this field automatically.
5. Configure a separate production deployment environment, here `dbt_Prod_FEI`, with a deployment credential whose **Dataset** is `DBT_FEI_PROD`. Confirm its branch and BigQuery location. The production output dataset must be in `australia-southeast1` to build views over the source.

dbt Cloud manages the connection profile for its hosted runs. A local `profiles.yml` is only needed for local command-line development; never commit credentials or service-account key material in it.

## 3. Define and test the source

In `models/Bronze/sources.yml`:

```yaml
version: 2

sources:
  - name: fei_sources
    database: fei-website-f16b0
    schema: FEI_ADMIN_PORTAL
    tables:
      - name: FEI_TRAFFIC_NAMED
```

In `models/Bronze/fei_source_test.sql`:

```sql
{{ config(materialized='view') }}

select *
from {{ source('fei_sources', 'FEI_TRAFFIC_NAMED') }}
```

The `{{ ... }}` is essential: without it, BigQuery receives `source(...)` as SQL and reports **“Table-valued function not found: source.”** The source and table arguments must match the YAML `name` values. `database` is the BigQuery project; `schema` is the BigQuery dataset.

In `dbt_project.yml`, the key below `models:` must match the project's `name:` exactly. Folder keys configure existing folders; they do not create scaffolding:

```yaml
name: fei_dbt

models:
  fei_dbt:
    Bronze:
      +materialized: view
    Silver:
      +materialized: view
    Gold:
      +materialized: view
```

Create the `models/Bronze`, `models/Silver`, and `models/Gold` folders yourself. Folder capitalization must match the configuration.

### Bronze, Silver, and Gold model layout

This project can use the medallion names instead of `staging`, `intermediate`, and `marts`. They describe the transformation stages; dbt only requires that model files live under `model-paths` and that folder-specific YAML configuration matches the actual paths.

```text
models/
├── Bronze/
│   ├── sources.yml
│   └── br_fei_traffic.sql
├── Silver/
│   └── sl_fei_traffic_clean.sql
└── Gold/
    └── gd_traffic_summary.sql
```

| Folder | Role | Reference pattern |
| --- | --- | --- |
| Bronze | One source-aligned model per raw table; basic renaming, casting, and source checks | `{{ source('fei_sources', 'FEI_TRAFFIC_NAMED') }}` |
| Silver | Clean, deduplicate, standardize, and combine Bronze models for reuse | `{{ ref('br_fei_traffic') }}` |
| Gold | Business-ready tables/views and aggregates for reporting | `{{ ref('sl_fei_traffic_clean') }}` |

The raw BigQuery table stays in `FEI_ADMIN_PORTAL`; a Bronze model is a dbt-built view or table over it. Folder names alone do **not** create separate BigQuery datasets. With the current settings, all three layers build into the target dataset for that environment: `dbt_fei_mdelamettrie` in development or `DBT_FEI_PROD` in production. If separate Bronze/Silver/Gold datasets are needed later, design explicit `+schema` settings and check dbt's default custom-schema naming behavior before deployment.

`fei_source_test.sql` is the current proof-of-connection model. It can be renamed to a descriptive Bronze model once downstream models use `ref()` to express dependencies. Folder names and model names need not match one another.

### The equivalent staging / intermediate / marts vocabulary

Keep both vocabularies in mind. They describe broadly similar progression, but are not rigid one-to-one translations:

| Medallion term | Common dbt term | Typical file names and purpose |
| --- | --- | --- |
| Bronze | `staging` | `stg_fei__traffic.sql`: source-aligned, mostly one model per source table; select, rename, cast, and document fields |
| Silver | `intermediate` | `int_traffic_enriched.sql`: deduplicate, join, and apply reusable business logic |
| Gold | `marts` | `dim_visitor.sql`, `fct_traffic.sql`: business entities, facts, dimensions, and reporting aggregates |

`stg_`, `int_`, `dim_`, and `fct_` are **model naming conventions**, not dbt commands. You can keep `Bronze/Silver/Gold` as the actual folders and use these prefixes where they clarify a model's role:

```text
models/
├── Bronze/stg_fei__traffic.sql
├── Silver/int_traffic_enriched.sql
└── Gold/
    ├── dim_visitor.sql
    └── fct_traffic.sql
```

For a small project, one Bronze source model and one Gold reporting model may be sufficient; add Silver when reusable cleaning or joins justify it. dbt's [project structure guidance](https://docs.getdbt.com/best-practices/how-we-structure/2-staging) uses staging as the source-facing layer.

In Studio, save the files and run:

```bash
dbt build --select fei_source_test
```

`dbt build` runs selected models and their tests. `dbt run --select fei_source_test` builds just the selected model.

## 4. Publish code, then run production

1. Test in the development environment and confirm the result in `dbt_fei_mdelamettrie`.
2. In **Studio → Version control**, commit and sync the project files. An **A** beside a file means it was added in the workspace; the production job cannot see it until it is committed to the branch it clones. If `main` is protected, commit to a new branch and merge a pull request into the production branch.
3. Open the connected Git repository on the production branch. Confirm that `dbt_project.yml`, `models/Bronze/sources.yml`, and the SQL model are present. Check the exact path of `dbt_project.yml` against the Project subdirectory setting.
4. In **Orchestration → Jobs**, configure a deploy job for `dbt_Prod_FEI` with command `dbt build` and select **Run now**. Schedule it only after an initial successful run.
5. Verify that the job completed and the view or table appeared in `DBT_FEI_PROD`.

The Studio **“Defer to: DEV”** selector affects dependency resolution during development. It does not switch the Studio command bar into the production environment.

## 5. Running production with dbt Core instead of dbt Cloud jobs

dbt Core executes transformations but does not host a scheduler or deployment environment. In a Core-only setup, Git distributes code, a `profiles.yml` target selects the BigQuery destination, and an external runner (for example, a CI pipeline or scheduled VM/container) invokes dbt. Pushing Git code and building BigQuery objects are separate operations.

**Choose commands for the environment where they run.** The `--target dev` and `--target prod` examples below apply only to an external dbt Core profile that actually defines outputs with those names. In dbt Cloud Studio, use the command bar **without** those flags; Studio uses its own generated profile and development credentials. On 2026-09-29, a Studio/Fusion `dbt seed --select actions --target dev` failed with `target 'dev' not found in profile 'user'`. The fix in Studio is `dbt seed --select actions`, not a change to the BigQuery dataset.

### Prepare the runner

1. Keep `dbt_project.yml` and models committed on the production branch. A local development run can use uncommitted files; a production runner should check out a specific commit from the approved branch.
2. Install compatible `dbt-core` and `dbt-bigquery` versions on the runner and keep them pinned together. Make sure the runner starts in the directory containing `dbt_project.yml` (the root of the current `dbt_cert` repository).
3. Give the runner an identity with permission to run BigQuery jobs, read `FEI_ADMIN_PORTAL`, and write to `DBT_FEI_PROD`. Supply credentials through the runner's secret store or workload identity. Never commit a JSON key. Keep the production BigQuery job location at `australia-southeast1`.
4. Configure a `profiles.yml` **outside the Git repository**. Its top-level key must match `profile:` in `dbt_project.yml`; this project currently says `profile: 'default'`. Example using an externally supplied key-file path:

```yaml
default:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: fei-website-f16b0
      dataset: dbt_fei_mdelamettrie
      keyfile: "{{ env_var('DBT_BIGQUERY_KEYFILE') }}"
      location: australia-southeast1
      threads: 4
    prod:
      type: bigquery
      method: service-account
      project: fei-website-f16b0
      dataset: DBT_FEI_PROD
      keyfile: "{{ env_var('DBT_BIGQUERY_KEYFILE') }}"
      location: australia-southeast1
      threads: 4
```

The example assumes `DBT_BIGQUERY_KEYFILE` points to a key file mounted outside the repository. Use separate development and production identities when available; the runner may inject different key paths for each environment. A keyless identity method needs its own adapter-specific profile settings.

### Promote and execute

1. On a development machine, work on a branch and run `dbt build --target dev --profiles-dir <secure-profile-directory>`.
2. Commit the tested code and merge it into the production branch. `git push` publishes code; it does not execute dbt.
3. Have the production runner check out the approved commit, provide its credentials and profile, then run these commands from the project root:

```bash
dbt deps --target prod --profiles-dir <secure-profile-directory>
dbt build --target prod --profiles-dir <secure-profile-directory>
```

4. Schedule or trigger that runner through your chosen orchestrator, preserve logs and artifacts, and alert on a nonzero exit code. Verify the model output in `DBT_FEI_PROD`.

The `--target prod` flag selects the `prod` output in `profiles.yml`; it is the critical switch between the development and production datasets. A manual `dbt build --target prod` is possible on a machine with production credentials, but routine production execution should use a controlled runner so code version, identity, schedule, logs, and retries are repeatable. See dbt's [profile and target documentation](https://docs.getdbt.com/docs/local/profiles.yml).

### Small reference lists as dbt Core seeds

For a short, relatively static action list, create `seeds/actions.csv` in the dbt project:

```csv
action
Vue Page
Vue Article
Download Doc
Lead Doc
Contact
Newsletter
Commentaire
Action
```

The first line is the **column header**; the last `Action` is a data value, matching the supplied list. If the last `Action` was accidental, remove that final line. Use a simple lowercase header to make BigQuery SQL easier to write.

In the **dbt Cloud Studio** command bar, run:

```bash
dbt seed --select actions
```

This uses the Studio development dataset from **Your profile → Credentials**. For **dbt Core on your own machine** with the external `dev` profile defined above, run from the directory containing `dbt_project.yml`:

```bash
dbt seed --select actions --target dev --profiles-dir <secure-profile-directory>
```

This creates a table named `actions` in the development target dataset. Check it in BigQuery:

```sql
select * from `fei-website-f16b0.dbt_fei_mdelamettrie.actions`;
```

In a model, use `{{ ref('actions') }}` rather than `source()` because the CSV is managed by dbt. For a production Core runner, commit the CSV, merge it to the production branch, and run `dbt seed --select actions --target prod` before models that depend on it. A production job that runs `dbt build --target prod` can also include selected seeds in the build graph; an explicit seed step makes the load order clear. Keep personal or sensitive event-level data out of Git-backed seeds. See dbt's [seed guide](https://docs.getdbt.com/docs/build/seeds) and [`dbt seed` command](https://docs.getdbt.com/reference/commands/seed).

To assert that the **model** `fei_source_test` has no null `action` values, add `models/Bronze/fei_source_test.yml`:

```yaml
version: 2

models:
  - name: fei_source_test
    columns:
      - name: action
        data_tests:
          - not_null
```

The `name:` under `models:` must match the SQL model's filename without `.sql`. The column name must match the output column; use `Action` if that is the actual name in the model. To test the **seed itself**, add a separate file such as `seeds/actions.yml`:

```yaml
version: 2

seeds:
  - name: actions
    columns:
      - name: action
        data_tests:
          - not_null
```

In **Studio**, use `dbt build --select fei_source_test` to build the model and run its tests, or `dbt test --select fei_source_test` to test an already built model. For the seed, use `dbt build --select actions` after creating the CSV. In **external dbt Core**, append `--target dev` or `--target prod` only when that target is defined in the external profile; add `--profiles-dir <secure-profile-directory>` when the profile is outside dbt's default search path. A `not_null` test only checks for SQL `NULL`; it does not reject an empty string. See dbt's [data test guide](https://docs.getdbt.com/docs/build/data-tests).

To combine `not_null` with `accepted_values` for the model, keep one `models:` block and indent `arguments:` under `accepted_values:`. This version allows all eight values supplied for the seed:

```yaml
version: 2

models:
  - name: fei_source_test
    columns:
      - name: action
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values:
                  - Vue Page
                  - Vue Article
                  - Download Doc
                  - Lead Doc
                  - Contact
                  - Newsletter
                  - Commentaire
                  - Action
```

If the model should contain **only** `Action` and `Contact`, set `values: ['Action', 'Contact']` instead. The test will fail on any of the other six listed actions, which may be exactly what a filtered model intends. The test is case sensitive for string values in BigQuery.

The `orders` example with two separately named tests uses `config.where` to limit rows by date. Only copy that pattern if this model has a real date column. For example, with a DATE column named `event_date`, a BigQuery filter for yesterday is `where: "event_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)"`. Replace `event_date` with the model's actual date column, and use `DATE(timestamp_column)` if the source field is a TIMESTAMP. The PostgreSQL expression `current_date - interval '1 day'` should not be copied into BigQuery-specific YAML.

### One model YAML or one folder YAML?

Both are valid. dbt discovers model property `.yml` files under the configured model path; the filename does not have to match the SQL filename. The `models: - name:` value must match the model name.

- For a small Bronze folder, one `models/Bronze/models.yml` containing a `models:` list for several models is easy to manage.
- As models gain descriptions, column tests, contracts, or versions, co-locate `fei_source_test.sql` and `fei_source_test.yml` (one YAML per model) to make reviews and ownership clearer.
- Keep `sources.yml` for source definitions and `seeds/actions.yml` for seed properties. Do not declare the same model in two different YAML files.

There is no performance benefit to either file layout. For this small project, start with one YAML file per folder if it remains short; split into per-model files when the folder file becomes hard to scan. dbt's [staging example](https://docs.getdbt.com/best-practices/how-we-structure/2-staging) shows co-located per-model YAML, while its [quickstart](https://docs.getdbt.com/guides/bigquery?step=1) shows multiple models in a shared `schema.yml`.

### First macro: count rows

Create `macros/count_macro.sql`:

```sql
{% macro count_macro() %}
    count(*)
{% endmacro %}
```

The working project uses a separate model, `models/Bronze/count_records_fei_source_test.sql`:

```sql
select {{ count_macro() }} as Number_of_Records
from {{ ref('fei_source_test') }}
```

The macro generates the SQL expression `count(*)`; the model supplies the table through `ref()`. A macro does not execute a query by itself. dbt Jinja block syntax uses `{% macro ... %}` and `{% endmacro %}`, while `{{ count_macro() }}` inserts its output into SQL. See dbt's [Jinja and macros guide](https://docs.getdbt.com/docs/build/jinja-macros).

To see the number immediately in dbt Studio, open `count_records_fei_source_test.sql`, click **Preview**, and read the single `Number_of_Records` cell in the **Results** tab. The user-provided screenshot from 2026-09-29 shows a successful Preview returning **1,562**. This count reflects the data at that time. The working SQL has an output alias and no trailing semicolon. To persist it as a view or table, run `dbt run --select count_records_fei_source_test`, then query the resulting relation in the development BigQuery dataset. Keep this SQL in a new model: putting `{{ ref('fei_source_test') }}` inside `fei_source_test.sql` itself would create a circular dependency. See dbt's [Studio Preview documentation](https://docs.getdbt.com/docs/platform/studio-ide/ide-user-interface).

The successful Preview was shown in Studio on branch `MatthieudeLaMettrie-patch-1`. The screenshot also showed `seeds/actions.csv` and `models/Bronze/fei_source_test.yml` in the project tree, but did not show a seed load, data-test run, merged pull request, or production build.

## Troubleshooting from this setup

| Error or symptom | Cause | Check or fix |
| --- | --- | --- |
| `Table-valued function not found: source` | `source()` was sent to BigQuery as raw SQL | Use `{{ source('fei_sources', 'FEI_TRAFFIC_NAMED') }}` |
| `FEI_ADMIN_PORTAL was not found in location US` | BigQuery job ran in US while the source is in `australia-southeast1` | Set the BigQuery connection/job location to the source dataset's exact location |
| `dbt_mdelamettrie was not found in location australia-southeast1` | Development credential still targeted an old or differently located output dataset | Create/select an output dataset in `australia-southeast1`; set **Your profile → Credentials → Dataset** to its exact ID |
| `valid dbt project was not found` at `dbt deps` | Deployment could not find `dbt_project.yml` in the cloned branch at the configured path | Commit and sync the project; inspect the production branch; set Project subdirectory to the actual relative folder, or blank for a root file |
| Studio build succeeds but deployment does not | Studio uses workspace code and development credentials; deploy job uses committed code and production credentials | Check commit/branch/path first, then production BigQuery credentials and location |
| `CREATE VIEW columns must be named, but column 1 has no name` | A computed expression such as `{{ count_macro() }}` has no output column alias | Write `{{ count_macro() }} as row_count` in the model SELECT list, save, and rerun the model |
| Studio Preview: `Unexpected keyword LIMIT` | A trailing SQL semicolon before Studio adds its Preview row limit was the likely cause in the earlier failing query | The later Preview succeeded with no final `;`; if this error recurs, inspect the **Compiled code** tab around the reported line |

The session established that the repository's `main` branch contained `dbt_project.yml` **at its root**. Clearing the mistaken `dbt_cert` Project subdirectory resolved the project-discovery issue, according to the user's report. A completed production `dbt build` and its BigQuery output have not yet been independently verified in this record.

## Further findings

### Use Spark in a BigQuery Studio notebook

BigQuery Studio Python notebooks can start a **Managed Service for Apache Spark** interactive session through Spark Connect. This is a separate execution engine from BigQuery SQL and from dbt Cloud jobs. Use it when a PySpark DataFrame workflow is useful; the dbt production model must already exist before the notebook can read it. [Google's notebook guide](https://docs.cloud.google.com/bigquery/docs/use-spark) documents this workflow.

1. In Google Cloud project `fei-website-f16b0`, verify billing and enable the **Managed Service for Apache Spark (Dataproc)**, **BigQuery**, and **Cloud Storage** APIs. You can use **APIs & Services → Library** in the console; API enablement requires `serviceusage.services.enable`. Use a Cloud Storage bucket as required by Google's notebook setup guide. [Prerequisites](https://docs.cloud.google.com/bigquery/docs/use-spark#before_you_begin).
2. Give the notebook user `roles/dataproc.editor` and `roles/bigquery.studioUser`, plus `roles/iam.serviceAccountUser` on the session service account. Give that service account `roles/dataproc.worker`; for this read, it also needs BigQuery Data Viewer on `DBT_FEI_PROD` and BigQuery User on the job project. These are separate from the dbt Cloud service account grants. [Notebook IAM](https://docs.cloud.google.com/bigquery/docs/use-spark#before_you_begin); [Spark BigQuery IAM](https://docs.cloud.google.com/managed-spark/docs/guides/query-bigquery-tables#grant_iam_roles).
3. In **BigQuery Studio**, use the **+** menu to create a **Notebook** (or choose **Query using Spark**). Select a notebook/runtime and session region compatible with the `australia-southeast1` BigQuery dataset. Confirm that `fei-website-f16b0.DBT_FEI_PROD.fei_source_test` actually exists; a dbt Studio Preview on a feature branch does not create a production object.
4. Run these cells. `fei_source_test` was configured as a dbt **view**, so `viewsEnabled` is required. The Spark BigQuery connector reads a named object with `table`, even if that object is a view; `option("view", ...)` is not the documented object selector. [Connector view documentation](https://github.com/GoogleCloudDataproc/spark-bigquery-connector#reading-from-views).

```python
from google.cloud.dataproc_spark_connect import DataprocSparkSession
from google.cloud.dataproc_v1 import Session
import pyspark.sql.connect.functions as f

session = Session()
spark = (
    DataprocSparkSession.builder
    .appName("BigQueryPySparkExample")
    .dataprocSessionConfig(session)
    .getOrCreate()
)

df = (
    spark.read.format("bigquery")
    .option("table", "fei-website-f16b0.DBT_FEI_PROD.fei_source_test")
    .option("viewsEnabled", "true")
    .load()
)

df.printSchema()
df.show(20, truncate=False)
```

`df.show()` prints up to 20 rows in the notebook output; it does not write a BigQuery table. Spark's DataFrame transformations are lazy until an action such as `show()` runs. Reading a BigQuery view can materialize it temporarily and incur BigQuery query costs. If the production model is a physical table instead, omit `viewsEnabled`. The commented word-count example from the original snippet requires a real `word` column; inspect `df.printSchema()` and substitute an existing text column before using `f.split` and `f.explode`.

5. When finished, run `spark.stop()` or terminate the active session in the notebook UI. A BigQuery Studio notebook can have one active Spark session. Interactive Spark and notebook runtime usage are billable. [Session cleanup](https://docs.cloud.google.com/bigquery/docs/use-spark#end_the_spark_session).

**Code help in the notebook:** BigQuery Studio provides code completion as you type and documentation when you hover over a class or method. For example, type `df.` or `spark.read.` to inspect available methods; use `df.printSchema()` and `df.columns` to discover the actual columns. For more directed help, use **+ Code → generate** and ask Gemini for a PySpark operation on a named table. Gemini code completion/generation is a separate feature that might need project enablement and IAM. The session uses Spark Connect, which supports most DataFrame, Column, and functions APIs but not `SparkContext` or RDD APIs; in the [Spark SQL API reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/index.html), look for “Supports Spark Connect.” [Google's notebook code-help and Spark Connect guidance](https://docs.cloud.google.com/bigquery/docs/use-spark#write_and_run_pyspark_code_in_your_bigquery_studio_notebook).

The completion popup after `spark.` lists **SparkSession** members: `read` loads data, `sql` runs Spark SQL, `conf` controls runtime settings, `catalog` inspects tables and views, and `stop()` ends the session. `builder` configures a session and `active()` retrieves one. `addArtifact(s)` distributes files or packages, `addTag`/`clearTags` label operations, `client` exposes the Spark Connect client, and `clearProgressHandlers`/`copyFromLocalToFs` are specialized progress/file helpers. Once `df` is loaded, type `df.` for DataFrame operations such as `select`, `filter`, `groupBy`, `count`, and `show`. [SparkSession API](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/spark_session.html).

**CSV and Google Sheets:** To read a CSV directly with Spark, upload it to Cloud Storage and use `spark.read.option("header", "true").option("inferSchema", "true").csv("gs://BUCKET/path/file.csv")`. Replace the placeholder with a real object path and grant the Spark session identity access to the bucket. `load("")` supplies no file path; a Windows local path is not a path on the remote Spark workers. See [PySpark CSV reader](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.csv.html).

For a Google Sheet, create a BigQuery **Drive external table** with source format **Sheets**, the Sheet URL, and an appropriate sheet range/schema. Share the Sheet with the identity used to query it. [Google's external table setup](https://docs.cloud.google.com/bigquery/docs/external-data-drive). The Spark BigQuery connector uses the Storage Read API, which does not directly read ordinary Drive external tables; run a BigQuery `CREATE OR REPLACE TABLE project.dataset.sheet_snapshot AS SELECT * FROM project.dataset.sheet_external` query, then read `sheet_snapshot` with `spark.read.format("bigquery").option("table", "project.dataset.sheet_snapshot").load()`. The snapshot needs to be refreshed when the Sheet changes. [Storage Read API limitations](https://docs.cloud.google.com/bigquery/docs/reference/storage).

The runnable [Google Sheet notebook script](examples/read_google_sheet_with_spark.py) creates the external table with the BigQuery Python client, replaces a native snapshot in a **scratch dataset**, and reads that snapshot into a Spark DataFrame. Set its Sheet URL, tab/range, and dataset first. The notebook identity needs Drive access as well as BigQuery permissions. The script is an example and has not been run here; its snapshot replacement is intentional.

**Google Analytics 4 and Looker Studio:** If GA4 BigQuery export is enabled, its daily tables are `analytics_<property_id>.events_YYYYMMDD`; Spark can read an existing daily table with the BigQuery connector. The intraday table is temporary and daily tables can receive late events for several days. [GA4 export schema](https://support.google.com/analytics/answer/7029846). Data Studio is now **Looker Studio**. Its report is a visualization, so inspect the report's data source: if it uses BigQuery, read that underlying table or view from Spark. [Looker Studio BigQuery connector](https://docs.cloud.google.com/looker/docs/studio/connect-to-google-bigquery). The [second notebook script](examples/read_ga4_or_looker_source_with_spark.py) shows both reads with placeholders. Neither source was accessed in this session.

This is a documented setup and corrected code example, **not an observed successful Spark run** in this project. If the read fails, check the production object and region first, then the session identity's BigQuery permissions and whether view reads are enabled.

Add dated entries here when new behavior is observed. For each entry, record the symptom, exact cause, fix, and how it was verified. Keep credentials and private key material out of this file.

## References

- [dbt and BigQuery quickstart](https://docs.getdbt.com/guides/bigquery?step=1)
- [dbt SQL models and hierarchical model configuration](https://docs.getdbt.com/docs/build/sql-models)
- [dbt deployment environments and jobs](https://docs.getdbt.com/docs/deploy/deployments)
- [dbt Studio interface and defer selector](https://docs.getdbt.com/docs/platform/studio-ide/ide-user-interface)
- [dbt BigQuery OAuth and Workload Identity Federation](https://docs.getdbt.com/docs/platform/manage-access/set-up-bigquery-oauth)
- [dbt profiles, targets, and production execution](https://docs.getdbt.com/docs/local/profiles.yml)
- [dbt staging structure and model naming](https://docs.getdbt.com/best-practices/how-we-structure/2-staging)
