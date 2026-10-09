-- Databricks metric view lab: section 4 of ../SEMANTIC_LAYERS_DATABRICKS_SNOWFLAKE_GUIDE.md
--
-- HOW TO RUN
--   1. Databricks workspace -> SQL Editor -> New query. Attach a running SQL warehouse
--      (or any compute on Databricks Runtime 17.3+).
--   2. Paste this whole file and click "Run all".
--   3. Copy back into the chat: the section 4 result grid (columns n / check_name / expected / actual / pass)
--      and the one-cell result of section 5. If any statement fails, copy its error message instead
--      (execution stops at the first error).
--
-- Creates schema mdlm_db_trial.semantic_lab (3 tables + 1 metric view). Cleanup is at the bottom, commented out.

-- 1. Schema and tables -------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS mdlm_db_trial.semantic_lab;
USE mdlm_db_trial.semantic_lab;

CREATE OR REPLACE TABLE customers (customer_id STRING NOT NULL, customer_name STRING, region STRING);
INSERT INTO customers VALUES ('C1','Acme','East'), ('C2','Birch','West'), ('C3','Cedar','East');

CREATE OR REPLACE TABLE orders (order_id STRING NOT NULL, customer_id STRING, order_date DATE, order_status STRING);
INSERT INTO orders VALUES
  ('O1','C1',DATE'2026-01-10','COMPLETE'), ('O2','C2',DATE'2026-01-20','COMPLETE'),
  ('O3','C1',DATE'2026-02-05','RETURNED'), ('O4','C3',DATE'2026-02-14','COMPLETE');

CREATE OR REPLACE TABLE order_lines (
  order_id STRING, line_no INT, product STRING,
  quantity INT, unit_price DECIMAL(10,2), discount DECIMAL(4,2));
INSERT INTO order_lines VALUES
  ('O1',1,'Widget',2,50,0.00), ('O1',2,'Gadget',1,200,0.10), ('O2',1,'Widget',4,50,0.00),
  ('O3',1,'Gadget',1,200,0.00), ('O4',1,'Widget',3,50,0.20), ('O4',2,'Gizmo',1,80,0.00);

-- Informational (not enforced) primary keys
ALTER TABLE customers ADD CONSTRAINT customers_pk PRIMARY KEY (customer_id);
ALTER TABLE orders    ADD CONSTRAINT orders_pk    PRIMARY KEY (order_id);

-- 2. Metric view (identical to guide section 4, step 2, minus the optional format block) ----
CREATE OR REPLACE VIEW mdlm_db_trial.semantic_lab.sales_metrics
WITH METRICS LANGUAGE YAML AS
$$
version: 1.1
comment: "Sales performance over order lines. One source row = one order line."
source: mdlm_db_trial.semantic_lab.order_lines

joins:
  - name: orders
    source: mdlm_db_trial.semantic_lab.orders
    on: source.order_id = orders.order_id
    joins:
      - name: customers
        source: mdlm_db_trial.semantic_lab.customers
        on: orders.customer_id = customers.customer_id

fields:
  - name: region
    expr: orders.customers.region
    comment: "Sales region of the customer (East or West)."
    display_name: "Region"
  - name: customer_name
    expr: orders.customers.customer_name
    display_name: "Customer"
  - name: order_date
    expr: orders.order_date
    display_name: "Order date"
  - name: order_month
    expr: DATE_TRUNC('MONTH', orders.order_date)
    display_name: "Order month"
  - name: order_status
    expr: orders.order_status
    comment: "COMPLETE or RETURNED."
  - name: product
    expr: product
    comment: "Product on the order line."

measures:
  - name: net_sales
    expr: SUM(quantity * unit_price * (1 - discount))
    comment: "Revenue after line discounts. Includes returned orders unless filtered."
    display_name: "Net sales"
    synonyms: ["revenue", "net revenue"]
  - name: gross_sales
    expr: SUM(quantity * unit_price)
    display_name: "Gross sales"
  - name: order_count
    expr: COUNT(DISTINCT orders.order_id)
    comment: "Number of distinct orders. DISTINCT is required because the source is at line grain."
    display_name: "Orders"
  - name: avg_order_value
    expr: MEASURE(net_sales) / MEASURE(order_count)
    display_name: "Average order value"
    synonyms: ["AOV"]
  - name: completed_net_sales
    expr: SUM(quantity * unit_price * (1 - discount)) FILTER (WHERE orders.order_status = 'COMPLETE')
    display_name: "Completed net sales"
$$;

-- 3. Inspect (look at the output, nothing to paste back) ----------------------
DESCRIBE TABLE EXTENDED mdlm_db_trial.semantic_lab.sales_metrics;

-- 4. ALL CHECKS IN ONE GRID: paste this result back -------------------------
WITH
tot AS (
  SELECT MEASURE(net_sales) AS net, MEASURE(gross_sales) AS gross, MEASURE(order_count) AS oc,
         MEASURE(avg_order_value) AS aov, MEASURE(completed_net_sales) AS cns
  FROM mdlm_db_trial.semantic_lab.sales_metrics),
reg AS (
  SELECT region, MEASURE(net_sales) AS net, MEASURE(order_count) AS oc, MEASURE(avg_order_value) AS aov
  FROM mdlm_db_trial.semantic_lab.sales_metrics GROUP BY ALL),
mon_all AS (
  SELECT order_month, MEASURE(net_sales) AS net, MEASURE(order_count) AS oc
  FROM mdlm_db_trial.semantic_lab.sales_metrics GROUP BY ALL),
mon_done AS (
  SELECT order_month, MEASURE(net_sales) AS net
  FROM mdlm_db_trial.semantic_lab.sales_metrics WHERE order_status = 'COMPLETE' GROUP BY ALL),
prod AS (
  SELECT product, MEASURE(net_sales) AS net, MEASURE(order_count) AS oc
  FROM mdlm_db_trial.semantic_lab.sales_metrics GROUP BY ALL),
raw AS (
  SELECT SUM(l.quantity * l.unit_price * (1 - l.discount)) AS net,
         COUNT(o.order_id) AS line_grain_count             -- the grain trap: expect 6
  FROM order_lines l JOIN orders o ON l.order_id = o.order_id),
checks AS (
  SELECT 01 AS n, 'total net_sales'          AS check_name, 880.00 AS expected, net   AS actual FROM tot UNION ALL
  SELECT 02, 'total gross_sales',             930.00, gross FROM tot UNION ALL
  SELECT 03, 'total order_count',             4,      oc    FROM tot UNION ALL
  SELECT 04, 'total avg_order_value',         220.00, aov   FROM tot UNION ALL
  SELECT 05, 'completed_net_sales',           680.00, cns   FROM tot UNION ALL
  SELECT 06, 'East net_sales',                680.00, net FROM reg WHERE region = 'East' UNION ALL
  SELECT 07, 'East order_count',              3,      oc  FROM reg WHERE region = 'East' UNION ALL
  SELECT 08, 'East avg_order_value',          226.67, aov FROM reg WHERE region = 'East' UNION ALL
  SELECT 09, 'West net_sales',                200.00, net FROM reg WHERE region = 'West' UNION ALL
  SELECT 10, 'West avg_order_value',          200.00, aov FROM reg WHERE region = 'West' UNION ALL
  SELECT 11, '2026-01 net_sales (all)',       480.00, net FROM mon_all WHERE order_month = DATE'2026-01-01' UNION ALL
  SELECT 12, '2026-02 net_sales (all)',       400.00, net FROM mon_all WHERE order_month = DATE'2026-02-01' UNION ALL
  SELECT 13, '2026-02 order_count (all)',     2,      oc  FROM mon_all WHERE order_month = DATE'2026-02-01' UNION ALL
  SELECT 14, '2026-01 net_sales (completed)', 480.00, net FROM mon_done WHERE order_month = DATE'2026-01-01' UNION ALL
  SELECT 15, '2026-02 net_sales (completed)', 200.00, net FROM mon_done WHERE order_month = DATE'2026-02-01' UNION ALL
  SELECT 16, 'Widget net_sales',              420.00, net FROM prod WHERE product = 'Widget' UNION ALL
  SELECT 17, 'Gadget net_sales',              380.00, net FROM prod WHERE product = 'Gadget' UNION ALL
  SELECT 18, 'Gizmo net_sales',               80.00,  net FROM prod WHERE product = 'Gizmo' UNION ALL
  SELECT 19, 'Widget order_count (non-additive)', 3,  oc  FROM prod WHERE product = 'Widget' UNION ALL
  SELECT 20, 'Sum of per-product order_count',    6,  SUM(oc) FROM prod UNION ALL
  SELECT 21, 'Reconcile: raw net = view net', 880.00, net FROM raw UNION ALL
  SELECT 22, 'Grain trap: COUNT(order_id) at line grain', 6, line_grain_count FROM raw UNION ALL
  SELECT 23, 'Rows returned by region', 2, COUNT(*) FROM reg)
SELECT n, check_name, expected, ROUND(actual, 2) AS actual,
       CASE WHEN ROUND(actual, 2) = expected THEN 'PASS' ELSE 'FAIL' END AS pass
FROM checks
ORDER BY n;

-- 5. OPTIONAL: test the guide's `format` block in a separate view.
--    If this errors, the guide's format syntax is wrong: paste the error back.
CREATE OR REPLACE VIEW mdlm_db_trial.semantic_lab.sales_metrics_fmt
WITH METRICS LANGUAGE YAML AS
$$
version: 1.1
source: mdlm_db_trial.semantic_lab.order_lines
measures:
  - name: net_sales
    expr: SUM(quantity * unit_price * (1 - discount))
    format:
      type: currency
      currency_code: USD
      decimal_places:
        type: exact
        places: 2
$$;
SELECT MEASURE(net_sales) AS net_sales_fmt_check FROM mdlm_db_trial.semantic_lab.sales_metrics_fmt;  -- expect 880.00

-- 6. CLEANUP (run later, when you are done exploring)
-- DROP SCHEMA mdlm_db_trial.semantic_lab CASCADE;
