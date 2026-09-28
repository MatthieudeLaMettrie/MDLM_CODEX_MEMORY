# Repository folder cleanup

Date: 2026-09-28 (Australia/Sydney)

## Request and changes

The user asked to clean the repository by allocating Markdown files to folders. Inspected the root documents, existing subject folders, repository instructions, and cross-links. Kept README.md, MEMORY.md, and AGENTS.md at the root as entry point, durable memory, and working instructions. Moved the three Azure/GCP/AWS RAG courses into `learning/rag/`; the curriculum and roadmap into `learning/certifications/`; continuity and email guides into `guides/`; the related runtime HTML guide into `guides/programming/`; and the FEI ETF record into `projects/fei/`. Existing `dbt/`, `snowpro-genai/`, and `sessions/` remain organized as before.

Updated README navigation, MEMORY links and durable layout description, and relative links inside moved guides. Historical session notes retain the filenames as they existed when those notes were written; they are faithful records, not navigation pages.

## Validation

Checked that all relative Markdown links resolve after the moves and reviewed Git's rename/diff output. No source code or live service was changed. Next step is to stage, commit, and push this reorganization under the repository's standing authorization.
