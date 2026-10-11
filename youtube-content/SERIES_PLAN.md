# Series plan: what to publish first

[Back to the YouTube content folder](README.md) · [Video planner](VIDEO_PLANNER.md) · [Production checklist](PRODUCTION_CHECKLIST.md) · [Channel branding](CHANNEL_BRANDING.md)

Written 11 October 2026. This plan follows one judgement: a **narrow, series-based channel grows more predictably than a broad one**. That comes from general YouTube knowledge. It was **not tested** against analytics or search data for your niche, and views are not guaranteed. The channel name, "Data & AI in 10", is broad enough to add other tools later.

## The idea

Publish one focused series of 8 to 12 videos before adding other tools. Viewers who like video 1 should find video 2 an obvious next step. Then start a second series that links data work to AI.

## Series 1: Databricks pipelines in 10

Audience: Beginner first, then Practitioner. Material: your Auto Loader sample files and guides already exist. Rehearse each demo before recording, because none of the guides have been run in a live workspace yet.

| Order | Video | Planner # | Audience | Guide and data | Notes |
|--:|---|--:|---|---|---|
| 1 | **Auto Loader explained in 10 minutes** | 1 | Beginner | [Video 1 guide](../databricks/video-demo-auto-loader/README.md) | Start here: three files, then only new ones load |
| 2 | **Schema evolution: what happens when a file gets a new column** | extra | Practitioner | [Video 2 guide](../databricks/video-demo-auto-loader/02_SCHEMA_EVOLUTION_VIDEO.md) | Not one of the 50 ideas; a natural second step |
| 3 | **CDC vs CDF with a live AUTO CDC demo** | 4 | Practitioner | [Video 3 guide](../databricks/video-demo-auto-loader/03_CDC_VIDEO.md) | Confirm AUTO CDC syntax first |
| 3b (optional overview) | **Data Engineer Skills Map: What to Learn First (Databricks)** | 51 | Beginner | [Lesson 20](../databricks/20_DATA_ENGINEER_SKILLS_MAP_AND_PYSPARK_ESSENTIALS.md) | Placed after the hands-on videos so the channel starts with demos. Generic topic with heavy competition: run the demand check; PySpark code not yet run |
| 4 | **Fix 5 common pipeline errors** | 2 | Practitioner | [Runbook](../databricks/18_PIPELINE_MONITORING_AND_TROUBLESHOOTING_RUNBOOK.md) | Strong search intent: use real error messages |
| 5 | **Volumes vs managed tables vs external locations** | 3 | Beginner | [Volumes guide](../databricks/10_UNITY_CATALOG_VOLUMES_GUIDE.md) | Good for newcomers |
| 6 | **Delta MERGE: "multiple source rows matched" and the fix** | 5 | Practitioner | [Delta guide](../databricks/04_DELTA_AND_STREAMING.md) | Reproduce the error first |
| 7 | **Genie Code: build a pipeline from one prompt** | 6 | Practitioner | [Field notes §7](../databricks/15_NOTEBOOK_AND_CATALOG_FIELD_NOTES.md) | The AI bridge inside the series; documented as a preview feature |
| 8 | **Deploy dev to prod with bundles** | 8 | Practitioner | [Bundles guide](../databricks/06_BUNDLES_AND_ORCHESTRATION.md) | Needs a personal workspace with a prod-like target |
| 9 (optional) | **Azure Blob with file events mode** | extra | Practitioner | [Video 4 guide](../databricks/video-demo-auto-loader/04_AZURE_FILE_NOTIFICATION_VIDEO.md) | Riskiest to record (Azure permissions); do it last, or skip |

Rules for the series:
- Same title pattern, for example "Databricks: <topic> in 10 Minutes".
- Each video ends by naming the next one.
- Reuse the same sample dataset (retail sales) so viewers recognise it.
- Add a playlist called "Databricks pipelines in 10" on day one.

## Series 2: AI for data work

Start after Series 1 has at least five videos published. Audience: Practitioner.

| Order | Video | Planner # |
|--:|---|--:|
| 1 | Claude Code for data engineers | 33 |
| 2 | MCP explained: connect Claude to a database | 35 |
| 3 | Build a simple agent with the Claude API and tools | 36 |
| 4 | Claude vs ChatGPT for data work | 37 |
| 5 | ChatGPT and Codex for SQL and pipelines | 38 |
| 6 | Gemini vs Claude vs GPT on one real task | 44 |

These need hands-on research first (nothing is written yet). Genie Code, in Series 1, links the two series.

## Later

All other ideas (Snowflake, BigQuery, Fabric, dbt, Power BI, certification and cross-platform) stay in the planner marked **Later**. Promote one into a new series when Series 1 shows what your viewers respond to. Certification ideas work best as a short side series, not the main focus.

## Decision rules

- **After 5 videos:** check which got the best average view duration and which titles drew clicks. Copy that pattern into the next ones.
- **If a video flops:** change the title and thumbnail once, then move on. Don't abandon the series after one result.
- **If a topic needs a live workspace you don't have:** skip or postpone it.

## First 30 days (suggested, not a promise)

1. Choose the channel handle and set up a **Brand Account** ([branding drafts](CHANNEL_BRANDING.md)).
2. Run the demand check on videos 1 to 4 and record the results in `demand_check_notes` in the CSV.
3. Rehearse and record video 1, then publish it.
4. Record 2 and 3 in the same sitting if the setup is the same.
5. Review the [pre-publish safety check](PRODUCTION_CHECKLIST.md) every time.
