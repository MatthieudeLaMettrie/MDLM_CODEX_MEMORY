# dbt preparation guide and workflow publication

Date: 2026-09-23 Australia/Sydney
Task: 01a0c682-332f-7fa2-8a8a-ae93f9dad156

## User requests and choices

The original request was certification preparation after completing courses and building projects, with debugging as the weak spot and readiness uncertain. Begin with a diagnostic, then adapt deliberate-fault practice; withhold answers until an attempt or request for help. The 7–10 day window is provisional. Broader certification strategy remains in the original roadmap task.

The user asked for the best preparation resource, then a flow to collect dbt Learn/documentation and produce a robust learning guide. Chose local Python and later guide writing/refinement in this task rather than local model installation. Asked to run the workflow, continue, and publish the materials; explicitly confirmed MDLM_CODEX_MEMORY as destination.

## Completed preparation work (2026-09-22)

- Checked the official exam page: version 1.11, 65 questions, two hours, 65% passing score, seven domains. These are dated findings, not a fresh policy check on publication day.
- Built a standard-library Python workflow using llms.txt and sitemap discovery, robots checks, bounded retries, pacing, resumable manifest, content hashes, coverage reporting and Markdown/HTML extraction. HTML fallback was added after real sitemap URLs lacked Markdown endpoints; short-page fallback recovered further URLs.
- Full collection plus retry: 1,558 saved of 1,573 discovered URLs, 15 unsuccessful. After navigation/duplicate filtering, 1,300 documents contributed to 712 source packets. Discovery is not proof of all-site or all-course coverage.
- Created an approximately 3,939-word core guide citing 34 official references, twenty original fault cases without an answer key, a readiness plan, progress-log template and source provenance. Start with Cases 1–3; no attempts or readiness score yet.
- Enrolled dbt Learn lessons and unavailable transcripts were not collected. Live docs are not a version-pinned 1.11 corpus. Teaching examples are reviewed text, not executed warehouse labs.
- Optional Ollama generation exists in the collector but was not installed or run. No scheduled automation created.

## Repository publication

- Read AGENTS.md, MEMORY.md and the latest session notes; inspected clean main and origin. Fetched and fast-forwarded two existing remote commits before editing, preserving the runtime guide and other task records.
- Added dbt/ with the authored guide, exercises, readiness/log files, collector, tests, original coverage, source metadata and public reading index.
- Excluded raw scraped pages, generated source packets, optional AI outputs and imports through dbt/.gitignore. Documented how to regenerate them and that historical verification describes the original local corpus.
- Replaced source-copy links with official references for a working GitHub reading experience. Added landing links in README.md and durable state in MEMORY.md. Original projectless deliverables remain intact.

## Validation and limits

Nine offline tests passed in the publication copy: URL boundaries, lossless source splitting, inventory deduplication, reporting gaps, HTML text/code extraction, fallback/authentication behavior and exclusion of listings/duplicates. Test output includes Python ResourceWarnings for synthetic HTTPError fixtures; all tests pass. Publication-copy local Markdown links passed and no machine-specific paths were found in Markdown. Original verification also checked all 34 cited references existed in the local corpus and the twenty cases were present.

Review staged diff/whitespace and local links before commit; verify the remote hash after push. Do not infer that these checks execute dbt examples or audit every downloaded page. Fresh collection was not rerun just to publish the existing materials.

## Next step and publication evidence

Learner should attempt Cases 1–3 and provide warehouse/adapter, dbt runtime and daily study time. Adapt practice to the scored reasoning gaps. This note is prepared before commit/push; Git history and the final response establish publication outcome. Repository instructions and the explicit user request authorize normal commit/push on current main without force.
