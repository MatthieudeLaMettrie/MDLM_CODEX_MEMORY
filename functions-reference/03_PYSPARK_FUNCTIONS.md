# PySpark on Databricks: functions worth knowing, with examples

Scope: the Python DataFrame API on Databricks (`pyspark.sql`). It mirrors [02_DATABRICKS_SQL_FUNCTIONS.md](02_DATABRICKS_SQL_FUNCTIONS.md): almost every SQL function has a PySpark twin in `pyspark.sql.functions`, so this file concentrates on **how the Python API differs**, the Python-only features (UDFs, `Window`, `Column` methods, NA/stat helpers) and the Databricks additions (AI functions and geospatial via `dbf`).

Sources, read on 2026-10-09: the [Databricks PySpark reference](https://docs.databricks.com/aws/en/pyspark/reference/) (classes) and the [PySpark functions list](https://docs.databricks.com/aws/en/pyspark/reference/functions/) (about 230,000 characters, read in full), plus the individual pages for `ai_query`, `ai_classify`, `ai_extract`, `ai_parse_document` and `st_point`.

**How to read it.** Function names come from that list. Python examples were adapted from the docs or written to match them and **have not been run in a workspace**. Everything assumes a Databricks notebook, where `spark` already exists.

## Contents

1. [Setup, imports and the three import styles](#1-setup-imports-and-the-three-import-styles)
2. [AI functions in Python](#2-ai-functions-in-python)
3. [Columns, conditions and NULLs](#3-columns-conditions-and-nulls)
4. [String and regex](#4-string-and-regex)
5. [Date and time](#5-date-and-time)
6. [Numeric](#6-numeric)
7. [Aggregation and `groupBy`](#7-aggregation-and-groupby)
8. [Window functions](#8-window-functions)
9. [Arrays, maps, structs and lambdas](#9-arrays-maps-structs-and-lambdas)
10. [JSON and VARIANT](#10-json-and-variant)
11. [Generators: `explode`, `inline`, `stack`](#11-generators-explode-inline-stack)
12. [User-defined functions](#12-user-defined-functions)
13. [Geospatial and H3](#13-geospatial-and-h3)
14. [NA and statistics helpers, joins, dedup](#14-na-and-statistics-helpers-joins-dedup)
15. [Reading, writing, streaming, catalog](#15-reading-writing-streaming-catalog)
16. [Python-only traps](#16-python-only-traps)
17. [Ten you should be able to write from memory](#17-ten-you-should-be-able-to-write-from-memory)

---

## 1. Setup, imports and the three import styles

```python
from pyspark.sql import functions as F                     # the standard functions module
from pyspark.sql import Window
from pyspark.sql import types as T
from pyspark.sql import functions as dbf                   # Databricks AI functions (ai_classify, ai_extract, ai_parse_document, ai_query ...)
from pyspark.databricks.sql import functions as dbf_geo    # Databricks geospatial ST_ functions (the docs call this dbf too)
```

The Databricks pages use the alias **`dbf`** for two different modules: the **AI** page examples import `from pyspark.sql import functions as dbf`, while the **geospatial** page imports `from pyspark.databricks.sql import functions as dbf`. Use two distinct aliases (as above) so you never mix them up.

**The escape hatch.** Any SQL function, including ones with no Python wrapper yet, is reachable with `F.expr()` or `selectExpr()`:

```python
df.select(F.expr("ai_summarize(text, 20)").alias("summary"))
df.selectExpr("order_id", "try_divide(amount, 0) AS safe")
```

**Sample DataFrame** used below:

```python
from datetime import date
from decimal import Decimal

schema = "order_id INT, customer STRING, country STRING, order_date DATE, amount DECIMAL(10,2), status STRING"
orders = spark.createDataFrame([
    (1, "alice", "AU", date(2026, 10, 1), Decimal("120.50"), "shipped"),
    (2, "bob",   "AU", date(2026, 10, 2), Decimal("80.00"),  "shipped"),
    (3, "alice", "NZ", date(2026, 10, 5), Decimal("200.00"), "returned"),
    (4, "carol", "US", date(2026, 10, 6), None,              "pending"),
    (5, "bob",   "AU", date(2026, 10, 9), Decimal("45.25"),  "shipped"),
], schema)
orders.createOrReplaceTempView("orders")        # so the SQL file's examples also work
```

---

## 2. AI functions in Python

The Python module exposes only a **subset** of the SQL AI functions. For the rest use `F.expr(...)`.

| Python function | Signature | SQL twin |
| --- | --- | --- |
| `dbf.ai_query` | `ai_query(endpoint, request, return_type=None)` | `ai_query` |
| `dbf.ai_classify` | `ai_classify(col, labels, options=None)` | `ai_classify` |
| `dbf.ai_extract` | `ai_extract(col, schema, options=None)` | `ai_extract` |
| `dbf.ai_parse_document` | `ai_parse_document(col, options=None)` | `ai_parse_document` |
| `F.vector_avg`, `vector_sum`, `vector_cosine_similarity`, `vector_inner_product`, `vector_l2_distance`, `vector_norm`, `vector_normalize` | vector math on `ARRAY<FLOAT>` | same names |
| everything else (`ai_summarize`, `ai_translate`, `ai_mask`, `ai_fix_grammar`, `ai_analyze_sentiment`, `ai_similarity`, `ai_gen`, `ai_transcribe`, `ai_forecast`, `vector_search` ...) | use `F.expr()` / `spark.sql()` | the SQL function |

```python
from pyspark.sql import functions as F, functions as dbf

# ai_classify: static labels (list), labels with descriptions (dict), or a per-row JSON column
df.select(dbf.ai_classify("text", ["positive", "negative", "neutral"]).alias("label"))
df.select(dbf.ai_classify("text", {"positive": "Happy tone", "negative": "Unhappy tone"}))
df.select(dbf.ai_classify("text", F.col("labels_json")))          # a JSON array/object string per row

# ai_extract: a list of field names, or a dict of field -> {"type", "description"}. Returns a VARIANT.
df.select(dbf.ai_extract("text", ["name", "age"]).alias("fields"))
df.select(dbf.ai_extract("text", {"name": {"type": "string", "description": "Name"}}))

# ai_parse_document: BINARY input, so read files with the binaryFile format
docs = spark.read.format("binaryFile").load("/Volumes/main/docs/pdfs")
parsed = docs.select("path", dbf.ai_parse_document("content").alias("doc"))      # VARIANT

# Compose them, just like the SQL version
parsed.select("path", dbf.ai_classify("doc", ["invoice", "contract", "report"]).alias("doc_type"))

# ai_query: any Model Serving endpoint
prompts = orders.select("order_id", F.concat(F.lit("Write a one-line note for a "), "status", F.lit(" order")).alias("prompt"))
prompts.select("order_id",
               dbf.ai_query(endpoint="databricks-meta-llama-3-3-70b-instruct",
                            request=F.col("prompt")).alias("note"))

# Anything else: SQL expression
reviews.select(F.expr("ai_analyze_sentiment(text)").alias("sentiment"),
               F.expr("ai_translate(text, 'es')").alias("es"),
               F.expr("ai_mask(text, array('person', 'email'))").alias("masked"))
```

`ai_classify` and `ai_extract` accept a `STRING` or the `VARIANT` output of `ai_parse_document`. The Python wrappers do **not** expose every SQL option as a named argument: pass the rest through `options={...}` (for example `{"version": "2.1", "enableConfidenceScores": "true"}`), and read the SQL file's section 2 for what the options mean. All the SQL platform rules apply here too: Runtime 15.4 LTS+ (18.2+ recommended), not on classic compute, region limits, and versioned `VARIANT` output.

---

## 3. Columns, conditions and NULLs

| Python | Meaning | Trap |
| --- | --- | --- |
| `F.col("a")`, `df["a"]`, `df.a` | Column reference | `df.a` breaks for names that clash with DataFrame attributes |
| `F.lit(5)`, `F.lit(None)` | Literal | A bare Python value is **not** a column in most functions |
| `F.when(cond, v).when(...).otherwise(v)` | `CASE WHEN` | No `.otherwise()` leaves NULL |
| `F.coalesce(...)`, `F.ifnull`, `F.nvl`, `F.nvl2`, `F.nullif`, `F.nullifzero`, `F.zeroifnull` | NULL handling | |
| `c.isNull()`, `c.isNotNull()`, `F.isnull`, `F.isnan` | NULL tests | `c == None` does **not** work |
| `c.eqNullSafe(d)`, `F.equal_null(c, d)` | Null-safe equality | `==` returns NULL when either side is NULL |
| `c.isin(1, 2)`, `c.between(a, b)` | Membership, inclusive range | |
| `c.cast("int")`, `c.try_cast`-style via `F.expr("try_cast(...)")` | Convert | Bad casts become NULL or raise errors depending on ANSI mode |
| `&`, `\|`, `~` | And / or / not | **Wrap each condition in parentheses**; Python `and`/`or` do not work on columns |
| `F.greatest(...)`, `F.least(...)` | Max/min across columns | Skips NULLs |
| `F.assert_true(cond)`, `F.raise_error(msg)` | Fail on purpose | |

```python
orders.select(
    "order_id",
    F.when(F.col("amount") >= 100, "large").otherwise("small").alias("size"),     # NULL amount -> 'small'
    F.coalesce("amount", F.lit(0)).alias("amount_filled"),
    F.nvl2("amount", F.lit("has amount"), F.lit("no amount")).alias("flag"),
    F.zeroifnull("amount").alias("amount_zero"),
    F.expr("try_divide(10, order_id - 3)").alias("safe_div"),                      # NULL for order 3
).show()

orders.filter((F.col("country") == "AU") & (F.col("status") == "shipped"))        # parentheses are mandatory
orders.filter(F.col("amount").isNull())
orders.filter(~F.col("status").isin("returned", "pending"))
orders.filter(F.col("amount").between(50, 150))
orders.select(F.col("amount").eqNullSafe(None).alias("is_null_safe"))

# Chained when: first match wins
orders.withColumn("tier", F.when(F.col("amount") >= 150, "gold")
                           .when(F.col("amount") >= 75, "silver")
                           .otherwise("bronze"))
```

---

## 4. String and regex

| Function | Use | Trap |
| --- | --- | --- |
| `F.concat(...)`, `F.concat_ws(sep, ...)` | Join | `concat` returns NULL if any input is NULL; `concat_ws` skips NULLs |
| `F.split(col, regex [, limit])` | String to array | The separator is a **regex**: escape `.` as `"\\."` |
| `F.split_part(col, F.lit(delim), F.lit(n))` | n-th piece | **1-based**; all three arguments are columns, so wrap literals in `F.lit` |
| `F.substring(col, pos, len)`, `F.substr`, `F.left`, `F.right`, `F.substring_index` | Slice | `pos` is 1-based |
| `F.trim`, `F.ltrim`, `F.rtrim`, `F.btrim` | Strip | |
| `F.upper`, `F.lower`, `F.initcap`, `F.length`, `F.reverse`, `F.repeat`, `F.lpad`, `F.rpad` | Basics | |
| `F.replace`, `F.translate`, `F.overlay` | Replace | |
| `c.contains`, `c.startswith`, `c.endswith`, `c.like`, `c.ilike`, `c.rlike` | Tests as column methods | `rlike` matches anywhere |
| `F.regexp_extract(col, pattern, idx)`, `F.regexp_extract_all`, `F.regexp_replace`, `F.regexp_count`, `F.regexp_substr`, `F.regexp_like` | Regex | Use raw strings (`r"..."`); idx `0` is the whole match |
| `F.levenshtein`, `F.soundex`, `F.mask`, `F.format_number`, `F.format_string`, `F.printf` | Fuzzy, masking, formatting | |
| `F.base64`, `F.unbase64`, `F.hex`, `F.unhex`, `F.encode`, `F.decode`, `F.parse_url`, `F.url_encode`, `F.url_decode` | Encoding | |

```python
df = spark.createDataFrame([("a,b,c", "order 4521 shipped", "hello world")], "csv STRING, txt STRING, s STRING")
df.select(
    F.split("csv", ",").alias("parts"),                                          # ["a","b","c"]
    F.split_part(F.col("csv"), F.lit(","), F.lit(2)).alias("second"),           # b
    F.regexp_extract("txt", r"([0-9]+)", 1).alias("order_no"),                   # 4521
    F.regexp_replace("txt", r"[0-9]+", "#").alias("masked"),                     # order # shipped
    F.regexp_extract_all("txt", F.lit(r"([a-z]+)"), F.lit(1)).alias("words"),
    F.initcap("s").alias("title"),                                               # Hello World
    F.lpad(F.lit("7"), 3, "0").alias("padded"),                                  # 007
    F.concat_ws("-", F.lit("a"), F.lit(None), F.lit("c")).alias("joined"),       # a-c
    F.levenshtein(F.lit("kitten"), F.lit("sitting")).alias("distance"),          # 3
).show(truncate=False)

orders.filter(F.col("customer").ilike("AL%"))
orders.filter(F.col("customer").rlike("^(alice|bob)$"))
```

---

## 5. Date and time

| Function | Use | Trap |
| --- | --- | --- |
| `F.current_date()`, `F.current_timestamp()`, `F.now()` | Now | Session time zone |
| `F.date_add(d, n)`, `F.date_sub(d, n)`, `F.dateadd(unit, n, d)`, `F.add_months(d, n)` | Add | `date_add` is days; `dateadd` takes a unit |
| `F.datediff(end, start)`, `F.date_diff(unit, start, end)` / `F.timestamp_diff` | Difference | **`datediff` takes END first**; the unit form takes start then end |
| `F.months_between(a, b)` | Fractional months | |
| `F.date_trunc("month", ts)`, `F.trunc(d, "MM")` | Truncate | `date_trunc` unit first, returns a timestamp; `trunc` date first, returns a date |
| `F.year`, `F.month`, `F.dayofmonth`, `F.dayofweek`, `F.dayofyear`, `F.weekofyear`, `F.quarter`, `F.hour`, `F.minute`, `F.second`, `F.extract`, `F.date_part` | Parts | `dayofweek`: 1 = Sunday |
| `F.date_format(ts, fmt)`, `F.to_date(col, fmt)`, `F.to_timestamp(col, fmt)`, `F.try_to_timestamp`, `F.try_to_date` | Parse/format | `MM` month vs `mm` minute |
| `F.last_day`, `F.next_day(d, "Mon")`, `F.dayname`, `F.monthname` | Calendar | |
| `F.make_date(y, m, d)`, `F.make_timestamp(...)`, `F.make_interval(...)` | Build | |
| `F.from_utc_timestamp(ts, tz)`, `F.to_utc_timestamp(ts, tz)`, `F.convert_timezone(...)` | Time zones | `from_utc_timestamp` assumes the input is UTC |
| `F.unix_timestamp`, `F.from_unixtime`, `F.timestamp_seconds/millis/micros` | Epoch | |
| `F.window("ts", "10 minutes")`, `F.session_window("ts", "5 minutes")` | Time buckets | `window` yields a struct with `start` and `end` |

```python
orders.select(
    F.date_add("order_date", 7).alias("plus_week"),
    F.datediff(F.current_date(), "order_date").alias("age_days"),                 # END first
    F.date_trunc("month", "order_date").alias("month_start"),
    F.last_day("order_date").alias("month_end"),
    F.date_format("order_date", "yyyy-MM-dd").alias("txt"),
    F.dayname("order_date").alias("dow"),
).show()

F.to_date(F.lit("09/10/2026"), "dd/MM/yyyy")                                         # 2026-10-09

# Monthly revenue
(orders.groupBy(F.date_trunc("month", "order_date").alias("month"))
       .agg(F.sum("amount").alias("revenue"))
       .orderBy("month"))

# Time zone shift
events.select(F.from_utc_timestamp("event_ts", "Australia/Sydney").alias("local_ts"))

# 15-minute buckets
events.groupBy(F.window("event_ts", "15 minutes")).count()

# Calendar spine: build with sequence(), then explode
spark.range(1).select(F.explode(F.sequence(F.lit(date(2026, 10, 1)), F.lit(date(2026, 10, 10)))).alias("d"))
```

---

## 6. Numeric

| Function | Use | Trap |
| --- | --- | --- |
| `F.round(c, n)`, `F.bround(c, n)`, `F.ceil`, `F.floor`, `F.abs`, `F.signum` | Rounding | `round` is half-up, `bround` half-even |
| `F.pow`, `F.sqrt`, `F.log`, `F.log10`, `F.exp`, `F.pmod`, `F.hypot` | Maths | `pmod` is always non-negative |
| `F.try_add`, `F.try_subtract`, `F.try_multiply`, `F.try_divide`, `F.try_mod` | Safe arithmetic | `try_divide(x, 0)` is NULL |
| `F.width_bucket(v, lo, hi, n)` | Histogram bucket | |
| `F.rand(seed)`, `F.randn(seed)`, `F.uniform(lo, hi, seed)`, `F.randstr` | Random | Pass a seed for repeatability |
| `F.greatest`, `F.least`, `F.isnan`, `F.nanvl` | Misc | |

```python
orders.select(F.round("amount", 1), F.ceil("amount"), F.floor("amount"), F.try_divide("amount", F.lit(0)))
orders.withColumn("pct", F.round(100 * F.col("amount") / F.sum("amount").over(Window.partitionBy()), 1))
spark.range(5).select("id", F.rand(42).alias("r"))        # reproducible
```

---

## 7. Aggregation and `groupBy`

`df.groupBy(...)` returns `GroupedData`; call `.agg(...)` with functions, or a shortcut (`.sum`, `.count`, `.avg`, `.min`, `.max`, `.pivot`). Use `.alias()` or you get names like `sum(amount)`.

| Function | Use | Trap |
| --- | --- | --- |
| `F.count("*")`, `F.count("col")`, `F.count_distinct("col")`, `F.count_if(cond)` | Counting | `count("col")` skips NULLs. The name is `count_distinct` (older `countDistinct` still works) |
| `F.sum`, `F.avg`/`F.mean`, `F.min`, `F.max`, `F.product`, `F.try_sum`, `F.try_avg` | Basics | |
| `F.max_by(val, key)`, `F.min_by(val, key)` | Value at max/min of another column | |
| `F.first(c, ignorenulls=True)`, `F.last(...)`, `F.any_value(c)` | Pick a value | Nondeterministic without ordering |
| `F.collect_list`, `F.collect_set`, `F.array_agg` | Rows to array | **No guaranteed order** |
| `F.listagg(c, delimiter)`, `F.listagg_distinct`, `F.string_agg` | Rows to string | Ordering needs a sort first or SQL `WITHIN GROUP` via `F.expr` |
| `F.median`, `F.mode`, `F.percentile`, `F.percentile_approx`, `F.approx_percentile`, `F.approx_count_distinct`, `F.approx_top_k` | Statistics | `percentile` exact, `percentile_approx` cheap |
| `F.stddev`, `F.variance`, `F.corr`, `F.covar_pop`, `F.skewness`, `F.kurtosis`, `F.regr_*` | Statistics | |
| `F.bool_and`, `F.bool_or`, `F.every`, `F.some`, `F.bit_and` ... | Boolean/bitwise | |
| `F.grouping`, `F.grouping_id`, `df.rollup(...)`, `df.cube(...)` | Subtotals | Use `df.rollup("a", "b").agg(...)` |

```python
orders.agg(
    F.count("*").alias("all_rows"),                              # 5
    F.count("amount").alias("with_amount"),                      # 4
    F.count_if(F.col("status") == "shipped").alias("shipped"),   # 3
    F.sum("amount").alias("total"),
    F.median("amount").alias("median_amount"),
    F.count_distinct("customer").alias("customers"),
).show()

(orders.groupBy("customer")
       .agg(F.sum("amount").alias("total"),
            F.max_by("status", "order_date").alias("latest_status"),
            F.collect_list("order_id").alias("ids"),
            F.approx_count_distinct("country").alias("countries"))
       .orderBy(F.desc("total")))

# Conditional aggregation inside agg
orders.groupBy("country").agg(F.sum(F.when(F.col("status") == "shipped", F.col("amount"))).alias("shipped_amount"))

# Pivot: list the values (faster and stable)
orders.groupBy("customer").pivot("status", ["shipped", "returned", "pending"]).sum("amount")

# Subtotals
orders.rollup("country", "customer").agg(F.sum("amount").alias("total")).orderBy("country", "customer")

# Ordered string aggregation: drop to SQL for WITHIN GROUP
orders.createOrReplaceTempView("orders")
spark.sql("SELECT customer, listagg(status, ', ') WITHIN GROUP (ORDER BY order_date) AS statuses FROM orders GROUP BY customer")
```

---

## 8. Window functions

There is **no `QUALIFY`** in the DataFrame API. Compute the window column, then `filter`.

```python
from pyspark.sql import Window
w = Window.partitionBy("customer").orderBy(F.col("order_date").desc())
```

| Piece | Python |
| --- | --- |
| Ranking | `F.row_number()`, `F.rank()`, `F.dense_rank()`, `F.ntile(n)`, `F.percent_rank()`, `F.cume_dist()` `.over(w)` (**need `orderBy`**) |
| Analytic | `F.lag(col, 1, default)`, `F.lead(...)`, `F.first_value`, `F.last_value`, `F.nth_value(col, n)` `.over(w)` |
| Aggregates | `F.sum("x").over(w)`, `F.avg`, `F.count`, `F.max` ... |
| Frames | `.rowsBetween(start, end)`, `.rangeBetween(start, end)` with `Window.unboundedPreceding`, `Window.currentRow`, `Window.unboundedFollowing` or integers |
| No partition | `Window.partitionBy()` or `Window.orderBy(...)` alone moves all data to one partition, so avoid on big data |

```python
# Latest order per customer (the QUALIFY replacement)
latest = (orders.withColumn("rn", F.row_number().over(w))
                .filter("rn = 1")
                .drop("rn"))

# Change versus previous order
w_time = Window.orderBy("order_date")
orders.select("order_id", "order_date", "amount",
              (F.col("amount") - F.lag("amount", 1).over(w_time)).alias("change_vs_prev"))

# Running total and a 3-row moving average
w_run = Window.orderBy("order_date").rowsBetween(Window.unboundedPreceding, Window.currentRow)
w_mov = Window.orderBy("order_date").rowsBetween(-2, Window.currentRow)
orders.select("order_id",
              F.sum("amount").over(w_run).alias("running_total"),
              F.avg("amount").over(w_mov).alias("moving_avg_3"))

# last_value needs a widened frame
w_all = Window.partitionBy("customer").orderBy("order_date") \
              .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
orders.select("order_id", F.last_value("status").over(w_all).alias("final_status"))

# Ranking and share of total
orders.select("customer", "amount",
              F.rank().over(Window.orderBy(F.col("amount").desc_nulls_last())).alias("rnk"),
              (F.col("amount") / F.sum("amount").over(Window.partitionBy())).alias("share"))
```

---

## 9. Arrays, maps, structs and lambdas

Python lambdas work with the higher-order functions: `F.transform`, `F.filter`, `F.aggregate` (alias `F.reduce`), `F.exists`, `F.forall`, `F.zip_with`, `F.map_filter`, `F.map_zip_with`, `F.transform_keys`, `F.transform_values`, and `F.array_sort` with a comparator.

| Function | Use | Trap |
| --- | --- | --- |
| `F.array(...)`, `F.sequence(a, b [, step])`, `F.array_repeat`, `F.array_append/prepend/insert/remove/compact` | Build and edit | |
| `F.size`, `F.cardinality`, `F.array_size` | Length | |
| `F.array_contains(arr, v)`, `F.array_position(arr, v)` | Search | `array_position` is **1-based** |
| `F.element_at(arr, i)`, `col.getItem(i)`, `arr[i]` | Access | `getItem`/`[i]` **0-based**; `element_at` **1-based** |
| `F.array_distinct`, `F.array_union`, `F.array_intersect`, `F.array_except`, `F.arrays_overlap`, `F.arrays_zip`, `F.flatten`, `F.slice`, `F.array_join`, `F.sort_array`, `F.array_min/max` | Set and order | |
| `F.create_map(...)`, `F.map_from_arrays`, `F.map_keys`, `F.map_values`, `F.map_entries`, `F.map_concat`, `F.map_contains_key`, `F.str_to_map` | Maps | |
| `F.struct(...)`, `F.named_struct(...)`, `col.getField("a")`, `col["a"]` | Structs | `F.struct("*")` bundles all columns |

```python
df = spark.createDataFrame([([1, 2, 3, 3],)], "arr ARRAY<INT>")
df.select(
    F.array_distinct("arr").alias("distinct"),                              # [1,2,3]
    F.array_contains("arr", 2).alias("has2"),                               # true
    F.element_at("arr", 1).alias("first_1based"),                           # 1
    F.col("arr")[0].alias("first_0based"),                                  # 1
    F.slice("arr", 2, 2).alias("slice"),                                    # [2,3]
    F.size("arr").alias("n"),
).show()

# Lambdas
df.select(F.transform("arr", lambda x: x * 2))                                       # [2,4,6,6]
df.select(F.transform("arr", lambda x, i: x + i))                                    # element plus index
df.select(F.filter("arr", lambda x: x > 1))                                          # [2,3,3]
df.select(F.aggregate("arr", F.lit(0), lambda acc, x: acc + x))                      # 9
df.select(F.exists("arr", lambda x: x > 2), F.forall("arr", lambda x: x > 0))        # true, true
two = spark.createDataFrame([([1, 2], [10, 20])], "a ARRAY<INT>, b ARRAY<INT>")
two.select(F.zip_with("a", "b", lambda x, y: x + y))                                 # [11,22]

m = spark.createDataFrame([({"a": 1, "b": 5},)], "m MAP<STRING,INT>")
m.select(F.map_filter("m", lambda k, v: v > 2), F.transform_values("m", lambda k, v: v * 10))

# Structs and maps
orders.select(F.struct("customer", "amount").alias("s")).select("s.customer")
orders.select(F.create_map(F.lit("country"), "country", F.lit("status"), "status").alias("attrs"))
```

---

## 10. JSON and VARIANT

| Function | Use | Trap |
| --- | --- | --- |
| `F.from_json(col, schema)` | JSON string to struct/array/map | `schema` can be a DDL string (`"id INT, name STRING"`), a `StructType`, or `F.schema_of_json(F.lit(sample))` |
| `F.to_json(col)` | Struct to JSON | |
| `F.schema_of_json(F.lit(sample))` | Infer a DDL schema | Needs a **literal** sample |
| `F.get_json_object(col, "$.a.b")`, `F.json_tuple(col, "a", "b")` | Quick extraction | Returns strings |
| `F.json_array_length`, `F.json_object_keys` | Inspect | |
| `F.parse_json(col)`, `F.try_parse_json(col)` | String to VARIANT | |
| `F.variant_get(v, "$.path", "type")`, `F.try_variant_get(...)` | Typed extraction | Missing path is NULL; bad cast errors (the `try_` form returns NULL) |
| `F.schema_of_variant`, `F.schema_of_variant_agg`, `F.is_variant_null`, `F.to_variant_object` | Inspect/convert | |
| `F.from_xml`, `F.to_xml`, `F.xpath*`, `F.from_csv`, `F.to_csv`, `F.from_avro`, `F.to_avro` | Other formats | |

```python
j = spark.createDataFrame([('{"id": 1, "name": "alice", "items": [{"sku": "X1", "qty": 2}, {"sku": "Y2", "qty": 5}]}',)], "json STRING")

parsed = j.select(F.from_json("json", "id INT, name STRING, items ARRAY<STRUCT<sku: STRING, qty: INT>>").alias("d"))
parsed.select("d.id", "d.name").show()
parsed.select(F.explode("d.items").alias("item")).select("item.sku", "item.qty").show()     # explode the array

j.select(F.get_json_object("json", "$.items[1].qty").alias("qty"))                           # "5" (a string)
j.select(F.to_json(F.struct(F.lit(1).alias("id"), F.lit("alice").alias("name"))))

# VARIANT: parse once, query many times
v = j.select(F.parse_json("json").alias("v"))
v.select(F.variant_get("v", "$.items[1].sku", "string").alias("sku"),                        # Y2
         F.try_variant_get("v", "$.name", "int").alias("bad_cast"))                          # NULL, no error
v.select(F.col("v")["name"].cast("string"))                                                  # bracket access

# Derive a schema from sample data
sample = '{"a": 1, "b": "x"}'
j.select(F.schema_of_json(F.lit(sample)))                                                    # STRUCT<a: BIGINT, b: STRING>
```

---

## 11. Generators: `explode`, `inline`, `stack`

| Function | Use | Trap |
| --- | --- | --- |
| `F.explode`, `F.explode_outer` | One row per array/map element | `explode` **drops** NULL/empty arrays; `_outer` keeps them |
| `F.posexplode`, `F.posexplode_outer` | Element and **0-based** position | |
| `F.inline`, `F.inline_outer` | Array of structs to columns | |
| `F.stack(n, ...)` | Unpivot | `n` is the number of rows produced, so use `F.expr("stack(...)")` for the alias list |
| `F.variant_explode`, `F.variant_explode_outer` | Explode a VARIANT | |
| `spark.range(start, end, step)` | Number table | `end` is exclusive |

```python
t = spark.createDataFrame([(1, ["a", "b"]), (2, [])], "id INT, tags ARRAY<STRING>")
t.select("id", F.explode("tags").alias("tag")).show()                 # only id 1 (id 2 dropped)
t.select("id", F.explode_outer("tags").alias("tag")).show()           # id 2 kept with NULL
t.select("id", F.posexplode("tags")).show()                           # pos, col

spark.createDataFrame([(1, 10, 20)], "id INT, q1 INT, q2 INT") \
     .selectExpr("id", "stack(2, 'Q1', q1, 'Q2', q2) AS (quarter, revenue)")             # unpivot

spark.range(1, 11, 2).show()                                          # 1,3,5,7,9
```

---

## 12. User-defined functions

Prefer built-ins; they run in the JVM (and Photon). Python UDFs cross a process boundary and are much slower.

| Kind | Decorator / call | Use | Trap |
| --- | --- | --- | --- |
| Python UDF | `F.udf(f, returnType)` / `@F.udf("type")` | Row-at-a-time Python | Slow; NULL inputs reach your code as `None` |
| **pandas UDF** | `@F.pandas_udf("type")` | Vectorised on `pd.Series` | Much faster than a plain UDF; type hints decide the flavour |
| UDTF | `@F.udtf(returnType="a int, b int")` | One input row to many rows | Class with an `eval` method; use in SQL with `FROM my_udtf(...)` |
| Arrow UDTF | `arrow_udtf` | Vectorised table function | Newer |
| Registered UDF | `spark.udf.register("name", f, "type")` | Use from SQL | |
| `F.call_udf("name", col)` | Call a registered function | |

```python
import pandas as pd

@F.udf("string")
def label(amount):                                   # plain UDF: avoid when a built-in will do
    return None if amount is None else ("big" if amount >= 100 else "small")

@F.pandas_udf("double")
def with_tax(amount: pd.Series) -> pd.Series:        # vectorised
    return amount.astype("float64") * 1.1

orders.select(label("amount"), with_tax("amount"))

spark.udf.register("label_sql", label)               # reuse from SQL
spark.sql("SELECT label_sql(amount) FROM orders")

# UDTF: explode a string into (word, length) rows
@F.udtf(returnType="word string, length int")
class SplitWords:
    def eval(self, text: str):
        for w in (text or "").split():
            yield w, len(w)

spark.udtf.register("split_words", SplitWords)
spark.sql("SELECT * FROM split_words('hello big world')")
```

---

## 13. Geospatial and H3

Geospatial `ST_` functions live in a **separate module**, `pyspark.databricks.sql.functions`. They need Runtime 17.1+ and are not on classic warehouses. `GEOMETRY` support is GA and `GEOGRAPHY` is Public Preview. The `Geometry` and `Geography` classes represent single values.

```python
from pyspark.databricks.sql import functions as dbf_geo
from pyspark.sql import functions as F

pts = spark.createDataFrame([(1.0, 2.0, 4326)], ["x", "y", "srid"])
pts.select(dbf_geo.st_asewkt(dbf_geo.st_point("x", "y", "srid")).alias("result")).collect()
# [Row(result='SRID=4326;POINT(1 2)')]

# Other ST functions have the same names as their SQL twins (st_contains, st_intersects, st_buffer, st_distance ...)
stores.join(regions, dbf_geo.st_contains("boundary", dbf_geo.st_point("lon", "lat")))

# Not sure a function has a Python wrapper? Use the SQL expression
stores.select(F.expr("st_distancesphere(st_point(lon, lat), st_point(151.2093, -33.8688))").alias("metres"))

# H3 functions are in pyspark.sql.functions (argument types: confirm in the PySpark reference; F.expr("h3_longlatash3(lon, lat, 8)") is the safe form)
stores.select(F.expr("h3_longlatash3(lon, lat, 8)").alias("cell"))
```

Same traps as SQL: `st_distance` returns **coordinate units**, `st_distancesphere` returns **metres** between points with the same SRID, and **longitude comes first** in `st_point` and `h3_longlatash3`.

---

## 14. NA and statistics helpers, joins, dedup

**`DataFrameNaFunctions`** (`df.na`), **`DataFrameStatFunctions`** (`df.stat`):

```python
orders.fillna({"amount": 0, "status": "unknown"})                    # per-column defaults
orders.na.fill(0, subset=["amount"])
orders.dropna(subset=["amount"])                                      # drop rows with NULL amount
orders.dropna(how="all")                                              # only rows where EVERY column is NULL
orders.na.replace("returned", "refunded", subset=["status"])

orders.stat.approxQuantile("amount", [0.5, 0.9], 0.01)                # [median, p90], relative error 0.01
orders.stat.corr("order_id", "amount")
orders.stat.crosstab("customer", "status")                           # contingency table
orders.describe("amount").show()                                      # count, mean, stddev, min, max
orders.summary("count", "min", "50%", "max").show()
```

**Joins and de-duplication:**

```python
orders.join(customers, "customer", "left")                            # inner (default), left, right, outer, left_semi, left_anti, cross
orders.join(customers, orders.customer == customers.name, "inner")
orders.join(F.broadcast(small_dim), "country")                         # broadcast hint for a small table

orders.join(blocked, "customer", "left_anti")                          # rows with NO match (NOT IN / NOT EXISTS)
orders.join(vip, "customer", "left_semi")                              # rows WITH a match, no extra columns

orders.dropDuplicates(["customer"])                                    # arbitrary row per key (NOT the latest!)
orders.distinct()
```

`dropDuplicates` keeps an **arbitrary** row per key. To keep the latest, use the `row_number()` pattern from section 8.

---

## 15. Reading, writing, streaming, catalog

```python
# DataFrameReader
df = spark.read.format("csv").option("header", True).schema("id INT, name STRING").load("/Volumes/main/raw/people")
df = spark.read.table("main.sales.orders")
df = spark.read.format("binaryFile").load("/Volumes/main/docs/pdfs")           # path, modificationTime, length, content

# DataFrameWriter (v1) and DataFrameWriterV2
df.write.format("delta").mode("overwrite").saveAsTable("main.sales.orders_clean")
df.writeTo("main.sales.orders_clean").createOrReplace()                        # v2 API
df.writeTo("main.sales.orders_clean").append()

# SQL from Python, and the other way
res = spark.sql("SELECT customer, sum(amount) AS total FROM orders GROUP BY customer")

# Structured Streaming (Auto Loader shown)
stream = (spark.readStream.format("cloudFiles").option("cloudFiles.format", "json")
               .load("/Volumes/main/raw/events"))
q = (stream.writeStream.option("checkpointLocation", "/Volumes/main/chk/events")
           .toTable("main.bronze.events"))

# Catalog, schema and plan inspection
spark.catalog.listTables("main.sales")
df.printSchema(); df.explain(); df.show(5, truncate=False)

# Collect metrics while a query runs
from pyspark.sql import Observation
obs = Observation("quality")
checked = orders.observe(obs, F.count("*").alias("rows"), F.count_if(F.col("amount").isNull()).alias("null_amounts"))
checked.write.format("noop").mode("overwrite").save()
print(obs.get)
```

Classes in the reference worth recognising: `DataFrame`, `Column`, `Row`, `GroupedData`, `DataFrameReader`/`Writer`/`WriterV2`, `DataFrameNaFunctions`, `DataFrameStatFunctions`, `Window`/`WindowSpec`, `UserDefinedFunction`/`UDFRegistration`, `UserDefinedTableFunction`/`UDTFRegistration`, `Catalog`, `Observation`, `SparkSession`, `RuntimeConfig`, `VariantVal`, `Geography`, `Geometry`, streaming (`DataStreamReader`/`Writer`, `StreamingQuery`, `StreamingQueryListener`, `StreamingQueryManager`) and the custom data source classes (`DataSource`, `DataSourceReader`, `DataSourceWriter` ...).

---

## 16. Python-only traps

| Trap | Why |
| --- | --- |
| `df.filter(a == 1 and b == 2)` fails | Use `(a == 1) & (b == 2)`; the parentheses are mandatory because `&` binds tighter than `==` |
| `col == None` never matches | Use `.isNull()` / `.eqNullSafe(None)` |
| Transformations are **lazy**; `show`, `count`, `collect`, `write`, `toPandas` are the actions | Nothing runs until an action; each action can re-run the whole plan, so `cache()` only when reused |
| `collect()` / `toPandas()` pull everything to the driver | Out-of-memory on large data; use `limit`, `take`, or write to a table |
| `F.when(...)` without `.otherwise(...)` | NULL, not the original value |
| `F.col("a") + "b"` | Adds a string literal, not column `b`; use `F.col("b")` |
| `withColumn` in a loop | Builds a huge plan; use one `select` with all expressions |
| `F.split(c, ".")` | The separator is a regex, so `.` matches everything |
| `F.datediff(a, b)` | Computes `a - b` in days (end first) |
| `F.first`/`F.last`/`collect_list` | Order is not guaranteed without an explicit ordering step |
| `dropDuplicates(subset)` | Keeps an arbitrary row |
| Window without `partitionBy` | Single-partition bottleneck |
| Python UDF in a hot path | Use a built-in or a pandas UDF |
| `ai_*` in Python | Only `ai_query`, `ai_classify`, `ai_extract`, `ai_parse_document` have wrappers; the rest need `F.expr` |

---

## 17. Ten you should be able to write from memory

```python
latest = df.withColumn("rn", F.row_number().over(Window.partitionBy("k").orderBy(F.col("ts").desc()))).filter("rn = 1")  # QUALIFY
df.filter((F.col("a") > 1) & F.col("b").isNotNull())                                                                   # parentheses
df.groupBy("k").agg(F.sum("x").alias("total"), F.count_distinct("y").alias("users"))                                    # aggregate
df.select(F.explode("arr").alias("item"))                                                                              # explode
df.withColumn("v", F.from_json("json", "id INT, name STRING"))                                                         # JSON to struct
df.select(F.variant_get(F.parse_json("json"), "$.a.b", "string"))                                                      # VARIANT
df.select(F.transform("arr", lambda x: x * 2), F.filter("arr", lambda x: x > 0))                                        # lambdas
df.select(F.date_trunc("month", "d"), F.datediff(F.current_date(), "d"))                                                # dates (end first)
df.select(dbf.ai_classify("text", ["a", "b"]), F.expr("ai_summarize(text, 20)"))                                        # AI functions
df.write.format("delta").mode("overwrite").saveAsTable("c.s.t")                                                         # write a Delta table
```
