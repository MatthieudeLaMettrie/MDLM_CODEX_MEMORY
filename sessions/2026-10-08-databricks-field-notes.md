# Databricks field notes: volume files, drop catalog/schema, pipeline SQL error

Date: 2026-10-08 (Australia/Sydney)
Task identifier: not available (Claude Code session)

## Request and evidence

User asked four things in sequence, with two workspace screenshots and one pasted error: how to read a volume file in a Databricks notebook; how to drop a catalog; how to drop only a schema; and how to fix a pipeline error saying a `SELECT` is not supported in a DLT pipeline. Finally, user asked for these findings to be added to `databricks/` in this repository.

Screenshots showed catalog `mdlm_db_trial` (schemas default, dev, uat, prod; `uat`/`prod` empty), volume `/Volumes/mdlm_db_trial/dev/dev_volume` containing `fct_retail_sales_item_v.xlsx` (5.19 KB), and a pipeline notebook with `df = spark.read.` unfinished.

## Changes and decisions

Added [databricks/15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md](../databricks/15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md) and linked it as lesson 15 in the databricks README table. Key points: `.xlsx` needs pandas+openpyxl (or the newer native Excel reader), not plain `spark.read`; `DROP CATALOG/SCHEMA ... CASCADE` also deletes volumes and uploaded files; pipeline SQL files may only contain dataset definitions (`CREATE ... MATERIALIZED VIEW` / `STREAMING TABLE`), so a bare `SELECT` must be wrapped.

## Validation and unresolved issues

Documentation only. No SQL or notebook code was run, and no Databricks workspace was accessed; syntax comes from general knowledge and was not re-checked against current docs, notably the native `format("excel")` reader. `databricks/validate_materials.py` passed its local structure/reference checks (YAML parsing skipped, no PyYAML). Next step: try the readers and pipeline fix in the trial workspace.

## Follow-up: CDF/CDC explainer and monitoring runbook

User asked what CDF and CDC are (clearly, with use cases) and for a pipeline monitoring/troubleshooting file, both added to the repo. Existing lessons 12 (fake-table examples) and 14 (operations deep dive) already covered these in depth, so the new files are short plain-language entry points that link to them. A remote session had meanwhile published lesson 16 (retail-table CDC/CDF walkthrough); pulled it and numbered the new files 17 and 18 to avoid a collision.

Added [17_CDF_AND_CDC_EXPLAINED.md](../databricks/17_CDF_AND_CDC_EXPLAINED.md) (definitions, worked order story, AUTO CDC SCD1/SCD2, enabling/reading CDF, use cases, comparison table, decision guide, mistakes, quiz) and [18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md](../databricks/18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md) (health definition, where to look, event-log queries, troubleshooting sequence, common-problems table, recovery options, alerting, pre-flight checklist). Documentation only: no SQL/Python executed and no workspace accessed; event-log field paths and the AUTO CDC SQL syntax are unverified against current docs and the files say so.

## Follow-up: table operations and dashboard publishing

User asked how to see the operation on a table and whether a Databricks dashboard can be published to a website or SharePoint. Added sections 5 and 6 to [15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md](../databricks/15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md): `DESCRIBE HISTORY` (operations on the table) versus CDF `_change_type` (per-row operations), and dashboard options (publish, iframe embed needing admin-approved surfaces, email subscriptions, PDF). One standard web search informed section 6. Not executed or tested; SharePoint embedding is explicitly unverified.

## Follow-up: Genie Code and where errors/event logs live

User asked whether Genie AI can create/fix/monitor/optimise pipelines and where to find the event log for notebook or pipeline errors. A standard web search showed Genie Code Agent mode (Public Preview) builds and fixes Lakeflow pipelines, distinct from Genie Agents (data Q&A). Added sections 7 and 8 to [15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md](../databricks/15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md): Genie Code usage and safety, and a table of where to see errors (pipeline update/event log, notebook output, job runs, Query History, table history). Documentation only; UI labels and the Genie Code rename claim are unverified in a workspace.

## Follow-up (2026-10-10): Auto Loader video demo

User plans YouTube videos on IT and AI and asked for a step-by-step guide for Auto Loader ("data loaders") and a Databricks pipeline, using Azure Blob or a Volume, with one initial file and two more added later. Created [video-demo-auto-loader/](../databricks/video-demo-auto-loader/README.md): a guide, plus three CSVs in `data/` (8, 6 and 7 rows; revenue 172.90, 202.60, 207.30; running 582.80). Chose the Volume for the main path with an Azure Blob/ADLS section, a notebook version (cloudFiles, availableNow) and a Lakeflow pipeline (Bronze streaming table via `STREAM read_files`, Silver and Gold materialized views), expected numbers per step, troubleshooting, cleanup and a video outline. Totals and per-store/day revenue were computed locally. No Databricks code was run; UI labels and syntax are unverified in a workspace and the guide says to rehearse first. Registered as lesson 19 in the databricks README.
