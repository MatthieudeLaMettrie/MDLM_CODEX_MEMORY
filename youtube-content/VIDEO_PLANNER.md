# Video planner: 50 concepts

[Back to the YouTube content folder](README.md) · [Production checklist](PRODUCTION_CHECKLIST.md) · [Sortable CSV](video-planner.csv)

Created 11 October 2026. **View counts cannot be guaranteed, and search volume and competition were not checked for any idea.** Priority is a judgement based on search intent and on what you already have written. Test each idea against YouTube autocomplete and recent competing videos before you commit (see the checklist).

**Priority:** High = start here; Medium = good next; Low = later. **Readiness:** Ready = a guide with demo data exists in this repo; Partly = a related guide exists; Needs research = nothing written yet.

**Audience:** Beginner = explains a concept from scratch; Practitioner = fixes a real problem or compares options for working data people; Certification = exam preparation. The channel targets all three, so mix them (25 Practitioner, 20 Beginner, 5 Certification; see the folder README).

**Series:** S1 = Databricks pipelines in 10 (publish first, in the order shown), S2 = AI for data work (second), Later = hold until the first two series have an audience. See [SERIES_PLAN.md](SERIES_PLAN.md).

**Target length:** 6–10 minutes (never above 10).


## Databricks

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 1 | Auto Loader explained in 10 minutes | Drop 3 files, watch only new ones load; notebook then pipeline | Beginner | S1 #1 | High | Ready | [guide](../databricks/video-demo-auto-loader/README.md) |
| 2 | Fix 5 common pipeline errors ("not supported in a DLT pipeline" and more) | Show the real error, the cause, the 1-line fix | Practitioner | S1 #4 | High | Ready | [guide](../databricks/18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md) |
| 3 | Volumes vs managed tables vs external locations | When to use each, with a live example | Beginner | S1 #5 | Medium | Ready | [guide](../databricks/10_UNITY_CATALOG_VOLUMES_GUIDE.md) |
| 4 | CDC vs CDF with a live AUTO CDC demo | Insert, update, delete and a late event that must be ignored | Practitioner | S1 #3 | High | Ready | [guide](../databricks/video-demo-auto-loader/03_CDC_VIDEO.md) |
| 5 | Delta MERGE: "multiple source rows matched" and the fix | Reproduce the failure, then dedupe by sequence | Practitioner | S1 #6 | Medium | Partly | [guide](../databricks/04_DELTA_AND_STREAMING.md) |
| 6 | Genie Code: build a pipeline from one prompt | Prompt, plan approval, run, review the diff | Practitioner | S1 #7 | High | Partly | [guide](../databricks/15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md) |
| 7 | Unity Catalog permissions for beginners | Catalog, schema, volume grants and the run-as identity trap | Beginner | Later | Medium | Partly | [guide](../databricks/01_CORE_STUDY_GUIDE.md) |
| 8 | Deploy dev to prod with bundles | One bundle, two targets, what breaks and why | Practitioner | S1 #8 | Medium | Partly | [guide](../databricks/06_BUNDLES_AND_ORCHESTRATION.md) |

## Snowflake

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 9 | Cortex AI functions in plain SQL | Summarise, classify and extract with a few lines of SQL | Beginner | Later | Medium | Partly | [guide](../snowpro-genai/README.md) |
| 10 | Dynamic tables vs streams and tasks | Same pipeline built both ways, which is simpler | Practitioner | Later | Medium | Needs research | none yet |
| 11 | Stop burning credits: warehouse sizing mistakes | 5 settings that quietly cost money | Beginner | Later | High | Needs research | none yet |
| 12 | Time Travel and zero-copy clone | Undo a bad delete in 60 seconds | Beginner | Later | Medium | Needs research | none yet |
| 13 | SnowPro Core: 10 exam traps | Your own cert experience, concept by concept | Certification | Later | Medium | Needs research | none yet |

## BigQuery

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 14 | Partitioning and clustering to cut your bill | Same query before and after, bytes scanned | Beginner | Later | High | Needs research | none yet |
| 15 | Dry run and cost control before you click Run | Estimate cost, set limits, avoid surprise bills | Beginner | Later | Medium | Needs research | none yet |
| 16 | Gemini inside BigQuery: what actually works | Honest tests, not a feature tour | Practitioner | Later | Low | Needs research | none yet |
| 17 | BigQuery + dbt Cloud setup, step by step | Connection, dataset, Git, production job | Practitioner | Later | Medium | Ready | [guide](../dbt/DBT_BIGQUERY_CLOUD_GUIDE.md) |

## Fabric

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 18 | Lakehouse vs Warehouse: which one to pick | Decision tree with a small example | Beginner | Later | High | Needs research | none yet |
| 19 | OneLake shortcuts explained | Zero-copy access across workspaces and clouds | Beginner | Later | Medium | Needs research | none yet |
| 20 | Direct Lake in 8 minutes | What it is, what makes it fall back to DirectQuery | Beginner | Later | Medium | Needs research | none yet |
| 21 | Fabric data agents over a semantic model | Set up, instruction layers, test questions | Practitioner | Later | Medium | Ready | [guide](../guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md) |
| 22 | DP-600 and DP-700: what to study first | Priorities from your own certs | Certification | Later | Medium | Needs research | none yet |

## dbt

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 23 | Incremental models: the 4 strategies | Append, merge, delete+insert, insert_overwrite with examples | Practitioner | Later | High | Partly | [guide](../guides/data-engineering/DATA_AND_DBT_CONCEPTS_GUIDE.md) |
| 24 | Snapshots and SCD2 made simple | Track a changing customer address over time | Beginner | Later | Medium | Needs research | none yet |
| 25 | Tests and source freshness that catch real problems | Beyond not_null and unique | Practitioner | Later | Medium | Partly | [guide](../guides/data-engineering/DATA_AND_DBT_CONCEPTS_GUIDE.md) |
| 26 | dbt semantic layer and metrics | Define a metric once, query it anywhere (RSS example) | Practitioner | Later | Medium | Ready | [guide](../dbt/dbt-study-guide/02_SEMANTIC_MODELS_AND_METRICS_COURSE.md) |
| 27 | dbt vs Dataform vs stored procedures | When each is the right tool | Beginner | Later | Low | Needs research | none yet |

## Power BI

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 28 | Import vs DirectQuery vs Direct Lake | One slow report, three modes, results compared | Practitioner | Later | High | Partly | [guide](../dbt/dbt-study-guide/11_POWER_BI_CONNECTION_AND_SLICERS.md) |
| 29 | CALCULATE explained with visuals | Filter context without the jargon | Beginner | Later | High | Needs research | none yet |
| 30 | Why your report is slow: star schema fixes | Before and after performance analyzer | Practitioner | Later | High | Needs research | none yet |
| 31 | Copilot and Prep for AI: make a model AI-ready | Descriptions, synonyms, verified answers | Practitioner | Later | Medium | Ready | [guide](../guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md) |
| 32 | PL-300: the hardest topics | Your exam experience, concept by concept | Certification | Later | Medium | Needs research | none yet |

## Claude

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 33 | Claude Code for data engineers | Real tasks: read a repo, fix a pipeline, write tests | Practitioner | S2 #1 | High | Needs research | none yet |
| 34 | Give your AI memory: a repo-based setup | Session notes and MEMORY.md, as you use them | Beginner | Later | Medium | Ready | [guide](../guides/continuity/VISUAL_GUIDE.md) |
| 35 | MCP explained: connect Claude to a database | What MCP is, a minimal working example | Beginner | S2 #2 | High | Needs research | none yet |
| 36 | Build a simple agent with the Claude API and tools | Tool use loop in about 40 lines | Practitioner | S2 #3 | Medium | Needs research | none yet |
| 37 | Claude vs ChatGPT for data work | Same 5 tasks, honest results | Practitioner | S2 #4 | High | Needs research | none yet |

## OpenAI

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 38 | ChatGPT and Codex for SQL and pipelines | Where it helps and where it fails | Practitioner | S2 #5 | Medium | Needs research | none yet |
| 39 | Structured outputs: get clean JSON every time | Schema, validation, retries | Practitioner | Later | Medium | Needs research | none yet |
| 40 | Build a RAG chatbot in 10 minutes | Chunk, embed, retrieve, answer, evaluate | Practitioner | Later | High | Partly | [guide](../learning/rag/AZURE_FOUNDRY_RAG_STUDY_COURSE.md) |
| 41 | Agents SDK basics | One agent, two tools, handoff | Practitioner | Later | Low | Needs research | none yet |

## Gemini

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 42 | NotebookLM as a study tool for certifications | Turn docs into quizzes and audio | Certification | Later | Medium | Needs research | none yet |
| 43 | Gemini API grounding and agent search | Grounded answers with sources | Practitioner | Later | Medium | Partly | [guide](../learning/rag/GCP_AGENT_SEARCH_RAG_STUDY_COURSE.md) |
| 44 | Gemini vs Claude vs GPT on one real task | Same prompt, scored on a rubric | Practitioner | S2 #6 | High | Needs research | none yet |

## Cross-platform

| # | Working title | Hook / angle | Audience | Series | Priority | Readiness | Supporting guide |
|--:|---|---|---|---|---|---|---|
| 45 | Databricks vs Snowflake vs Fabric: pick one in 10 minutes | Decision guide for beginners and teams | Beginner | Later | High | Needs research | none yet |
| 46 | Medallion architecture with real files | Bronze, Silver, Gold using the sample CSVs | Beginner | Later | Medium | Ready | [guide](../databricks/video-demo-auto-loader/README.md) |
| 47 | RAG on Azure vs GCP vs Snowflake side by side | Same documents, three stacks | Practitioner | Later | Low | Partly | [guide](../learning/rag/AZURE_FOUNDRY_RAG_STUDY_COURSE.md) |
| 48 | AI agent vs workflow: stop overbuilding | When a fixed pipeline beats an agent | Beginner | Later | Medium | Needs research | none yet |
| 49 | How I study for data certifications | Your real stack, schedule and mistakes | Certification | Later | Medium | Partly | [guide](../guides/continuity/VISUAL_GUIDE.md) |
| 50 | Data engineer roadmap 2027 with AI tools | What to learn, what AI changes | Beginner | Later | Medium | Needs research | none yet |

## Suggested order for the High-priority videos

Videos with ready material come first:

- **#1 Auto Loader explained in 10 minutes** (Databricks, Ready)
- **#2 Fix 5 common pipeline errors ("not supported in a DLT pipeline" and more)** (Databricks, Ready)
- **#4 CDC vs CDF with a live AUTO CDC demo** (Databricks, Ready)
- **#6 Genie Code: build a pipeline from one prompt** (Databricks, Partly)
- **#23 Incremental models: the 4 strategies** (dbt, Partly)
- **#28 Import vs DirectQuery vs Direct Lake** (Power BI, Partly)
- **#40 Build a RAG chatbot in 10 minutes** (OpenAI, Partly)
- **#11 Stop burning credits: warehouse sizing mistakes** (Snowflake, Needs research)
- **#14 Partitioning and clustering to cut your bill** (BigQuery, Needs research)
- **#18 Lakehouse vs Warehouse: which one to pick** (Fabric, Needs research)
- **#29 CALCULATE explained with visuals** (Power BI, Needs research)
- **#30 Why your report is slow: star schema fixes** (Power BI, Needs research)
- **#33 Claude Code for data engineers** (Claude, Needs research)
- **#35 MCP explained: connect Claude to a database** (Claude, Needs research)
- **#37 Claude vs ChatGPT for data work** (Claude, Needs research)
- **#44 Gemini vs Claude vs GPT on one real task** (Gemini, Needs research)
- **#45 Databricks vs Snowflake vs Fabric: pick one in 10 minutes** (Cross-platform, Needs research)

## Counts

Priority: High 17, Medium 29, Low 4. Readiness: Ready 10, Partly 12, Needs research 28.

