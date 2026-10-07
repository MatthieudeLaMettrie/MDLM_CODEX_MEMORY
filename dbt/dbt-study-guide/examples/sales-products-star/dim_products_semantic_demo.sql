-- Synthetic BigQuery fixture: one row per product; no fact join here.
select 10 as Product_Key, 'Laptop' as Product_Name, 'Electronics' as Category,
       'Example Computing' as Brand
union all
select 20, 'Mouse', 'Electronics', 'Example Peripherals'
union all
select 30, 'Cable', 'Accessories', 'Example Cables'
