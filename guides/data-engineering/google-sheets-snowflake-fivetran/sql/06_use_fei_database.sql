-- For the existing FEI database when changing the Fivetran destination.
-- Run as an authorized administrator in Snowsight.
-- Database grants on FIVETRAN_DATABASE do not apply to FEI.
USE ROLE ACCOUNTADMIN;

GRANT USAGE, MONITOR, CREATE SCHEMA
ON DATABASE FEI
TO ROLE FIVETRAN_ROLE;

SHOW GRANTS TO ROLE FIVETRAN_ROLE;

-- In Fivetran: Database = FEI; Role = FIVETRAN_ROLE; then Save & Test.
-- Keep the existing matching key pair, user, and warehouse.
-- Pre-existing schema/table privileges require separate inspection.
-- This does not migrate tables from FIVETRAN_DATABASE.
-- Successful retry and actual FEI target tables have not been verified.
