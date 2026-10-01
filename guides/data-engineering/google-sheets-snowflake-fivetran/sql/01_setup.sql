-- Run selected statements in Snowsight as an authorized administrator.
-- Reuses COMPUTE_WH, observed in this session. Does not recreate that warehouse.
-- Confirm SHOW WAREHOUSES includes COMPUTE_WH before running its grant.
USE ROLE ACCOUNTADMIN;
SHOW WAREHOUSES;

CREATE ROLE IF NOT EXISTS FIVETRAN_ROLE;
GRANT ROLE FIVETRAN_ROLE TO ROLE SYSADMIN;

CREATE USER IF NOT EXISTS FIVETRAN_USER
  TYPE = SERVICE
  DEFAULT_ROLE = FIVETRAN_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH;

-- IF NOT EXISTS does not update an existing user. Set these defaults explicitly.
-- An existing PERSON user can use a key pair too; this script does not change its type.
ALTER USER FIVETRAN_USER SET
  DEFAULT_ROLE = FIVETRAN_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH
  BINARY_INPUT_FORMAT = 'BASE64'
  TIMESTAMP_INPUT_FORMAT = 'AUTO'
  QUOTED_IDENTIFIERS_IGNORE_CASE = FALSE;

GRANT ROLE FIVETRAN_ROLE TO USER FIVETRAN_USER;
CREATE DATABASE IF NOT EXISTS FIVETRAN_DATABASE;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE FIVETRAN_ROLE;
GRANT USAGE, MONITOR, CREATE SCHEMA ON DATABASE FIVETRAN_DATABASE
  TO ROLE FIVETRAN_ROLE;

-- Fivetran creates the source schema/table during its sync.
-- These grants assume Fivetran creates its own schema, not a pre-existing one.
-- For a pre-existing target schema, verify its ownership and grant CREATE TABLE,
-- USAGE, and any table-management rights required by the destination setup tests.

SELECT CURRENT_REGION() AS SNOWFLAKE_REGION;
-- ONLY for Snowflake hosted on GCP when required by the destination guide:
-- GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE FIVETRAN_ROLE;
-- The supplied successful destination screenshot is AWS ap_southeast_2.

SHOW GRANTS TO USER FIVETRAN_USER;
SHOW GRANTS TO ROLE FIVETRAN_ROLE;
DESCRIBE USER FIVETRAN_USER;

-- Optional alternative: dedicated compute instead of shared COMPUTE_WH.
-- CREATE WAREHOUSE IF NOT EXISTS FIVETRAN_WAREHOUSE
--   WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE
--   INITIALLY_SUSPENDED = TRUE;
-- GRANT USAGE ON WAREHOUSE FIVETRAN_WAREHOUSE TO ROLE FIVETRAN_ROLE;
-- ALTER USER FIVETRAN_USER SET DEFAULT_WAREHOUSE = FIVETRAN_WAREHOUSE;
-- Then select FIVETRAN_WAREHOUSE in Fivetran too.
