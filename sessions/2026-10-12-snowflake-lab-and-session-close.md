# 2026-10-12 — Snowflake paste-and-run lab, and closing the semantic-layer session

Tool: Claude Code (Opus 5.5). Closes the session that began in sessions/2026-10-09-semantic-layers-databricks-snowflake.md and continued in sessions/2026-10-10-semantic-layer-vs-model-scenarios.md.

## Request

Add a Snowflake paste-and-run lab script (matching the Databricks one), confirm whether everything for the session was done, save everything and close the session.

## Changes

- Added `guides/data-engineering/semantic-layers-lab/snowflake_semantic_view_lab.sql`: optional ACCOUNTADMIN block 0 (GENAI_LAB, XSMALL GENAI_WH, role GENAI_SV_LAB), the three SV_* tables, `SALES_SV` semantic view (guide section 6 plus customer_name/order_date and descriptions), DESCRIBE/SHOW, a 21-check PASS/FAIL grid using both `SEMANTIC_VIEW(...)` and standard-SQL `AGG()` forms (including the `is_completed` filter dimension), `SHOW SEMANTIC DIMENSIONS ... FOR METRIC order_count`, and a final deliberate grain-rule failure (product × order_count). Cleanup commented. It replaces any existing SnowPro 08 `SALES_SV` (noted in the guide).
- Linked from semantic layers guide section 6 and the agents/publishing guide section 3.

## Whole-session summary (2026-10-09 → 2026-10-12)

Deliverables in `guides/data-engineering/`:
1. `SEMANTIC_LAYERS_DATABRICKS_SNOWFLAKE_GUIDE.md` — same fixture built as a Databricks metric view and a Snowflake semantic view; layer-vs-model and dim/fact relationships vs Power BI/Tableau subsections; grain difference; tests; NL benchmark; exercises.
2. `semantic-layers-lab/databricks_metric_view_lab.sql` — 23 checks + optional `format` test.
3. `semantic-layers-lab/snowflake_semantic_view_lab.sql` — 21 checks + expected grain failure.
4. `SEMANTIC_LAYER_AI_AGENTS_AND_PUBLISHING_GUIDE.md` — Genie Agent / Cortex Agent build, permissions, publishing (in-platform, Teams/M365, SharePoint/website, Power BI/Tableau, cross-org).
5. `SEMANTIC_LAYER_VS_SEMANTIC_MODEL_SCENARIOS.md` — nine scenarios, quiz, ownership table.

Expected values (both platforms): net 880.00, gross 930.00, 4 orders, AOV 220.00; East 680.00/3/226.67, West 200.00/1/200.00; months 480/400 (completed 480/200); products 420/380/80; completed 680; line-grain COUNT trap 6. Verified locally in SQLite only.

## Status at close

Done: all requested guides, scenarios and both lab scripts written, linked, committed and pushed.

Not done (requires the user's accounts; nothing executed by Claude):
- Run `databricks_metric_view_lab.sql` in `mdlm_db_trial` and paste the 23-row grid + section 5 result.
- Run `snowflake_semantic_view_lab.sql` and paste the 21-row grid + the section 6 error.
- Then: reconcile any FAIL into the guides; test metric-view consumer privileges with a non-owner; confirm the Databricks `format` block, Snowflake role-playing pattern, `CREATE AGENT` warehouse placement and Genie API field names.
- No Chrome extension, Databricks CLI or Snowflake connection exists on this work laptop; the user chose paste-and-run to keep credentials off it.
