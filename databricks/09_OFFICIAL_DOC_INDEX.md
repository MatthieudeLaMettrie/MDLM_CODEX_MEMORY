# 09 — Official documentation index

[Learning path](README.md) · [Core](01_CORE_STUDY_GUIDE.md) · [Practice](07_TROUBLESHOOTING_PRACTICE.md)

This is a **curated topic index**, not a downloaded documentation atlas or a claim to have reviewed every Databricks page. The course was researched on **7 October 2026** using official Databricks/Microsoft documentation and Apache Spark references. The links below support the named topics; pages can redirect or change after that date. Consult the actual runtime/CLI and each feature's availability notes before using code.

Microsoft Learn hosts official Azure Databricks documentation. Generic Spark `latest` currently documents a newer open-source release than some Databricks runtimes; use the Spark version bundled with your compute as the code reference. Databricks extensions such as AUTO CDC are not established merely by an Apache Spark API of a similar name.

## A. Platform, architecture and governance

| ID | Official source | Read for |
|---|---|---|
| A01 | [Azure Databricks introduction](https://learn.microsoft.com/en-us/azure/databricks/introduction/) | Platform components and execution surfaces |
| A02 | [Medallion lakehouse architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion) | Layer responsibilities and source-to-consumer progression |
| A03 | [Unity Catalog overview](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/) | Governance object hierarchy |
| A04 | [Unity Catalog best practices](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/best-practices) | Identity, isolation and ownership decisions |
| A05 | [Privileges reference](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/privileges-reference) | Exact permissions for catalogs, schemas, tables and volumes |
| A06 | [Unity Catalog volumes](https://learn.microsoft.com/en-us/azure/databricks/volumes/) | Non-tabular files, access and runtime requirements |
| A07 | [Work with volume files](https://learn.microsoft.com/en-us/azure/databricks/volumes/volume-files) | Upload/read/write the lab fixtures |
| A08 | [Azure managed identities for UC storage](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/azure-managed-identities) | Access Connector/storage identity and storage permissions |
| A09 | [Constraints](https://learn.microsoft.com/en-us/azure/databricks/tables/constraints) | Enforced versus informational rules |

## B. Spark, transformations and performance

| ID | Official source | Read for |
|---|---|---|
| B01 | [Spark DataFrames guide](https://spark.apache.org/docs/latest/api/python/user_guide/dataframes.html) | Structured distributed transformations |
| B02 | [PySpark Column API](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.html) | Column expressions and operators |
| B03 | [Spark SQL null semantics](https://spark.apache.org/docs/latest/sql-ref-null-semantics.html) | Null predicates, comparisons, joins and aggregates |
| B04 | [Spark JDBC](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html) | Database extraction, partition options and source load |
| B05 | [Spark SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html) | Plan, joins, adaptive execution and partitioning |
| B06 | [Spark Structured Streaming](https://spark.apache.org/docs/latest/streaming/index.html) | Streaming concepts and links to operator-specific guidance |
| B07 | [Liquid clustering](https://learn.microsoft.com/en-us/azure/databricks/tables/clustering) | Layout selection, compatibility and limitations |
| B08 | [Monitor and optimize workloads training](https://learn.microsoft.com/en-us/training/modules/monitor-troubleshoot-optimize-workloads-azure-databricks/) | Guided Spark/job diagnostic learning |

## C. Delta, changes, schema and recovery

| ID | Official source | Read for |
|---|---|---|
| C01 | [Merge into Delta](https://learn.microsoft.com/en-us/azure/databricks/delta/merge) | Match behavior, clauses and runtime-dependent duplicates |
| C02 | [Table history](https://learn.microsoft.com/en-us/azure/databricks/tables/history) | Versions, retained snapshots and recovery evidence |
| C03 | [Table properties](https://learn.microsoft.com/en-us/azure/databricks/tables/table-properties) | Table settings and retention-related configuration |
| C04 | [Schema enforcement](https://learn.microsoft.com/en-us/azure/databricks/tables/schema-enforcement) | Writer compatibility and source/target projections |
| C05 | [Schema evolution](https://learn.microsoft.com/en-us/azure/databricks/tables/update-schema) | Supported schema updates and streaming/write impact |
| C06 | [Isolation and conflicts](https://learn.microsoft.com/en-us/azure/databricks/optimizations/isolation/) | Transaction concurrency and troubleshooting |
| C07 | [Row-level concurrency](https://learn.microsoft.com/en-us/azure/databricks/optimizations/isolation/row-level-concurrency) | Table/runtime conditions and conflict behavior |
| C08 | [Deletion vectors](https://learn.microsoft.com/en-us/azure/databricks/delta/deletion-vectors) | Feature/reader consequences of updates/deletes |
| C09 | [Change data feed](https://learn.microsoft.com/en-us/azure/databricks/tables/features/change-data-feed) | Delta change consumption and retention |
| C10 | [table_changes function](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/table_changes) | Batch queries over enabled retained change history |

## D. File ingestion and declarative pipelines

| ID | Official source | Read for |
|---|---|---|
| D01 | [Auto Loader](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/) | Incremental cloud-file ingestion |
| D02 | [Auto Loader schema inference/evolution](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/schema) | Schema location, rescue and schema-change behavior |
| D03 | [foreachBatch](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/foreach) | Callback guarantees, full consumption and repeatable sinks |
| D04 | [Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/) | Managed pipeline model |
| D05 | [Pipeline Python reference](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-ref) | Dataset functions, decorators and valid definition behavior |
| D06 | [Pipeline expectations](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations) | Observe, drop and fail quality policies |
| D07 | [AUTO CDC overview](https://learn.microsoft.com/en-us/azure/databricks/ldp/cdc) | Keys, sequencing, SCD and required pipeline capabilities |
| D08 | [Replicate RDBMS with AUTO CDC](https://learn.microsoft.com/en-us/azure/databricks/ldp/database-replication) | Initial hydration and ongoing changes |
| D09 | [Lakeflow Connect concepts](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/) | Managed source connectors and ingestion boundaries |
| D10 | [SQL Server connector concepts](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sql-server-concepts) | Source-specific incremental/authentication behavior |
| D11 | [Federated external databases/catalogs](https://learn.microsoft.com/en-us/azure/databricks/query-federation/) | Live query access versus ingestion |

## E. Bundles, authentication and operations

| ID | Official source | Read for |
|---|---|---|
| E01 | [Declarative Automation Bundles overview](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/) | Current DAB name and deployment model |
| E02 | [Bundle configuration](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/settings) | Target/variable/configuration structure |
| E03 | [Bundle resources](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/resources) | Current resource/task schema |
| E04 | [Sharing bundle files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing) | Paths, state roots and external shared code |
| E05 | [Deployment modes](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/deployment-modes) | Development/production defaults and overrides |
| E06 | [Run identity](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/run-as) | Deployer versus execution principal |
| E07 | [Direct deployment engine](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/direct) | Engine/state migration and changed-setting semantics |
| E08 | [CLI bundle commands](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/bundle-commands) | Actual flags for validate/plan/deploy/run and parameters |
| E09 | [CLI authentication](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/authentication) | Profiles and supported user/workload routes |
| E10 | [OAuth M2M](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/oauth-m2m) | Databricks-managed service-principal authorization |
| E11 | [OAuth federation](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/oauth-federation) | Configured external workload identity |
| E12 | [Bundle library dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies) | Reproducible task artifacts/packages |
| E13 | [Serverless environment dependencies](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies) | Environment/version/library configuration |
| E14 | [Job task control flow](https://learn.microsoft.com/en-us/azure/databricks/jobs/control-flow) | Dependencies, run conditions and failure paths |
| E15 | [Repair job failures](https://learn.microsoft.com/en-us/azure/databricks/jobs/repair-job-failures) | Identify failure and rerun appropriate task scope |
| E16 | [Billable usage system table](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/billing) | Usage units, metadata and correction records |
| E17 | [Jobs system tables](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/jobs) | Operational job history and cost-attribution limits |

E02's Azure page repeatedly timed out in the browsing tool during authoring. Its public search entry was available; resource/path/mode/identity details were cross-checked with E03–E08 and official examples. This is a retrieval limitation, not evidence that your workspace cannot use bundles.

## F. Synapse and existing Azure orchestration

| ID | Official source | Read for |
|---|---|---|
| F01 | [Synapse serverless Delta queries](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/query-delta-lake-format) | Delta v1 reader support and newer-feature limits |
| F02 | [ADLS-to-dedicated-SQL-pool loading](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-load-from-azure-data-lake-store) | Staging/COPY route and warehouse ingestion |
| F03 | [ADF/Synapse connector overview](https://learn.microsoft.com/en-us/azure/data-factory/connector-overview) | Supported integration directions/capabilities |
| F04 | [Databricks Job activity](https://learn.microsoft.com/en-us/azure/data-factory/transform-data-databricks-job) | External orchestrator triggering a Databricks job |
| F05 | [Databricks Notebook activity](https://learn.microsoft.com/en-us/azure/data-factory/transform-data-using-databricks-notebook) | Existing notebook activity integration |
| F06 | [Archived Databricks Synapse connector](https://learn.microsoft.com/en-us/azure/databricks/archive/connectors/synapse-analytics) | Legacy connector diagnosis; not default new-architecture advice |

## Version/compatibility questions to revisit before a live implementation

| Question | Source | Why it matters |
|---|---|---|
| Which duplicate-match rules apply on this runtime? | C01 | 16.0+ and 15.4 LTS differ |
| Which reader features does the table require? | C03, C08, F01 | A downstream engine can misread or reject modern tables |
| Which streaming changes can resume with existing state? | D02, D03, B06 | State reset can replay/miss effects |
| Which CDC/pipeline capabilities are enabled? | D04–D08 | Databricks extensions and editions are not generic PySpark |
| Which CLI engine and schema are active? | E03, E07, E08 | State/config/command behavior changes by version |
| Which principal actually executes? | A05, E06, E09–E11 | Successful deployment does not grant data access |
| Which Synapse component and connector is in use? | F01–F06 | Serverless/dedicated/Spark/pipelines have different contracts |

## How to use this index

The 61-entry core index is supplemented by source links beside the explanations in [10 — Volumes](10_UNITY_CATALOG_VOLUMES_GUIDE.md), [11 — Pipelines and DLT](11_LAKEFLOW_PIPELINES_AND_DLT_GUIDE.md), [12 — Fake-table pattern examples](12_PIPELINES_CDF_CDC_AUTO_LOADER_EXAMPLES.md), [13 — Managed/external storage](13_MANAGED_AND_EXTERNAL_STORAGE_GUIDE.md) and [14 — Pipeline operations and optimisation](14_PIPELINE_OPERATIONS_AND_OPTIMISATION.md). Guide 14 adds event-log/system-table monitoring, profiles, recovery, statistics/layout and compute/cost references. Guide 11 explicitly incorporates the requested AWS pipeline-concepts page; Azure storage/identity guidance remains the course default.

Start with the failing boundary and the [workbook case](07_TROUBLESHOOTING_PRACTICE.md), then open the narrowest relevant page. Write down the rule, its runtime/feature conditions and the check that proves it applies. Add that evidence to your master notebook. Do not substitute copying a long page for reproducing the small behavior you need to understand.

[16 — Retail-table CDC/CDF walkthrough](16_CDC_CDF_RETAIL_TABLE_WALKTHROUGH.md) adds screenshot-specific UI/SQL steps and references for properties/history, feed modes, `table_changes` and AUTO CDC application.

Keep your locked certification sequence in the [existing curriculum](../learning/certifications/AI_STUDY_CURRICULUM.md). This course adds practical Databricks data engineering materials; it does not assign another credential or imply full coverage of a live exam blueprint.
