# SnowPro Gen AI GES-C02 study guide

Date: 2026-09-24 (Australia/Sydney)

## Request

The user wants to pass SnowPro Specialty: Gen AI GES-C02 and asked for a repository study guide based on the official certification page, the local `SnowProGenAIStudyGuideC02.pdf`, and relevant Snowflake documentation. The request included a third-party exam-experience account emphasizing exact syntax, billing for Agents/Search/Analyst/AI functions, and the location of files uploaded to Snowflake Intelligence. Later, the user supplied a Snowflake training catalog link with a session parameter and a BigDataPrep article.

## Research and decisions

- Read the 16-page official PDF (last updated 2026-04-30). Its blueprint gives Domains 1-4 weights of 18%, 38%, 29%, and 15%. Read its objectives, five sample answers, and extracted hyperlinks. Did not copy the PDF or its sample questions into the repository because the source says it is for internal use only.
- Checked the official current certification page and primary Snowflake documentation for product selection, SQL signatures, access control, cost, document parsing, Search, Analyst, Agents, cross-region inference, and training.
- Corrected the anecdote's ambiguous `AI_TRANSLATE` phrasing: source language can be **auto-detected by passing an empty string in the required source-language argument**, e.g. `AI_TRANSLATE(text, '', 'en')`; current SQL reference does not show a two-argument form.
- Snowflake's current Snowflake Intelligence documentation URL redirects to Snowflake CoWork. Direct chat uploads are documented as saved to the user's personal stage and cleaned up when the thread is deleted or expires. This differs from application-owned named/external stages.
- Distinguished current billing: Agent orchestration tokens plus tool costs; standalone Analyst per 1,000 messages versus Analyst through Agents token-based; Search embedding, serving, refresh warehouse and storage; AI functions largely token-based, with document parsing page-based. Documented current AI Credits/Platform Credits and the risk of double-counting overlapping history views.
- Flagged current documentation drift: `CORTEX_MODELS_ALLOWLIST` is legacy and moving to model RBAC; Snowflake Intelligence naming redirects; current `AI_PARSE_DOCUMENT` reference describes `page_filter` where the PDF names `page_limit`; several old usage views are being deprecated. The guide states which claims are blueprint terms and which are current-doc behavior.
- The supplied `training.snowflake.com` session URL was not accessible to the public web tool. Used stable public official course pages for the instructor-led GenAI training and two free on-demand modules. The second module's public description uses legacy function names. The BigDataPrep article aligned with official weights and broad topic map; its question count, timing, score, and price were not confirmed on the accessible official certification page, so they were not adopted as exam facts.

## Artifacts

- Added `snowpro-genai/README.md` as the entry point and linked it from root README.
- Added `snowpro-genai/STUDY_GUIDE.md` with four blueprint chapters, syntax and billing sheets, examples, version-drift notes, and a practical mini-lab.
- Added `snowpro-genai/PRACTICE_EXAM.md` with 28 original questions and explanations in an approximate 5/11/8/4 domain split. The official sample questions were not copied.
- Added `snowpro-genai/extract_official_links.py` and generated `OFFICIAL_DOC_INDEX.md` with 130 grouped official Snowflake resource-link entries from the four PDF domain resource pages. This is an extracted reading map; not every indexed URL was individually reviewed or availability-checked.
- Updated `MEMORY.md` with the durable material location and remaining work.

## Validation and limits

- Confirmed the local PDF has 16 pages and extracted its 176 hyperlink annotations; the curated official resource index has 130 domain entries, including duplicates across domains.
- Counted 28 original questions and 28 answer-key entries. Checked the core syntax and billing claims against Snowflake's live reference pages. SQL examples were **not executed** in a Snowflake account; no live training login or official practice-exam result was available.
- Next: do the mini-lab in a Snowflake test account, take the official practice exam, keep an error log, and update any behavior that changes before booking. A detailed week-by-week plan and cross-vendor master notebook remain open from the earlier curriculum task.
