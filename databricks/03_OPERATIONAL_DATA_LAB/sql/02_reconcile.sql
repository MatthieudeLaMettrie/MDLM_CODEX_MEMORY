-- Run after the corresponding notebook stages. Adjust catalog once if required.
USE CATALOG training_dev;
SELECT batch_id, COUNT(*) AS delivered_lines, COUNT(DISTINCT event_id) AS distinct_events
FROM bronze.order_events GROUP BY batch_id ORDER BY batch_id;

SELECT line_id, order_id, amount_raw, reject_reason
FROM silver.order_quarantine ORDER BY line_id;

-- Expected: no duplicate current-state business keys.
SELECT source_system, order_id, COUNT(*) AS copies
FROM silver.orders_current GROUP BY source_system, order_id HAVING COUNT(*) > 1;

SELECT order_id, sequence, is_deleted, amount, event_id
FROM silver.orders_current ORDER BY order_id;

-- Compare counts and amounts; Gold is active state only.
SELECT 'silver_active' AS layer, COUNT(*) AS orders, SUM(amount) AS amount
FROM silver.orders_current WHERE NOT is_deleted
UNION ALL
SELECT 'gold', SUM(order_count), SUM(order_amount) FROM gold.daily_store_sales;

-- Expected: no duplicate Gold grain.
SELECT order_date, store_id, COUNT(*) AS copies
FROM gold.daily_store_sales GROUP BY order_date, store_id HAVING COUNT(*) > 1;

SELECT * FROM gold.daily_store_sales ORDER BY order_date, store_id;
DESCRIBE HISTORY silver.orders_current;
