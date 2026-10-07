# Numbered SnowPro GenAI reading path

Date: 2026-10-07 (Australia/Sydney)

## Request

The user asked for the files in the GitHub `snowpro-genai` folder to be ordered by what to study first, explicitly naming `STUDY_GUIDE.md` as step 1 and `COURSE_COMPANION.md` as step 2.

## Change and reason

- Added a seven-step linked table at the top of the folder README: study guide, course companion, Cortex enablement/RAG lab, AI/ML deep dive, original practice exam, official C02 document index, and broader AI/ML documentation atlas.
- Marked the two indexes as references to consult when a lab or practice question exposes a gap, rather than cover-to-cover reading assignments.
- Converted the older numbered “How to use this” list to a short study-method section and clarified that optional training-track modules supplement the path. This leaves one primary numbered sequence.
- Kept stable filenames because existing materials and generator scripts cross-link them; the GitHub folder automatically renders README as its landing guide. Updated durable memory.

## Repository state and validation

The chat's attached worktree had a stale `.git` pointer after the main repository moved. Work was made in a clean clone inside the writable GitHub directory. Remote `main` advanced with an unrelated dbt course during the edit; fetched and rebased this change on top without conflict. Checked the seven local README links, the Markdown table, repository diff, and Git whitespace. No course, lab, exam, or Snowflake account was used in this organization-only change.

## Follow-up: make the order visible in the file list

The user could not see the changes. The first update numbered only the README table; it left the GitHub directory listing unchanged. Renamed the seven study documents with `01` to `07` prefixes, preserving the recommended order above. This supersedes the earlier decision to keep the filenames stable. Updated all local study links, current memory links, and both regeneration scripts so they write the numbered index filenames. Historical notes retain their original artifact names.

Validation: all seven numbered documents exist in order, all 31 local Markdown links in the SnowPro folder resolve, and the three Python scripts compile in memory. The atlas retains its 320 external links unchanged, including the normal browser-facing Snowflake URLs. Reviewed the rename-aware diff and Git whitespace checks. This is a file organization correction; live Snowflake lab validation remains outstanding. Publication is recorded by the commit and verified remote branch.
