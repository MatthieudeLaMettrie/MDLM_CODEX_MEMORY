# Function reference: Fabric, Databricks, PySpark (and Snowflake)

One example-driven file per platform. Each has the **AI functions** first, then the functions worth knowing, with a trap list and "ten to write from memory". Written on 2026-10-09 from the official reference pages; examples are adapted from them and **have not been executed** in a live workspace.

| File | Platform | Covers |
| --- | --- | --- |
| [01_FABRIC_TSQL_FUNCTIONS.md](01_FABRIC_TSQL_FUNCTIONS.md) | Microsoft Fabric Warehouse and SQL analytics endpoint (T-SQL) | 7 Warehouse AI functions plus `ON ERROR`; the SQL-database-in-Fabric chunk/embedding functions; Fabric-only `MEDIAN`/`QUANTILE`/`QUALIFY`/`GROUP BY ALL`; a matrix of what does **not** run in the Warehouse (`REGEXP_*`, `VECTOR_*`, triggers ...) |
| [02_DATABRICKS_SQL_FUNCTIONS.md](02_DATABRICKS_SQL_FUNCTIONS.md) | Databricks SQL / Spark SQL | 22 AI functions (`ai_query`, `ai_classify`, `ai_extract`, `ai_parse_document`, `ai_decide`, `ai_enrich`, `ai_search`, `ai_forecast` ...), `vector_search`, plus conditional, date, string, aggregate, window, lambda, JSON/VARIANT, generators, geospatial `ST_`/H3 and sketches |
| [03_PYSPARK_FUNCTIONS.md](03_PYSPARK_FUNCTIONS.md) | PySpark on Databricks | The Python API: `F.*`, `Window`, `Column` methods, lambdas, UDFs/pandas UDFs/UDTFs, `dbf` AI and geospatial functions, NA/stat helpers, reading/writing |
| Snowflake counterparts | Snowflake | [AI functions](../snowpro-genai/09_AI_FUNCTION_EXAMPLES.md) and [SQL functions](../snowpro-genai/10_SQL_FUNCTIONS_ESSENTIALS.md) in the SnowPro Gen AI guide |

The existing [Databricks data engineering course](../databricks/README.md) teaches the platform; this folder is the function look-up that goes with it.

## Same task, four dialects

**General SQL**

| Task | Snowflake | Fabric T-SQL | Databricks SQL | PySpark |
| --- | --- | --- | --- | --- |
| Latest row per key | `QUALIFY ROW_NUMBER() OVER (...) = 1` | `QUALIFY ...` (Fabric only) | `QUALIFY ...` | `row_number().over(w)` then `filter` |
| Inline if/else | `IFF(c, a, b)` | `IIF(c, a, b)` | `if(c, a, b)` / `iff` | `F.when(c, a).otherwise(b)` |
| Replace NULL | `COALESCE`, `NVL` | `ISNULL`, `COALESCE` | `coalesce`, `nvl` | `F.coalesce` |
| Safe cast | `TRY_CAST` | `TRY_CAST`, `TRY_CONVERT` | `try_cast` | `F.expr("try_cast(..)")` |
| Safe divide | `DIV0(a, b)`, `a / NULLIF(b, 0)` | `a / NULLIF(b, 0)` | `try_divide(a, b)` | `F.try_divide` |
| Truncate date | `DATE_TRUNC('month', d)` | `DATETRUNC(month, d)` | `date_trunc('MONTH', d)` | `F.date_trunc("month", d)` |
| Date difference | `DATEDIFF(day, a, b)` | `DATEDIFF(day, a, b)` | `datediff(DAY, a, b)` or `datediff(b, a)` | `F.datediff(end, start)` |
| Add days | `DATEADD(day, n, d)` | `DATEADD(day, n, d)` | `dateadd(DAY, n, d)` / `date_add(d, n)` | `F.date_add(d, n)` |
| Calendar / number table | `TABLE(GENERATOR(ROWCOUNT => n))` + `SEQ4()` | `GENERATE_SERIES(a, b)` | `range(n)` / `sequence` + `explode` | `spark.range(n)` / `F.sequence` |
| Ordered string aggregate | `LISTAGG(x, ',') WITHIN GROUP (ORDER BY ..)` | `STRING_AGG(x, ',') WITHIN GROUP (ORDER BY ..)` | `listagg(x, ',') WITHIN GROUP (ORDER BY ..)` | `F.listagg` or SQL via `F.expr` |
| Collect rows to array | `ARRAY_AGG(x)` | no array type; `JSON_ARRAYAGG` | `collect_list(x)` / `array_agg` | `F.collect_list` |
| n-th piece of a string | `SPLIT_PART(s, d, n)` (1-based) | `STRING_SPLIT` returns rows (no `SPLIT_PART`) | `split_part(s, d, n)` (1-based) | `F.split_part` |
| Regex extract | `REGEXP_SUBSTR` | **none in the Warehouse** | `regexp_extract(s, re, idx)` | `F.regexp_extract` |
| Count rows matching a condition | `COUNT_IF(c)` | `SUM(CASE WHEN c THEN 1 ELSE 0 END)` | `count_if(c)` | `F.count_if(c)` |
| Median | `MEDIAN(x)` | `MEDIAN(x)` (Fabric only) | `median(x)` | `F.median` |
| Approximate percentile | `APPROX_PERCENTILE(x, p)` | `APPROX_QUANTILE(p, x)` | `approx_percentile(x, p)` | `F.approx_percentile` |
| Group by every non-aggregate | `GROUP BY ALL` | `GROUP BY ALL` | `GROUP BY ALL` | not applicable |
| NULL-safe equality | `EQUAL_NULL(a, b)` | none listed | `a <=> b`, `equal_null` | `c.eqNullSafe(d)` |

**Semi-structured data**

| Task | Snowflake | Fabric T-SQL | Databricks SQL | PySpark |
| --- | --- | --- | --- | --- |
| Parse a JSON string | `PARSE_JSON(s)` | keep as text; `ISJSON`, `OPENJSON` | `parse_json(s)` (VARIANT) / `from_json(s, schema)` | `F.parse_json` / `F.from_json` |
| Read a nested value | `v:a.b::STRING` | `JSON_VALUE(j, '$.a.b')` | `v:a.b::STRING` / `variant_get(v, '$.a.b', 'string')` | `F.variant_get` / `F.get_json_object` |
| Explode an array | `LATERAL FLATTEN(input => arr)` | `CROSS APPLY OPENJSON(j) WITH (...)` | `LATERAL VIEW explode(arr)` | `F.explode` |
| Array lambda | `TRANSFORM(arr, a INT -> a * 2)` | none | `transform(arr, x -> x * 2)` | `F.transform(arr, lambda x: x * 2)` |

**AI functions** (all text unless noted)

| Task | Snowflake | Fabric Warehouse | Databricks SQL |
| --- | --- | --- | --- |
| Classify | `AI_CLASSIFY(text, ['a','b'] [, config])` (object with `labels`) | `AI_CLASSIFY(text, 'a', 'b')` (one label) | `ai_classify(text, '["a","b"]', MAP('version','2.1'))` (VARIANT) |
| Extract fields | `AI_EXTRACT(text_or_file, responseFormat)` | `AI_EXTRACT(text, 'p1', 'p2')` (JSON text) | `ai_extract(text_or_variant, schema, options)` (VARIANT) |
| Sentiment | `AI_SENTIMENT(text [, categories])` (object, aspects) | `AI_ANALYZE_SENTIMENT(text)` (one label) | `ai_analyze_sentiment(text)` (one label) |
| Summarize | `AI_SUMMARIZE`, `AI_SUMMARIZE_AGG` | `AI_SUMMARIZE(text)` | `ai_summarize(text [, max_words])` |
| Translate | `AI_TRANSLATE(text, source, target)` (`''` = detect) | `AI_TRANSLATE(text, lang)` (10 codes) | `ai_translate(text, lang)` (8 languages) |
| Generate | `AI_COMPLETE(model, prompt ...)` | `AI_GENERATE_RESPONSE(prompt [, data])` | `ai_query(endpoint, request ...)`, `ai_gen` |
| Redact PII | `AI_REDACT` | none | `ai_mask(text, array('person','email'))` |
| Fix grammar | none | `AI_FIX_GRAMMAR` | `ai_fix_grammar` |
| Similarity | `AI_SIMILARITY` | none in the Warehouse | `ai_similarity` |
| Embeddings | `AI_EMBED`, `AI_MULTI_EMBED` | `AI_GENERATE_EMBEDDINGS` (**SQL database in Fabric only**) | via `ai_query` with an embedding endpoint |
| Parse documents | `AI_PARSE_DOCUMENT` | none | `ai_parse_document` |
| Transcribe audio | `AI_TRANSCRIBE` | none | `ai_transcribe` (Beta) |
| Row filter / aggregate | `AI_FILTER`, `AI_AGG` | none | none |
| Measure/optimise a function | `AI_FUNCTION_EVALUATION`, `AI_FUNCTION_OPTIMIZATION` (preview) | none | none listed |
| Forecast / anomalies | ML Functions | none | `ai_forecast`, `ai_detect_anomalies` |
| Error handling | row returns `NULL`; optional `return_error_details` | row returns `NULL`; `ON ERROR` clause | `failOnError`/`error_message` fields |

## Errors that look the same but are not

- **A function exists in the generic docs but not in your engine.** Check "Applies to": Fabric Warehouse lacks `REGEXP_*`, `VECTOR_*` and the embeddings function, even though all three exist for SQL database in Fabric.
- **Same name, different shape.** `AI_CLASSIFY` returns an object in Snowflake, a plain label in Fabric and a VARIANT in Databricks. `AI_TRANSLATE` takes three arguments in Snowflake and two elsewhere.
- **Argument order.** `datediff(end, start)` in Spark's two-argument form and PySpark, but `DATEDIFF(unit, start, end)` everywhere else. `DATEADD` and `date_trunc` also differ in whether the unit or the date comes first.
- **Longitude first.** `ST_MAKEPOINT`/`st_point`/`h3_longlatash3` take longitude then latitude; Snowflake's `HAVERSINE` and `H3_LATLNG_TO_CELL` take latitude then longitude.
- **Ordering inside aggregates.** `collect_list`, `ARRAY_AGG` and `listagg` do not guarantee order unless you ask for it (`WITHIN GROUP`).
