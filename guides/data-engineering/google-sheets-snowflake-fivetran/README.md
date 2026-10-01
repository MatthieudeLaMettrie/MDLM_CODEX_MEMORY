# Google Sheets to Snowflake through Fivetran

An end-to-end field guide based on the FEI RSS connection setup on 1 October 2026. The destination is connected using key-pair authentication; the supplied screenshots do not yet prove that Sheet rows arrived in Snowflake.

## Read and run in this order

1. Read [the complete guide](GUIDE.md) for architecture, authentication, configuration, and troubleshooting.
2. Run [01_setup.sql](sql/01_setup.sql) in Snowflake to prepare the dedicated user, role, database, and warehouse permissions.
3. Run [New-FivetranKeys.ps1](scripts/New-FivetranKeys.ps1) locally in PowerShell to generate the keys outside this repository.
4. Run the generated `assign_public_key.sql` locally in Snowflake. [02_assign_public_key.sql](sql/02_assign_public_key.sql) explains the equivalent manual step.
5. Complete the Fivetran destination and Google Sheets connection forms using the guide.
6. Run [03_validate_data.sql](sql/03_validate_data.sql) to discover the actual tables, then query the correct relation.
7. Optionally run [04_reader_access.sql](sql/04_reader_access.sql) for an analyst role and adapt [05_bronze_silver_gold.sql](sql/05_bronze_silver_gold.sql) for transformations.

[Session evidence and what remains unverified](SESSION_EVIDENCE.md) distinguishes observed results from example scripts. No Snowflake SQL or key generation was executed by Codex in producing this guide. Script syntax and local documentation links were checked.

## Package map

| File | Purpose |
|---|---|
| `GUIDE.md` | Complete setup, reasons for each step, operations, and troubleshooting |
| `SESSION_EVIDENCE.md` | Incident, resolution evidence, and open checks |
| `scripts/New-FivetranKeys.ps1` | Generate RSA keys and a public-key registration SQL file |
| `sql/01_setup.sql` | Snowflake integration identity and privileges |
| `sql/02_assign_public_key.sql` | Manual public-key registration template |
| `sql/03_validate_data.sql` | Inspect configuration and verify loaded rows |
| `sql/04_reader_access.sql` | Optional read access for analysts |
| `sql/05_bronze_silver_gold.sql` | Optional transformation example with explicit assumptions |

The key-generation script contains instructions, not keys. Keep generated credentials outside Git and outside shared or synced folders.
