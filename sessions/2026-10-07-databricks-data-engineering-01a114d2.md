# Databricks data engineering course

Date: 2026-10-07 (Australia/Sydney)
Task identifier: 01a114d2-e84c-7300-8f56-42147cce9849

## Request and context

User requested Databricks materials with the same organization, quality and depth as dbt/dbt-study-guide and snowpro-genai. Requested coverage includes ETL/data preparation, collaboration on reliable/efficient pipelines, data cleansing, Delta merge failures, PySpark errors, DAB deployment failures, ingestion/orchestration failures, Azure Synapse integration, operational-source onboarding, medallion architecture, schema integrity, quality and performance. Additional relevant topics were permitted.

Read MEMORY.md, the three latest filename-ordered notes, AGENTS.md and both existing guide structures. Initial working tree was clean on main with the configured requested GitHub origin. During authoring, another chat committed dbt RSS metric explanation/filter/category updates in this shared checkout. Preserved them; did not edit or stage that course/session. Rechecked repository state before navigation/memory updates. The concurrent dbt commit bc7caae also carried the newly written Databricks memory entry; confirmed that durable entry was already in HEAD, so the course commit does not duplicate the memory diff.

## Changes and decisions

- Created databricks/ as a numbered 00–09 collection, with README learning path and coverage matrix, matching guide/course/lab/practice/reference organization.
- Core guide explains platform boundaries, UC catalogs/schemas/environments, source contracts, Bronze/Silver/Gold, Spark plans/expressions/joins, parsing/quarantine, incremental matching, identities, performance and operation.
- Course companion provides 16 lessons, deliverables/exit checks, a flexible four-week 24–36-hour route and cross-vendor master-notebook prompts. This is an authored professional-skills curriculum, not an official certification blueprint; no existing exam order changed.
- Added a bounded development lab with 16 synthetic delivered lines across B1/B2/B3, JSON expected results, parameterized PySpark source notebook, setup/reconciliation SQL, development bundle with direct engine and a four-task job, and independent standard-library fixture oracle.
- Lab preserves raw values and source-line identity, distinguishes duplicate events from changes, quarantines three invalid records, retains unknown store S99, applies authoritative sequence, retains a delete tombstone and protects state from stale replay. B1: 4 active orders/215.00. B2/B3: 4 active orders/270.00; current state has 5 rows including deleted 1002. Gold attribution also has fixed expected results.
- Deep chapters cover Delta/CDC/streaming, schema/retention/recovery, optional Auto Loader and declarative CDC fragments, Azure source/network/identity integration, Synapse component/reader distinctions, versioned Parquet publication/dedicated-pool loading, bundles/CI/CD/deployment identities, retries/task control and monitoring/cost interpretation.
- Added 28 original incident exercises with answers withheld under the existing practice preference, practical readiness rubric, capstone, failure matrix and handoff/runbook templates.
- Added a curated 61-entry official reference index, progress CSV, reusable local structure validator and explicit verification record. Linked new course from root README and updated concise durable memory.

## Research and boundaries

Used official Microsoft Azure Databricks, Synapse/ADF and Apache Spark documentation. Current name is Declarative Automation Bundles (formerly Databricks Asset Bundles). Covered the 16.0+/15.4 merge duplicate-match boundary, current direct engine guidance, UC/table/volume privileges, streaming callback replay, CDF retention and serverless Synapse Delta-v1 reader limitations. The Azure bundles/settings page repeatedly timed out in web retrieval; its official search entry and related resource/sharing/mode/identity/CLI references supplied cross-checks. The index states this limitation and does not claim a full documentation crawl.

Real operational sources, SLAs, Synapse component, workspace/compute capabilities and user-selected production architecture remain unspecified. The lab uses an existing dedicated *_dev catalog, uploaded fixture and compatible classic compute; no production target/schedule or external side effects. It deliberately full-rebuilds tiny Gold. It is not a live ingestion integration, a permanent historical conflict ledger, an SCD2 implementation or an atomic multi-table release system. Optional code fragments state their prerequisites and limits.

## Validation and limits

- Independent fixture oracle passed raw/reject/state counts, decimal arithmetic, day/store attribution, reverse input ordering, exact/stale re-delivery, delete tombstone and contradiction checks.
- Validator passed 11 Markdown documents/81 relative links/balanced fences, three Python files and eight Python documentation blocks via AST, two YAML files and one YAML documentation block with duplicate-key rejection, and two JSON files.
- Confirmed 00–09 path, all 16 lessons/all 28 cases, bundle local notebook/sync paths, four-task dependencies and max concurrency. These checks are not Databricks bundle schema validation.
- Python 3.14.4 used. Reused PyYAML 6.0.3 from an existing isolated temporary directory; sandboxed Python could not read it, so the read-only local check ran through approved escalation with bytecode writes disabled. No project dependency/CLI/runtime installed.
- Reviewed authored code, expected assertions, consistency, navigation/memory diff and Git whitespace before publication.
- No Databricks workspace/source inspection, Spark execution, bundle validate/deploy/run, Azure resource change, Synapse query/load or performance benchmark was performed. Cloud/runtime evidence remains a learner follow-up, not a claimed completed check.

## Publication and next step

Commit only databricks/, root navigation, relevant memory and this session record; push current main under standing authorization and verify publication. Git history/final response provide exact publication evidence without follow-up hash-only commits. Preserve concurrent work and reconcile any remote advancement safely.

Start with 00 diagnostics, study core/course and run the lab in an authorized development workspace. Next live tailoring needs source contract, actual runtime/CLI, compute/access mode, run identity, selected Synapse component and sanitized error evidence if applicable.
