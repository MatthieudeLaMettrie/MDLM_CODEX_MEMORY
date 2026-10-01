# Google Sheets to Snowflake through Fivetran

## Request and location

The user requested a complete repository guide in MDLM_CODEX_MEMORY, saved in an appropriate folder, covering lessons from connecting Google Sheets to Snowflake through Fivetran, public/private key generation and why it is needed, and Snowflake scripts for setup and data access. Organized the package under guides/data-engineering/google-sheets-snowflake-fivetran and linked it from the root README.

## Evidence and decisions

Earlier destination setup failed during warehouse discovery with incorrect username/password; database field fivetran differed from FIVETRAN_DATABASE. Inspected three later screenshots: destination Connected with KEY_PAIR, FIVETRAN_DATABASE, FIVETRAN_USER, direct connection, AWS ap_southeast_2, unencrypted key; source later Active on a six-hour schedule. Associated connections were Paused in the earlier destination overview. Blank Last synced and absence of SQL results mean completed ingestion remains unverified.

## Artifacts

- Complete guide with pipeline diagram, Google authorization, key rationale, destination settings, troubleshooting, operations, rotation, and completion checks.
- PowerShell generator that writes PKCS#8 keys outside the repository, refuses existing output, optionally encrypts, and emits public-key registration SQL without displaying secrets.
- Five SQL files: integration setup, public-key registration, data discovery/validation, optional analyst reads, and an explicitly hypothetical Bronze/Silver/Gold example.
- Session evidence note and package .gitignore; no screenshots or keys included.

## Validation and limits

Checked PowerShell parser syntax, local Markdown links, and Git whitespace/diff. Reviewed statements against official Fivetran, Snowflake, and OpenSSL references. No keys generated, cloud SQL executed, source edited, or Fivetran settings changed in this documentation task. The example source relation/columns must be replaced after inspecting the real table. Next live check: completed sync, table discovery, row count, and a controlled source edit.
