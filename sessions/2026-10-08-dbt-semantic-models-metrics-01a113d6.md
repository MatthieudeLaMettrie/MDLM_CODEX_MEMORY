# Additional RSS metrics

Date: 2026-10-08 (Australia/Sydney)
Task identifier: 01a113d6-b790-7580-8187-69fc923348ed
Continues [the prior day's session](2026-10-07-dbt-semantic-models-metrics-01a113d6.md).

## Request and evidence

User requested four more metrics based on an attached BigQuery schema screenshot and their complete embedded semantic YAML. Read memory, the three latest filename-ordered notes and repository instructions, then verified clean main with the configured origin (initial HEAD 661f5ad). Inspected the attachment. It shows DBT_FEI_PROD.fei_rss_source_brz with nullable Date_Published DATE and Article_Title, Content, Categories, URL and Date STRING. The YAML includes the original count/average plus Sydney last-seven-days count and Investing/Shares count. Schema evidence does not establish actual rows or uniqueness.

## Changes and decisions

Created 09_RSS_ADDITIONAL_METRICS.md and examples/rss-additional-metrics/fei_rss_source_brz.yml. Chose four metrics supported by visible fields: total_article_content_chars = sum(length(Content)); max_article_length = max(length(Content)); avg_article_title_length = average(length(Article_Title)); articles_missing_categories = count_distinct of conditional URL for Categories IS NULL OR TRIM(Categories) = ''. The last expression counts a URL if at least one selected row qualifies; null URLs are excluded. Physical-column CASE logic is distinct from qualified semantic Jinja filter references.

The complete YAML reference preserves the two other model entries, all original four RSS metrics, their filters, and the user's inactive tests. It is a merge/reference example, not a new duplicate declaration in the real dbt project. Guide includes insertion steps, query filters, category/date examples, equivalent dbt SQL, independent synthetic arithmetic and publication pointers. Lengths intentionally retain the user's row-grain semantics; no hidden deduplication, null-to-zero substitution or date-string conversion introduced. The missing-category count should be queried with dates/all categories, since selecting Investing/Shares removes its qualifying rows. Updated course and 00–09 navigation and durable schema context.

Checked official dbt simple/latest metric definitions and BigQuery string/aggregate references. No live dbt project edit, parse/build, API/warehouse query, metric-value inspection or deployment performed. Validation and publication evidence are recorded below after the local checks; next step is to paste/merge into the actual project, validate, reconcile the chosen selections and deploy.

## Validation and publication

Passed local YAML parsing with duplicate-key rejection using the existing temporary PyYAML 6.0.3 through approved read-only escalation. Verified all three model entries, eight unique metric names, four exact snippet additions, preserved original semantic filters and active action test. Local in-memory SQLite arithmetic on synthetic rows returned 27 total content characters, 10 maximum body length, 2.4 average title length and 2 distinct uncategorized URLs. Additional checks covered a selected-category filter, empty input, all-null lengths and surrounding line breaks. These are local formula checks, not dbt/BigQuery runtime tests; the synthetic values are not inferred article-table results.

Checked twelve Markdown files with 94 local links/anchors and balanced fences, plus Git whitespace/diff. Reviewed the guide, complete YAML and task-owned navigation/memory/session changes before commit/push to current main under standing authorization. Verify remote publication before responding; Git history/final response provide the exact commit outcome. No project dependency, live semantic configuration or warehouse relation was changed.
