# SnowPro GenAI guide review and semantic-layer part

Date: 2026-10-08 (Australia/Sydney)

## Request

Review the whole `snowpro-genai` guide, check it is correct, add anything missing, and add a new part on the Snowflake semantic layer (what it is, how to build it).

## Changes

- Added [08_SEMANTIC_LAYER.md](../snowpro-genai/08_SEMANTIC_LAYER.md): concept and diagram, element anatomy and grain, consumers, a three-table synthetic lab with hand-calculated answers (net 880.00, 4 orders, AOV 220.00, East 680.00, completed-order months 480.00/200.00), authoring options (Autopilot, Semantic Studio, DDL, YAML, dbt), privileges and the two access paths, modeling best practices, cost, exam traps, 12 closed-book checks.
- Corrected the existing guides against live docs:
  - 01 said YAML specs and SQL semantic views are distinct representations. They are two authoring formats for one object; the legacy object is the stage-based YAML semantic model.
  - Renamed "Semantic Views Autopilot" to "Semantic View Autopilot".
  - Added the Analyst-to-Agents recommendation and the real custom-instruction names (`AI_SQL_GENERATION`, `AI_QUESTION_CATEGORIZATION`, `module_custom_instructions`).
  - Stated the aggregate-function privilege exception exactly (`USE AI FUNCTIONS` without `CORTEX_USER` still allows `AI_AGG` and `AI_SUMMARIZE_AGG`). `AI_FUNCTIONS_USER` is not granted to PUBLIC by default.
  - Added Agent inaccessible-tool behavior (`accept` default vs `reject`), AI Credit price differing by cross-region routing, and `AI_PARSE_DOCUMENT` `extract_images`/`page_filter` details.
  - Fixed six redirected links (verified-query, custom-instructions, structured-outputs, llm-functions, evaluate-ai-applications, document-ai troubleshooting).
- Linked 08 from README (step 8, with a note that it is best studied before step 5), 01, 02 Unit 7, 03 and 04. Left 06 (PDF-faithful link list) and 07 (script-generated) untouched.

## Validation

- Fetched current Snowflake semantic-view, CREATE SEMANTIC VIEW, SEMANTIC_VIEW, YAML, privileges, Agent setup, pricing and cost-governance pages as Markdown and compared claims.
- All 95 original doc links checked; 8 now use canonical pages. All new external links in 08 return 200 without redirect. All local links and anchors in the folder resolve.
- Lab arithmetic computed locally in Python. No Snowflake account was used: all SQL, including the lab, is unexecuted.

## Unresolved / not verified

- Playground limits (50 MB UI, ten documents), CoWork upload behavior beyond the quoted line, fine-tuning details and the 04 ML sections were not re-verified.
- Dev best-practices page says changes other than comments need CREATE OR REPLACE, while the CREATE reference documents CREATE OR ALTER. 08 follows the reference and flags it.
- The semantic-view pages are outside the atlas indexes; the atlas was not regenerated.

## Next steps

Run the 08 lab in a trial account, then take the practice exam. Consider adding semantic-layer questions to 05 (not done, to preserve the 28-question blueprint balance).

## Follow-up (2026-10-09): practice questions

The user asked to add some questions. Appended a 17-question semantic-layer supplement (Q33-49, with answer key and doc links) to snowpro-genai/05_PRACTICE_EXAM.md; the original 28-question blueprint set is unchanged. README step 5 now mentions the supplement. Answers were derived from the same live-doc pages used for 08; no Snowflake execution.
