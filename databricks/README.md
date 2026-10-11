# Databricks data engineering: numbered study path

**Start with [00 — Start here](00_START_HERE.md).** This is an Azure-focused, practical course for building and operating reliable Databricks pipelines. It follows the guide → course → lab → deeper references → practice structure of the [dbt guide](../dbt/dbt-study-guide/README.md) and [SnowPro GenAI collection](../snowpro-genai/README.md).

Prepared **7 October 2026** using current official documentation. The teaching examples are original. This is a professional skills curriculum, not an official certification blueprint; it does not change your existing exam order.

| Order | Material | What you will do |
|---:|---|---|
| **00** | [Start here](00_START_HERE.md) | Check prerequisites, attempt three diagnostic cases and choose a route |
| **01** | [Core study guide](01_CORE_STUDY_GUIDE.md) | Understand the lakehouse, Spark, Delta, Unity Catalog, medallion layers and pipeline contracts |
| **02** | [Course companion](02_COURSE_COMPANION.md) | Work through 16 lessons with deliverables, retrieval checks and a flexible four-week route |
| **03** | [Operational-data lab](03_OPERATIONAL_DATA_LAB/README.md) | Build Bronze → Silver → Gold using supplied CSV, a PySpark notebook, SQL checks and a bundle |
| **04** | [Delta Lake and streaming deep dive](04_DELTA_AND_STREAMING.md) | Reason about merges, CDC, sequencing, state, schema changes, retention and recovery |
| **05** | [Azure integration and source onboarding](05_AZURE_INTEGRATION.md) | Integrate ADLS, operational databases, APIs, ADF/Synapse and downstream consumers |
| **06** | [Bundles, deployment and orchestration](06_BUNDLES_AND_ORCHESTRATION.md) | Diagnose DAB failures and design promotion, identities, task dependencies and release controls |
| **07** | [Troubleshooting practice workbook](07_TROUBLESHOOTING_PRACTICE.md) | Attempt 28 original incidents; answers are withheld until an attempt or request for help |
| **08** | [Readiness, capstone and runbooks](08_READINESS_AND_CAPSTONE.md) | Demonstrate correctness, recovery, performance and collaboration with evidence |
| **09** | [Official documentation index](09_OFFICIAL_DOC_INDEX.md) | Find the precise source for a concept, syntax rule or compatibility limitation |
| **10** | [Unity Catalog volumes](10_UNITY_CATALOG_VOLUMES_GUIDE.md) | Understand volumes, choose managed/external, create/upload/read files and set permissions |
| **11** | [Lakeflow pipelines and DLT](11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md) | Map legacy DLT APIs, define streaming/materialized datasets, validate quality and reason about refresh/recovery |
| **12** | [Pipelines, CDF, CDC and Auto Loader examples](12_PIPELINES_CDF_CDC_AUTO_LOADER_EXAMPLES.md) | Work through fake order tables, file deliveries, corrections, deletes, stale events and expected reconciliations |
| **13** | [Managed and external storage](13_MANAGED_AND_EXTERNAL_STORAGE_GUIDE.md) | Distinguish locations, credentials, tables and volumes; choose ownership/lifecycle and set up each approach |
| **14** | [Pipeline operations and optimisation](14_PIPELINE_OPERATIONS_AND_OPTIMISATION.md) | Monitor delivery and correctness, diagnose/fix 15 worked incidents, recover safely and measure query/ingestion/compute/cost improvements |
| **15** | [Field notes: volume files, dropping catalogs/schemas, pipeline SQL errors](15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md) | Read Excel/CSV from a volume, safely drop a catalog or schema, and fix the "not supported in a DLT pipeline" error |
| **16** | [CDC/CDF retail-table walkthrough](16_CDC_CDF_RETAIL_TABLE_WALKTHROUGH.md) | Locate/check/read CDF on your screenshot's table, test fake corrections/deletes and include AUTO CDC in a separate pipeline |
| **17** | [CDF and CDC explained](17_CDF_AND_CDC_EXPLAINED.md) | Understand what CDC and CDF are, how they differ and combine, with use cases and when to choose each |
| **18** | [Pipeline monitoring and troubleshooting runbook](18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md) | Check health, query the event log, diagnose common failures and recover safely |
| **19** | [Video demo: Auto Loader and a Lakeflow pipeline](video-demo-auto-loader/README.md) | Step-by-step demo with three sample CSVs (one initial, two added later), notebook and pipeline versions, Azure Blob option and a video outline; follow-up guides for schema evolution, CDC and Azure file-notification mode |
| **20** | [Data engineer skills map and PySpark essentials](20_DATA_ENGINEER_SKILLS_MAP_AND_PYSPARK_ESSENTIALS.md) | Where Auto Loader and CDC/CDF fit among core skills, PySpark basics on the retail sample, and a video outline |

Use 04–06 alongside the related lessons. The default path is numbered so the order is also visible in the GitHub file listing. References are available whenever you need them.

Read **10** before the volume/upload setup in lab **03** if volumes are new to you. Read **11** alongside **04**, then use **12** for concrete pattern comparisons and fake-table exercises. Use **13** to choose managed/external storage and understand external-location setup. Continue with **14** for monitoring, worked fixes, recovery and measured optimisation; **16** walks through CDC/CDF using your retail-table screenshot and an isolated demo. These are supplementary practical guides; existing 00–09 filenames remain stable.

## What the course covers

| Your requested responsibility | Coverage | Evidence you will produce |
|---|---|---|
| Design and maintain ETL workflows | 01 §§3–6; 02 lessons 3–8; 03 lab | Source contract, executable transformations, reconciled output |
| Collaborate on reliability and efficiency | 02 lessons 12–16; 06; 08; 14 | Ownership map, runbook, release evidence, measured performance |
| Cleanse and prepare datasets | 01 §§5–6; 03; 07 cases 5–9 | Explicit types, quarantine reasons, uniqueness and join checks |
| Investigate Delta merge failures | 04 §§2–5; 07 cases 1–4 | Candidate-key analysis, sequencing policy, verified repair |
| Investigate PySpark errors | 01 §5; 07 cases 5–9, 22–23 | First failing stage, schema/plan evidence, minimal fix |
| Investigate DAB deployment issues | 06; 07 cases 14–18, 28 | Resolved target, identity, deployment plan, runtime check |
| Investigate ingestion/orchestration failures | 04 §§6–8; 05; 06; 07 cases 10–13, 19–21 | Checkpoint/source evidence, retry boundaries, replay proof |
| Integrate Azure Synapse and Databricks | 05; 07 cases 19–21 | Explicit transfer direction, reader compatibility, both-side access checks |
| Maintain Bronze, Silver and Gold | 01; 03; 08 | Layer responsibilities, grain, incremental and delete behavior |
| Preserve schema, quality and performance | 04; 05; 08; 14 | Versioned contracts, quality gates, representative benchmark |

## What has been validated

The accompanying [verification record](verification.json) describes local checks. The fixture oracle runs without Spark; Python parsing and Markdown/YAML checks do not establish that the notebook or bundle runs in Databricks. **No Databricks workspace, Azure resource, Synapse query, Spark job or deployment was executed while authoring this course.** The lab includes expected results and assertions for you to verify in a development workspace.

Current names matter: **Declarative Automation Bundles** were formerly **Databricks Asset Bundles**; both use the DAB abbreviation and `databricks bundle` commands. **Lakeflow Spark Declarative Pipelines** is the current pipeline family formerly associated with Delta Live Tables. Existing projects can contain older names/APIs. Follow the installed CLI/runtime and current documentation rather than renaming code mechanically. [Bundles overview](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/) · [Pipelines overview](https://learn.microsoft.com/en-us/azure/databricks/ldp/)

Record attempts and evidence in [progress.csv](progress.csv). Your real source systems, SLAs, workspace capabilities and chosen environment layout remain unspecified; examples use a synthetic retail operations domain.
