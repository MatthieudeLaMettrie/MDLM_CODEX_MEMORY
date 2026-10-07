# 02 — Course companion: from source to operated data product

[Learning path](README.md) · [Core guide](01_CORE_STUDY_GUIDE.md) · [Lab](03_OPERATIONAL_DATA_LAB/README.md)

This companion turns the topics into work you can demonstrate. Sixteen lessons combine recall, implementation and incident investigation. Use one notebook/evidence record across lessons, as in your continuous cross-vendor curriculum. The flexible four-week route is an authored learning plan, not a Databricks course syllabus or certification timetable.

## Planning route

| Week | Lessons | Main deliverable | Indicative effort |
|---|---|---|---|
| 1 | 1–5 | Architecture, source contract, Bronze and typed validation | 6–9 hours |
| 2 | 6–9 | Sequenced Silver, reconciled Gold, replay and streaming design | 6–9 hours |
| 3 | 10–13 | Azure onboarding plan, deployable task graph and monitoring | 6–9 hours |
| 4 | 14–16 | Performance experiment, incident evidence and capstone | 6–9 hours |

Start the cloud lab after lesson 4. Keep its batches ordered: B1, then B2, then B3. Each lesson has a small deliverable and an exit check. If access blocks a hands-on step, record it as pending and complete independent design work; do not substitute a screenshot of code for observed execution.

## Lesson 1 — Draw the platform boundaries

**Purpose:** Know where a failure can occur before choosing a repair. Read core §§1–2. Sketch source → extraction → ADLS landing → Databricks Bronze/Silver/Gold → consumer. Draw a separate arrow from CI/CD to the workspace API. Label the SQL engine behind every consumer.

**Exercise:** Your browser can open a workspace, but a job cannot connect to an on-premises database. List the network/identity boundaries crossed by each. Add source hostname resolution, integration runtime or compute network, TLS, database authentication and storage access to your diagram.

**Deliverable:** A one-page component map, with the owner of each boundary. Separate code ownership from data stewardship and platform administration.

**Exit check:** Explain why a Databricks catalog name does not identify an Azure storage credential, and why a Git notebook folder cannot create a schema automatically.

## Lesson 2 — Define environment and layer responsibilities

**Purpose:** Avoid an architecture whose names suggest isolation that grants do not enforce. Compare domain/environment catalogs and environment-only catalogs using the [existing concepts explanation](../guides/data-engineering/DATA_AND_DBT_CONCEPTS_GUIDE.md). Document what each layer retains and who consumes it.

**Exercise:** Propose names for dev, UAT and prod for the synthetic operations domain. State which workspace can access which catalog, which identities can write, where managed storage is configured, and how masked development data is obtained. Use a smaller sample in dev without pretending it reproduces production performance.

**Deliverable:** Object hierarchy plus a privilege matrix. Include tables, volumes, job permissions and compute permissions; do not request broad administrator access merely to get a lab working.

**Exit check:** Describe promotion of `gold.daily_store_sales`: code version, configuration, source data, run identity and consumer cutover. Which of those does a catalog name automatically supply?

## Lesson 3 — Write the operational source contract

**Purpose:** Turn “load new orders” into a testable interface. Read core §3 and integration §2. Decide whether the source publishes events, changed rows or complete snapshots. Specify business grain, event identity, key, operation, sequence, timestamps, timezone and delivery guarantees.

**Exercise:** Contrast order header with order-line data. For an order-line feed, propose `(source_system, order_id, line_id)` as a candidate business key, then ask the owner whether lines are ever renumbered. Design a snapshot manifest proving scope and completion. Explain how a delete is delivered and how long changes remain replayable.

**Deliverable:** A filled [onboarding contract](05_AZURE_INTEGRATION.md), with unknowns marked and named owners to resolve them.

**Exit check:** Explain what happens if the extraction watermark advances before landing succeeds. Propose a resume point and evidence proving the repaired scope is complete.

## Lesson 4 — Preserve Bronze evidence

**Purpose:** Load data without disguising re-delivery or corruption. Read the lab setup and inspect the CSV before running. Predict B1's raw row count, invalid records and repeated event ID. Use the lab's stable `line_id` to distinguish two delivered lines containing the same event.

**Exercise:** Run only the Bronze stage for B1. Confirm the table stores source strings and provenance. Rerun it and verify the line count remains unchanged. Change a line's payload under the same `line_id` in a separate fixture copy and explain why the lab should refuse that mutation.

**Deliverable:** Bronze count, distinct event count, source-line count and evidence of the retry behavior.

**Exit check:** The lab's Bronze merge is insert-only by source-line identity. How does that differ from preserving every retry attempt in an operational audit, and from an append-only streaming event archive?

## Lesson 5 — Type, validate and quarantine

**Purpose:** Make parsing failures explicit and recoverable. Read core §§5–6. Use decimal arithmetic for monetary values and tolerant parsing with a rejection policy. Inspect schema before and after conversion.

**Exercise:** Run B1 Silver, then inspect all rejects. Prove every raw B1 line was either valid or rejected before event deduplication. Show why store `S99` remains valid while an empty order ID cannot enter current state. Add a separate exercise rule for accepted status codes without altering the supplied baseline fixture.

**Deliverable:** Rule catalogue, reason counts and examples of raw/parsed values. Describe the owner and replay route for each reason.

**Exit check:** What goes wrong with `coalesce(try_cast(amount AS DECIMAL), 0)`? When does a negative amount represent a valid refund rather than bad data?

## Lesson 6 — Deduplicate and sequence changes

**Purpose:** Resolve authoritative state rather than arbitrarily dropping rows. Read Delta §§2–4. Distinguish source-line ID, event ID and business key. Deduplicate exact event deliveries, then select the greatest source sequence per business key.

**Exercise:** Predict which B2 row wins for order 1003. Run B2 and show the difference between valid input events and resulting state rows. In a scratch candidate DataFrame, add two different payloads at the same key/sequence; identify the gate that should stop mutation. Do not use the baseline lab tables for contradictory experiments.

**Deliverable:** Candidate uniqueness query, equal-sequence conflict query and target-state comparison.

**Exit check:** Explain why `dropDuplicates(["order_id"])` is insufficient and why an additional date restriction in the merge match can insert a duplicate historical key.

## Lesson 7 — Apply deletes and survive stale replay

**Purpose:** Demonstrate that arrival order cannot override source order. Read Delta §4. The lab retains a tombstone for deleted order 1002 and excludes it from analytical sales.

**Exercise:** Run B3 after B2. Confirm the stale upsert for deleted 1002 cannot resurrect it, the old amount for 1001 cannot replace 120.00, and the same-sequence equivalent payload for 1003 changes no business state. Rerun B2 after B3 and check results again.

**Deliverable:** Before/after states with source sequence and deletion flag. Record the tombstone retention argument: how long can a stale event arrive?

**Exit check:** If you physically delete the tombstone and forget sequence 2, what could a later sequence-1 event do? What additional durable state would let you use physical deletes safely?

## Lesson 8 — Build a Gold product and reconcile it

**Purpose:** Deliver a business interface with a declared grain. Read core §4 and the lab's expected results. Gold groups active orders by order date and original store code, with known store names and an unknown label where needed.

**Exercise:** Run Gold/validation for B1, then B2, then B3 in their respective pipeline runs. Reconcile active Silver amount to Gold totals. Verify the store dimension is unique and unknown orders survive the left join. Explain which prior-day group changes after B2's late correction.

**Deliverable:** Grain statement, measure definition, row/key uniqueness and business reconciliation. Include a consumer-facing `data_as_of` design even though the tiny lab does not implement a production release manifest.

**Exit check:** Why can a Gold table have fewer rows than Silver while still be complete? Why can equal overall totals conceal wrong store attribution?

## Lesson 9 — Design incremental file ingestion and streaming state

**Purpose:** Move beyond the bounded CSV lab without claiming a new pipeline is already verified. Read Delta §§6–8. Build an optional Auto Loader experiment in separate tables/paths using the documented example; do not point it at existing lab checkpoints or sinks.

**Exercise:** Deliver one JSON file, run available-now ingestion, rerun with no new files, then deliver a different file containing a duplicate business event. Add an optional field and record your chosen schema-evolution behavior. Compare file progress with business-event deduplication.

**Deliverable:** Source path, checkpoint path, schema path, target, observed counts and recovery notes. If not executed, submit a reasoned prediction marked unverified.

**Exit check:** Explain a watermark's role in state management. Why can deleting a checkpoint replay business effects, and why does a `foreachBatch` callback need idempotent external side effects?

## Lesson 10 — Choose the source integration pattern

**Purpose:** Match the source contract to actual access and recovery capabilities. Read Azure §§1–4. Compare scheduled extraction, managed ingestion, JDBC, event streaming and federation for one new operational system.

**Exercise:** Assume the source database exposes a modification timestamp but no delete feed. Document what incremental extraction can and cannot preserve. Add a durable landing manifest and an overlap/composite-cursor policy for timestamp ties. Propose reconciliation snapshots for deleted or changed data and quantify the possible stale interval.

**Deliverable:** Decision table for latency, source load, network route, authentication, schema changes, deletes, replay and ownership.

**Exit check:** When is live federated querying useful? Why does it not supply an independently retained Bronze history? Who pays the cost of repeated queries against the operational database?

## Lesson 11 — Publish to or read from Synapse deliberately

**Purpose:** Avoid conflating a shared storage account with reader compatibility. Read Azure §§5–7. Name whether Synapse means serverless SQL, dedicated SQL pool, Spark pool or orchestration pipelines.

**Exercise:** Design two alternatives for Gold consumption: Databricks SQL directly, and a versioned Parquet export loaded into a dedicated SQL pool. For a serverless Delta query, inspect table features and reader support before choosing it. Explain why reading Parquet files directly from a Delta table path is unsafe after updates/deletes.

**Deliverable:** A transfer/publication contract including snapshot version, row count, total, downstream load state, data-as-of, SQL/schema mappings and atomic consumer cutover strategy.

**Exit check:** A dedicated SQL pool load reaches the JDBC endpoint but cannot read ADLS staging. Which distinct identity/network controls need investigation?

## Lesson 12 — Deploy a task graph with bundles

**Purpose:** Make the lab's execution repeatable. Read 06 and inspect the lab bundle. Use an existing compatible cluster, development catalog and uploaded fixture path. Validate the resolved target, review the plan, deploy and run B1 in a clean lab state.

**Exercise:** Compare local YAML parsing, bundle validation, deployment, runtime execution and data assertions. Capture one evidence item per stage. Do not treat `bundle validate` as a job dry run. Pin the CLI version you used and record the direct deployment engine.

**Deliverable:** A deployment evidence chain: commit → resolved config/plan → resource identity → run → reconciled table state.

**Exit check:** What happens if two developers use the same shared bundle state/root? What distinguishes a personal development target from a stable production deployment identity?

## Lesson 13 — Orchestrate and observe the whole chain

**Purpose:** Coordinate extraction, transformation and publication without duplicate owners. Read 06 §§4–6. Draw dependencies and specify exactly when a cursor or manifest can advance.

**Exercise:** Simulate Bronze completion followed by a Silver failure. Predict the committed tables and the appropriate repair scope. Design an always-run audit/notification path that cannot make failed required data tasks appear successful. If Synapse/ADF triggers Databricks, propagate batch ID and code/version evidence across both systems.

**Deliverable:** Retry matrix, correlation fields, freshness/quality alerts and a publication gate. Use system-table observations where you have access; log missing access rather than inventing metrics.

**Exit check:** Why does retrying an entire notebook start its logic again? Which external side effect needs its own idempotency key?

## Lesson 14 — Tune a measured bottleneck

**Purpose:** Improve a correct pipeline with a defensible experiment. Read core §10 and capstone performance requirements. Use a larger synthetic dataset in a separate namespace; the baseline lab proves logic, not scale.

**Exercise:** Measure an intentionally skewed join or many small files. Form one hypothesis, change one factor, hold the input/compute conditions comparable and compare duration, shuffle/spill, scan bytes and usage. Verify row/key/total parity after the change. Evaluate layout against all downstream readers.

**Deliverable:** Baseline, hypothesis, experiment, result, cost implications and correctness evidence. If you lack adequate data or compute access, explain the experiment design without claiming a speedup.

**Exit check:** Why is broadcasting a dimension useful only if it fits the actual execution memory budget? What would make a faster run incomparable to its baseline?

## Lesson 15 — Investigate incidents with evidence

**Purpose:** Recover quickly without hiding the defect. Attempt [workbook](07_TROUBLESHOOTING_PRACTICE.md) cases 1–4, 5–9, 10–13 and 14–18, then choose Azure/performance incidents. Keep answers closed until you have an attempt or explicitly ask for help.

**Exercise:** For each incident, state the observed impact and first failing boundary. Give two competing hypotheses, a discriminating check, minimal repair and business verification. Explain which evidence a teammate must supply and what you can investigate independently.

**Deliverable:** Three completed incident records: one data correctness incident, one deployment/identity incident and one orchestration or integration incident.

**Exit check:** When is retry appropriate, when is it ineffective, and when can it worsen the incident? How do you prove a historical backfill did not duplicate or delete records outside its scope?

## Lesson 16 — Deliver and defend the capstone

**Purpose:** Join implementation with operating responsibility. Complete [08](08_READINESS_AND_CAPSTONE.md). Give a reviewer a contract, diagram, commit, run evidence, reconciliations, failure drill and a runbook they can execute.

**Exercise:** Present your design as a data engineer, then as the source owner and finally as a BI consumer. Each perspective should reveal a different question: recovery, delivery completeness and measure/data-as-of semantics.

**Deliverable:** A reproducible data product plus an evidence pack. Mark optional integrations/cloud steps honestly if unexecuted. Agree on remaining gaps and the next bounded exercise rather than declaring readiness from hours studied.

**Exit check:** Can another engineer recover the failed batch from your record alone? Can a consumer identify the published dataset's source scope and freshness?

## Cross-vendor notebook prompts

Extend your existing master notebook with these comparisons. They are conceptual comparisons, not equivalence claims.

| Universal question | Databricks exercise | Comparison to your other study |
|---|---|---|
| Where is raw evidence retained? | Bronze events and source files | dbt sources often refer to data ingested by another tool |
| How is transformation dependency represented? | Job graph / declarative pipeline graph | dbt `ref()` graph; Snowflake task orchestration |
| What guarantees a key is unique? | Explicit validation; candidate selection | dbt tests; warehouse constraints vary |
| What publishes a release? | Versioned bundle and data publication gate | dbt production build; vendor-specific scheduling |
| How does incremental state recover? | Source offsets, checkpoints, sequences, replay | dbt incremental selection/matching; other CDC systems |
| What proves quality? | Reconciled counts, amounts and attribution | dbt tests and business reconciliations across platforms |

## Closed-book retrieval checks

1. Draw the data and control paths and name the identity crossing each.
2. State Bronze, Silver and Gold grain for the lab.
3. Give a counterexample to using arrival time as authoritative ordering.
4. Explain duplicate event delivery versus two legitimate changes to one key.
5. Predict the effect of an old upsert after a newer delete.
6. Explain why source progress and sink publication need coordinated recovery.
7. Distinguish table constraints from pipeline expectations and quarantine.
8. Name three ways a correct Databricks read can still produce a wrong Synapse result.
9. Separate parsing, deployment, runtime and data verification evidence.
10. Explain a performance experiment whose outputs remain correct.

Record weak explanations as next exercises. The [official index](09_OFFICIAL_DOC_INDEX.md) supplies targeted reading; it is not a requirement to read every linked page before implementing a small example.
