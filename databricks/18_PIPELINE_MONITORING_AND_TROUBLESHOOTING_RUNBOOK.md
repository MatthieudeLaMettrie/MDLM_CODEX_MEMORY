# 18 — Pipeline monitoring and troubleshooting runbook

[Learning path](README.md) · [14 — Operations and optimisation (deep dive)](14_PIPELINE_OPERATIONS_AND_OPTIMISATION.md) · [11 — Lakeflow pipelines](11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md) · [17 — CDF and CDC explained](17_CDF_AND_CDC_EXPLAINED.md)

Written 8 October 2026 as a short, practical checklist. Lesson 14 holds the 15 detailed worked incidents; start here when something looks wrong. Queries and UI paths are illustrative and **not executed**. Check names against your workspace and current documentation.

## 1. What "healthy" means

A run showing **Succeeded** is not automatically healthy. Check four things:

| Question | Example evidence |
|---|---|
| Did it **run**? | Update state, start/end time |
| Is the data **fresh**? | Latest source timestamp in the target vs now |
| Is it **complete**? | Row counts vs source or expected file/batch count |
| Is it **correct**? | Expectation results, totals that reconcile, no duplicates |

## 2. Where to look

| Place | Use it for |
|---|---|
| **Jobs & Pipelines → your pipeline → Updates** | Run history, state, duration, failure message |
| **Pipeline graph / flow details** | Which table failed; rows written, dropped and quarantined; expectation results |
| **Event log** | Full detail: errors, flow progress, data quality, user actions |
| **Compute / Spark UI** | Slow stages, skew, spill, memory problems |
| **Jobs run page** | Task dependencies, retries, parameters, who or what ran it |
| **Catalog → table → History / Lineage** | What changed, when, and what depends on it |
| **Query History / SQL Warehouses** | Slow or failing downstream queries |

## 3. Event log queries

Replace the pipeline ID with yours.

```sql
-- Recent errors and warnings
SELECT timestamp, event_type, level, message
FROM event_log("<pipeline_id>")
WHERE level IN ('ERROR', 'WARN')
ORDER BY timestamp DESC
LIMIT 50;

-- Update lifecycle (started, running, failed, completed)
SELECT timestamp, origin.update_id, details:update_progress.state AS state
FROM event_log("<pipeline_id>")
WHERE event_type = 'update_progress'
ORDER BY timestamp DESC;

-- Rows processed and data-quality results per table
SELECT timestamp, origin.flow_name,
       details:flow_progress.metrics.num_output_rows AS rows_out,
       details:flow_progress.data_quality.expectations AS expectations
FROM event_log("<pipeline_id>")
WHERE event_type = 'flow_progress'
ORDER BY timestamp DESC;
```

You can also query by table with `event_log(TABLE(catalog.schema.table))` where supported. Field paths can differ by version, so run `SELECT * ... LIMIT 5` first to confirm them.

## 4. A repeatable troubleshooting sequence

1. **State the symptom precisely:** failed, slow, stale, wrong numbers or duplicates? When did it last work?
2. **Find the first failing step**, not the last error. Read the earliest ERROR for that update in the event log.
3. **Check what changed:** code, source schema, new files, permissions or identity, runtime version, bundle target, compute settings.
4. **Separate causes:** code or logic; data (new column, bad types, duplicates, nulls); permission or identity; infrastructure (compute, quota, network).
5. **Make the smallest fix** and test it on a **small or development** scope.
6. **Re-run and verify** both the execution and the data (counts, totals, freshness).
7. **Add prevention:** an alert, expectation, test or runbook step.

## 5. Common problems and first moves

| Symptom | Likely causes | First checks and fixes |
|---|---|---|
| **"X is not supported in a DLT pipeline"** | A bare `SELECT`, `DROP`, `INSERT` or `USE` in a pipeline SQL file | Wrap in `CREATE OR REFRESH MATERIALIZED VIEW/STREAMING TABLE ... AS SELECT`. See [15](15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md) |
| **Works for me, fails when scheduled** | Run identity (for example a service principal) lacks permission on catalog, schema, volume or storage | Check who the job runs as; grant `USE CATALOG`, `USE SCHEMA`, `SELECT`/`MODIFY`, `READ VOLUME` as needed |
| **Table or view not found** | Wrong default catalog/schema, missing pipeline target setting, dataset not defined | Fully qualify names; check the pipeline target catalog/schema; confirm the dataset is defined in the pipeline |
| **Schema mismatch, unknown column, cast error** | Source added or retyped a column | Compare new data with the expected schema; use Auto Loader schema evolution or the rescue column deliberately; fix casts; do not silently drop data |
| **Delta MERGE: multiple source rows matched** | Duplicate keys in the source batch | Deduplicate by key using an authoritative ordering column before merging |
| **No new rows arriving** | Wrong path, no files delivered, Auto Loader discovery or permission problem | Check files exist in the volume/storage path; check checkpoint and permissions; read the stream's input metrics |
| **Stream stalls or backlog grows** | Batches too slow, skew, small compute, source burst | Compare input and processing rates; look for skew and spill in the Spark UI; scale compute or tune batch size |
| **CDF read fails: version not available** | Consumer fell behind retention, or CDF was not enabled at that version | Re-bootstrap from a snapshot and resume from a known version; reduce consumer lag; review retention. See [17](17_CDF_AND_CDC_EXPLAINED.md) |
| **Duplicates or inflated totals** | Join fan-out, replayed files, missing dedupe | Check key uniqueness on both sides of the join; compare counts before and after; add uniqueness checks |
| **Deleted rows reappear** | Late or replayed insert applied after the delete | Order CDC by a trusted sequence and keep delete tombstones; never order by arrival time |
| **Out-of-memory or heavy spill** | Huge shuffle, `collect()`, skew | Reduce data early; avoid collecting to the driver; fix skew; adjust partitions or compute |
| **Run succeeds but numbers are wrong** | Logic bug, stale source, expectation set to warn only | Reconcile against the source with simple totals; make critical expectations fail or drop |
| **Bundle deployed to the wrong environment** | Wrong target or profile | Verify the resolved target, workspace host and identity before deploying |
| **Stateful stream fails after a code change** | Changed grouping keys or schema, incompatible checkpoint | Use a new checkpoint or a full refresh with an agreed replay plan; avoid changing state keys in place |

## 6. Recovering safely

Choose the least destructive option that fixes the cause:

| Situation | Option |
|---|---|
| Transient failure (network, throttling) | Retry the update |
| One table is bad, the rest is fine | Refresh the selected table only |
| Logic or data bug in a derived table | Fix the code, then **full refresh** that table (it reprocesses source history) |
| Streaming checkpoint is incompatible | Reset the checkpoint or full refresh, after confirming the source still has the history |
| Bad data written to a Delta table | `RESTORE TABLE ... TO VERSION AS OF n` (within retention), then re-run |
| Source files are gone | Replay from Bronze or an archive; a full refresh cannot recreate missing source history |

**Warning:** a full refresh of a streaming table whose source no longer holds old data can permanently lose that data. Confirm retention before refreshing.

## 7. Alerting basics

Alert on things a person can act on:

- Update **failed** or ran far longer than usual.
- **Freshness** missed: no new data past the agreed deadline.
- **Row-count anomaly**: zero rows, or a sudden large jump or drop.
- **Expectation failures** above a threshold.
- **Backlog** growing across several batches.

Use job and pipeline notifications (email, Slack/Teams webhook) and Databricks SQL alerts on a monitoring query. Every alert should name an owner and a first step.

## 8. Pre-flight checklist for a new or changed pipeline

- [ ] Target catalog and schema are set, and names resolve in dev.
- [ ] The run identity has the minimum required grants.
- [ ] Pipeline SQL files contain only dataset definitions.
- [ ] Key uniqueness and ordering column are known for any CDC or merge.
- [ ] Expectations cover nulls, keys and ranges; critical ones fail loudly.
- [ ] A reconciliation query exists (source total vs target total).
- [ ] Notifications are configured and an owner is named.
- [ ] Recovery plan: how to replay, and how long the source keeps history.

## 9. Practice

1. An update shows Succeeded but yesterday's data is missing. List five checks in order.
2. Your CDF consumer fails with a missing-version error. Name two ways to recover and say which is safer.
3. After a source schema change, a table fails to cast `amount`. What do you check before editing code?
4. A scheduled run fails with permission denied but passes interactively. What differs?

Hints: (1) freshness query, source delivery, file path/discovery, filters, event-log flow metrics; (2) re-bootstrap from a snapshot and resume (safe) vs skip ahead (loses changes); (3) the actual new values and types; (4) the run-as identity and its grants.

Official references: [Monitor pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/observability) · [Pipeline event log](https://learn.microsoft.com/en-us/azure/databricks/ldp/monitor-event-logs) · [Delta table history and RESTORE](https://learn.microsoft.com/en-us/azure/databricks/delta/history)
