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

## Follow-up: volumes, Lakeflow/DLT and practical pattern examples

Same task, 2026-10-07. User requested another Markdown file explaining volumes, their setup and contents; deeper coverage of the linked AWS pipeline-concepts page including the previous Delta Live Tables/dlt name; and use cases/realistic examples for pipelines, CDF, CDC, Auto Loader and related patterns with a fake table.

Re-read durable memory, three latest filename-ordered session records and repository instructions, and checked the current main checkout. Original course was already published. Other chats had since published dbt/recruiter artifacts; preserved those commits and their current navigation. Follow-up started from a clean tree at 4717f32. No branch changes or unrelated artifacts staged.

- Added 10_UNITY_CATALOG_VOLUMES_GUIDE.md: catalog/schema/volume/file versus table, managed/external choices and lifecycle, appropriate contents, file layout/access boundaries, SQL/UI setup, grants/run identities, lab CSV upload/read, small support-file example, Azure ADLS external-volume prerequisites and troubleshooting. Linked it before lab setup. No objects/grants/files were created in the cloud.
- Added 11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md based on the requested concepts page and current official reference pages. Explains current Lakeflow terminology, legacy dlt mappings (batch dlt.table becomes materialized_view; streaming becomes table), publishing-mode migration, dataset types, pipeline/job/bundle/volume boundaries, setup, expectations, refresh/reset and operational checks. Original optional five-dataset Python example uses Auto Loader, Bronze, typed temporary view, accepted/quarantine branches and Gold; expected 3 raw/2 accepted/1 rejected/165.00. Includes a SQL Silver alternative and explicit contexts/limits.
- Added 12_PIPELINES_CDF_CDC_AUTO_LOADER_EXAMPLES.md: proposed retail/ADLS/Synapse/history/quality use cases, fake current-order and append-only CDC tables, newline-delimited JSON files, ordinary notebook Auto Loader, mutable Delta CDF reads/archive, AUTO CDC SCD1 with a stale correction/delete, Gold output and CDF-to-CDC replica. Expected file totals 245/270 differ intentionally from corrected current-state 240. Wrong totals 530/405 illustrate event-versus-state and update-preimage semantics. SCD2 extension discusses temporal joins without pretending to implement them.
- Explicitly distinguishes legacy enabled Delta CDF from current automatic CDF requirements (qualifying UC tables/DBR 19+/Delta row tracking), authoritative source sequence from one table's commit version, business duplicates from file discovery and retention/replay from an unlimited audit history. Source examples deliberately assume valid CDC records and call out conflicts/quality/retention as additional controls.
- Extended numbered navigation to 00–12 without renaming the original assets; added lab/deep-dive/reference cross-links, updated root navigation/memory and verification metadata, and extended the reusable structure validator to require all 13 numbered assets.

Research used official Azure Databricks volume/SQL/identity/CDF/Auto Loader pages, the requested AWS pipeline concepts and related current configuration/Python/dataset/expectation/update/event-log/CDC pages, and Delta Lake CDF documentation. AWS concepts were applied without substituting AWS IAM/storage for the Azure course. Invalid guessed page paths were replaced with working current references; linked examples state runtime/context assumptions.

Validation: 14 Markdown files, 104 local links, balanced fences, 3 Python files and 17 Python documentation blocks parsed, 2 YAML files/1 YAML block with duplicate-key rejection, 2 JSON records parsed and existing bundle/local lesson/case checks passed. Reused the existing isolated PyYAML under approved read-only escalation. A separate local standard-library check read the new JSON/SQL fixtures, checked 245/270 file totals, and verified 240 latest state across all 5,040 permutations of seven CDC events plus 530/405 incorrect-metric and 165 quality arithmetic. Its first extraction expression missed whitespace in two SQL values; corrected the extraction and the complete seven-record check passed. These checks do not execute Spark, Delta SQL, expectations or AUTO CDC.

No workspace creation/inspection, upload, grants, pipeline update, ordinary stream execution, bundle deployment, Azure/Synapse changes or benchmark performed. Live output, restart/replay, access and retention evidence remain learner follow-ups. Reviewed task-owned changes and whitespace before committing/pushing current main under standing authorization; verify remote publication before the final response. Git history/final response provide publication hash evidence.

## Follow-up: when to choose pipelines, CDC, CDF and Auto Loader

User asked for a plain explanation of when to use each mechanism with realistic scenarios. Rechecked current memory, three latest session records, clean main and current official pipeline/CDF/CDC/Auto Loader documentation. Extended guide 12 section 1 with four decision questions, five proposed scenarios (recurring POS files, corrected/cancelled database orders, Delta-to-downstream changes, investigation/history and small nightly complete snapshots) and a combined architecture diagram.

Clarified broad data pipeline versus Databricks declarative pipeline, source CDC capture versus AUTO CDC application, CDF table evidence versus completed downstream synchronization, and file discovery versus business change/deduplication semantics. Batch schedules can use change feeds. AUTO CDC is not a universal source database extractor; an external CDF consumer needs supported transport/idempotency/progress. Cancellation may be a status update; missing rows imply deletion only for a guaranteed complete authoritative snapshot. CDF archive and SCD2 history serve distinct evidence/reporting requirements and do not supply missing actor/reason attributes automatically.

These are illustrative designs, not claims about the user's workplace or live implementation. Existing code/fixtures/expected results unchanged; durable memory already records the guide's scope, so no memory update needed. Checked local structure/navigation/fences and reviewed diff/whitespace before publishing only the guide and this continued session note. No cloud or runtime execution performed.
