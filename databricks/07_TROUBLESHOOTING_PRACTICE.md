# 07 — Troubleshooting workbook: 28 original incidents

[Learning path](README.md) · [Readiness rubric](08_READINESS_AND_CAPSTONE.md) · [Official index](09_OFFICIAL_DOC_INDEX.md)

These are original professional-skills scenarios, not official exam questions. **Answers are deliberately withheld until you make an attempt or request help**, following your dbt debugging practice approach. Ask for a small hint, stronger hint or full explanation by case number. The numbered learning path supplies the related material without claiming a particular certification weighting.

For each case, write:

```text
Impact and first failing boundary:
Diagnosis and competing hypothesis:
Evidence/check that distinguishes them:
Smallest appropriate repair and safe replay scope:
Verification of data and execution:
Prevention and owner:
Confidence and remaining uncertainty:
```

Some cases intentionally require additional evidence. State exactly what is missing; do not invent the source contract, engine, identity or runtime.

## Delta Lake and incremental state

### Case 1 — Ambiguous matched update

Assume DBR 15.4 LTS, one target row per `(source_system, order_id)` and an unconditional matched update. Source contains three rows for order 101: sequence 7 amount 90.00, sequence 8 amount 110.00, and an exact re-delivery of the sequence-8 event. Merge fails with multiple source rows matching the same target.

A colleague proposes `dropDuplicates(["order_id"])`. Give the candidate-selection contract, investigation and verification you require. What changes if two different source systems both have order 101?

### Case 2 — Empty target, successful duplicate inserts

A Delta target is empty. Source contains two identical rows with the same business key but different delivered-line IDs. An insert-only merge on the business key completes; the target contains two rows. Why did no duplicate matched-row failure occur? Propose checks before and after the merge, preserving raw delivery evidence.

### Case 3 — Runtime upgrade changes observed behavior

The same merge with several conditional `WHEN MATCHED` clauses is accepted in one runtime and rejected in another. The team moved from DBR 15.4 LTS to 16.0+, but the failing input was not retained. What evidence is needed to establish the cause? Explain a design that avoids depending on the duplicate-match semantic difference rather than immediately rolling back the runtime.

### Case 4 — Deleted order resurrects

Sequence 10 physically deletes order 501. Later a replay delivers sequence 9 `UPSERT` for 501. The merge sees no target key and inserts it. The pipeline processed source records in arrival order and retained no delete sequence elsewhere. Design immediate repair and durable recurrence prevention, including retention assumptions.

## PySpark transformation failures

### Case 5 — Python boolean applied to Columns

The notebook fails before a write:

```python
valid = df.filter((F.col("amount") >= 0) and (F.col("order_id").isNotNull()))
```

Identify the execution boundary and repair the expression. How does your answer differ from catching the exception and returning an empty DataFrame? Verify behavior for amount null, amount zero and empty order ID under a declared policy.

### Case 6 — Ambiguous join column

Both `orders` and `stores` contain `region`. A join written with an explicit equality condition preserves two `region` columns. A downstream `select("region")` fails as ambiguous. Propose an explicit projection with aliases. Which additional data check is necessary even if the ambiguity is repaired?

### Case 7 — Parsing silently inflates apparent completeness

Amounts include `25.00`, `oops`, blank and `1,200.00`. A transformation replaces any failed cast with 0.00. No rejected records remain, and the job is green. The source format contract has not been agreed. Explain why syntax success is insufficient, what you ask the source owner, and how to preserve evidence while continuing approved valid records.

### Case 8 — Left join loses unknown stores

Orders are left joined to stores, then filtered with `where(stores.is_active = true)`. Three orders have no matching store; they disappear from Gold. Business owners require every valid order to remain visible. Give the intended join/filter contract, repair and reconciliation. Consider the separate case of a known inactive store.

### Case 9 — Dimension duplicates double revenue

Silver has 1,000 orders and amount 80,000.00. Store S01 occurs twice in the dimension because it has two historical versions. Join uses only `store_id`; output has 1,250 rows and amount 102,000.00. The team proposes `distinct()` after the join. Explain what business decision is missing, the temporal/current join alternatives and the checks proving correct attribution.

## Ingestion, schema and streaming

### Case 10 — Duplicate business event in a new file

Auto Loader ingests file A with event e100. The source later publishes file B containing e100 again. Both files are discovered exactly once, yet current business effects are duplicated downstream. Separate file identity, event identity and business state. Propose the correct layer for each control and evidence for a safe retry.

### Case 11 — New optional field stops ingestion

A JSON producer adds `promotion_code`. The Auto Loader stream fails after schema tracking updates. The developer deletes both schema and checkpoint directories, then starts again. Before accepting this fix, identify the configured evolution mode, expected restart behavior, target schema and replay risk. Describe a bounded development reproduction.

### Case 12 — Callback retry repeats a side effect

`foreachBatch` merges Silver, posts a “batch loaded” message to an external service, then fails updating a control table. The callback is retried with the same batch. The merge is stable but the external message appears twice. Design a side-effect contract and failure test that remains safe if the checkpoint/query is replaced. A Spark sink guarantee alone is not an answer.

### Case 13 — Late correction beyond aggregation watermark

The consumer needs all order corrections applied, even 30 days late. A streaming event-time aggregate retains state for two days. A 15-day-old correction does not appear in the monthly total. What guarantees were confused? Propose a state/correction/backfill design with separate latency and completeness expectations.

## DAB deployment and identities

### Case 14 — Parse passes, bundle validation fails

A local YAML parser accepts the file. `databricks bundle validate -t uat` reports an unsupported property and an undefined variable. The developer's machine and CI runner have different CLI versions. Give an investigation order, what to pin and what a successful follow-up validation still does not prove.

### Case 15 — Wrong notebook deployed

`resources/jobs.yml` points to a notebook renamed last week. A similarly named old file still exists; deployment succeeds and the job returns old columns. Identify the relevant local/resource-relative/deployed paths and code provenance. Design a check that proves the intended commit's artifact was executed.

### Case 16 — Interactive works, job cannot read volume

Developer D reads `/Volumes/ops_dev/ops/source_files/...` successfully. CI principal C deploys the job. The job runs as principal R and gets a volume permission denial. All three have workspace access. State which principal needs which data grants, how you verify that conclusion and why job-management permission alone is insufficient.

### Case 17 — Duplicate production jobs appear

Two CI pipelines use the same bundle name but different target root paths. Each successfully deploys a production-looking job. Both schedules are active and write the same Gold table. Explain resource identity/state ownership, immediate containment, data reconciliation and safe consolidation. Do not prescribe deleting state or arbitrary job IDs without an inventory.

### Case 18 — Validation reaches the wrong workspace

CI reports `bundle validate -t prod` succeeded, but the output host alias is DEV. The runner has a default profile, environment variables and a YAML target host; their effective precedence is unknown. No production deployment has happened yet. Determine the exact evidence needed, how to correct the invocation and the checks required before promotion.

## Azure integration and orchestration

### Case 19 — Synapse query returns old deleted rows

Databricks current state correctly excludes deleted orders. A Synapse query reads the same storage directory as `FORMAT='PARQUET'` and includes deleted or duplicate old records. The Databricks table uses modern Delta features. Identify the engines/formats involved, a safe immediate consumer alternative and the compatibility evidence needed for any Delta reader proposal.

### Case 20 — SQL connects, staging fails

An existing notebook uses the legacy dedicated SQL pool connector. JDBC login succeeds, but the transfer fails on staging-storage access. Someone proposes using a Unity Catalog volume as `tempDir` and enabling credential forwarding. Which runtime/connector/identity/path evidence do you inspect? Explain why SQL connectivity and volume browsing are separate from the bulk transfer's storage access.

### Case 21 — Two orchestration owners

ADF extracts and invokes a Databricks job every hour. The same job also has its own hourly schedule. Both runs overlap; one sees a partial extraction file set, and two append to a downstream staging table. Design a single-owner trigger/completion/retry contract and the correlation evidence needed to repair affected releases.

## Performance and schema integrity

### Case 22 — Driver memory failure after collect

A Silver notebook collects 20 million orders to a Python list to calculate per-store totals. Workers have spare memory, but the driver crashes. Propose a distributed transformation and a bounded diagnostic method. What counts/totals and plan/stage evidence should accompany the repair?

### Case 23 — One task takes 25 minutes

A join's other tasks finish in under a minute; one takes 25 minutes and spills heavily. Forty percent of facts use store code UNKNOWN. The dimension's size and actual join strategy are not known. Give competing hypotheses, the evidence distinguishing skew from oversized input/partitioning, and a measured optimization with parity checks.

### Case 24 — Layout optimization breaks an external reader

A Gold table was readable by a downstream client. After a layout/table-feature change, writes still succeed but that reader fails. The team assumes switching a table property off will instantly repair it. Explain the protocol/feature/reader inventory required, how to contain consumer impact and why re-exporting a pinned snapshot may be a separate publication option.

## Deeper correctness and recovery

### Case 25 — Incremental Gold leaves an obsolete group

Order 900 was the only order for store S03 on 1 October. A correction moves it to S02 on 2 October. Gold upserts newly calculated groups but never removes groups absent from its update source. Its old S03/1 October group remains. Design affected-group detection, scoped reconstruction/removal and verification of both old and new attribution.

### Case 26 — CDF consumer falls behind retention

A downstream consumer last applied table version 120. The source table is at 180; retained changes begin after 120, so the requested resume range is unavailable. A colleague suggests restarting from 180 to restore green status. Propose an accurate bootstrap/resume strategy, publication boundary and changes to monitoring/retention expectations.

### Case 27 — Missing rows from timestamp extraction

Extraction uses `modified_at > last_max`. Two rows share the maximum timestamp, one page was not durably landed, and the source later hard-deletes another row without a delete feed. The cursor has advanced. Explain each independent completeness problem, immediate recovery evidence, a durable future cursor/landing policy and the limit of timestamp-only ingestion.

### Case 28 — Code rollback leaves bad data

A production release changes a schema and accidentally doubles yesterday's Gold totals. Rolling back the bundle restores the old notebook but the table still contains bad rows, and old code expects the prior schema. New valid orders arrived after the defective release. Propose coordinated code/schema/data recovery preserving those later valid changes, consumer publication and replay proof.

## Suggested practice sequence

| Round | Cases | Purpose |
|---|---|---|
| Diagnostic | 1, 9, 16 | Match the three start-here diagnostics |
| Data preparation | 5–9, 22 | Explain and reproduce transformations |
| Incremental reliability | 1–4, 10–13, 25–27 | Defend ordering, state, retention and recovery |
| Deployment/integration | 14–21, 24, 28 | Trace identities and publication boundaries |
| Performance | 22–24 | Form a measured hypothesis and preserve correctness |

After feedback, retry a variant with changed IDs/dates/values and no notes. A repaired syntax example does not establish that you can operate a source-to-consumer pipeline; use the [capstone](08_READINESS_AND_CAPSTONE.md) for that evidence.
