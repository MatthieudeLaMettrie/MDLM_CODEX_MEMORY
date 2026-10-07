-- Synthetic BigQuery fixture: one row per sales line; no product join here.
select 101 as Sale_Line_Key, 1001 as Order_Key, 10 as Product_Key,
       date '2026-10-01' as Sale_Date, 1 as Quantity, cast(1000 as numeric) as Sales_Amount
union all
select 102, 1001, 20, date '2026-10-01', 2, cast(50 as numeric)
union all
select 103, 1002, 10, date '2026-10-02', 1, cast(1200 as numeric)
union all
select 104, 1003, 30, date '2026-10-02', 1, cast(30 as numeric)
