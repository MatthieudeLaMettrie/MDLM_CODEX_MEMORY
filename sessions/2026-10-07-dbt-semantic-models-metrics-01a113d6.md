# dbt semantic models and metrics course

Date: 2026-10-07 (Australia/Sydney)
Task identifier: 01a113d6-b790-7580-8187-69fc923348ed

## Request and context

User requested a full guide/course on dbt semantic models and metrics using the screenshot at Pictures/Screenshots/Screenshot 2026-10-07 114856.png, and a file in MDLM_CODEX_MEMORY. Questions were permitted if needed. Existing BigQuery/FEI context was sufficient for a course; live implementation details remain unverified.

Read MEMORY.md, the three latest filename-ordered notes, AGENTS.md and navigation files. Verified clean working tree on main with the configured requested GitHub origin. Inspected the supplied screenshot: TEST_ANALYTICS Production catalogue lineage shows fei_rss_source_brz -> rss_articles -> articles_published / avg_article_length, with article primary entity described as an article URL natural key. Screenshot does not expose formulas, YAML format or execution results.

## Changes and decisions

- Created dbt/SEMANTIC_MODELS_AND_METRICS_COURSE.md: 16 lessons, flexible 10–14-hour route, plain explanations, diagrams, screenshot interpretation, grain/identity contracts, entities/dimensions/measures, latest and legacy YAML, querying, five metric types, time spine/timezones/freshness, joins/fanout, saved queries/exports/BI, release and governance, troubleshooting, 20 exercises with solutions withheld, capstone and rubric.
- Added dbt/semantic-models-lab/ with deterministic synthetic CSV, BigQuery SQL models, daily calendar, alternative semantic YAML examples, negative-length test and independent reconciliation SQL. Expected overall count 5, known lengths 4, total characters 1500, average 375, coverage 0.8. Missing day and missing length are intentional teaching cases.
- Used current official dbt documentation. Latest spec availability listed for v1 Latest, v2 and v1.12; legacy examples retained separately. Warned against mixed syntax, duplicate metric/model declarations and assuming plain Core supplies hosted dbt sl access.
- Preserved Bronze/Silver/Gold context and Studio target caveat. Recommended grain cleanup based on actual data, not folder name. No rename or modification of live dbt_cert authorized or performed.
- Linked course from root and dbt README and recorded availability in durable memory.

## Validation and limits

Passed Markdown relative-link/anchor and fence checks, YAML parsing with duplicate-key rejection (three lab alternatives/configuration files and all course YAML blocks), synthetic overall/publisher/language arithmetic, metric-reference parity between both formats, and Git whitespace checks. Reviewed the authored changes against current official references, correcting the integrations link to its current platform-integrations path. PyYAML 6.0.3 was installed only in a temporary validation folder; sandbox networking and access required approved escalated commands. No project dependency was changed. These checks are local documentation/fixture checks, not dbt schema validation. No dbt compilation, MetricFlow query, warehouse execution, hosted account check or deployment performed. Current runtime/release track and real source columns are required before adapting the lab to the live project.

## Publication and next steps

Commit and push only course/lab/navigation/memory/session artifacts to current main under standing authorization; verify remote hash afterward. Git output and final response provide publication evidence. User can begin the course immediately; later live tailoring requires existing YAML, model output columns, runtime and any query error without secrets.

## Follow-up: requested folder and numbered learning order

User requested saving the course under dbt/dbt-study-guide and organizing it like snowpro-genai, with numbers showing where to begin. Read current memory/session records and inspected both folder layouts. Working tree was clean on main after the initial published course commit 0384787.

Moved the course and its complete lab into the requested folder. Numbered the study materials: 00_START_HERE.md, 01_CORE_GUIDE.md, 02_SEMANTIC_MODELS_AND_METRICS_COURSE.md, 03_SEMANTIC_MODELS_LAB/, 04_PRACTICE.md, 05_READINESS.md, 06_SOURCES.md. Added a folder README with the full sequence and a focused 02-course -> 03-lab -> course exercises/capstone route. Kept the initial core diagnostic before explanations and sources available at any stage. Matched SnowPro's guide/lab/practice/reference structure; did not modify SnowPro itself.

Updated current navigation, relocated relative links, document titles and durable memory. Preserved substantive lessons, lab SQL/YAML/CSV, progress data and historical verification. Original creation paths above remain historical descriptions; current paths are in this follow-up and memory. Passed checks for 105 relative links/anchors, balanced Markdown fences and the complete 00–06 path. Confirmed all eight lab data/SQL/YAML assets, progress.csv and verification.json are unchanged compared with the initial commit. Reviewed Git diff and whitespace before publication to current main. No warehouse or dbt runtime checks are needed for this file-organization-only change.

The first push was rejected because remote main concurrently received the SnowPro numbered-path changes. Fetched and reviewed those commits, their memory changes and session note; rebased the unpublished dbt organization commit onto remote main without conflict. Preserved both sets of numbering changes and reran navigation checks before publishing.

## Follow-up: calculate the user's supplied metrics

User provided the actual latest-format YAML for fei_rss_source_brz / rss_articles: article primary entity on URL, date_published semantic time alias on Date_Published, raw categories dimension on Categories, articles_published count_distinct(URL), and avg_article_length average(length(Content)). URL not_null/unique tests are commented out. The request was to explain how these metrics are calculated.

Added a worked example in course lesson 7 using those exact names and formulas, overall and daily equivalent dbt SQL, platform query commands, row-by-row arithmetic and duplicate/null/empty-string behavior. Explained that agg_time_dimension selects the analytical clock when time is requested rather than automatically grouping or filtering; raw category strings are not exploded; Content STRING character length includes stored whitespace/markup. Checked current official dbt simple-metric, dimension and command references plus BigQuery LENGTH/aggregate documentation. Formula explanations are based on supplied YAML; actual column types, duplicates, runtime behavior and warehouse values remain unverified. No live project changed or queries executed. Check arithmetic, links/fences and Git diff before publication.

## Follow-up: add date and publisher logic

User asked how to add logic such as articles in the last seven days or articles from two specific publishers. Extended course lesson 8 with query-time versus named metric filters, publisher dimension prerequisite, separate latest-format simple metrics, combined date/publisher query and reconciliation SQL, plus a cumulative metric for a historical rolling chart. Used explicit BigQuery Australia/Sydney dates and defined today plus six preceding dates, previous seven completed dates and exact 168 hours separately. Explained IN/OR membership, combined versus per-publisher results, future-date upper bound, current-date evaluation/cache/export timing and rolling time-spine needs.

Publisher column and values were not supplied; examples explicitly assume Publisher and use Publisher A/B placeholders. Date type/timezone and runtime acceptance remain unverified. Checked current official dbt simple/filter/dimension/query/cumulative and BigQuery date-function references. No live dbt or warehouse changes. Preserved unrelated untracked databricks/ work. Passed calendar-boundary arithmetic, Markdown links/fences and Git whitespace checks; reviewed the diff before committing/pushing this course update and note under standing authorization. No additional durable memory change is needed beyond the existing supplied-model record.
