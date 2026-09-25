# Snowflake AI/ML documentation deep dive

Date: 2026-09-25 (Australia/Sydney)

## Request

The user asked to go through Snowflake's Cortex AI Functions overview and every page associated with the Snowflake AI/ML overview, especially functions and governance, and extend the SnowPro GenAI study material with what they need to know.

## Research and scope

- Read the two supplied entry pages and Snowflake's top-level `llms.txt` index. Its linked section indexes list 111 Cortex pages, 76 CoCo pages, and 94 Snowflake ML pages.
- Built a regenerable inventory from those 281 pages plus 29 directly relevant ML Function and SQL AI Function references. The script fetched all 310 pages, read headings, and reported zero fetch failures. This is breadth/index coverage, not a claim that every page was semantically reviewed in full.
- Read the current AI Function overview and SQL signatures, function privilege/model-access guidance, pricing and cost-governance pages, guardrails, Agent access, Search, AI observability, ML Functions, Snowflake ML lifecycle, and relevant product pages in depth.
- Added short guidance on the newly documented preview Cortex AI Gateway, managed MCP versus connectors, and Provisioned Throughput's reserved-capacity billing.
- Key updates versus the previous guide: AI Function access combines account-level `USE AI FUNCTIONS` (or per-function privilege) with a Snowflake database role; `AI_FUNCTIONS_USER` is narrower than `CORTEX_USER`; model allowlist is legacy and only changeable to `None` from August 2026; Agent execution depends on the user's default role/warehouse; Cortex Guard and account-level Cortex AI Guardrails address different risks and charges; the dedicated function-cost page still names legacy usage views while the current cross-feature cost matrix favors `CORTEX_AI_FUNCTIONS_USAGE_HISTORY` and warns about overlapping Search embeddings.
- Confirmed 15 current task functions and three helpers in the overview, with exact reference pages for core signatures. `AI_TRANSLATE` still takes text, source, target, using `''` for source detection. `AI_PARSE_DOCUMENT` has `page_filter` rather than the older blueprint's `page_limit`.

## Artifacts

- Added `snowpro-genai/AI_ML_DEEP_DIVE.md`: product choice, 15-function table, syntax examples, lookalike decisions, multimodal/stage handling, full access path, model RBAC, Agent/Search rights, privacy/guardrails, billing and usage views, observability, broader Snowflake ML, and ten original recall checks.
- Added `snowpro-genai/AI_ML_DOC_ATLAS.md` with 310 official documentation links and checked headings.
- Added `snowpro-genai/build_ai_ml_doc_atlas.py` for refreshing the atlas and `inspect_ai_function_refs.py` for read-only current SQL syntax inspection.
- Updated the SnowPro README and four-domain study guide to point to the new material and correct current privilege, model allowlist, and cost-reference details.
- Updated MEMORY.md with the durable material and limitations.

## Validation and limits

- All 310 linked documentation Markdown pages returned successfully in the automated inventory. The 15-function SQL signature inspection completed, after fixing the extractor's Markdown fence handling.
- The new guide's local Markdown links, generated atlas count, and repository diff were checked. No Snowflake account was available to execute SQL or verify feature availability/charges in a live account.
- The atlas is a research navigation aid. The deep dive synthesizes the high-value pages; it does not reproduce or deeply analyze every detail of all 310 documents. Snowflake documentation and pricing can change, so repeat the reference checks before exam booking or production use.
