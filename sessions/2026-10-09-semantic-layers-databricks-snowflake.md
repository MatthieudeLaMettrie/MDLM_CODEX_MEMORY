# 2026-10-09 — Semantic layers guide: Databricks and Snowflake

Tool: Claude Code (Opus 5.5).

## Request

The user asked whether another guide could be created on building semantic layers/models in Databricks and Snowflake.

## What was done

- Reviewed existing material to avoid duplication: SnowPro 08 (Snowflake semantic views deep dive), dbt semantic course 02/10 and the Power BI agents guide section 13.
- Checked current Databricks docs (uc-semantics metric views: create, YAML reference, query, manage, feature availability, TPC-H tutorial) and the GA announcement.
- Added [guides/data-engineering/SEMANTIC_LAYERS_DATABRICKS_SNOWFLAKE_GUIDE.md](../guides/data-engineering/SEMANTIC_LAYERS_DATABRICKS_SNOWFLAKE_GUIDE.md). It reuses the SnowPro 08 fixture (customers/orders/order_lines) and contains a vocabulary map (Databricks/Snowflake/dbt), modeling decisions, a full Databricks metric view build in `mdlm_db_trial.semantic_lab` (YAML 1.1, nested join, COUNT DISTINCT, MEASURE() composition, FILTER measure, queries incl. CTE join), a compact Snowflake semantic view with a line-by-line diff, a grain-behaviour comparison, post-deploy tests, an NL benchmark for Genie/Cortex Agents, a choice table, mistakes and 6 exercises with answers.
- Linked it in README.md.

## Key facts and decisions

- Databricks metric views: `CREATE VIEW ... WITH METRICS LANGUAGE YAML AS $$...$$`; create on DBR 16.4+, agent metadata/snowflake joins/materialization on 17.3+, one_to_many joins on 18.1+, parameters on 18.2+. Current key is `fields` (`dimensions` still accepted). Query with `MEASURE()` (or `agg` on 18.1+); no `SELECT *`; no direct joins (use a CTE). `ALTER VIEW` replaces the full YAML. GA announced as part of UC Business Semantics; Catalog Explorer UI editor in Public Preview.
- Main teaching difference: Snowflake enforces grain (rejects order_count by product); Databricks does not (COUNT(order_id) at line grain = 6, not 4; distinct counts by product are non-additive).
- Expected answers verified by running the fixture in local SQLite: 880/930/4/220; East 680/3/226.67, West 200/1/200; months 480/400 (completed 480/200); products 420/380/80; completed 680.

## Unverified / open

- No SQL run on Databricks or Snowflake.
- Unclear in official docs whether metric-view consumers need SELECT on source tables and whether source row filters/masks apply; guide asks for a non-owner test.
- Databricks `format` block shape and the Snowflake cross-table CASE metric in exercise 3 should be confirmed live.

## Next steps

Run section 4 in the `mdlm_db_trial` trial workspace and section 6 in the Snowflake lab account, then record actual results against section 2.

## Follow-up (same day): layer vs model, and relationships

- User asked for status (guide was complete and pushed in 368a2f4; the earlier final reply had wrongly said "No response requested" instead of reporting) and asked: is a semantic layer different from a semantic model, and how are dim/fact relationships created compared with Power BI or Tableau?
- Explained, then on the user's "yes" added two subsections to the guide (no renumbering):
  - Section 1 "Semantic layer vs semantic model": layer = architectural idea; model = concrete object (Power BI semantic model, Tableau data source, dbt semantic_model, Databricks metric view, Snowflake semantic view, LookML); vendor naming confusion; BI-tool vs warehouse-native models.
  - Section 3 "Relationships between dimension and fact tables": comparison table (Power BI, Tableau logical layer, Snowflake RELATIONSHIPS, Databricks joins, dbt entities), the fixture relationship written in Snowflake/Databricks/dbt, and six mindset changes (draw first, no relationship = no join, key uniqueness, filter direction vs grain, role-playing dims, bridge tables for many-to-many).
- Unverified: Snowflake role-playing pattern (same table as two logical tables) flagged for confirmation against validation rules; Power BI/Tableau descriptions from general product knowledge, not re-checked against docs this session.

## Follow-up: running the Databricks lab

- User asked to run the Databricks lab in the trial workspace. No Databricks CLI/SDK/profile on this (work) laptop and the Claude in Chrome extension was not connected.
- User chose the paste-and-run option (no credentials stored on the work laptop). Added `guides/data-engineering/semantic-layers-lab/databricks_metric_view_lab.sql`: creates `mdlm_db_trial.semantic_lab`, the three tables and the `sales_metrics` metric view, and ends with a 23-check PASS/FAIL grid; an optional separate view tests the guide's unverified `format` block. Cleanup is commented out. Linked from guide section 4.
- Status: waiting for the user to run it and paste back results; nothing executed in Databricks yet.
