-- Snowflake semantic view lab: section 6 of ../SEMANTIC_LAYERS_DATABRICKS_SNOWFLAKE_GUIDE.md
-- Same fixture and expected answers as databricks_metric_view_lab.sql, so the two platforms can be compared.
--
-- HOW TO RUN
--   1. Snowsight -> Projects -> Workspaces (or Worksheets) -> new SQL file.
--   2. First time only: run block 0 as ACCOUNTADMIN (replace <your_user>), or skip it if
--      GENAI_LAB / GENAI_WH / role GENAI_SV_LAB already exist from snowpro-genai/03 and 08.
--   3. Paste this whole file and "Run all".
--   4. Copy back into the chat: the section 4 result grid (N / CHECK_NAME / EXPECTED / ACTUAL / PASS)
--      and the error message from section 6 (that statement is EXPECTED to fail; it is last on purpose).
--      Run all stops at the first error, so any earlier error means something is wrong: paste it instead.
--
-- Creates 3 tables + 1 semantic view in GENAI_LAB.PUBLIC. Cleanup is at the bottom, commented out.
-- Cost: a few seconds of an XSMALL warehouse. No Cortex/AI credits are used.

-- 0. ONE-TIME SETUP (ACCOUNTADMIN) -- uncomment if needed ---------------------
-- USE ROLE ACCOUNTADMIN;
-- CREATE DATABASE IF NOT EXISTS GENAI_LAB;
-- CREATE WAREHOUSE IF NOT EXISTS GENAI_WH WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
-- CREATE ROLE IF NOT EXISTS GENAI_SV_LAB;
-- GRANT USAGE ON DATABASE GENAI_LAB TO ROLE GENAI_SV_LAB;
-- GRANT USAGE ON SCHEMA GENAI_LAB.PUBLIC TO ROLE GENAI_SV_LAB;
-- GRANT USAGE ON WAREHOUSE GENAI_WH TO ROLE GENAI_SV_LAB;
-- GRANT CREATE TABLE ON SCHEMA GENAI_LAB.PUBLIC TO ROLE GENAI_SV_LAB;
-- GRANT CREATE SEMANTIC VIEW ON SCHEMA GENAI_LAB.PUBLIC TO ROLE GENAI_SV_LAB;
-- GRANT ROLE GENAI_SV_LAB TO USER <your_user>;

-- 1. Context and tables -------------------------------------------------------
USE ROLE GENAI_SV_LAB;
USE WAREHOUSE GENAI_WH;
USE SCHEMA GENAI_LAB.PUBLIC;

CREATE OR REPLACE TABLE SV_CUSTOMERS (CUSTOMER_ID VARCHAR, CUSTOMER_NAME VARCHAR, REGION VARCHAR);
INSERT INTO SV_CUSTOMERS VALUES ('C1','Acme','East'), ('C2','Birch','West'), ('C3','Cedar','East');

CREATE OR REPLACE TABLE SV_ORDERS (ORDER_ID VARCHAR, CUSTOMER_ID VARCHAR, ORDER_DATE DATE, ORDER_STATUS VARCHAR);
INSERT INTO SV_ORDERS VALUES
  ('O1','C1','2026-01-10','COMPLETE'), ('O2','C2','2026-01-20','COMPLETE'),
  ('O3','C1','2026-02-05','RETURNED'), ('O4','C3','2026-02-14','COMPLETE');

CREATE OR REPLACE TABLE SV_ORDER_LINES (
  ORDER_ID VARCHAR, LINE_NO NUMBER, PRODUCT VARCHAR,
  QUANTITY NUMBER, UNIT_PRICE NUMBER(10,2), DISCOUNT NUMBER(4,2));
INSERT INTO SV_ORDER_LINES VALUES
  ('O1',1,'Widget',2,50,0.00), ('O1',2,'Gadget',1,200,0.10), ('O2',1,'Widget',4,50,0.00),
  ('O3',1,'Gadget',1,200,0.00), ('O4',1,'Widget',3,50,0.20), ('O4',2,'Gizmo',1,80,0.00);

-- 2. Semantic view (guide section 6 + customer_name and descriptions) ---------
CREATE OR REPLACE SEMANTIC VIEW GENAI_LAB.PUBLIC.SALES_SV
  TABLES (
    customers   AS GENAI_LAB.PUBLIC.SV_CUSTOMERS   PRIMARY KEY (customer_id)       COMMENT = 'One row per customer.',
    orders      AS GENAI_LAB.PUBLIC.SV_ORDERS      PRIMARY KEY (order_id)          COMMENT = 'One row per order. ORDER_STATUS is COMPLETE or RETURNED.',
    order_lines AS GENAI_LAB.PUBLIC.SV_ORDER_LINES PRIMARY KEY (order_id, line_no) COMMENT = 'One row per order line.'
  )
  RELATIONSHIPS (
    orders_to_customers AS orders (customer_id) REFERENCES customers,
    lines_to_orders     AS order_lines (order_id) REFERENCES orders
  )
  FACTS (
    order_lines.line_net_amount   AS quantity * unit_price * (1 - discount) COMMENT = 'Line revenue after discount.',
    order_lines.line_gross_amount AS quantity * unit_price                   COMMENT = 'Line revenue before discount.'
  )
  DIMENSIONS (
    customers.customer_name AS customer_name COMMENT = 'Customer display name.',
    customers.region        AS region        COMMENT = 'Sales region of the customer.',
    orders.order_date       AS order_date    COMMENT = 'Date the order was placed.',
    orders.order_month      AS DATE_TRUNC('MONTH', order_date) COMMENT = 'First day of the order month.',
    orders.order_status     AS order_status  COMMENT = 'COMPLETE or RETURNED.',
    orders.is_completed LABELS = (FILTER) AS order_status = 'COMPLETE' COMMENT = 'TRUE for orders that were not returned.',
    order_lines.product     AS product       COMMENT = 'Product on the order line.'
  )
  METRICS (
    order_lines.net_sales   AS SUM(order_lines.line_net_amount)   WITH SYNONYMS = ('revenue') COMMENT = 'Revenue after line discounts. Includes returned orders unless filtered.',
    order_lines.gross_sales AS SUM(order_lines.line_gross_amount) COMMENT = 'Revenue before discounts.',
    orders.order_count      AS COUNT(orders.order_id)             COMMENT = 'Number of orders.',
    avg_order_value         AS order_lines.net_sales / orders.order_count COMMENT = 'Derived metric: net sales per order.'
  )
  COMMENT = 'Sales performance: same fixture as the Databricks metric view lab.';

-- 3. Inspect (look at the output, nothing to paste back) ----------------------
DESCRIBE SEMANTIC VIEW SALES_SV;
SHOW SEMANTIC METRICS IN SALES_SV;

-- 4. ALL CHECKS IN ONE GRID: paste this result back -------------------------
--    Uses both query styles: SEMANTIC_VIEW(...) clause and standard SQL with AGG().
WITH
tot AS (
  SELECT * FROM SEMANTIC_VIEW(SALES_SV
    METRICS order_lines.net_sales, order_lines.gross_sales, orders.order_count, avg_order_value)),
reg AS (
  SELECT * FROM SEMANTIC_VIEW(SALES_SV
    DIMENSIONS customers.region
    METRICS order_lines.net_sales, orders.order_count, avg_order_value)),
mon_all AS (
  SELECT * FROM SEMANTIC_VIEW(SALES_SV
    DIMENSIONS orders.order_month
    METRICS order_lines.net_sales, orders.order_count)),
mon_done AS (                                   -- standard-SQL form with a filter dimension
  SELECT order_month, AGG(net_sales) AS net_sales
  FROM SALES_SV WHERE is_completed GROUP BY order_month),
done_tot AS (
  SELECT AGG(net_sales) AS net_sales FROM SALES_SV WHERE is_completed),
prod AS (
  SELECT * FROM SEMANTIC_VIEW(SALES_SV
    DIMENSIONS order_lines.product
    METRICS order_lines.net_sales)),
raw AS (
  SELECT SUM(l.quantity * l.unit_price * (1 - l.discount)) AS net,
         COUNT(o.order_id) AS line_grain_count             -- the grain trap: expect 6
  FROM SV_ORDER_LINES l JOIN SV_ORDERS o ON l.order_id = o.order_id),
checks AS (
  SELECT 1 AS n, 'total net_sales' AS check_name, 880.00 AS expected, net_sales AS actual FROM tot UNION ALL
  SELECT 2,  'total gross_sales',             930.00, gross_sales     FROM tot UNION ALL
  SELECT 3,  'total order_count',             4,      order_count     FROM tot UNION ALL
  SELECT 4,  'total avg_order_value',         220.00, avg_order_value FROM tot UNION ALL
  SELECT 5,  'completed net_sales (AGG form)', 680.00, net_sales      FROM done_tot UNION ALL
  SELECT 6,  'East net_sales',                680.00, net_sales       FROM reg WHERE region = 'East' UNION ALL
  SELECT 7,  'East order_count',              3,      order_count     FROM reg WHERE region = 'East' UNION ALL
  SELECT 8,  'East avg_order_value',          226.67, avg_order_value FROM reg WHERE region = 'East' UNION ALL
  SELECT 9,  'West net_sales',                200.00, net_sales       FROM reg WHERE region = 'West' UNION ALL
  SELECT 10, 'West avg_order_value',          200.00, avg_order_value FROM reg WHERE region = 'West' UNION ALL
  SELECT 11, '2026-01 net_sales (all)',       480.00, net_sales   FROM mon_all WHERE order_month = '2026-01-01'::DATE UNION ALL
  SELECT 12, '2026-02 net_sales (all)',       400.00, net_sales   FROM mon_all WHERE order_month = '2026-02-01'::DATE UNION ALL
  SELECT 13, '2026-02 order_count (all)',     2,      order_count FROM mon_all WHERE order_month = '2026-02-01'::DATE UNION ALL
  SELECT 14, '2026-01 net_sales (completed)', 480.00, net_sales   FROM mon_done WHERE order_month = '2026-01-01'::DATE UNION ALL
  SELECT 15, '2026-02 net_sales (completed)', 200.00, net_sales   FROM mon_done WHERE order_month = '2026-02-01'::DATE UNION ALL
  SELECT 16, 'Widget net_sales',              420.00, net_sales FROM prod WHERE product = 'Widget' UNION ALL
  SELECT 17, 'Gadget net_sales',              380.00, net_sales FROM prod WHERE product = 'Gadget' UNION ALL
  SELECT 18, 'Gizmo net_sales',               80.00,  net_sales FROM prod WHERE product = 'Gizmo' UNION ALL
  SELECT 19, 'Reconcile: raw net = view net', 880.00, net       FROM raw UNION ALL
  SELECT 20, 'Grain trap: COUNT(order_id) at line grain', 6, line_grain_count FROM raw UNION ALL
  SELECT 21, 'Rows returned by region',       2,      COUNT(*)  FROM reg)
SELECT n, check_name, expected, ROUND(actual, 2) AS actual,
       IFF(ROUND(actual, 2) = expected, 'PASS', 'FAIL') AS pass
FROM checks
ORDER BY n;

-- 5. Which dimensions are valid for order_count? (product should NOT be listed)
SHOW SEMANTIC DIMENSIONS IN SALES_SV FOR METRIC order_count;

-- 6. EXPECTED TO FAIL: grain rule (product is finer than order_count's orders table).
--    Databricks returns Widget 3 / Gadget 2 / Gizmo 1 here; Snowflake rejects it. Paste the error back.
SELECT * FROM SEMANTIC_VIEW(SALES_SV DIMENSIONS order_lines.product METRICS orders.order_count);

-- 7. CLEANUP (run later, when you are done exploring)
-- DROP SEMANTIC VIEW IF EXISTS GENAI_LAB.PUBLIC.SALES_SV;
-- DROP TABLE IF EXISTS SV_ORDER_LINES; DROP TABLE IF EXISTS SV_ORDERS; DROP TABLE IF EXISTS SV_CUSTOMERS;
