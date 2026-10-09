# Microsoft Fabric T-SQL functions: AI functions plus the ones worth knowing

Scope: **Fabric Data Warehouse** and the **SQL analytics endpoint** of a Lakehouse (both "Warehouse" below). Where behavior differs for **SQL database in Fabric** (the OLTP engine, same as Azure SQL Database), the file says so, because several functions you read about in generic T-SQL docs **do not exist in the Warehouse**.

Sources, read in full on 2026-10-09: [AI functions (T-SQL, Fabric)](https://learn.microsoft.com/en-us/sql/t-sql/functions/ai-functions-transact-sql?view=fabric), [T-SQL functions (Fabric)](https://learn.microsoft.com/en-us/sql/t-sql/functions/functions?view=fabric), the nine individual AI function pages, [AI functions in Fabric Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/ai-functions), [T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area), and the pages for `MEDIAN`, `QUANTILE`, `QUALIFY`, `GROUP BY`, `GENERATE_SERIES`, `STRING_AGG`, `DATETRUNC`, JSON, aggregate, analytic and vector functions.

**How to read it.** Examples were taken or adapted from those pages and **have not been executed in a Fabric workspace**. The "Fabric" column in the tables uses two labels: **✓ verified** means the function's own reference page lists the Warehouse/SQL analytics endpoint as applicable; **standard** means it is ordinary T-SQL I did not individually check against Fabric, so confirm on first use.

## Contents

1. [Where each function runs (read this first)](#1-where-each-function-runs-read-this-first)
2. [AI functions](#2-ai-functions)
3. [Fabric-only additions: `MEDIAN`, `QUANTILE`, `QUALIFY`, `GROUP BY ALL`](#3-fabric-only-additions)
4. [Conditional and NULL handling](#4-conditional-and-null-handling)
5. [Conversion](#5-conversion)
6. [Date and time](#6-date-and-time)
7. [String](#7-string)
8. [JSON](#8-json)
9. [Aggregate](#9-aggregate)
10. [Analytic, ranking and windows](#10-analytic-ranking-and-windows)
11. [Math and rowset functions](#11-math-and-rowset-functions)
12. [System, metadata and security](#12-system-metadata-and-security)
13. [Not available in the Warehouse](#13-not-available-in-the-warehouse)
14. [Ten you should be able to write from memory](#14-ten-you-should-be-able-to-write-from-memory)

**Sample table** used below (create in a Warehouse; the SQL analytics endpoint is read-only for tables):

```sql
CREATE TABLE dbo.orders
(
    order_id   INT,
    customer   VARCHAR(50),
    country    VARCHAR(2),
    order_date DATE,
    amount     DECIMAL(10,2),
    status     VARCHAR(20)
);

INSERT INTO dbo.orders VALUES
 (1, 'alice', 'AU', '2026-10-01', 120.50, 'shipped'),
 (2, 'bob',   'AU', '2026-10-02',  80.00, 'shipped'),
 (3, 'alice', 'NZ', '2026-10-05', 200.00, 'returned'),
 (4, 'carol', 'US', '2026-10-06', NULL,   'pending'),
 (5, 'bob',   'AU', '2026-10-09',  45.25, 'shipped');
```

---

## 1. Where each function runs (read this first)

The generic Microsoft docs describe T-SQL across SQL Server, Azure SQL, Synapse and Fabric. These are **different engines**. The exam-style trap is assuming a function works because it is "T-SQL".

| Capability | Warehouse and SQL analytics endpoint | SQL database in Fabric (and Azure SQL DB) |
| --- | --- | --- |
| `AI_ANALYZE_SENTIMENT`, `AI_CLASSIFY`, `AI_EXTRACT`, `AI_FIX_GRAMMAR`, `AI_GENERATE_RESPONSE`, `AI_SUMMARIZE`, `AI_TRANSLATE` | **Yes** (preview) | No |
| `AI_GENERATE_CHUNKS`, `AI_GENERATE_EMBEDDINGS` | **No** | **Yes** (needs an external model) |
| `VECTOR` data type, `VECTOR_DISTANCE`, `VECTOR_SEARCH`, `VECTOR_NORM`, `VECTOR_NORMALIZE`, `VECTORPROPERTY` | **No** ("the vector data type isn't supported") | **Yes** |
| `REGEXP_LIKE` and the other `REGEXP_*` functions | **Not listed as applying** | Yes (compatibility level 170) |
| `MEDIAN`, `QUANTILE`, `APPROX_MEDIAN`, `APPROX_QUANTILE` | **Yes (Fabric only)** | **No** ("not supported in ... SQL database in Fabric") |
| `QUALIFY`, `GROUP BY ALL` (no column list), `FROM`-first syntax | **Yes** | Different `GROUP BY ALL` meaning |
| `DATETRUNC`, `GENERATE_SERIES`, `STRING_AGG`, JSON functions | Yes ✓ | Yes |
| Triggers, synonyms, materialized views, recursive queries, `FOR XML`, `PREDICT`, `SET ROWCOUNT` | **Not supported** | Mostly yes |

So for **embeddings and vector search in Fabric**, the Warehouse is the wrong place at the moment: use SQL database in Fabric (T-SQL `AI_GENERATE_EMBEDDINGS` and `VECTOR`), or a Fabric Lakehouse with Spark, or an external service.

---

## 2. AI functions

Built-in functions that call an AI model from inside T-SQL. **Preview** in the Warehouse and SQL analytics endpoint.

| Function | Syntax | Returns | Task |
| --- | --- | --- | --- |
| `AI_ANALYZE_SENTIMENT` | `(text)` | `nvarchar`: `positive`, `negative`, `mixed`, `neutral` | Sentiment |
| `AI_CLASSIFY` | `(text, class1, class2 [, ...n])` | `nvarchar`: the chosen label | One label from your list |
| `AI_EXTRACT` | `(text, class1, class2 [, ...n])` | `nvarchar(max)`: JSON | Pull named properties |
| `AI_FIX_GRAMMAR` | `(text)` | `nvarchar(max)` | Correct grammar |
| `AI_GENERATE_RESPONSE` | `(prompt [, data])` | `nvarchar(max)` | General generation |
| `AI_SUMMARIZE` | `(text)` | `nvarchar` | Summary |
| `AI_TRANSLATE` | `(text, lang_code)` | `nvarchar(max)` | Translate to a target language |

Every one accepts an optional trailing `(NULL | ERROR | DEFAULT <value>) ON ERROR`.

### Prerequisites and limits

- A **paid Fabric capacity** (F2 or higher, or any P edition). Trial capacity is not listed.
- The tenant admin must enable the tenant switch for **Copilot and other features powered by Azure OpenAI**, and cross-geo processing if your region needs it. Only **supported regions** work.
- The functions call an external model, so they are slow per row: the tutorial quotes about **20-100 rows per second** and the remarks about **10-30 values per second**. Precompute results into a column or staging table instead of recomputing in every `SELECT`.
- Input limit: **the pages disagree.** Each function page says the model supports up to **15 KB** of text per value; the tutorial page says **99 KB**. Plan for 15 KB until Microsoft reconciles them.
- `AI_TRANSLATE` supports exactly these codes: `de`, `en`, `fr`, `it`, `es`, `el`, `pl`, `sv`, `fi`, `cs`.

### Examples

```sql
-- Sentiment
SELECT AI_ANALYZE_SENTIMENT('This hotel was great!') AS sentiment;          -- positive

-- Classification: ONE label from the list
SELECT AI_CLASSIFY('Room was dirty', 'service', 'dirt', 'food') AS classification;   -- dirt

-- Extraction: returns JSON text
SELECT AI_EXTRACT('Check-in was late and room dirty', 'sentiment', 'problem') AS extraction;
-- {"sentiment":"Negative","problem":"Dirty room"}

-- Summarize
SELECT AI_SUMMARIZE('The hotel was clean and staff were friendly.') AS summary;     -- Clean hotel, friendly staff.

-- Generate: the prompt, then optional data it should work on
SELECT AI_GENERATE_RESPONSE('Reply in 20 words:', 'The room was noisy.') AS response;

-- Translate: a code, not a language name
SELECT AI_TRANSLATE('The hotel was great', 'de') AS translation_de;                -- Das Hotel war großartig.

-- Fix grammar
SELECT AI_FIX_GRAMMAR('Th room are clean and staff were nice') AS fixed_text;
-- The rooms are clean, and the staff were nice.
```

### Error handling: `ON ERROR`

By default a failing value returns **`NULL`** and the query continues. Reasons include Responsible AI blocking the text, input over the token limit, or a transient service problem.

```sql
SELECT order_id,
       AI_FIX_GRAMMAR(status NULL ON ERROR)                                  AS fixed_text,   -- default, optional
       AI_EXTRACT(status, 'sentiment', 'problem' ERROR ON ERROR)             AS info,         -- whole query fails on any error
       AI_CLASSIFY(status, 'service', 'dirt', 'food' DEFAULT 'Other' ON ERROR) AS category    -- 'Other' instead of NULL
FROM dbo.orders;
```

| Clause | On a failed value |
| --- | --- |
| `NULL ON ERROR` (default) | Returns `NULL` |
| `ERROR ON ERROR` | Fails the entire query |
| `DEFAULT <value> ON ERROR` | Returns your default |

### Patterns from the docs

```sql
-- Enrich while loading: OPENROWSET reads a Lakehouse file, AI functions add columns (CTAS)
CREATE TABLE HotelDW.dbo.hotel_reviews
AS
SELECT
    city, name, reviews_rating, reviews_text,
    AI_SUMMARIZE(reviews_text)                                   AS reviews_summary,
    AI_CLASSIFY(reviews_text, 'service', 'dirt', 'food', 'air conditioning', 'other') AS reviews_classification,
    AI_ANALYZE_SENTIMENT(reviews_text)                           AS reviews_sentiment,
    AI_TRANSLATE(reviews_text, 'de')                             AS reviews_text_de
FROM OPENROWSET( BULK '/Files/csv/hotel_reviews_demo.csv', DATA_SOURCE = 'TextLakehouse', HEADER_ROW = TRUE);

-- Never overwrite good text with NULL when the model fails
UPDATE HotelDW.dbo.hotel_reviews
SET reviews_text = ISNULL(AI_FIX_GRAMMAR(reviews_text), reviews_text);

-- Turn the JSON from AI_EXTRACT into columns
SELECT sentiment, time_reported, problem
FROM hotel_reviews
CROSS APPLY OPENJSON(AI_EXTRACT(reviews_text, 'sentiment', 'time_reported', 'problem'))
     WITH (sentiment VARCHAR(1000), time_reported VARCHAR(100), problem VARCHAR(1000));
```

**Exam traps:**
- `AI_CLASSIFY` returns **one** label (no multi-label, no confidence score). `AI_EXTRACT` takes **property names**, not questions, and returns **JSON**, so combine it with `OPENJSON` or `JSON_VALUE`.
- `AI_TRANSLATE` takes a **code** (`'de'`), has **no source-language argument**, and supports only ten languages.
- There is **no document, image, or audio** function and **no embeddings** function in the Warehouse. Text only.
- Always check for `NULL`; wrap updates in `ISNULL(ai_function(...), original)`.
- AI functions are **per row** and see only the values you pass. They cannot aggregate across a table, so never use them for medians, sums or counts (see the worked example below); use `MEDIAN`, `QUANTILE` and the other aggregates, then pass the result as text.

### Don't use an AI function for a calculation (worked example)

A real mistake: asking the model for a median over a table.

```sql
-- WRONG: runs once PER ROW, and each call sees only that row's value
SELECT AI_GENERATE_RESPONSE('what is the median Price', [sale_price_aud])
FROM [dbo].[gld_market_sale];
```

Why it fails:

| Problem | Detail |
| --- | --- |
| **No table-wide view** | `AI_GENERATE_RESPONSE(prompt, data)` is a scalar function. The `data` argument is that one row's value, so the model can never see the other prices and cannot compute a median |
| **Cost and speed** | One external model call per row, at roughly 10-100 rows per second. A large table means a long, billable query for a meaningless result |
| **Wrong data type** | `data` is documented as text. A numeric column may raise an error or, under the default `NULL ON ERROR`, silently return `NULL` |
| **Wrong tool** | An LLM is not a reliable calculator. Even with every number in the prompt it can return a plausible but wrong answer |
| **Square brackets** | `[sale_price_aud]` is just a T-SQL **delimited identifier** (a column), not an array of values |

Use the aggregates built for it. `MEDIAN` and `QUANTILE` are Fabric-only (section 3) and are exact:

```sql
-- Exact median of the whole column
SELECT MEDIAN(sale_price_aud) AS median_price
FROM dbo.gld_market_sale;

-- QUANTILE(p, column): the median plus other percentiles in one pass
SELECT QUANTILE(0.5, sale_price_aud) AS median_price,
       QUANTILE(0.9, sale_price_aud) AS p90_price
FROM dbo.gld_market_sale;

-- Per group (suburb is a hypothetical column), or the group median beside every row
SELECT suburb, MEDIAN(sale_price_aud) AS median_price
FROM dbo.gld_market_sale
GROUP BY suburb;

SELECT *, MEDIAN(sale_price_aud) OVER (PARTITION BY suburb) AS suburb_median
FROM dbo.gld_market_sale;
```

Both return `NULL` if every value is `NULL`, need a numeric column, and do not support `DISTINCT`.

**If you want the model to comment on a number, compute the number first, then pass it as text.** Do the arithmetic in SQL and let the model do the language:

```sql
WITH stats AS (
    SELECT suburb,
           MEDIAN(sale_price_aud)                AS median_price,
           COUNT(*)                              AS sales
    FROM dbo.gld_market_sale
    GROUP BY suburb
)
SELECT suburb,
       median_price,
       AI_GENERATE_RESPONSE(
           'In one sentence, describe this suburb market for a buyer:',
           CONCAT('Suburb: ', suburb,
                  '. Median sale price AUD: ', CAST(median_price AS VARCHAR(20)),
                  '. Number of sales: ', CAST(sales AS VARCHAR(10)))
           NULL ON ERROR) AS commentary
FROM stats;                                    -- one model call per SUBURB, not per sale
```

Rule of thumb: **SQL for numbers, AI functions for text.** Aggregate down to few rows *before* calling an AI function, and always cast non-text values to text for the `data` argument.

### In SQL database in Fabric: chunking and embeddings

Different engine, different functions. They need a **registered external model** and the `external rest endpoint` option (on by default in SQL database in Fabric and Azure SQL Database).

```sql
-- Chunk text: FIXED type, size in CHARACTERS, OVERLAP is a PERCENT (0 to 50)
SELECT c.chunk, c.chunk_order, c.chunk_offset, c.chunk_length
FROM docs_table AS t
CROSS APPLY AI_GENERATE_CHUNKS (SOURCE = t.text_column, CHUNK_TYPE = FIXED, CHUNK_SIZE = 100, OVERLAP = 10) AS c;

-- Register an embedding model (Azure OpenAI shown), then embed each chunk into a VECTOR column
CREATE EXTERNAL MODEL MyAzureOpenAIModel
WITH (
      LOCATION = 'https://my-azure-openai-endpoint.cognitiveservices.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15',
      API_FORMAT = 'Azure OpenAI',
      MODEL_TYPE = EMBEDDINGS,
      MODEL = 'text-embedding-ada-002',
      CREDENTIAL = [https://my-azure-openai-endpoint.cognitiveservices.azure.com/]
);

INSERT INTO text_embeddings (chunked_text, vector_embeddings)
SELECT c.chunk,
       AI_GENERATE_EMBEDDINGS(c.chunk USE MODEL MyAzureOpenAIModel)
FROM textchunk AS t
CROSS APPLY AI_GENERATE_CHUNKS (SOURCE = t.text_to_chunk, CHUNK_TYPE = FIXED, CHUNK_SIZE = 100) AS c;
```

`AI_GENERATE_CHUNKS` needs database compatibility level **170** and returns `chunk`, `chunk_order`, `chunk_offset`, `chunk_length` (plus `chunk_set_id` when `ENABLE_CHUNK_SET_ID = 1`). `AI_GENERATE_EMBEDDINGS` returns a JSON array of floats per row; pass `PARAMETERS` to override model settings such as `dimensions` or `retry_count` (0 to 10).

---

## 3. Fabric-only additions

These are **not** in SQL Server or Azure SQL, so they are easy exam distractors and handy shortcuts.

| Feature | What it does | Trap |
| --- | --- | --- |
| `MEDIAN(x)` | **Exact** median (continuous 50th percentile); aggregate or windowed | Equivalent to `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)`; interpolates for an even count; no `DISTINCT`; numeric types only; returns `float(53)` |
| `QUANTILE(p, x)` | **Exact** continuous quantile, `p` from 0.0 to 1.0 | Same as `PERCENTILE_CONT(p)`; `p` first, column second |
| `APPROX_MEDIAN`, `APPROX_QUANTILE` | Approximate versions | **Nondeterministic**; cheaper on large data |
| `QUALIFY` | Filter on a window function result without a subquery | The predicate **must contain a window function**; not allowed in `UPDATE` or `DELETE` |
| `GROUP BY ALL` | Group by every non-aggregated `SELECT` column | Adding a column to `SELECT` silently changes the grouping; use `ANY_VALUE` to carry extra columns |
| `FROM`-first syntax | `FROM t SELECT ...` | Alternative ordering only |
| `ORDER BY ALL` | Order by all select columns | |

```sql
-- MEDIAN: even count, so it interpolates between 4 and 5
SELECT MEDIAN(value) AS MedianValue
FROM (VALUES (1), (2), (3), (4), (5), (6), (7), (8)) AS t(value);          -- 4.5

-- MEDIAN per group, and as a window
SELECT customer, MEDIAN(amount) AS median_amount FROM dbo.orders GROUP BY customer;
SELECT order_id, amount, MEDIAN(amount) OVER (PARTITION BY customer) AS customer_median FROM dbo.orders;

-- QUANTILE: quartiles and P95 in one pass (NULLs ignored)
WITH Samples AS (SELECT * FROM (VALUES (1), (NULL), (2), (3), (4), (5), (6), (7), (8), (13)) AS v(value))
SELECT QUANTILE(0.25, value) AS Q1,
       QUANTILE(0.50, value) AS Median,
       QUANTILE(0.75, value) AS Q3,
       QUANTILE(0.95, value) AS P95
FROM Samples;

-- QUALIFY: top-priced product per colour, no subquery
SELECT *
FROM (VALUES ('Red', 'Road Bike', 1200.00), ('Red', 'City Bike', 800.00),
             ('Blue', 'Mountain Bike', 1500.00), ('Blue', 'Road Bike', 1100.00)) AS Source (Color, Product, Price)
QUALIFY ROW_NUMBER() OVER (PARTITION BY Color ORDER BY Price DESC) = 1;

-- QUALIFY using an alias from the SELECT list: top 3 per category
SELECT ProductSubcategoryID, ProductID, ListPrice,
       ROW_NUMBER() OVER (PARTITION BY ProductSubcategoryID ORDER BY ListPrice DESC, ProductID) AS rn
FROM Production.Product
QUALIFY rn <= 3;

-- GROUP BY ALL
SELECT Region, Territory, SUM(Sales) AS TotalSales
FROM Sales
GROUP BY ALL;
```

**Evaluation order with `QUALIFY`:** `FROM` → `WHERE` → `GROUP BY` → `HAVING` → window functions → `QUALIFY` → `ORDER BY`. A window function in `WHERE` is an error; use `QUALIFY`.

---

## 4. Conditional and NULL handling

| Function | What it does | Fabric | Trap |
| --- | --- | --- | --- |
| `ISNULL(a, b)` | Replace NULL | standard | Result takes the type of the **first** argument (can truncate) |
| `COALESCE(a, b, ...)` | First non-NULL | standard | Takes the type of highest precedence |
| `NULLIF(a, b)` | NULL if equal | standard | Guard against divide by zero |
| `IIF(cond, a, b)` | Inline if/else | ✓ verified | Shorthand for `CASE`; false **and unknown** return `b`; nests to 10 levels; `IIF(cond, NULL, NULL)` is an error |
| `CHOOSE(n, a, b, ...)` | Pick by 1-based index | standard | Out of range returns NULL |
| `CASE` | Branching | ✓ | No `ELSE` returns NULL |
| `GREATEST`, `LEAST` | Max/min across columns | standard | Confirm on first use |

```sql
SELECT order_id,
       ISNULL(amount, 0)                              AS amount_filled,
       COALESCE(amount, 0)                            AS amount_coalesce,
       IIF(amount >= 100, 'large', 'small')           AS size,        -- NULL amount -> 'small'
       CHOOSE(2, 'a', 'b', 'c')                       AS second,      -- b
       10 / NULLIF(order_id - 3, 0)                   AS safe_div,    -- order 3 -> NULL, not an error
       CASE WHEN status = 'shipped' THEN 'done'
            WHEN status = 'returned' THEN 'problem'
            ELSE 'open' END                           AS stage
FROM dbo.orders;
```

---

## 5. Conversion

| Function | Use | Trap |
| --- | --- | --- |
| `CAST(x AS type)` | ANSI conversion | Errors on bad input |
| `CONVERT(type, x [, style])` | T-SQL conversion with a style code | Style `23` is `yyyy-mm-dd`, `126` is ISO 8601 |
| `TRY_CAST`, `TRY_CONVERT` | NULL instead of an error | Use on dirty data and during CTAS loads |
| `FORMAT(x, fmt [, culture])` | Locale-aware text | **Nondeterministic and slow**; avoid on big tables |

```sql
SELECT CAST('42' AS INT) + 1;                        -- 43
SELECT TRY_CAST('abc' AS INT);                       -- NULL, no error
SELECT TRY_CONVERT(DATE, '2026-13-45');              -- NULL
SELECT CONVERT(VARCHAR(10), CAST('2026-10-09' AS DATE), 23);   -- 2026-10-09
```

---

## 6. Date and time

The list comes from the generic T-SQL date page. `DATETRUNC` is individually confirmed for the Warehouse; treat the rest as **standard** (they are core T-SQL) and confirm on first use.

| Function | Use | Trap |
| --- | --- | --- |
| `GETDATE()`, `SYSDATETIME()`, `SYSUTCDATETIME()`, `GETUTCDATE()`, `CURRENT_TIMESTAMP`, `CURRENT_DATE` | Now | `GETDATE` is `datetime`; `SYSDATETIME` is `datetime2(7)`; the `UTC` variants return UTC |
| `DATEADD(part, n, d)` | Add an interval | Part first |
| `DATEDIFF(part, start, end)`, `DATEDIFF_BIG` | Count boundaries crossed | `DATEDIFF` returns `int` and overflows on fine units; use `_BIG` |
| `DATETRUNC(part, d)` ✓ | Truncate to a part | `week` start follows `@@DATEFIRST` (Sunday by default in US English); `iso_week` starts Monday; `weekday`, `tzoffset`, `nanosecond` unsupported |
| `DATE_BUCKET(part, n, d [, origin])` | Start of an n-unit bucket | Default origin is `1900-01-01` (a Monday) |
| `DATEPART`, `DATENAME`, `DAY`, `MONTH`, `YEAR` | Extract parts | `DATENAME` returns text |
| `DATEFROMPARTS`, `DATETIME2FROMPARTS`, `TIMEFROMPARTS` ... | Build from numbers | |
| `EOMONTH(d [, n])` | Last day of a month | Optional month offset |
| `SWITCHOFFSET`, `TODATETIMEOFFSET` | Change or attach a UTC offset | For `datetimeoffset` values |
| `ISDATE(x)` | Validate | |

```sql
SELECT DATEADD(day, 7, CAST('2026-10-09' AS DATE));                   -- 2026-10-16
SELECT DATEDIFF(day, '2026-10-01', '2026-10-09');                      -- 8
SELECT DATEDIFF(month, '2026-01-31', '2026-02-01');                    -- 1  (one month boundary crossed)
SELECT DATETRUNC(month, CAST('2026-10-09' AS DATE));                   -- 2026-10-01
SELECT DATETRUNC(iso_week, CAST('2026-10-09' AS DATE));                -- 2026-10-05 (Monday)
SELECT DATE_BUCKET(week, 1, CAST('2026-10-09' AS DATE));               -- 2026-10-05 with the default origin
SELECT EOMONTH('2026-02-10');                                          -- 2026-02-28
SELECT DATEFROMPARTS(2026, 10, 9);
SELECT DATENAME(weekday, '2026-10-09'), DATEPART(quarter, '2026-10-09');   -- Friday, 4

-- Monthly revenue
SELECT DATETRUNC(month, order_date) AS month, SUM(amount) AS revenue
FROM dbo.orders
GROUP BY DATETRUNC(month, order_date)
ORDER BY month;

-- GENERATE_SERIES gives a number list; turn it into a calendar spine
SELECT DATEADD(day, value, CAST('2026-10-01' AS DATE)) AS d
FROM GENERATE_SERIES(0, 9);
```

---

## 7. String

| Function | Use | Fabric | Trap |
| --- | --- | --- | --- |
| `CONCAT`, `CONCAT_WS(sep, ...)`, `+` | Join | standard | `+` returns NULL if any input is NULL; `CONCAT` treats NULL as empty |
| `STRING_AGG(x, sep) [WITHIN GROUP (ORDER BY ...)]` | Rows to one string | ✓ verified | Skips NULLs; **not allowed with `OVER`**; non-string input becomes `nvarchar(4000)` unless you cast to `MAX` |
| `STRING_SPLIT(s, sep)` | One row per piece | standard | Returns a table with a `value` column |
| `SUBSTRING(s, start, len)`, `LEFT`, `RIGHT` | Slice | standard | 1-based; `SUBSTRING` requires the length |
| `CHARINDEX(find, s)`, `PATINDEX('%pat%', s)` | Find | standard | Returns 0 if not found; `PATINDEX` takes `LIKE`-style wildcards |
| `TRIM`, `LTRIM`, `RTRIM` | Strip | standard | |
| `REPLACE`, `TRANSLATE`, `STUFF` | Replace | standard | `TRANSLATE` swaps characters one-for-one |
| `UPPER`, `LOWER`, `LEN`, `DATALENGTH`, `REVERSE`, `REPLICATE`, `FORMAT` | Basics | standard | `LEN` ignores trailing spaces; `DATALENGTH` counts bytes |
| `REGEXP_*` | Regular expressions | **Not for the Warehouse** | Available in SQL database in Fabric (compat level 170). Use `LIKE`, `PATINDEX` or `AI_EXTRACT` instead |

```sql
SELECT CONCAT_WS('-', 'a', NULL, 'c');                       -- a-c   (NULL skipped)
SELECT 'a' + NULL;                                           -- NULL
SELECT SUBSTRING('snowflake', 1, 4);                         -- snow
SELECT CHARINDEX('flake', 'snowflake');                      -- 5
SELECT TRANSLATE('2*3+4', '*+', 'x-');                       -- 2x3-4
SELECT value FROM STRING_SPLIT('a,b,c', ',');                -- three rows

-- STRING_AGG, ordered, per customer (GROUP BY required)
SELECT customer,
       STRING_AGG(CONVERT(NVARCHAR(MAX), status), ', ') WITHIN GROUP (ORDER BY order_date) AS statuses
FROM dbo.orders
GROUP BY customer;

-- NULLs are ignored; use ISNULL for a placeholder
SELECT STRING_AGG(CONVERT(NVARCHAR(MAX), ISNULL(amount, 0)), ',') FROM dbo.orders;
```

---

## 8. JSON

All of these list the Warehouse and SQL analytics endpoint as applicable.

| Function | Use | Trap |
| --- | --- | --- |
| `ISJSON(s)` | Is it valid JSON? | Returns 1/0/NULL |
| `JSON_VALUE(s, path)` | One **scalar** | Returns NULL on a missing path; returns NULL (lax mode) if the value is an object or array |
| `JSON_QUERY(s, path)` | An **object or array** | Use this, not `JSON_VALUE`, for nested JSON |
| `JSON_MODIFY(s, path, v)` | Update a property | Returns the new JSON; does not change the source |
| `JSON_PATH_EXISTS(s, path)` | Does the path exist? | |
| `OPENJSON(s [, path]) [WITH (...)]` | JSON to rows and columns | Use `WITH` to type columns; combine with `CROSS APPLY` |
| `JSON_OBJECT('k': v, ...)`, `JSON_ARRAY(v, ...)` | Build JSON | |
| `JSON_OBJECTAGG`, `JSON_ARRAYAGG` | Aggregate rows into JSON | |
| `FOR JSON` | Query result to JSON | **Must be the last operator**; cannot be used in a subquery in the Warehouse |

```sql
DECLARE @j NVARCHAR(MAX) = N'{"user":{"name":"alice","tags":["a","b"]},"items":[{"sku":"X1","qty":2},{"sku":"Y2","qty":5}]}';

SELECT ISJSON(@j)                              AS valid,        -- 1
       JSON_VALUE(@j, '$.user.name')           AS name,         -- alice
       JSON_VALUE(@j, '$.items[1].qty')        AS qty,          -- 5   (text; CAST if you need a number)
       JSON_QUERY(@j, '$.user.tags')           AS tags,         -- ["a","b"]
       JSON_PATH_EXISTS(@j, '$.user.email')    AS has_email;    -- 0

-- Explode an array into rows with typed columns
SELECT * FROM OPENJSON(@j, '$.items') WITH (sku VARCHAR(10) '$.sku', qty INT '$.qty');

-- Update
SELECT JSON_MODIFY(@j, '$.user.name', 'bob');

-- Construct
SELECT JSON_OBJECT('id': 1, 'name': 'alice') AS obj, JSON_ARRAY(1, 2, 3) AS arr;
SELECT customer, SUM(amount) AS total FROM dbo.orders GROUP BY customer FOR JSON PATH;   -- last operator
```

---

## 9. Aggregate

Rules that apply to all: aggregates **ignore NULLs** (except `COUNT(*)`); they are allowed in the select list and `HAVING`; `OVER` can follow all of them **except** `STRING_AGG`, `GROUPING` and `GROUPING_ID`.

| Function | Use | Trap |
| --- | --- | --- |
| `COUNT(*)`, `COUNT(col)`, `COUNT_BIG` | Row / non-NULL count | `COUNT` returns `int`; `COUNT_BIG` returns `bigint` |
| `SUM`, `AVG`, `MIN`, `MAX`, `PRODUCT` | Basics | Integer `AVG` truncates; cast to decimal |
| `ANY_VALUE(x)` | One arbitrary value | Avoids adding columns to `GROUP BY` |
| `APPROX_COUNT_DISTINCT(x)` | Fast distinct count | Approximate |
| `MEDIAN`, `QUANTILE` | Exact median/quantile | Fabric only |
| `APPROX_MEDIAN`, `APPROX_QUANTILE`, `APPROX_PERCENTILE_CONT/DISC` | Approximate percentiles | Nondeterministic |
| `PERCENTILE_CONT(p) WITHIN GROUP (ORDER BY x)` | Interpolated percentile | SQL Server needs `OVER (...)`; Fabric's aggregate list also names it, so confirm which form your item accepts. `QUANTILE`/`MEDIAN` are the simpler Fabric route |
| `STDEV`, `STDEVP`, `VAR`, `VARP` | Statistics | Sample versus population |
| `STRING_AGG`, `JSON_ARRAYAGG`, `JSON_OBJECTAGG` | Collect rows | |
| `GROUPING`, `GROUPING_ID`, `ROLLUP`, `CUBE`, `GROUPING SETS` | Subtotals | `GROUPING()` separates subtotal NULLs from real NULLs |
| `CHECKSUM_AGG` | Change detection | |

```sql
SELECT COUNT(*) AS all_rows,             -- 5
       COUNT(amount) AS with_amount,     -- 4
       SUM(amount) AS total,             -- 445.75
       AVG(amount) AS avg_amount,        -- NULLs ignored
       APPROX_COUNT_DISTINCT(customer) AS customers
FROM dbo.orders;

-- Conditional count: there is no COUNT_IF, so use SUM or COUNT with CASE
SELECT SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) AS shipped,
       COUNT(CASE WHEN status = 'shipped' THEN 1 END)      AS shipped_too
FROM dbo.orders;

-- Subtotals
SELECT country, customer, SUM(amount) AS total, GROUPING(customer) AS is_subtotal
FROM dbo.orders
GROUP BY ROLLUP (country, customer);

SELECT Region, SUM(Sales) AS TotalSales FROM Sales GROUP BY GROUPING SETS (Region, ());   -- region totals + grand total
```

---

## 10. Analytic, ranking and windows

| Function | Use | Trap |
| --- | --- | --- |
| `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE(n)` | Ranking | `RANK` leaves gaps after ties; `DENSE_RANK` does not; they need `ORDER BY` |
| `LAG(x [, n [, default]])`, `LEAD(...)` | Previous/next row | NULL at the edge unless you pass a default |
| `FIRST_VALUE`, `LAST_VALUE` | First/last in the window | Default frame ends at the current row, so `LAST_VALUE` needs `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` |
| `CUME_DIST`, `PERCENT_RANK` | Relative position | |
| `PERCENTILE_CONT`, `PERCENTILE_DISC` | Window percentile | Use `OVER (PARTITION BY ...)` |
| `MEDIAN`, `QUANTILE` `OVER (PARTITION BY ...)` | Partition benchmark | `OVER` here takes **no** `ORDER BY` or frame |
| `SUM/AVG/COUNT ... OVER (... ROWS ...)` | Running and moving totals | |

```sql
-- Latest order per customer, no subquery
SELECT * FROM dbo.orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer ORDER BY order_date DESC) = 1;

-- Change versus previous order
SELECT order_id, order_date, amount,
       amount - LAG(amount) OVER (ORDER BY order_date) AS change_vs_prev
FROM dbo.orders;

-- Running total and a moving average
SELECT order_id,
       SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)         AS moving_avg_3
FROM dbo.orders;

-- Last value needs a widened frame
SELECT order_id,
       LAST_VALUE(status) OVER (PARTITION BY customer ORDER BY order_date
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS final_status
FROM dbo.orders;

-- Ranks and buckets
SELECT customer, SUM(amount) AS total,
       RANK()   OVER (ORDER BY SUM(amount) DESC) AS rnk,
       NTILE(2) OVER (ORDER BY SUM(amount) DESC) AS half
FROM dbo.orders GROUP BY customer;
```

---

## 11. Math and rowset functions

| Function | Use | Trap |
| --- | --- | --- |
| `ROUND(x, n)`, `CEILING`, `FLOOR`, `ABS`, `SIGN`, `POWER`, `SQRT`, `LOG`, `EXP`, `PI` | Maths | standard; `ROUND(x, n, 1)` truncates |
| `x % y` | Remainder | There is no `MOD()` |
| `GENERATE_SERIES(start, stop [, step])` ✓ | Number table | Column is named `value`; `start` and `stop` must be the same type; step 0 is invalid; a wrong-direction step returns no rows |
| `OPENROWSET(BULK '/Files/...', DATA_SOURCE = ..., HEADER_ROW = TRUE)` | Read Lakehouse files | Used in the AI examples |
| `OPENJSON`, `STRING_SPLIT`, table constructors `VALUES` | Rowsets | |

```sql
SELECT ROUND(2.567, 2), CEILING(2.1), FLOOR(2.9), ABS(-4), 7 % 3;        -- 2.570, 3, 2, 4, 1
SELECT value FROM GENERATE_SERIES(1, 50, 5);                              -- 1, 6, 11 ... 46
SELECT value FROM GENERATE_SERIES(0.0, 1.0, 0.1);                         -- decimal steps (declare precision for variables)
SELECT 10 / 0;                                                            -- error: divide by zero
SELECT 10 / NULLIF(0, 0);                                                 -- NULL
```

---

## 12. System, metadata and security

Standard T-SQL; confirm each in your item type.

| Function | Returns |
| --- | --- |
| `@@VERSION`, `@@SERVERNAME` | Engine version / server name |
| `DB_NAME()`, `SCHEMA_NAME()`, `OBJECT_ID('dbo.t')`, `OBJECT_NAME(id)` | Names and ids |
| `USER_NAME()`, `SUSER_SNAME()`, `IS_MEMBER('role')`, `IS_SRVROLEMEMBER` | Who you are |
| `SESSION_CONTEXT(key)` | Session values |
| `NEWID()`, `HASHBYTES('SHA2_256', x)`, `CHECKSUM(...)`, `BINARY_CHECKSUM(...)` | Ids and hashes |
| `@@ROWCOUNT`, `@@ERROR`, `TRY...CATCH` helpers such as `ERROR_MESSAGE()` | Execution state |

```sql
SELECT @@VERSION, DB_NAME(), SUSER_SNAME();
SELECT OBJECT_ID('dbo.orders');
SELECT CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'snowflake'), 2);
```

---

## 13. Not available in the Warehouse

From the T-SQL surface-area page, as of 2026-10-09. "Don't try to use these ... even if they appear to succeed, they might cause problems."

- `BULK LOAD` (`bcp` is preview) and `CREATE USER`.
- **Vector data type and search functions**, `PREDICT`.
- Triggers, synonyms, **materialized views**, **recursive queries**, manually created multi-column statistics.
- `FOR XML`; `FOR JSON` only as the last operator.
- `SET ROWCOUNT`, `SET TRANSACTION ISOLATION LEVEL`, `sp_showspaceused`.
- Schema or table names containing `/` or `\`.
- Limited `ALTER TABLE`: add **nullable** columns, drop columns, and constraints only `NOT ENFORCED`. Nested CTEs are preview.
- Tables can be created, altered or written only in a **Warehouse**, not in the SQL analytics endpoint.

Supported and worth remembering: `MERGE` (GA), `TRUNCATE TABLE`, session `#temp` tables, identity columns, CTEs, `sp_rename` for columns, `QUALIFY`, `GROUP BY ALL`, `FROM`-first syntax.

---

## 14. Ten you should be able to write from memory

```sql
SELECT AI_CLASSIFY(txt, 'service', 'dirt', 'food' DEFAULT 'other' ON ERROR) FROM t;      -- classify with a fallback
SELECT AI_TRANSLATE(txt, 'de') FROM t;                                                  -- code, no source argument
UPDATE t SET txt = ISNULL(AI_FIX_GRAMMAR(txt), txt);                                     -- never overwrite with NULL
SELECT j.* FROM t CROSS APPLY OPENJSON(AI_EXTRACT(txt, 'sentiment', 'problem')) WITH (sentiment VARCHAR(50), problem VARCHAR(200)) j;
SELECT * FROM t QUALIFY ROW_NUMBER() OVER (PARTITION BY k ORDER BY ts DESC) = 1;          -- latest per key
SELECT k, MEDIAN(x), QUANTILE(0.95, x) FROM t GROUP BY k;                                -- Fabric-only exact percentiles
SELECT DATETRUNC(month, d), COUNT(*) FROM t GROUP BY DATETRUNC(month, d);                -- monthly count
SELECT STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name) FROM t;                       -- ordered concatenation
SELECT JSON_VALUE(j, '$.a.b'), JSON_QUERY(j, '$.arr') FROM t;                            -- scalar versus object/array
SELECT DATEADD(day, value, '2026-10-01') FROM GENERATE_SERIES(0, 29);                    -- a 30-day calendar
```
