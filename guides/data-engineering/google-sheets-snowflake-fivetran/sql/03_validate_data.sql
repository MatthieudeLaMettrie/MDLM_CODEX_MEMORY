-- Run section A first. Section B requires discovered schema/table names.
-- ACCOUNTADMIN is used here for initial administrative inspection.
-- Use the optional analyst role for everyday reads.
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE FIVETRAN_DATABASE;

-- A: discover actual objects. Empty PUBLIC is not an ingestion failure.
SHOW SCHEMAS IN DATABASE FIVETRAN_DATABASE;
SHOW TABLES IN DATABASE FIVETRAN_DATABASE;
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM FIVETRAN_DATABASE.INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
ORDER BY TABLE_SCHEMA, TABLE_NAME;

SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE, ORDINAL_POSITION
FROM FIVETRAN_DATABASE.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION;

-- B: REPLACE this example with the fully qualified name discovered above.
-- Connection display name google_sheets.fei_rss_fivetran is not proof of SQL names.
SET source_table = 'FIVETRAN_DATABASE.GOOGLE_SHEETS.FEI_RSS_FIVETRAN';
SELECT COUNT(*) AS ROW_COUNT FROM IDENTIFIER($source_table);
SELECT * FROM IDENTIFIER($source_table) LIMIT 20;

-- C: run ONLY after confirming this exact system column exists and its case.
-- SELECT COUNT(*) AS ROW_COUNT, MAX(_FIVETRAN_SYNCED) AS LAST_ROW_SYNCED_AT
-- FROM IDENTIFIER($source_table);
-- MAX(_FIVETRAN_SYNCED) is row-load recency, not article publication recency.
-- A successful no-change poll may leave this timestamp unchanged.

-- D: inspect identity/defaults if warehouse discovery or authentication fails.
SHOW GRANTS TO USER FIVETRAN_USER;
SHOW GRANTS TO ROLE FIVETRAN_ROLE;
DESCRIBE USER FIVETRAN_USER;
SELECT CURRENT_ACCOUNT(), CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME(),
       CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE();
