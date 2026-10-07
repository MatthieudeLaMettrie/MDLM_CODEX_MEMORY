# 03 — Operational-data lab: Bronze → Silver → Gold

[Learning path](../README.md) · [Course lessons](../02_COURSE_COMPANION.md) · [Delta deep dive](../04_DELTA_AND_STREAMING.md) · [Deployment chapter](../06_BUNDLES_AND_ORCHESTRATION.md)

This bounded lab builds current order state from synthetic events. It deliberately includes duplicates, three bad records, a late correction, a delete, an unknown store, a superseded update and stale replay. The notebook is intended for Databricks; it was syntax-checked locally but **has not been executed on Spark/Databricks**. An independent offline oracle verifies the fixture's arithmetic and state expectations.

## 1. Assets and responsibilities

| Asset | Purpose |
|---|---|
| [order_events.csv](data/order_events.csv) | 16 delivered source lines across B1/B2/B3; no real data |
| [expected_results.json](data/expected_results.json) | Fixed cumulative counts and day/store results |
| [operational_pipeline.py](notebooks/operational_pipeline.py) | Parameterized Bronze, Silver, Gold and validation stages |
| [01_setup.sql](sql/01_setup.sql) | Create schemas/managed volume in an existing dev catalog |
| [02_reconcile.sql](sql/02_reconcile.sql) | Inspect rejects, keys, current state, Gold and table history |
| [databricks.yml](bundle/databricks.yml) / [jobs.yml](bundle/resources/jobs.yml) | Development-only classic-compute bundle and task graph |
| [verify_fixture.py](verify_fixture.py) | Standard-library offline oracle; does not run PySpark |

The intended data model is **one current row per `(source_system, order_id)`**. The source sequence is authoritative for that key; sequence 0 is allowed. An event ID describes a change. A source-line ID describes a delivered line: B1-02 and B1-03 contain the same event, so raw evidence is retained while business effect is deduplicated.

An upsert amount must be a nonnegative `DECIMAL(18,2)` in this example. Delete events need no amount; a tombstone retains source key and sequence. The example is an order-state exercise, not a financial ledger or an order-line model. Refunds, multiple currencies, tax, partial cancellation and SCD2 dimensions need further contracts.

## 2. Predict the result

| Cumulative stage | Bronze lines | Quarantine lines | Silver state rows, including tombstones | Active orders | Active amount |
|---|---:|---:|---:|---:|---:|
| B1 | 8 | 3 | 4 | 4 | 215.00 |
| B1 + B2 | 13 | 3 | 5 | 4 | 270.00 |
| B1 + B2 + B3 | 16 | 3 | 5 | 4 | 270.00 |

B1 has five valid delivered lines but four distinct business events after exact re-delivery is collapsed. Three rejected lines contain an empty order key, `oops` amount and negative amount. Order 1005 has store S99: it remains valid and visible as Unknown.

B2 updates 1001 from 100.00 to 120.00, marks 1002 deleted, makes 1003 45.00, and adds 1007 at 80.00 on 2 October. Its sequence-0 event for 1003 is superseded by sequence 2. B3 must change no current business result.

After B2/B3:

| Order date | Store | Label | Orders | Amount |
|---|---|---|---:|---:|
| 2026-10-01 | S01 | Sydney | 1 | 120.00 |
| 2026-10-01 | S02 | Newcastle | 1 | 45.00 |
| 2026-10-01 | S99 | Unknown | 1 | 25.00 |
| 2026-10-02 | S02 | Newcastle | 1 | 80.00 |

Before cloud work, run from the repository root:

```powershell
python databricks/03_OPERATIONAL_DATA_LAB/verify_fixture.py
```

The oracle selects global latest state across accepted events independently of the notebook's per-batch Delta merge. Passing it confirms the fixture expectations, not equivalence of Spark parsing, Delta transactions, permissions or deployment.

## 3. Set up in a dedicated development namespace

1. Use an existing Unity Catalog catalog ending in `_dev`, such as `training_dev`. Ask the platform owner to configure its managed storage and appropriate development permissions if you do not have them. The sample intentionally rejects production-style catalog names.
2. Use compatible compute and record runtime/access mode. Volume access, Delta and tolerant SQL casts are required. Intended classic baseline is DBR 15.4 LTS or a later supported version; verify exact functions/features on your runtime. Do not install another PySpark over Databricks' provided runtime.
3. Inspect whether the lab's four tables already exist. Use an unused dev catalog or inspect/reset only the documented lab tables before starting. Existing unrelated tables must not be reused.
4. Run [setup SQL](sql/01_setup.sql) after replacing `training_dev` if needed. This creates Bronze/Silver/Gold/ops schemas and a managed volume, not a catalog, storage credential or cloud resource.
5. In Catalog Explorer, open the `ops.lab_files` volume and upload [order_events.csv](data/order_events.csv). Verify the path is `/Volumes/<catalog>/ops/lab_files/order_events.csv`. The notebook constrains inputs to that lab volume.
6. Import the [Python source notebook](notebooks/operational_pipeline.py) into the development workspace or deploy it with the bundle below. The `# Databricks notebook source` header and command separator comments describe a source-format notebook.
7. Set `catalog` and `input_file` widgets to match your uploaded fixture. Keep table names dedicated to this lab. Set `batch_id=B1` and `stage=bronze`.

The interactive caller or configured job run identity must be able to read the volume, use the catalog/schemas, create the initial tables and modify the relevant existing tables. Creating the volume requires creation privileges; uploading files requires write access. Access to compute and workspace notebook files is separate from data privileges. [Volume files](https://learn.microsoft.com/en-us/azure/databricks/volumes/volume-files) · [Privileges](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/privileges)

## 4. Execute the baseline manually

Run the entire notebook once per selected stage, in this order:

```text
batch B1: bronze → silver → gold → validate
batch B2: bronze → silver → gold → validate
batch B3: bronze → silver → gold → validate
```

Each stage is controlled by the `stage` widget; other sections do not execute. Each batch's Bronze stage selects only that batch from the CSV. Silver reads its corresponding Bronze events. Gold recomputes the full tiny aggregate from current state. Validation expects cumulative B1, B1+B2 or B1+B2+B3; an out-of-order or partial fixture run should fail expected-count checks.

Run [reconciliation SQL](sql/02_reconcile.sql) after each completed batch. Confirm rejects, sequences and day/store attribution, not only the total. Record table history versions and the code/input parameters in your evidence sheet.

**Why replays are stable:** Bronze insert-only merge uses stable line IDs and fails if the same line ID changes payload. Silver retains raw evidence but collapses event re-delivery; it selects the highest sequence per business key and only updates current state for a greater sequence. Equal-sequence contradictory payloads are rejected; equal payloads have no new state effect. Quarantine uses stable line IDs. Gold fully recomputes a small development dataset.

The notebook's conflict gates cover observed event-ID contradictions, within-batch sequence contradictions and equal-sequence contradictions against current state. It does **not** implement a permanent ledger of every historical key/sequence fingerprint; a contradictory older sequence with a new event ID in a later batch can be ignored as stale. A production contract may require that durable historical conflict detection. Hash equality is a practical diagnostic, not a mathematical guarantee of payload identity.

## 5. Execute with the supplied bundle

From the [bundle directory](bundle/databricks.yml), authenticate and resolve environment-specific configuration. Replace placeholders locally; never put tokens into YAML or Git. These commands are for your workspace and were not run during course creation.

```powershell
databricks version
databricks auth login --host https://<your-workspace-host> --profile STUDY_DEV
databricks bundle validate -t dev -p STUDY_DEV --var "existing_cluster_id=<your-compatible-cluster-id>"
databricks bundle plan -t dev -p STUDY_DEV --var "existing_cluster_id=<your-compatible-cluster-id>"
databricks bundle deploy -t dev -p STUDY_DEV --var "existing_cluster_id=<your-compatible-cluster-id>"
databricks bundle run -t dev -p STUDY_DEV --var "existing_cluster_id=<your-compatible-cluster-id>" --params "batch_id=B1" operational_pipeline
```

Repeat `bundle run` for B2 and B3 **after** each prior run completes. If you used different catalog/path values, supply all overrides consistently, for example `--var "existing_cluster_id=<id>,catalog=ops_study_dev,input_file=/Volumes/ops_study_dev/ops/lab_files/order_events.csv"`. Inspect the resolved configuration before deployment. This YAML uses `sync.paths` to include the notebook outside the bundle directory; its relative path is resolved from the resource file.

The bundle uses `engine: direct`, one development target, a four-task dependency chain, `max_concurrent_runs: 1`, no schedule and no automatic retry policy. It reuses classic compute because your cloud SKU/runtime/policy are unknown. Inspect resource access and the job's run identity after deploy. Do not interpret this minimal development bundle as a production architecture or add a prod target pointing at the guarded notebook. For production adaptation, extract general transformation code, replace fixture assertions and add a reviewed environment/identity/publication contract.

Current CLI help remains authoritative if flags change. Bundle schema validation/deploy/run remain unverified here. [Sharing files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing) · [Bundle resources](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/resources) · [CLI bundle commands](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/bundle-commands)

## 6. Required recovery drills

| Drill | Action in development | Evidence to inspect |
|---|---|---|
| Exact retry | Rerun B3 Bronze/Silver/Gold/validate | Cumulative counts and business state remain B3 expectations |
| Old batch replay | After B3, rerun B1 Bronze/Silver/Gold | State remains latest; **use B3 validation**, since B1 expectations no longer apply |
| Delete replay | Inspect B3's old upsert for 1002 | Tombstone sequence 2 remains; active order count stays 4 |
| Partial pipeline | On a clean fixture run, complete Bronze then stop before Silver | Bronze is committed; downstream results have not been published |
| Contradictory sequence | Use a separate scratch namespace/fixture with changed payload and new event ID at an existing sequence | Gate detects ambiguity before current-state merge |
| Join multiplication | In a scratch DataFrame, duplicate S01 in the dimension | Uniqueness gate fails; an ungated join inflates sales |

Capture intended failure messages and the minimal repair. Do not change the baseline fixture to make expected assertions pass. An old-batch bundle run would automatically invoke that old batch's validation and fail its cumulative expectations; use manual stages and B3 validation for this specific drill, or deliberately build a separate general-purpose validation task.

## 7. What this lab intentionally leaves for later

- The CSV is bounded and manually uploaded. It exercises state transformations; it is not a live Auto Loader, source CDC or API integration. The streaming extension is in [04](../04_DELTA_AND_STREAMING.md).
- Bronze/Silver/quarantine/Gold commit separately. Recovery is idempotent for the declared fixture; whole-pipeline atomicity is not supplied.
- The source-line ID comes from the fixture. Real ingestion needs a stable file/message/offset identity and a delivery-attempt audit if retries must be recorded separately.
- The dimension is a static, unique two-row mapping. Slowly changing dimensions and temporal joins require additional modeling.
- Gold uses full overwrite only for this tiny guarded dev lab. A production incremental aggregate must handle prior-period corrections, removed groups, consumer publication and concurrent writers.
- There is no secret retrieval, external database/network setup, persisted run-control table or Synapse export. Those are taught as separate integration/operating designs.
- A single writer is assumed across all ways of running the notebook, including manual runs. Job concurrency does not prevent another job or notebook writing the same table.

## 8. Clean up deliberately

Preserve your evidence and check all target names first. Optional cleanup applies only to `order_events`, `order_quarantine`, `orders_current` and `daily_store_sales` in the dedicated lab schemas. Dropping those tables removes the lab's replay state; the next run must start at B1. Do not drop a shared catalog/schema/volume or delete cloud storage/checkpoints to reset the lab. Bundle resource destruction is a separate operation from data cleanup; review its scope before using it. No cleanup is run by the notebook.
