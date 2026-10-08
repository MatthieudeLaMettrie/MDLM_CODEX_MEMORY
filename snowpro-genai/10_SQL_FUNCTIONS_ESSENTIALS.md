# Snowflake SQL functions worth knowing

A curated, example-driven cut of Snowflake's [full function list](https://docs.snowflake.com/en/sql-reference/functions-all) (about 300,000 characters of reference, read end to end on 2026-10-09). It keeps the functions you will use weekly in data engineering, analytics and Gen AI/RAG work, and skips the long tail (administration, private link, replication, marketplace, `SYSTEM$` plumbing and so on).

**How to read it:** each section starts with a table of the function, what it does and a one-line trap, then a block of examples you can paste into a worksheet. Expected results appear in comments where they are simple and certain. Everything was adapted from the reference pages or checked against them, but **not executed in an account**. Snowflake changes quickly, so open the linked reference before relying on an edge case.

**Companion:** the AI functions (`AI_COMPLETE`, `AI_CLASSIFY` and so on) have their own file, [09_AI_FUNCTION_EXAMPLES.md](09_AI_FUNCTION_EXAMPLES.md). This file covers the rest, plus the legacy Cortex names and the Gen AI-adjacent SQL (vectors, chunking, `SEARCH`).

## Contents

1. [Conditional and NULL handling](#1-conditional-and-null-handling)
2. [Conversion](#2-conversion)
3. [Date and time](#3-date-and-time)
4. [String and regular expressions](#4-string-and-regular-expressions)
5. [Numeric](#5-numeric)
6. [Aggregate](#6-aggregate)
7. [Window and `QUALIFY`](#7-window-and-qualify)
8. [Semi-structured: JSON, arrays, objects](#8-semi-structured-json-arrays-objects)
9. [Table functions: `GENERATOR`, `FLATTEN`, history, `INFER_SCHEMA`](#9-table-functions)
10. [Context](#10-context)
11. [Hash, ids and encoding](#11-hash-ids-and-encoding)
12. [File and stage](#12-file-and-stage)
13. [Vector and similarity](#13-vector-and-similarity)
14. [Text search and chunking for RAG](#14-text-search-and-chunking-for-rag)
15. [Legacy `SNOWFLAKE.CORTEX` names](#15-legacy-snowflakecortex-names)
16. [Data quality (data metric functions)](#16-data-quality-data-metric-functions)
17. [System functions worth knowing](#17-system-functions-worth-knowing)
18. [Geospatial in five lines](#18-geospatial-in-five-lines)
19. [Not covered, and where to look](#19-not-covered-and-where-to-look)

**Shared sample data** (create once, used in many examples):

```sql
CREATE OR REPLACE TEMP TABLE orders AS
SELECT * FROM VALUES
  (1, 'alice', 'AU', '2026-10-01'::DATE, 120.50, 'shipped'),
  (2, 'bob',   'AU', '2026-10-02'::DATE,  80.00, 'shipped'),
  (3, 'alice', 'NZ', '2026-10-05'::DATE, 200.00, 'returned'),
  (4, 'carol', 'US', '2026-10-06'::DATE, NULL,   'pending'),
  (5, 'bob',   'AU', '2026-10-09'::DATE,  45.25, 'shipped')
AS t(order_id, customer, country, order_date, amount, status);
```

---

## 1. Conditional and NULL handling

| Function | What it does | Trap |
| --- | --- | --- |
| `IFF(cond, a, b)` | Inline if/else | Cleaner than a one-branch `CASE` |
| `CASE` | Multi-branch logic | No `ELSE` returns `NULL` |
| `COALESCE(a, b, ...)` | First non-NULL | Accepts many arguments |
| `NVL(a, b)` / `IFNULL(a, b)` | Two-argument `COALESCE` | Same behavior |
| `NVL2(x, if_not_null, if_null)` | Branch on NULL-ness | Argument 1 is only tested, not returned |
| `NULLIF(a, b)` | `NULL` if equal | Classic guard against divide-by-zero |
| `ZEROIFNULL(x)` | NULL to 0 | Numeric only |
| `DECODE(x, s1, r1, ..., default)` | Value lookup | Treats `NULL = NULL` as a match |
| `EQUAL_NULL(a, b)` | NULL-safe equality | `NULL = NULL` is TRUE here, unlike `=` |
| `GREATEST` / `LEAST` | Max/min across columns | Any NULL gives NULL (use the `_IGNORE_NULLS` variants to skip) |
| `BETWEEN` | Inclusive range | Both ends are included |

```sql
SELECT order_id,
       IFF(amount >= 100, 'large', 'small')                 AS size,          -- NULL amount -> 'small'
       COALESCE(amount, 0)                                  AS amount_filled,
       NVL2(amount, 'has amount', 'no amount')              AS flag,
       CASE status WHEN 'shipped' THEN 'done'
                   WHEN 'returned' THEN 'problem'
                   ELSE 'open' END                          AS stage,
       DECODE(country, 'AU', 'Australia', 'NZ', 'New Zealand', 'Other') AS country_name,
       10 / NULLIF(order_id - 3, 0)                         AS safe_div,      -- order 3 -> NULL, not an error
       ZEROIFNULL(amount)                                   AS amount_zero
FROM orders;

SELECT EQUAL_NULL(NULL, NULL);        -- TRUE
SELECT NULL = NULL;                   -- NULL (not TRUE)
SELECT GREATEST(3, 9, 5), LEAST(3, 9, 5);   -- 9, 3
```

---

## 2. Conversion

| Function | What it does | Trap |
| --- | --- | --- |
| `CAST(x AS T)` / `x::T` | Convert, error on failure | Use `TRY_` forms for dirty data |
| `TRY_CAST(x AS T)` | Convert, `NULL` on failure | `TRY_CAST` works on strings only |
| `TO_NUMBER` / `TO_DECIMAL`, `TRY_TO_NUMBER` | String to number with a format | Specify precision/scale: `TO_NUMBER(x, 10, 2)` |
| `TO_DATE`, `TO_TIMESTAMP[_NTZ/_LTZ/_TZ]`, `TRY_TO_*` | String to date/time | Pass a format for non-ISO input |
| `TO_VARCHAR` / `TO_CHAR` | Anything to string with a format | Date format uses `YYYY-MM-DD HH24:MI:SS` |
| `TO_VARIANT`, `TO_ARRAY`, `TO_OBJECT` | Wrap into semi-structured types | |
| `TO_BOOLEAN`, `TO_DOUBLE`, `TO_DECFLOAT` | Other scalar conversions | `TO_DECFLOAT` is the exact decimal-float type |

```sql
SELECT '42'::INT + 1;                               -- 43
SELECT TRY_CAST('abc' AS INT);                      -- NULL, no error
SELECT TRY_TO_DATE('2026-13-45');                   -- NULL
SELECT TO_DATE('09/10/2026', 'DD/MM/YYYY');         -- 2026-10-09
SELECT TO_TIMESTAMP_NTZ('2026-10-09 14:30:00');
SELECT TO_VARCHAR(CURRENT_DATE(), 'YYYY-MM-DD');
SELECT TO_NUMBER('1234.50', 10, 2);                 -- 1234.50
SELECT TRY_TO_NUMBER('12,5');                       -- NULL (comma not parsed without a format)
```

---

## 3. Date and time

| Function | What it does | Trap |
| --- | --- | --- |
| `CURRENT_DATE()`, `CURRENT_TIMESTAMP()`, `SYSDATE()` | Now | `CURRENT_TIMESTAMP` uses the session time zone; `SYSDATE` is UTC |
| `DATEADD(unit, n, d)` | Add an interval | Unit first: `DATEADD(day, 7, d)` |
| `DATEDIFF(unit, start, end)` | Count unit boundaries crossed | Counts boundaries, not elapsed time |
| `DATE_TRUNC(unit, d)` | Round down | `'month'` returns the 1st of the month |
| `DATE_PART` / `EXTRACT` | Pull a part | `EXTRACT(year FROM d)` |
| `LAST_DAY(d [, unit])` | End of month/quarter/year | |
| `DAYNAME`, `MONTHNAME` | Short names | English abbreviations |
| `CONVERT_TIMEZONE(from, to, ts)` | Shift zones | Two-argument form converts from the session zone |
| `TIME_SLICE(ts, n, unit)` | Bucket into fixed windows | Good for 5/15-minute rollups |
| `DATE_FROM_PARTS`, `TIMESTAMP_FROM_PARTS` | Build from numbers | |
| `ADD_MONTHS`, `MONTHS_BETWEEN`, `NEXT_DAY`, `PREVIOUS_DAY` | Calendar helpers | |

```sql
SELECT DATEADD(day, 7, DATE '2026-10-09');                 -- 2026-10-16
SELECT DATEDIFF(day, DATE '2026-10-01', DATE '2026-10-09'); -- 8
SELECT DATEDIFF(month, DATE '2026-01-31', DATE '2026-02-01'); -- 1 (one month boundary crossed, one day apart)
SELECT DATE_TRUNC('month', DATE '2026-10-09');             -- 2026-10-01
SELECT LAST_DAY(DATE '2026-02-10');                        -- 2026-02-28
SELECT EXTRACT(year FROM DATE '2026-10-09'), DAYNAME(DATE '2026-10-09');
SELECT CONVERT_TIMEZONE('UTC', 'Australia/Sydney', '2026-10-09 00:00:00'::TIMESTAMP_NTZ);
SELECT TIME_SLICE('2026-10-09 14:37:00'::TIMESTAMP_NTZ, 15, 'MINUTE');  -- 14:30:00
SELECT DATE_FROM_PARTS(2026, 10, 9);
SELECT NEXT_DAY(DATE '2026-10-09', 'Monday');

-- Monthly revenue
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY 1;

-- Calendar spine of 10 days (uses GENERATOR, section 9)
SELECT DATEADD(day, SEQ4(), DATE '2026-10-01') AS d
FROM TABLE(GENERATOR(ROWCOUNT => 10));
```

---

## 4. String and regular expressions

| Function | What it does | Trap |
| --- | --- | --- |
| `CONCAT`, `\|\|`, `CONCAT_WS(sep, ...)` | Join strings | `\|\|` and `CONCAT` return NULL if any input is NULL; `CONCAT_WS` skips NULLs |
| `SPLIT(s, sep)` | String to array | Returns an ARRAY |
| `SPLIT_PART(s, sep, n)` | n-th piece | **1-based**; out of range gives `''` |
| `SUBSTR(s, start, len)` | Substring | 1-based |
| `LEFT`, `RIGHT`, `LENGTH`, `REVERSE`, `REPEAT` | Basics | |
| `TRIM`, `LTRIM`, `RTRIM` | Strip characters | Default strips spaces |
| `UPPER`, `LOWER`, `INITCAP` | Case | |
| `LPAD`, `RPAD` | Pad to length | Truncates if longer |
| `REPLACE`, `TRANSLATE` | Replace text / per-character map | `TRANSLATE` swaps characters one-for-one |
| `CHARINDEX`, `POSITION` | Find a substring | Returns 0 if not found |
| `CONTAINS`, `STARTSWITH`, `ENDSWITH` | Boolean tests | Case-sensitive |
| `LIKE`, `ILIKE`, `LIKE ANY/ALL` | Wildcard match | `ILIKE` is case-insensitive |
| `SPLIT_TO_TABLE`, `STRTOK_TO_ARRAY` | One row per token | Table function, use with `LATERAL` |
| `EDITDISTANCE`, `JAROWINKLER_SIMILARITY`, `SOUNDEX` | Fuzzy matching | Jaro-Winkler returns 0 to 100 |
| `REGEXP_SUBSTR`, `REGEXP_REPLACE`, `REGEXP_LIKE`, `REGEXP_COUNT`, `REGEXP_INSTR`, `REGEXP_SUBSTR_ALL` | Regular expressions | `REGEXP_LIKE` must match the **whole** string |

```sql
SELECT CONCAT_WS('-', 'a', NULL, 'c');                 -- a-c  (NULL skipped)
SELECT 'a' || NULL;                                    -- NULL
SELECT SPLIT('a,b,c', ',');                            -- ["a","b","c"]
SELECT SPLIT_PART('a,b,c', ',', 2);                    -- b
SELECT SUBSTR('snowflake', 1, 4);                      -- snow
SELECT LPAD('7', 3, '0');                              -- 007
SELECT INITCAP('hello snowflake world');               -- Hello Snowflake World
SELECT CHARINDEX('flake', 'snowflake');                -- 5
SELECT TRANSLATE('2*3+4', '*+', 'x-');                 -- 2x3-4
SELECT EDITDISTANCE('kitten', 'sitting');              -- 3
SELECT JAROWINKLER_SIMILARITY('Snowflake', 'Snowflaek');   -- close to 100

-- Regular expressions
SELECT REGEXP_SUBSTR('order 4521 shipped', '[0-9]+');          -- 4521
SELECT REGEXP_REPLACE('a1b22c', '[0-9]+', '#');                -- a#b#c
SELECT REGEXP_COUNT('a1b22c333', '[0-9]+');                    -- 3
SELECT REGEXP_LIKE('abc123', '[a-z]+[0-9]+');                  -- TRUE (whole string matches)
SELECT REGEXP_LIKE('abc123 tail', '[a-z]+[0-9]+');             -- FALSE (does not match the whole string)
SELECT REGEXP_SUBSTR_ALL('a1b22c333', '[0-9]+');               -- ["1","22","333"]

-- One row per word
SELECT t.value FROM TABLE(SPLIT_TO_TABLE('the quick brown fox', ' ')) t;

-- Pattern filters
SELECT * FROM orders WHERE customer ILIKE 'AL%';
SELECT * FROM orders WHERE customer ILIKE ANY ('al%', 'bo%');
```

---

## 5. Numeric

| Function | What it does | Trap |
| --- | --- | --- |
| `ROUND(x, n)`, `CEIL`, `FLOOR`, `TRUNC(x, n)` | Rounding | `ROUND` is half away from zero |
| `ABS`, `SIGN`, `MOD`, `POWER`, `SQRT`, `LN`, `EXP` | Maths | `MOD` takes the dividend's sign |
| `DIV0(a, b)` | Divide, 0 when `b` is 0 | Hides the error, so check it fits your logic |
| `DIV0NULL(a, b)` | Divide, 0 when `b` is 0 **or NULL** | |
| `WIDTH_BUCKET(x, lo, hi, n)` | Histogram bucket number | Out of range returns 0 or n+1 |
| `RANDOM()`, `UNIFORM(lo, hi, gen)`, `NORMAL(mean, sd, gen)` | Random values | Pass `RANDOM()` as the generator |
| `SEQ1/2/4/8()` | Increasing integers | Not guaranteed gap-free; use with `GENERATOR` |
| `UUID_STRING()` | Random UUID | |

```sql
SELECT ROUND(2.567, 2), CEIL(2.1), FLOOR(2.9), TRUNC(2.99);   -- 2.57, 3, 2, 2
SELECT DIV0(10, 0);                                           -- 0, no error
SELECT 10 / 0;                                                -- error: division by zero
SELECT WIDTH_BUCKET(45.25, 0, 200, 4);                        -- 1 (0-50 bucket)
SELECT UNIFORM(1, 100, RANDOM());                             -- random integer 1..100

-- Share of total per customer
SELECT customer, SUM(amount) AS total,
       ROUND(100 * DIV0(SUM(amount), SUM(SUM(amount)) OVER ()), 1) AS pct
FROM orders GROUP BY customer;
```

---

## 6. Aggregate

| Function | What it does | Trap |
| --- | --- | --- |
| `COUNT(*)` vs `COUNT(col)` | All rows vs non-NULL values | `COUNT(col)` ignores NULLs |
| `COUNT_IF(cond)` | Count rows meeting a condition | Replaces `SUM(IFF(...))` |
| `COUNT(DISTINCT x)` / `APPROX_COUNT_DISTINCT(x)` | Exact vs fast approximate | The approximation is HyperLogLog |
| `SUM`, `AVG`, `MIN`, `MAX`, `MEDIAN`, `MODE` | Basics | Aggregates skip NULLs |
| `MIN_BY(val, key)`, `MAX_BY(val, key)` | Value at the min/max of another column | "Latest status per user" |
| `LISTAGG(x, sep)` | Concatenate rows | Needs `WITHIN GROUP (ORDER BY ...)` for a stable order |
| `ARRAY_AGG(x)`, `OBJECT_AGG(k, v)` | Collect rows into array/object | |
| `ANY_VALUE(x)` | One arbitrary value | Handy to avoid adding columns to `GROUP BY` |
| `APPROX_PERCENTILE(x, p)`, `PERCENTILE_CONT(p) WITHIN GROUP (...)` | Percentiles | `APPROX_` is cheaper, `_CONT` interpolates exactly |
| `STDDEV`, `VARIANCE`, `CORR`, `COVAR_POP` | Statistics | |
| `HLL`, `APPROX_TOP_K(x, k)` | Sketches and top values | |
| `GROUPING SETS`, `ROLLUP`, `CUBE`, `GROUPING()` | Subtotals | `GROUPING()` tells subtotal NULLs from real NULLs |

```sql
SELECT COUNT(*)        AS all_rows,          -- 5
       COUNT(amount)   AS with_amount,       -- 4
       COUNT_IF(status = 'shipped') AS shipped,   -- 3
       SUM(amount)     AS total,             -- 445.75
       AVG(amount)     AS avg_amount,        -- NULL ignored
       MEDIAN(amount), MODE(country)
FROM orders;

SELECT customer,
       LISTAGG(status, ', ') WITHIN GROUP (ORDER BY order_date) AS statuses,
       ARRAY_AGG(order_id)                                       AS ids,
       MAX_BY(status, order_date)                                AS latest_status,
       APPROX_COUNT_DISTINCT(country)                            AS countries
FROM orders GROUP BY customer;

SELECT OBJECT_AGG(customer, total) FROM (SELECT customer, SUM(amount) AS total FROM orders GROUP BY customer);

SELECT APPROX_PERCENTILE(amount, 0.9) FROM orders;
SELECT APPROX_TOP_K(country, 2) FROM orders;

-- Subtotals
SELECT country, customer, SUM(amount) AS total
FROM orders
GROUP BY ROLLUP (country, customer);
```

---

## 7. Window and `QUALIFY`

| Function | What it does | Trap |
| --- | --- | --- |
| `ROW_NUMBER()` | 1,2,3 without ties | Needs an `ORDER BY` for determinism |
| `RANK()`, `DENSE_RANK()` | Ranking with ties | `RANK` leaves gaps, `DENSE_RANK` does not |
| `LAG(x, n)`, `LEAD(x, n)` | Previous/next row | Returns NULL at the edge unless you pass a default |
| `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE` | Value at a position | `LAST_VALUE` default frame ends at the current row, so widen the frame |
| `NTILE(n)` | Split into n buckets | |
| `PERCENT_RANK`, `CUME_DIST`, `RATIO_TO_REPORT` | Relative position / share | |
| `SUM(x) OVER (... ROWS BETWEEN ...)` | Running and moving totals | Frame default differs by `ORDER BY` |
| `CONDITIONAL_TRUE_EVENT`, `CONDITIONAL_CHANGE_EVENT` | Counters that bump on a condition/change | Useful for sessionization |
| `INTERPOLATE_LINEAR/FFILL/BFILL` | Fill gaps in time series | |
| **`QUALIFY`** | Filter on a window function | Snowflake-specific: no subquery needed |

```sql
-- Latest order per customer, no subquery
SELECT *
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer ORDER BY order_date DESC) = 1;

-- Day-over-day change
SELECT order_id, order_date, amount,
       amount - LAG(amount) OVER (ORDER BY order_date) AS change_vs_prev
FROM orders;

-- Running total and 3-row moving average
SELECT order_id,
       SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)        AS moving_avg_3
FROM orders;

-- Ranking and quartiles
SELECT customer, SUM(amount) AS total,
       RANK()       OVER (ORDER BY SUM(amount) DESC NULLS LAST) AS rnk,
       NTILE(2)     OVER (ORDER BY SUM(amount) DESC NULLS LAST) AS half
FROM orders GROUP BY customer;

-- Share of the whole
SELECT customer, amount, RATIO_TO_REPORT(amount) OVER () AS share FROM orders;

-- Deduplicate: keep the newest row per key
SELECT * FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date DESC) = 1;
```

---

## 8. Semi-structured: JSON, arrays, objects

| Function | What it does | Trap |
| --- | --- | --- |
| `PARSE_JSON(s)` / `TRY_PARSE_JSON(s)` | String to VARIANT | `TRY_` returns NULL on bad JSON |
| `v:key`, `v:a.b`, `v:arr[0]` | Path access | Keys are **case-sensitive**; cast with `::` |
| `GET_PATH(v, 'a.b')`, `GET(v, 'k')` | Function form of path access | |
| `TO_JSON(v)` | VARIANT to JSON text | |
| `OBJECT_CONSTRUCT(k, v, ...)` | Build an object | NULL values are dropped (use `_KEEP_NULL` to keep) |
| `OBJECT_KEYS`, `OBJECT_INSERT`, `OBJECT_DELETE`, `OBJECT_PICK` | Edit objects | |
| `FLATTEN(input => ...)` | One row per element | Use `OUTER => TRUE` to keep empty/NULL inputs |
| `ARRAY_CONSTRUCT`, `ARRAY_APPEND`, `ARRAY_CAT`, `ARRAY_SLICE`, `ARRAY_SORT`, `ARRAY_DISTINCT` | Build and edit arrays | Arrays are 0-based |
| `ARRAY_CONTAINS(val::VARIANT, arr)` | Membership | **Value first**, and it must be cast to VARIANT |
| `ARRAY_SIZE`, `ARRAY_TO_STRING`, `ARRAYS_OVERLAP`, `ARRAY_INTERSECTION`, `ARRAY_FLATTEN`, `ARRAY_COMPACT`, `ARRAY_MAX/MIN` | Inspect and combine | |
| `TRANSFORM`, `FILTER`, `REDUCE` | Lambdas over arrays | Lambda form `x -> expr` |
| `TYPEOF(v)`, `IS_ARRAY`, `IS_OBJECT`, `IS_NULL_VALUE` | Type checks | JSON `null` is not SQL `NULL` |
| `STRIP_NULL_VALUE(v)` | JSON null to SQL NULL | |
| `MAP_*` (`MAP_CONSTRUCT`, `MAP_KEYS`, `MAP_CONTAINS_KEY` ...) | Typed maps | For structured types |

```sql
-- Query JSON
WITH raw AS (
  SELECT PARSE_JSON('{"user":{"name":"alice","tags":["a","b"]},"items":[{"sku":"X1","qty":2},{"sku":"Y2","qty":5}]}') AS v
)
SELECT v:user.name::STRING          AS name,       -- alice
       v:user.tags[0]::STRING       AS first_tag,  -- a
       v:items[1].qty::INT          AS qty,        -- 5
       TYPEOF(v:items)              AS items_type, -- ARRAY
       GET_PATH(v, 'user.name')     AS via_path
FROM raw;

-- Explode an array into rows, with its position
WITH raw AS (SELECT PARSE_JSON('{"items":[{"sku":"X1","qty":2},{"sku":"Y2","qty":5}]}') AS v)
SELECT f.index, f.value:sku::STRING AS sku, f.value:qty::INT AS qty
FROM raw, LATERAL FLATTEN(input => raw.v:items) f;

-- Keep rows whose array is empty
SELECT f.value FROM (SELECT PARSE_JSON('{"a":[]}') AS v) raw,
       LATERAL FLATTEN(input => raw.v:a, OUTER => TRUE) f;

-- Build JSON
SELECT OBJECT_CONSTRUCT('id', order_id, 'who', customer, 'amount', amount) FROM orders;   -- NULL amount is omitted
SELECT OBJECT_CONSTRUCT(*) FROM orders;                                                    -- every column

SELECT TRY_PARSE_JSON('{bad json');                        -- NULL
SELECT OBJECT_KEYS(PARSE_JSON('{"a":1,"b":2}'));           -- ["a","b"]

-- Arrays
SELECT ARRAY_CONSTRUCT(1, 2, 3, 3);
SELECT ARRAY_CONTAINS(2::VARIANT, ARRAY_CONSTRUCT(1, 2, 3));      -- TRUE
SELECT ARRAY_SIZE(ARRAY_CONSTRUCT(1, 2, 3));                      -- 3
SELECT ARRAY_DISTINCT(ARRAY_CONSTRUCT(1, 2, 3, 3));               -- [1,2,3]
SELECT ARRAY_SLICE(ARRAY_CONSTRUCT(10, 20, 30, 40), 1, 3);        -- [20,30]
SELECT ARRAY_TO_STRING(ARRAY_CONSTRUCT('a', 'b'), '-');           -- a-b
SELECT ARRAYS_OVERLAP(ARRAY_CONSTRUCT(1, 2), ARRAY_CONSTRUCT(2, 3));   -- TRUE

-- Lambdas (verified against the reference)
SELECT TRANSFORM([1, 2, 3], a INT -> a * 2);                      -- [2,4,6]
SELECT FILTER([1, NULL, 3, 5, NULL], a -> a IS NOT NULL);         -- [1,3,5]
SELECT REDUCE([1, 2, 3], 0, (acc, val) -> acc + val);             -- 6
```

---

## 9. Table functions

| Function | What it does | Trap |
| --- | --- | --- |
| `TABLE(GENERATOR(ROWCOUNT => n))` | Make n rows | Pair with `SEQ4()`, `RANDOM()`; it has no columns of its own |
| `FLATTEN` | Explode semi-structured data | See section 8 |
| `SPLIT_TO_TABLE`, `STRTOK_SPLIT_TO_TABLE` | Split text into rows | |
| `RESULT_SCAN(query_id)` | Query a previous result | Result cache lasts 24 hours; use `LAST_QUERY_ID()` |
| `INFER_SCHEMA(...)` | Detect columns from staged files | Pair with `CREATE TABLE ... USING TEMPLATE` |
| `INFORMATION_SCHEMA.QUERY_HISTORY(...)` | Recent queries | Current database only, short retention |
| `INFORMATION_SCHEMA.TASK_HISTORY`, `COPY_HISTORY`, `LOGIN_HISTORY`, `WAREHOUSE_METERING_HISTORY` | Operational history | Wrap in `TABLE(...)` |
| `VALIDATE(table, JOB_ID => '_last')` | Rows rejected by the last `COPY` | |
| `TAG_REFERENCES(...)` | Which objects carry a tag | |

```sql
-- 5 rows with a running id and random values
SELECT SEQ4() AS id, UNIFORM(1, 6, RANDOM()) AS dice
FROM TABLE(GENERATOR(ROWCOUNT => 5));

-- Re-use the last result without re-running it
SHOW WAREHOUSES;
SELECT "name", "size" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

-- Slowest recent queries
SELECT query_id, total_elapsed_time/1000 AS secs, query_text
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(RESULT_LIMIT => 100))
ORDER BY total_elapsed_time DESC
LIMIT 5;

-- Recent task runs
SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(RESULT_LIMIT => 20));

-- Warehouse credit use over the last day
SELECT * FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_METERING_HISTORY(
  DATE_RANGE_START => DATEADD(day, -1, CURRENT_TIMESTAMP())));

-- Detect a staged file's columns (Parquet shown)
SELECT * FROM TABLE(INFER_SCHEMA(
  LOCATION    => '@MY_DB.MY_SCHEMA.DATA_STAGE',
  FILE_FORMAT => 'MY_PARQUET_FORMAT'));

-- Rows a COPY rejected
SELECT * FROM TABLE(VALIDATE(MY_TABLE, JOB_ID => '_last'));
```

---

## 10. Context

Functions that describe the session. Very useful for debugging **privilege and governance** issues, which feature heavily in the Gen AI exam.

| Function | Returns |
| --- | --- |
| `CURRENT_ROLE()`, `CURRENT_USER()` | Active role and user |
| `CURRENT_AVAILABLE_ROLES()`, `CURRENT_SECONDARY_ROLES()` | Roles you could use / secondary roles active |
| `CURRENT_WAREHOUSE()`, `CURRENT_DATABASE()`, `CURRENT_SCHEMA()` | Working context |
| `CURRENT_ACCOUNT()`, `CURRENT_REGION()`, `CURRENT_ORGANIZATION_NAME()` | Where you are |
| `CURRENT_VERSION()`, `CURRENT_CLIENT()` | Snowflake and client version |
| `CURRENT_SESSION()`, `CURRENT_STATEMENT()`, `LAST_QUERY_ID()` | Session and query ids |

```sql
SELECT CURRENT_ROLE(), CURRENT_USER(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
SELECT CURRENT_REGION(), CURRENT_ACCOUNT();
SELECT LAST_QUERY_ID();

-- Why does an AI function fail? Check the role you are actually running as.
SELECT CURRENT_ROLE(), CURRENT_AVAILABLE_ROLES();
```

---

## 11. Hash, ids and encoding

| Function | What it does | Trap |
| --- | --- | --- |
| `HASH(a, b, ...)` | 64-bit hash of columns | Not cryptographic, and its values may change between releases, so don't persist it as an external key |
| `MD5(s)`, `SHA1(s)`, `SHA2(s, 256)` | Cryptographic digests | `SHA2` length is 224/256/384/512 |
| `HASH_AGG(*)` | One hash for a whole result | Compare two tables' contents quickly |
| `UUID_STRING()` | Random id | |
| `BASE64_ENCODE`, `BASE64_DECODE_STRING`, `HEX_ENCODE`, `HEX_DECODE_STRING` | Encoding | `TRY_` variants return NULL on bad input |
| `COMPRESS`, `DECOMPRESS_STRING` | Compression | |

```sql
SELECT MD5('snowflake');
SELECT SHA2('snowflake', 256);
SELECT HASH(customer, country) FROM orders;
SELECT BASE64_ENCODE('hello'), BASE64_DECODE_STRING(BASE64_ENCODE('hello'));   -- aGVsbG8=, hello
SELECT UUID_STRING();

-- Did two tables end up identical?
SELECT (SELECT HASH_AGG(*) FROM orders) = (SELECT HASH_AGG(*) FROM orders_copy) AS same;
```

---

## 12. File and stage

Used by the document and multimodal AI functions.

| Function | What it does | Trap |
| --- | --- | --- |
| `TO_FILE('@stage', 'path')` | Build a FILE object | A local path is not a FILE |
| `DIRECTORY(@stage)` | Table of staged files | Stage needs `DIRECTORY = (ENABLE = TRUE)` and a refresh |
| `BUILD_SCOPED_FILE_URL(@stage, 'path')` | Temporary scoped URL | Expires; tied to the caller |
| `GET_PRESIGNED_URL(@stage, 'path', secs)` | Shareable time-limited URL | Treat like a secret |
| `FL_GET_SIZE`, `FL_GET_RELATIVE_PATH`, `FL_GET_LAST_MODIFIED`, `FL_GET_CONTENT_TYPE` | File metadata from a FILE | |
| `FL_IS_IMAGE`, `FL_IS_DOCUMENT`, `FL_IS_AUDIO`, `FL_IS_VIDEO` | Type tests | Route files to the right AI function |

```sql
ALTER STAGE MY_DB.MY_SCHEMA.DOC_STAGE REFRESH;

SELECT relative_path, size, last_modified
FROM DIRECTORY(@MY_DB.MY_SCHEMA.DOC_STAGE);

SELECT BUILD_SCOPED_FILE_URL(@MY_DB.MY_SCHEMA.DOC_STAGE, 'invoice.pdf');
SELECT GET_PRESIGNED_URL(@MY_DB.MY_SCHEMA.DOC_STAGE, 'invoice.pdf', 3600);

-- Send images to one function and documents to another
SELECT relative_path,
       IFF(FL_IS_IMAGE(TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', relative_path)), 'image', 'other') AS kind
FROM DIRECTORY(@MY_DB.MY_SCHEMA.DOC_STAGE);
```

---

## 13. Vector and similarity

The SQL side of embeddings and semantic search. Embeddings come from `AI_EMBED` (see file 09).

| Function | Better when | Trap |
| --- | --- | --- |
| `VECTOR_COSINE_SIMILARITY(a, b)` | **Higher** is closer (range -1 to 1) | Most common for text |
| `VECTOR_INNER_PRODUCT(a, b)` | **Higher** is closer | Same as cosine only for normalized vectors |
| `VECTOR_L2_DISTANCE(a, b)` | **Lower** is closer | Distance, so sort ascending |
| `VECTOR_L1_DISTANCE(a, b)` | **Lower** is closer | |
| `VECTOR_NORMALIZE(v)` | Scale to length 1 | Margin of error up to 1e-4 |
| `VECTOR_TRUNCATE(v, n)` | Keep the first n dimensions | Only for models trained to be truncatable; normalize afterwards |
| `VECTOR_SUM/AVG/MIN/MAX` | Aggregate vectors | Listed in the "Vector aggregation" group |

Both vectors must have the same dimension and come from the same embedding model.

```sql
SELECT VECTOR_NORMALIZE([1, 2, 3]::VECTOR(INT, 3));          -- [0.267261, 0.534522, 0.801784]
SELECT VECTOR_TRUNCATE([1, 2, 3]::VECTOR(INT, 3), 2);        -- [1,2]
SELECT VECTOR_COSINE_SIMILARITY([1, 0]::VECTOR(FLOAT, 2), [1, 1]::VECTOR(FLOAT, 2));   -- ~0.707
SELECT VECTOR_L2_DISTANCE([0, 0]::VECTOR(FLOAT, 2), [3, 4]::VECTOR(FLOAT, 2));         -- 5

-- A tiny semantic search
CREATE OR REPLACE TEMP TABLE docs AS
SELECT txt, AI_EMBED('snowflake-arctic-embed-l-v2.0', txt) AS v
FROM VALUES ('Refunds are issued within 14 days'), ('Our office is closed on public holidays'),
            ('To return an item, print a label') AS t(txt);

SELECT txt
FROM docs
ORDER BY VECTOR_COSINE_SIMILARITY(v, AI_EMBED('snowflake-arctic-embed-l-v2.0', 'how do I get my money back?')) DESC
LIMIT 2;

-- Smaller, cheaper vectors: truncate then normalize
SELECT VECTOR_NORMALIZE(VECTOR_TRUNCATE(AI_EMBED('snowflake-arctic-embed-m-v1.5', 'hello'), 256));
```

---

## 14. Text search and chunking for RAG

| Function | What it does | Trap |
| --- | --- | --- |
| `SEARCH(cols, 'text' [, ANALYZER =>, SEARCH_MODE =>])` | Token-based full-text match (BOOLEAN) | Matches whole tokens, not substrings like `LIKE '%x%'`; case-insensitive by default |
| `SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(text, format, size [, overlap, seps])` | Chunk by characters | Size is **characters**, not tokens |
| `SNOWFLAKE.CORTEX.SPLIT_TEXT_MARKDOWN_HEADER(text, headers_obj, size [, overlap])` | Chunk Markdown by headers | Returns `{chunk, headers}` objects, so headers travel with each chunk |
| `AI_PARSE_DOCUMENT` | Get text from files first | See file 09 |

`SEARCH_MODE` is `'OR'` (default), `'AND'`, `'PHRASE'` or `'EXACT'`.

```sql
-- Full-text search in a WHERE clause
SELECT * FROM docs WHERE SEARCH(txt, 'refunds');
SELECT * FROM docs WHERE SEARCH(txt, 'return label', SEARCH_MODE => 'AND');
SELECT SEARCH('king', 'KING');                       -- TRUE (case-insensitive)

-- Character chunks with overlap
SELECT SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER('hello world are you here', 'none', 15, 10);
-- ['hello world are', 'world are you', 'are you here']

-- Markdown-aware chunks that remember their headings
SELECT c.value:chunk::STRING   AS chunk,
       c.value:headers         AS headers
FROM TABLE(FLATTEN(input => SNOWFLAKE.CORTEX.SPLIT_TEXT_MARKDOWN_HEADER(
       '# Returns\nItems can be returned within 30 days.\n## Refunds\nRefunds take 5 days.',
       OBJECT_CONSTRUCT('#', 'section', '##', 'subsection'),
       200, 20))) c;

-- Typical RAG ingest: parse -> chunk -> embed -> store
CREATE OR REPLACE TABLE doc_chunks AS
SELECT d.relative_path,
       c.value:chunk::STRING AS chunk,
       AI_EMBED('snowflake-arctic-embed-l-v2.0', c.value:chunk::STRING) AS v
FROM (
  SELECT relative_path,
         PARSE_JSON(AI_PARSE_DOCUMENT(TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', relative_path),
                    {'mode': 'LAYOUT'})):content::STRING AS md
  FROM DIRECTORY(@MY_DB.MY_SCHEMA.DOC_STAGE)
) d,
LATERAL FLATTEN(input => SNOWFLAKE.CORTEX.SPLIT_TEXT_MARKDOWN_HEADER(
         d.md, OBJECT_CONSTRUCT('#', 'h1', '##', 'h2'), 1500, 150)) c;
```

---

## 15. Legacy `SNOWFLAKE.CORTEX` names

The function list still shows the older `SNOWFLAKE.CORTEX.*` functions beside the newer `AI_*` ones. **Learn the mapping**, because exam material and older tutorials use the old names. The docs say, for the ones marked below, *"This legacy function will be deprecated by the end of 2026"* and recommend the `AI_` replacement. They are kept for backward compatibility.

| Legacy function | Syntax | Use instead | Notes |
| --- | --- | --- | --- |
| `SNOWFLAKE.CORTEX.COMPLETE` | `(model, prompt_or_history [, options])` | `AI_COMPLETE` | Marked legacy |
| `SNOWFLAKE.CORTEX.TRY_COMPLETE` | same | `AI_COMPLETE` | **Returns NULL instead of an error**. Marked legacy |
| `SNOWFLAKE.CORTEX.TRANSLATE` | `(text, source, target)` | `AI_TRANSLATE` | Marked legacy |
| `SNOWFLAKE.CORTEX.EXTRACT_ANSWER` | `(source_document, question)` | `AI_EXTRACT` | Returns a single string. Marked legacy |
| `SNOWFLAKE.CORTEX.CLASSIFY_TEXT` | `(input, categories [, options])` | `AI_CLASSIFY` | 2 to 100 categories; returns an object with a `label`. Marked legacy |
| `SNOWFLAKE.CORTEX.EMBED_TEXT_768` / `EMBED_TEXT_1024` | `(model, text)` | `AI_EMBED` | 768-d models include `snowflake-arctic-embed-m-v1.5` and `e5-base-v2`. Marked legacy |
| `SNOWFLAKE.CORTEX.ENTITY_SENTIMENT` | `(text [, entities])` | `AI_SENTIMENT` | Returns an object with a `categories` array. Marked legacy |
| `SNOWFLAKE.CORTEX.SENTIMENT` | `(text)` | `AI_SENTIMENT` | Returns one FLOAT, -1 to 1. **No deprecation notice found on its page** |
| `SNOWFLAKE.CORTEX.SUMMARIZE` | `(text)` | `AI_SUMMARIZE` | The `AI_SUMMARIZE` page shows no deprecation language. Not fetched separately |
| `SNOWFLAKE.CORTEX.COUNT_TOKENS` | `(model, text)` | `AI_COUNT_TOKENS` | Not fetched; confirm on the page |

```sql
-- Old and new side by side
SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3.3-70b', 'Say hi');         -- old
SELECT AI_COMPLETE('llama3.3-70b', 'Say hi');                       -- new

SELECT SNOWFLAKE.CORTEX.TRANSLATE('Bonjour', 'fr', 'en');           -- old (three arguments)
SELECT AI_TRANSLATE('Bonjour', '', 'en');                           -- new ('' = detect)

SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT('The package arrived damaged', ['Shipping', 'Product Quality']);
SELECT AI_CLASSIFY('The package arrived damaged', ['Shipping', 'Product Quality']);

SELECT SNOWFLAKE.CORTEX.EXTRACT_ANSWER('Order 4521 ships on 12 Oct.', 'When does it ship?');
SELECT AI_EXTRACT(text => 'Order 4521 ships on 12 Oct.',
                  responseFormat => {'ship_date': 'When does it ship?'});

SELECT SNOWFLAKE.CORTEX.TRY_COMPLETE('llama3.3-70b', 'Say hi');     -- NULL if it cannot complete
```

**Rule of thumb for the exam:** if a question offers both an old `SNOWFLAKE.CORTEX.*` name and an `AI_*` name for a new build, the `AI_*` function is the current choice. Know that `TRY_COMPLETE` is the old NULL-on-error variant, and that `AI_*` functions return NULL on a failing row by default.

---

## 16. Data quality (data metric functions)

System data metric functions (DMFs) live in the `SNOWFLAKE.CORE` schema. You can call them ad hoc or attach them to a table on a schedule. Handy for checking the data you feed into AI functions.

| DMF | Measures |
| --- | --- |
| `NULL_COUNT`, `NULL_PERCENT` | Missing values |
| `DUPLICATE_COUNT`, `UNIQUE_COUNT` | Duplicates / distinct values |
| `ROW_COUNT` | Rows in a table |
| `FRESHNESS` | How recent the data is |
| `BLANK_COUNT`, `UNTRIMMED_STRING_COUNT` | Empty or whitespace-padded text |
| `STRING_LENGTH_MAX/MIN/AVG` | Text length (useful for chunk and token limits) |
| `ACCEPTED_VALUES`, `INVALID_JSON_COUNT`, `NEGATIVE_COUNT`, `OUTLIER_COUNT` | Domain checks |

```sql
SELECT SNOWFLAKE.CORE.NULL_COUNT(SELECT amount FROM orders);          -- 1
SELECT SNOWFLAKE.CORE.DUPLICATE_COUNT(SELECT customer FROM orders);
SELECT SNOWFLAKE.CORE.ROW_COUNT(SELECT * FROM orders);                -- 5
SELECT SNOWFLAKE.CORE.STRING_LENGTH_MAX(SELECT customer FROM orders);
```

The exact argument forms vary a little by function (some take a column list, some a whole table). The examples assume `orders` is a real table; DMFs are meant for permanent tables, so recreate the sample as a normal table if a call on the temp table fails. Check the reference for the specific DMF before attaching it with `ALTER TABLE ... ADD DATA METRIC FUNCTION`.

---

## 17. System functions worth knowing

Only the handful you may realistically type. The full `SYSTEM$` list is mostly administration.

| Function | Use |
| --- | --- |
| `SYSTEM$CLUSTERING_INFORMATION('table', '(col)')` | How well a table is clustered on a key |
| `SYSTEM$CANCEL_QUERY('query_id')` | Stop a running query |
| `SYSTEM$ESTIMATE_QUERY_ACCELERATION('query_id')` | Would query acceleration help this query? |
| `SYSTEM$PIPE_STATUS('pipe')` | Snowpipe health and backlog |
| `SYSTEM$STREAM_HAS_DATA('stream')` | Does a stream have changes? (used in task `WHEN`) |
| `SYSTEM$TYPEOF(x)` | The exact data type of an expression |
| `SYSTEM$WAIT(seconds)` | Pause, for tests |
| `SYSTEM$GET_TAG('tag', 'object', 'domain')` | Read a tag value |
| `GET_DDL('type', 'name')` | DDL text for an object |

```sql
SELECT SYSTEM$CLUSTERING_INFORMATION('MY_DB.MY_SCHEMA.EVENTS', '(event_date)');
SELECT SYSTEM$TYPEOF(1.5::NUMBER(10,2));
SELECT SYSTEM$CANCEL_QUERY('01b2c3d4-0000-1111-2222-333344445555');   -- replace with a real id
SELECT SYSTEM$STREAM_HAS_DATA('MY_DB.MY_SCHEMA.ORDERS_STREAM');
SELECT GET_DDL('TABLE', 'MY_DB.MY_SCHEMA.ORDERS');

-- Run a task only when the stream has changes
-- CREATE TASK t WAREHOUSE = wh SCHEDULE = '5 MINUTE'
--   WHEN SYSTEM$STREAM_HAS_DATA('ORDERS_STREAM') AS INSERT INTO ...;
```

---

## 18. Geospatial in five lines

The page lists about 100 geospatial functions (`ST_*`, `H3_*`). These are the ones to recognise.

```sql
SELECT ST_MAKEPOINT(151.2093, -33.8688);                                   -- a point (longitude first!)
SELECT ST_DISTANCE(ST_MAKEPOINT(151.2093, -33.8688), ST_MAKEPOINT(144.9631, -37.8136));   -- metres, Sydney to Melbourne
SELECT HAVERSINE(-33.8688, 151.2093, -37.8136, 144.9631);                  -- kilometres (latitude first)
SELECT ST_DWITHIN(ST_MAKEPOINT(151.2, -33.9), ST_MAKEPOINT(151.3, -33.9), 20000);   -- within 20 km?
SELECT H3_LATLNG_TO_CELL_STRING(-33.8688, 151.2093, 8);                    -- H3 cell id at resolution 8
```

**Trap:** `ST_MAKEPOINT` takes **longitude then latitude**, while `HAVERSINE` and `H3_LATLNG_TO_CELL` take **latitude then longitude**.

---

## 19. Not covered, and where to look

| Area on the page | Why skipped | Where |
| --- | --- | --- |
| Information Schema (replication, listings, dynamic table graphs, and so on) | Operations/admin | [functions-all](https://docs.snowflake.com/en/sql-reference/functions-all) |
| `SYSTEM$` private link, CMK, OAuth, behavior-change bundles and so on | Account administration | Same |
| Encryption (`ENCRYPT`, `DECRYPT`, `*_RAW`) | Niche | Reference pages |
| Differential privacy (`DP_INTERVAL_*`) | Niche | Reference pages |
| Bitwise (`BITAND`, `BITOR`, `BITMAP_*`) | Niche | Reference pages |
| Model monitor, organization user, Snowpark Container Services functions | Specialised | Reference pages |
| `XMLGET`, `PARSE_XML` | XML is rare | Reference pages |
| Agent helpers (`AGENT_RUN`, `DATA_AGENT_RUN`, `THREAD_MESSAGES`) | Agent runtime | See the course companion and AI deep dive |

## Ten you should be able to write from memory

```sql
SELECT * FROM t QUALIFY ROW_NUMBER() OVER (PARTITION BY k ORDER BY ts DESC) = 1;   -- latest row per key
SELECT TRY_CAST(col AS INT) FROM t;                                                -- safe conversion
SELECT v:a.b[0]::STRING FROM t;                                                    -- JSON path
SELECT f.value FROM t, LATERAL FLATTEN(input => t.arr) f;                          -- explode an array
SELECT DATE_TRUNC('month', d), COUNT_IF(status = 'x') FROM t GROUP BY 1;           -- monthly count
SELECT DIV0(a, b), COALESCE(x, 0), NULLIF(y, '') FROM t;                           -- NULL and zero guards
SELECT LISTAGG(col, ', ') WITHIN GROUP (ORDER BY col) FROM t;                      -- ordered concatenation
SELECT SPLIT_PART(s, ',', 2) FROM t;                                               -- 1-based
SELECT VECTOR_COSINE_SIMILARITY(a, b) FROM t ORDER BY 1 DESC LIMIT 5;              -- nearest neighbours
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));                                 -- re-query last result
```
