# 2026-10-13 — Python os and sys guide (Part 4 of API series)

## Request
Add a part to `guides/api/` explaining the `os` and `sys` libraries: what they are, why they matter, and which functions and methods to master.

## Changes
- New `guides/api/PYTHON_OS_SYS_GUIDE.md` (Part 4): definitions and comparison, importance, `os` environment/working-dir/files/process functions, `os.path`, `sys` interpreter identity, `sys.path`, argv and exit codes, streams, modern companions (pathlib, shutil, subprocess, argparse, secrets, tempfile, logging, python-dotenv), seven worked examples, pitfalls table, 25-item cheat sheet, 15 practice questions.
- Part 1 (`API_AUTHENTICATION_STUDY_GUIDE.md`): header link to Part 4; section 11 now points to Part 4 as the full version (kept as the short version).
- README.md: Part 4 listed with the other API guides.

## Validation
All 9 Python blocks compile. Examples 1, 3, 4, 5, 6 and the snippets were run in a scratch folder with dummy environment values on Python 3.14.4 / Windows: config loader parsed `DEBUG=false` correctly and failed fast on empty key; CLI returned exit 0, 2 (missing key) and argparse error for an invalid region; os.walk found .csv/.CSV and skipped .txt; doctor printed presence/length only; atomic write left only the final file. Example 7 raised FileNotFoundError because dbt is not installed — documented in the guide. Example 2 (python-dotenv) not run.

## Context
Earlier the same day five courses (Fabric/Databricks/Snowflake/BigQuery data APIs + governance, and a cloud identity/tokens/secrets course) were written as Claude Docs and exported to MDLM_CLAUDE_MEMORY; not part of this repository.
