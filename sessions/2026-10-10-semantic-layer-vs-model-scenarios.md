# 2026-10-10 — Semantic layer vs semantic model: real-life scenarios

Tool: Claude Code (Opus 5.5). Continues sessions/2026-10-09-semantic-layers-databricks-snowflake.md.

## Request

User asked for the repo link (given: https://github.com/MatthieudeLaMettrie/MDLM_CODEX_MEMORY), then for more examples distinguishing semantic layer from semantic model, with real-life scenarios, added to the repo.

## Changes

- Added `guides/data-engineering/SEMANTIC_LAYER_VS_SEMANTIC_MODEL_SCENARIOS.md`: one-line distinction and diagram; nine scenarios (retail two "net sales" versions; bank certified metric views + Genie; SaaS dbt Semantic Layer with MRR/churn/NRR; hospital masking/row policies; post-acquisition Databricks+Snowflake options; airline role-playing dates and semi-additive metrics; agency AI agent raw tables vs model vs layer; small business where one Power BI model is the layer; FEI RSS dbt semantic model/layer from repo records); seven-item layer/model/neither quiz; ownership cheat sheet.
- Linked from semantic layers guide section 1 and README; MEMORY updated.

## Notes and limits

- Scenarios 1–8 are labelled illustrative composites, not real companies. Scenario 9 restates repo-recorded FEI design; live production queries from every consumer remain unverified.
- No platform execution. The Databricks lab script from 2026-10-09 is still awaiting the user's run and pasted results.
