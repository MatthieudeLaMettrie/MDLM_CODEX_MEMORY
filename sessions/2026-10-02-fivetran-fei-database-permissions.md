# Add FEI destination permissions to the Fivetran guide

The user explicitly requested adding the explanation and SQL for changing the destination from FIVETRAN_DATABASE to FEI to MDLM_CODEX_MEMORY. Added a guide subsection explaining database-scoped grants, ACCOUNTADMIN versus FIVETRAN_ROLE, the FEI grant, and Save & Test with the existing key pair. Added sql/06_use_fei_database.sql, a troubleshooting row, package index entry, and evidence update.

Checked the diff, whitespace, and relative links. No SQL executed or remote destination changed. Missing FEI grants remains a likely diagnosis; no exact error or successful retry supplied.
