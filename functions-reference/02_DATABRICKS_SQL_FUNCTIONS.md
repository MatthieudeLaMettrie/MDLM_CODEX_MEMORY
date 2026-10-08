# Databricks SQL functions: AI functions plus the ones worth knowing

Scope: **Databricks SQL** and Databricks Runtime (Spark SQL dialect, Unity Catalog, Delta). The PySpark equivalents are in [03_PYSPARK_FUNCTIONS.md](03_PYSPARK_FUNCTIONS.md).

Sources, read on 2026-10-09: the [built-in functions index](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin) and its [alphabetical list](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin-alpha) (about 480 entries), the [lambda](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-lambda-functions), [window](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions) and [ST geospatial](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-st-geospatial-functions) pages, and the individual reference pages for every `ai_*` function plus `vector_search`, `vector_cosine_similarity`, `variant_get`, `read_files`, `listagg`, `h3_longlatash3`, `st_distance` and `st_distancesphere`.

**How to read it.** Syntax and constraints were taken from those pages. Examples were adapted from them or written to match them, and **have not been executed in a workspace**. Functions I did not open individually are standard Spark SQL; where a detail matters I say so. Statuses (Beta, Public Preview) change often, so re-check the page before building on a preview feature.

## Contents

1. [Platform rules that affect every AI function](#1-platform-rules-that-affect-every-ai-function)
2. [AI functions](#2-ai-functions)
3. [Operators, conditional and NULL handling](#3-operators-conditional-and-null-handling)
4. [Conversion and `try_` functions](#4-conversion-and-try_-functions)
5. [Date and time](#5-date-and-time)
6. [String and regular expressions](#6-string-and-regular-expressions)
7. [Numeric](#7-numeric)
8. [Aggregate](#8-aggregate)
9. [Window functions and `QUALIFY`](#9-window-functions-and-qualify)
10. [Arrays, maps, structs and lambda functions](#10-arrays-maps-structs-and-lambda-functions)
11. [JSON and VARIANT](#11-json-and-variant)
12. [Generators and table-valued functions](#12-generators-and-table-valued-functions)
13. [Hash, context and miscellaneous](#13-hash-context-and-miscellaneous)
14. [Geospatial: `ST_` and H3](#14-geospatial-st_-and-h3)
15. [Sketches and approximate analytics](#15-sketches-and-approximate-analytics)
16. [Not covered](#16-not-covered)
17. [Ten you should be able to write from memory](#17-ten-you-should-be-able-to-write-from-memory)

**Sample data** (a temporary view; Databricks SQL runs it as written):

```sql
CREATE OR REPLACE TEMP VIEW orders AS
SELECT * FROM VALUES
  (1, 'alice', 'AU', DATE'2026-10-01', 120.50, 'shipped'),
  (2, 'bob',   'AU', DATE'2026-10-02',  80.00, 'shipped'),
  (3, 'alice', 'NZ', DATE'2026-10-05', 200.00, 'returned'),
  (4, 'carol', 'US', DATE'2026-10-06', CAST(NULL AS DECIMAL(10,2)), 'pending'),
  (5, 'bob',   'AU', DATE'2026-10-09',  45.25, 'shipped')
AS t(order_id, customer, country, order_date, amount, status);
```

---

## 1. Platform rules that affect every AI function

| Rule | Detail |
| --- | --- |
| Compute | **Not available on Databricks SQL Classic** warehouses. Use a Pro or Serverless SQL warehouse, or a cluster on the right Runtime |
| Runtime | `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize` and most task functions need **15.4 LTS or above**, with **18.2 or above recommended**. `ai_parse_document` needs **17.3**. `ai_enrich`, `ai_search`, `ai_prep_search` need **18.2**. `ai_predict_class` / `ai_predict_value` need **19.3** or a Pro/Serverless warehouse |
| Region | Many need a region that supports "AI Functions optimized for batch inference" (or Model Serving). Workspaces with the Enhanced Security and Compliance add-on must check regional support and enable previews |
| Preview state | Most are **Public Preview**; `ai_transcribe`, `ai_decide`, `ai_detect_anomalies`, `ai_enrich`, `ai_search`, `ai_prep_search`, `ai_top_drivers`, `ai_predict_*` are **Beta**. The predictive ones need an admin to enable **Predictive AI Functions** on the Previews page |
| Language | Task functions are **tuned for English** even where the model handles other languages |
| Versioned output | `ai_classify`, `ai_extract`, `ai_decide`, `ai_prep_search` return a **`VARIANT`** and take a `version` option. A newer version can change the **output shape**, so pin `version` in production |
| Views | `ai_classify` and `ai_extract` **cannot be used in views** |
| Errors | The `VARIANT`-returning functions put failures in `error_message` and leave `response` NULL instead of failing the query |

---

## 2. AI functions

| Function | Syntax | Returns | Status |
| --- | --- | --- | --- |
| `ai_query` | `ai_query(endpoint, request [, returnType, failOnError, modelParameters, responseFormat, files])` | Parsed model response | See page |
| `ai_gen` | `ai_gen(prompt)` | `STRING` | Public Preview |
| `ai_generate_text` | `ai_generate_text(prompt, modelName[, k, v ...])` | `STRING` | **Deprecated**, use `ai_query` |
| `ai_classify` | `ai_classify(content, labels [, options])` | `VARIANT` (v2.x) | v2.1 recommended; v1.0 legacy |
| `ai_extract` | `ai_extract(content, schema [, options])` | `VARIANT` (v2.x) | v2.1/2.0 recommended; v1.0 legacy |
| `ai_summarize` | `ai_summarize(content [, max_words])` | `STRING` | Public Preview |
| `ai_translate` | `ai_translate(content, to_lang)` | `STRING` | Public Preview |
| `ai_fix_grammar` | `ai_fix_grammar(content)` | `STRING` | Public Preview |
| `ai_mask` | `ai_mask(content, labels)` | `STRING` | Public Preview |
| `ai_analyze_sentiment` | `ai_analyze_sentiment(content)` | `STRING` | Public Preview |
| `ai_similarity` | `ai_similarity(expr1, expr2)` | `FLOAT` | Public Preview |
| `ai_parse_document` | `ai_parse_document(content [, map(...)])` | `VARIANT` | Runtime 17.3+ |
| `ai_transcribe` | `ai_transcribe(content)` | `VARIANT` | **Beta** |
| `ai_prep_search` | `ai_prep_search(parsed [, options])` | `VARIANT` | **Beta** |
| `ai_decide` | `ai_decide(state, questions [, options])` | `VARIANT` | **Beta** |
| `ai_enrich` | `ai_enrich(content, schema [, knowledge_sources] [, options])` | `VARIANT` | **Beta** |
| `ai_search` | `ai_search(query, knowledge_sources [, instructions] [, options])` | `VARIANT` | **Beta** |
| `ai_forecast` | `ai_forecast(observed, horizon, time_col, value_col [, ...])` | Table | v1 Public Preview, v2 Beta |
| `ai_detect_anomalies` | `ai_detect_anomalies(observed, time_col, value_col [, ...])` | Table | **Beta** |
| `ai_top_drivers` | `ai_top_drivers(input =>, metric =>, is_test => [, ...])` | Table | **Beta** |
| `ai_predict_class` / `ai_predict_value` | `(input => TABLE(t), target_col =>, feature_cols => [, seed =>])` | Table | **Beta** |
| `vector_search` | `vector_search(index =>, query_text => \| query_vector => [, num_results =>, query_type =>])` | Table | Public Preview |

### 2.1 General: `ai_query`

The one function for any Model Serving endpoint: Foundation Model APIs, **external models** (OpenAI and similar) and **custom** endpoints.

```sql
-- External or foundation chat model: endpoint name, then the prompt
SELECT ai_query('my-external-model-openai-chat', 'Describe Databricks SQL in 30 words.') AS summary;

-- Per row, with parameters. modelParameters is a constant STRUCT; default temperature is 0.0.
SELECT order_id,
       ai_query(
         'databricks-meta-llama-3-3-70b-instruct',          -- use an endpoint that exists in YOUR workspace
         CONCAT('Write a one-line status note for an order that is ', status),
         modelParameters => named_struct('max_tokens', 60, 'temperature', 0.2)
       ) AS note
FROM orders;

-- Do not fail the whole query: returns a STRUCT of (response, errorMessage)
SELECT ai_query('databricks-meta-llama-3-3-70b-instruct', 'Say hi', failOnError => false) AS r;
-- r.response is NULL and r.errorMessage is set when the call fails

-- Structured output (chat foundation models only; Runtime 15.4 LTS+). A DDL-style string is shown;
-- the page also accepts a JSON string of type text, json_object or json_schema.
SELECT ai_query(
         'databricks-meta-llama-3-3-70b-instruct',
         'Extract city and country: I flew from Paris, France to Sydney.',
         responseFormat => 'STRUCT<city: STRING, country: STRING>'
       ) AS parsed;

-- Custom (non-LLM) endpoint: pass a STRUCT of features and a return type
SELECT ai_query('weekly-forecast', request => struct(*), returnType => 'FLOAT') AS predicted_revenue
FROM weekly_features;

-- Multimodal: pass image bytes with files => (JPEG and PNG only)
SELECT ai_query('<vision-capable-endpoint>', 'Describe this image', files => content)
FROM read_files('/Volumes/my_catalog/my_schema/my_volume/images', format => 'binaryFile');
```

**Exam traps:** the definer needs **`CAN QUERY`** on the endpoint. `failOnError` and `modelParameters` need **Runtime 15.3+**; `responseFormat` needs **15.4 LTS+**. `returnType` is optional from 15.2 and required below that for custom endpoints. With `failOnError => false` the return type becomes a STRUCT, so use `.response`.

`ai_gen(prompt)` is the old one-argument shortcut (`SELECT ai_gen('Generate a cheerful email title for a summer bike sale with 20% discount')`). `ai_generate_text` is deprecated and takes a model name plus key/value pairs; replace it with `ai_query` plus an external model.

### 2.2 Task functions

```sql
-- Sentiment: positive | negative | neutral | mixed (NULL if undetectable)
SELECT ai_analyze_sentiment('I am happy');                       -- positive

-- Grammar
SELECT ai_fix_grammar('She dont know what to did.');             -- She doesn't know what to do.

-- Mask: name the kinds of information to hide
SELECT ai_mask('John Doe lives in New York. His email is john.doe@example.com.', array('person', 'email'));
-- [MASKED] lives in New York. His email is [MASKED].

-- Translate: language code, name or phrase. No source argument.
SELECT ai_translate('Hello, how are you?', 'es');               -- Hola, ¿cómo estás?

-- Summarize with a target length (default 50 words; 0 removes the limit)
SELECT ai_summarize('Apache Spark is a unified analytics engine for large-scale data processing.', 20);

-- Similarity: 1 means equal. Use for RANKING only.
SELECT ai_similarity('Apache Spark', 'Apache Spark');           -- 1.0
SELECT company_name FROM customers ORDER BY ai_similarity(company_name, 'Databricks') DESC LIMIT 10;
```

**`ai_classify` v2.1** (recommended):

```sql
-- Labels are a JSON array string, or a JSON object of label -> description
SELECT ai_classify('My password is leaked.', '["urgent", "not_urgent"]', MAP('version', '2.1'));

-- Confidence and rationale
SELECT ai_classify('My password is leaked.', '["urgent", "not_urgent"]',
                   MAP('version', '2.1', 'enableConfidenceScores', 'true', 'enableRationales', 'true'));
-- {"response":[{"value":"urgent","confidence_score":0.97}],"metadata":{"version":"2.1"},"error_message":null}

-- Multi-label, with descriptions and a global instruction
SELECT ai_classify(
  'The charger overheated and support never replied',
  '{"hardware": "Physical product defects", "support": "Customer service quality", "billing": "Payments and invoices"}',
  MAP('version', '2.1', 'multilabel', 'true', 'instructions', 'Classify customer complaints'));

-- Read the label out of the VARIANT
SELECT ai_classify(review, '["positive","negative"]', MAP('version', '2.1')):response[0].value::STRING AS label
FROM reviews;
```

Limits: 2 to 500 unique labels (v2.x), label names up to 100 characters, descriptions up to 1,000, total context up to 1 million tokens. v1.0 allows only 2 to 20 labels and returns a plain `STRING`. **v2.1's output is not compatible with v2.0**, so read the label from `value`.

**`ai_extract` v2.1** (recommended):

```sql
-- Simple: a JSON array of field names
SELECT ai_extract('John Smith lives in San Francisco and works for Snowflake', '["name", "city", "employer"]');

-- Typed schema with descriptions, enums and nesting
SELECT ai_extract(
  invoice_text,
  '{"vendor":   {"type": "string",  "description": "Vendor name"},
    "total":    {"type": "number",  "description": "Total amount due"},
    "currency": {"type": "enum",    "labels": ["AUD", "USD", "EUR"]},
    "paid":     {"type": "boolean"}}',
  MAP('version', '2.1', 'enableConfidenceScores', 'true', 'instructions', 'Invoices are in Australian format'))
FROM invoices;

-- Read a field from the VARIANT
SELECT ai_extract(invoice_text, '["vendor","total"]'):response.vendor.value::STRING AS vendor FROM invoices;
```

Limits: at most **256 fields**, field names up to 150 characters, **12 levels** of nesting, **500 enum values**, 1 million tokens. `mode => 'precision'` helps long documents and complex schemas. `enableCitations` returns character offsets (text) or bounding boxes (documents). Mismatched types for integer/number/boolean/enum return an error.

### 2.3 Documents, audio and search preparation

```sql
-- Parse documents (PDF, JPG/PNG, TIFF, DOC/DOCX, PPT/PPTX). Input is BINARY, not a path.
SELECT path, ai_parse_document(content)
FROM read_files('/Volumes/path/to/your/directory', format => 'binaryFile');

-- Options: page range (1-indexed), image output, descriptions for figures
SELECT ai_parse_document(content, map('version', '2.0', 'pageRange', '1,3,5-10',
                                      'imageOutputPath', '/Volumes/main/docs/images/'))
FROM read_files('/Volumes/main/docs/pdfs', format => 'binaryFile');

-- Compose: parse, then classify and extract from the VARIANT output
WITH parsed AS (
  SELECT path, ai_parse_document(content) AS doc
  FROM read_files('/Volumes/main/docs/pdfs', format => 'binaryFile')
)
SELECT path,
       ai_classify(doc, '["invoice","contract","report"]', MAP('version', '2.1'))  AS doc_type,
       ai_extract(doc, '["vendor","total"]', MAP('version', '2.1'))               AS fields
FROM parsed;

-- Transcribe audio (Beta): FILE or BINARY in, speaker-labelled segments out
SELECT audio.uri AS path, ai_transcribe(audio) AS transcription
FROM my_catalog.my_schema.audio_files;

-- Prepare text or parsed documents for a search index: chunks ready to embed and to retrieve
SELECT ai_prep_search('Quarterly revenue grew twenty percent year over year.', options => map('version', '2.0'));
```

`ai_parse_document`: 500 pages and 100 MB per document; the `VARIANT` has `document.pages[]`, `document.elements[]` (type, content, confidence, bbox), `error_status[]` and `metadata`. Element types include text, table (returned as **HTML**), figure, title, caption, section_header, page_header/footer, page_number, footnote, signature. If the document has more than 500 pages and you give no `pageRange`, it **fails without parsing**. `ai_transcribe`: English and Spanish, MP3/WAV/FLAC/Opus/M4A (no video), up to 1 hour and 512 MB; Beta, an admin must enable it.

### 2.4 Reasoning over rows: `ai_decide`, `ai_enrich`, `ai_search` (Beta)

```sql
-- ai_decide: several typed questions about one record in a single call
SELECT ai_decide(
  '{"name": "TrailShell jacket", "description": "Lightweight waterproof hiking jacket made from recycled polyester."}',
  '{
    "category": {"type": "choice", "instructions": "Which category fits best?",
                 "criteria": {"outerwear": "Jackets and coats", "footwear": "Shoes and boots", "accessories": "Bags and hats"}},
    "recycled_materials": {"type": "noul", "instructions": "Does the listing say it uses recycled materials?"},
    "hiking_suitability": {"type": "score", "instructions": "How suitable is it for hiking in rain?",
                           "criteria": ["Not suitable", "Some protection", "Designed for rainy hiking"]}
  }',
  map('version', '1.0')) AS decision;
-- question types: noul (yes/no/unknown style), choice, score

-- ai_enrich: fill new columns for a row, optionally grounded by web search or a vector index
SELECT ai_enrich(company_name, '["industry", "headquarters_country", "year_founded"]',
                 PARSE_JSON('[{"type": "web_search", "config": {}}]')) AS result
FROM sales.accounts.companies;

-- ai_search: retrieve from AI Search indexes and optionally generate a grounded answer
SELECT ai_search(
  'How do I configure auto-scaling for my SQL warehouse?',
  PARSE_JSON('[{"type": "vector_search",
                "config": {"index_name": "prod_catalog.docs.support_articles",
                           "text_col": "article_body", "doc_uri_col": "article_url"}}]')) AS result;
```

`ai_search` takes up to **10 sources** (`vector_search` or `lakebase_search`), returns `document[]`, `answer` and optional `citations`, and `generate_answer` defaults to `'true'` (`generate_citations` needs `generate_answer`). `ai_enrich` allows at most one `web_search` source per call and `enableRationale` defaults to `'true'`.

### 2.5 Predictive and analytic table functions

These are **table-valued**: they take `TABLE(...)` and are used in `FROM`. Pass scalar arguments **by name**.

```sql
-- Forecast (version 2 is the recommended Beta; version 1 is the default)
WITH aggregated AS (
  SELECT DATE(tpep_pickup_datetime) AS ds, SUM(fare_amount) AS revenue
  FROM samples.nyctaxi.trips GROUP BY 1
)
SELECT * FROM AI_FORECAST(TABLE(aggregated), horizon => '2016-03-31',
                          time_col => 'ds', value_col => 'revenue', version => '2');
-- returns only FUTURE rows: ds, revenue_forecast, revenue_upper, revenue_lower

-- Anomaly detection: expected value, bounds, score (0 to 1) and a flag per row
SELECT * FROM ai_detect_anomalies(TABLE(daily_metric), time_col => 'ds', value_col => 'metric');
-- first 8 rows of each series are context: expected/score NULL, is_anomaly FALSE

-- Top drivers: which segments explain a change between test and control
SELECT * FROM ai_top_drivers(input => TABLE(input), metric => 'fare_amount', is_test => 'is_test',
                             dimensions => ARRAY('pickup_zip'), aggregation => 'sum')
ORDER BY ABS(change) DESC;

-- Predict: rows with a known target train the model; rows with a NULL target are scored
SELECT * FROM ai_predict_class(input => TABLE(customers), target_col => 'churned',
                               feature_cols => ARRAY('tenure', 'plan'), seed => 42);
-- adds churned_prediction and churned_confidence, and returns ONLY the NULL-target rows

SELECT * FROM ai_predict_value(input => TABLE(sales), target_col => 'revenue',
                               feature_cols => ARRAY('advertising_spend', 'region'), seed => 42);
-- adds revenue_prediction (DOUBLE)
```

Notes: `ai_forecast` output has `{v}_forecast`, `{v}_upper`, `{v}_lower` per value column; `ai_detect_anomalies` allows at most **8,192 rows per series**, unique timestamps per series and one value column per call (`anomaly_threshold` defaults to 0.95); `ai_top_drivers` needs **Photon** and Runtime 16.1+, and `min_support` defaults to 0.05.

### 2.6 Vector search and vector math

```sql
-- Query an AI Search (Vector Search) index. All arguments by name. num_results max 100, default 10.
SELECT * FROM vector_search(index => 'main.support_docs.index', query_text => 'Wi-Fi issues LMP-9R2',
                            query_type => 'HYBRID', num_results => 3);
-- query_type is ANN (default) or HYBRID; HYBRID requires query_text

-- Vector math on ARRAY<FLOAT> (Runtime 18.1+). Other element types raise an error.
SELECT vector_cosine_similarity(array(1.0f, 2.0f, 3.0f), array(4.0f, 5.0f, 6.0f));   -- 0.9746318461970762
SELECT vector_cosine_similarity(array(1.0f, 0.0f), array(0.0f, 1.0f));                -- 0.0
```

Related: `vector_inner_product`, `vector_l2_distance`, `vector_norm`, `vector_normalize`, and the aggregates `vector_avg`, `vector_sum`. Limits for `vector_search`: `DIRECT_ACCESS` indexes cannot be queried, `filters_json` and `columns` are unsupported, and it is not available on classic SQL warehouses.

---

## 3. Operators, conditional and NULL handling

| Function / operator | What it does | Trap |
| --- | --- | --- |
| `if(c, a, b)` / `iff(c, a, b)` | Inline conditional | Same function |
| `CASE WHEN ... END` | Branching | No `ELSE` returns NULL |
| `coalesce(a, b, ...)`, `nvl`, `ifnull` | First non-NULL | |
| `nvl2(x, if_not_null, if_null)` | Branch on NULL-ness | |
| `nullif(a, b)` | NULL if equal | |
| `nullifzero(x)`, `zeroifnull(x)` | Zero to NULL / NULL to zero | |
| `a <=> b`, `equal_null(a, b)` | **NULL-safe equality** | `NULL = NULL` is NULL, `NULL <=> NULL` is TRUE |
| `greatest`, `least` | Max/min across columns | **Skip NULLs** (unlike many engines); NULL only if all are NULL |
| `decode(expr, k1, v1, ..., default)` | Value lookup | There is also a character-set `decode(bin, 'utf-8')`; NULLs match |
| `a IS DISTINCT FROM b` | NULL-safe inequality | |
| `assert_true(cond [, msg])`, `raise_error(msg)` | Fail the query on purpose | Good for data checks |
| `x:path`, `x::type`, `x[i]`, `\|\|` | JSON/VARIANT path, cast, index, concat | |

```sql
SELECT order_id,
       if(amount >= 100, 'large', 'small')          AS size,        -- NULL amount -> 'small'
       coalesce(amount, 0)                          AS amount_filled,
       nvl2(amount, 'has amount', 'no amount')      AS flag,
       CASE status WHEN 'shipped' THEN 'done' WHEN 'returned' THEN 'problem' ELSE 'open' END AS stage,
       decode(country, 'AU', 'Australia', 'NZ', 'New Zealand', 'Other') AS country_name,
       try_divide(10, order_id - 3)                 AS safe_div,    -- order 3 -> NULL, not an error
       zeroifnull(amount)                           AS amount_zero
FROM orders;

SELECT NULL <=> NULL, NULL = NULL;                  -- true, NULL
SELECT greatest(3, NULL, 9), least(3, NULL, 9);     -- 9, 3   (NULLs skipped)
SELECT assert_true(count(*) > 0, 'orders is empty') FROM orders;
```

---

## 4. Conversion and `try_` functions

Databricks SQL runs with **ANSI mode** on by default, so invalid casts and arithmetic **raise errors**. The `try_` family returns NULL instead.

| Function | Use | Trap |
| --- | --- | --- |
| `cast(x AS T)`, `x::T` | Convert | Errors on bad input under ANSI mode |
| `try_cast(x AS T)` | Convert or NULL | |
| `to_number(s, fmt)`, `try_to_number` | Parse formatted numbers | Format uses `9`, `0`, `,`, `.` |
| `to_date`, `to_timestamp`, `try_to_timestamp`, `try_to_date` | Parse dates | Pattern letters are case-sensitive: `MM` month, `mm` minute |
| `to_char(x, fmt)`, `to_varchar` | Format | |
| `try_add`, `try_subtract`, `try_multiply`, `try_divide`, `try_mod` | Safe arithmetic | `try_divide(x, 0)` is NULL |
| `try_element_at`, `try_variant_get`, `try_parse_json`, `try_sum`, `try_avg` | Safe lookups and aggregates | `try_sum`/`try_avg` return NULL on overflow |
| `typeof(x)` | Data type name | |

```sql
SELECT cast('42' AS INT) + 1;                         -- 43
SELECT try_cast('abc' AS INT);                        -- NULL
SELECT try_to_timestamp('2026-13-45');                -- NULL
SELECT to_date('09/10/2026', 'dd/MM/yyyy');           -- 2026-10-09
SELECT to_number('1,234.50', '9,999.99');             -- 1234.50
SELECT try_divide(10, 0), try_add(2147483647, 1);     -- NULL, NULL (no error)
SELECT typeof(1.5), typeof(array(1, 2));              -- decimal(2,1), array<int>
SELECT 10 / 0;                                        -- error under ANSI mode (DIVIDE_BY_ZERO)
```

---

## 5. Date and time

| Function | Use | Trap |
| --- | --- | --- |
| `current_date()`, `current_timestamp()`, `now()`, `current_timezone()` | Now | Session time zone |
| `dateadd(unit, n, d)`, `date_add(d, n)`, `date_sub(d, n)`, `add_months(d, n)` | Add | `dateadd` takes the unit first; `date_add` takes days |
| `datediff(unit, start, end)` vs `datediff(end, start)` | Difference | **Argument order flips** between the unit form and the two-argument days form |
| `timestampdiff`, `timestampadd`, `months_between` | More differences | `months_between` returns a fractional number |
| `date_trunc('MONTH', ts)`, `trunc(d, 'MM')` | Truncate | `date_trunc` takes the unit first and returns a **timestamp**; `trunc` takes the date first and returns a **date** |
| `extract(part FROM d)`, `date_part`, `year`, `month`, `day`, `dayofweek`, `weekofyear`, `quarter` | Parts | `dayofweek`: 1 = Sunday |
| `date_format(ts, fmt)` | Format | Pattern letters: `yyyy-MM-dd HH:mm:ss` |
| `last_day`, `next_day(d, 'Mon')`, `dayname`, `monthname` | Calendar | |
| `make_date(y, m, d)`, `make_timestamp(...)`, `make_interval(...)` | Build | |
| `convert_timezone([src,] tgt, ts)`, `from_utc_timestamp`, `to_utc_timestamp` | Time zones | `from_utc_timestamp` treats the input as UTC |
| `unix_timestamp`, `from_unixtime`, `timestamp_seconds/millis/micros` | Epoch | |
| `window(ts, '10 minutes')`, `session_window`, `time_bucket` | Time bucketing | `window` returns a struct with `start` and `end` |

```sql
SELECT dateadd(DAY, 7, DATE'2026-10-09');                            -- 2026-10-16
SELECT datediff(DAY, DATE'2026-10-01', DATE'2026-10-09');            -- 8   (unit form: start, end)
SELECT datediff(DATE'2026-10-09', DATE'2026-10-01');                 -- 8   (two-arg form: END first)
SELECT date_trunc('MONTH', DATE'2026-10-09');                        -- 2026-10-01 00:00:00 (a TIMESTAMP)
SELECT trunc(DATE'2026-10-09', 'MM');                                -- 2026-10-01
SELECT last_day(DATE'2026-02-10'), next_day(DATE'2026-10-09', 'Mon');
SELECT extract(YEAR FROM DATE'2026-10-09'), dayname(DATE'2026-10-09'), quarter(DATE'2026-10-09');
SELECT date_format(TIMESTAMP'2026-10-09 14:30:00', 'yyyy-MM-dd HH:mm');
SELECT convert_timezone('UTC', 'Australia/Sydney', TIMESTAMP_NTZ'2026-10-09 00:00:00');
SELECT from_utc_timestamp(TIMESTAMP'2026-10-09 00:00:00', 'Australia/Sydney');

-- Monthly revenue
SELECT date_trunc('MONTH', order_date) AS month, sum(amount) AS revenue FROM orders GROUP BY 1 ORDER BY 1;

-- Calendar spine of 10 days
SELECT explode(sequence(DATE'2026-10-01', DATE'2026-10-10', INTERVAL 1 DAY)) AS d;

-- 15-minute buckets for streaming-style aggregation
SELECT window(event_ts, '15 minutes') AS w, count(*) FROM events GROUP BY window(event_ts, '15 minutes');
```

---

## 6. String and regular expressions

| Function | Use | Trap |
| --- | --- | --- |
| `concat(...)`, `\|\|`, `concat_ws(sep, ...)` | Join | `concat` and `\|\|` return NULL if any input is NULL; `concat_ws` skips NULLs and accepts arrays |
| `split(s, regex [, limit])` | String to array | **The separator is a regular expression**: escape `.` and `\|` |
| `split_part(s, delim, n)` | n-th piece | **1-based**; delimiter is literal |
| `substring(s, pos, len)`, `substr`, `left`, `right`, `substring_index(s, delim, n)` | Slice | `pos` is 1-based |
| `trim`, `ltrim`, `rtrim`, `btrim(s, chars)` | Strip | |
| `upper`, `lower`, `initcap`, `length`, `reverse`, `repeat`, `lpad`, `rpad` | Basics | `length` counts characters |
| `replace`, `translate`, `overlay` | Replace | `translate` is per character |
| `contains`, `startswith`, `endswith`, `instr`, `locate`, `position`, `charindex` | Find | |
| `like`, `ilike`, `like any/all`, `rlike` / `regexp` / `regexp_like` | Pattern match | `rlike` matches **anywhere** in the string (not the whole string) |
| `regexp_extract(s, re, idx)`, `regexp_extract_all`, `regexp_replace`, `regexp_count`, `regexp_instr`, `regexp_substr` | Regex | Index `0` is the whole match; non-matching returns `''` for `regexp_extract` |
| `levenshtein`, `soundex` | Fuzzy | |
| `format_number(x, d)`, `format_string`, `printf`, `mask`, `sentences` | Formatting and masking | |
| `parse_url`, `url_encode`, `url_decode`, `base64`, `unbase64`, `encode`, `decode`, `hex`, `unhex` | Encoding | |

```sql
SELECT concat_ws('-', 'a', NULL, 'c');                      -- a-c
SELECT 'a' || NULL;                                         -- NULL
SELECT split('a,b,c', ',');                                 -- ["a","b","c"]
SELECT split('a.b.c', '\\.');                               -- escape the dot, the separator is a regex
SELECT split_part('a,b,c', ',', 2);                         -- b
SELECT substring('snowflake', 1, 4);                        -- snow
SELECT substring_index('www.example.com', '.', 2);          -- www.example
SELECT lpad('7', 3, '0'), initcap('hello world');           -- 007, Hello World
SELECT translate('2*3+4', '*+', 'x-');                      -- 2x3-4
SELECT levenshtein('kitten', 'sitting');                    -- 3
SELECT mask('AbCd-1234');                                   -- XxXx-nnnn

SELECT regexp_extract('order 4521 shipped', '([0-9]+)', 1); -- 4521
SELECT regexp_extract_all('a1b22c333', '([0-9]+)', 1);      -- ["1","22","333"]
SELECT regexp_replace('a1b22c', '[0-9]+', '#');             -- a#b#c
SELECT regexp_count('a1b22c333', '[0-9]+');                 -- 3
SELECT 'abc123 tail' RLIKE '[a-z]+[0-9]+';                  -- true (matches anywhere)

SELECT * FROM orders WHERE customer ILIKE 'AL%';
SELECT * FROM orders WHERE customer LIKE ANY ('al%', 'bo%');
SELECT parse_url('https://example.com/a?x=1', 'HOST');      -- example.com
```

---

## 7. Numeric

| Function | Use | Trap |
| --- | --- | --- |
| `round(x, n)`, `bround(x, n)`, `ceil`, `floor` | Rounding | `round` is half-up, `bround` is half-even ("banker's") |
| `abs`, `sign`, `pmod`, `mod`, `power`, `sqrt`, `ln`, `log10`, `exp` | Maths | `%`/`mod` takes the dividend's sign, `pmod` is always non-negative |
| `try_divide`, `try_add`, `try_multiply` | Safe arithmetic | See section 4 |
| `width_bucket(x, lo, hi, n)` | Histogram bucket | Out of range returns 0 or n+1 |
| `rand([seed])`, `randn`, `uniform(lo, hi [, seed])`, `randstr` | Random | Not reproducible without a seed |
| `div` | Integer division | |
| `bit_count`, `shiftleft`, `&`, `\|`, `^`, `~` | Bitwise | |
| `isnan`, `nanvl` | NaN handling | `NaN = NaN` is true in Spark |

```sql
SELECT round(2.567, 2), bround(2.5, 0), round(2.5, 0), ceil(2.1), floor(2.9);   -- 2.57, 2, 3, 3, 2
SELECT pmod(-7, 3), -7 % 3;                                                    -- 2, -1
SELECT width_bucket(45.25, 0, 200, 4);                                         -- 1
SELECT uniform(1, 100, 42);                                                    -- reproducible with a seed
SELECT customer, sum(amount) AS total,
       round(100 * sum(amount) / sum(sum(amount)) OVER (), 1) AS pct
FROM orders GROUP BY customer;
```

---

## 8. Aggregate

Aggregates ignore NULLs (except `count(*)`). Any aggregate can take a `FILTER (WHERE ...)` clause.

| Function | Use | Trap |
| --- | --- | --- |
| `count(*)`, `count(col)`, `count(DISTINCT col)`, `count_if(cond)` | Counting | `count(col)` skips NULLs |
| `sum`, `avg`, `min`, `max`, `try_sum`, `try_avg` | Basics | `try_sum`/`try_avg` return NULL on overflow instead of an error |
| `max_by(val, key)`, `min_by(val, key)` | Value at max/min of another column | "latest row per key" |
| `first(x [, ignoreNulls])`, `last(...)`, `any_value(x)` | Pick a value | `first`/`last` are **nondeterministic** without ordering |
| `collect_list(x)`, `collect_set(x)`, `array_agg(x)` | Rows to array | `collect_list` has **no guaranteed order** |
| `listagg(x [, sep]) [WITHIN GROUP (ORDER BY ...)]`, `string_agg` | Rows to string | **Order is undefined without `WITHIN GROUP`** (the reference's own example shows `acb`); NULLs ignored; with `DISTINCT` the sort key must equal the expression |
| `median(x)`, `mode(x)`, `percentile(x, p)`, `percentile_cont(p) WITHIN GROUP (ORDER BY x)`, `percentile_disc` | Exact stats | `percentile` is exact and can be expensive |
| `approx_percentile(x, p)` / `percentile_approx`, `approx_count_distinct(x)`, `approx_top_k(x, k)` | Approximate | Cheap on big data |
| `stddev`, `variance`, `corr`, `covar_pop`, `regr_*`, `skewness`, `kurtosis` | Statistics | |
| `bool_and/every`, `bool_or/some/any`, `bit_and/or/xor` | Boolean/bitwise | |
| `grouping`, `grouping_id`, `ROLLUP`, `CUBE`, `GROUPING SETS`, `GROUP BY ALL` | Grouping | `GROUP BY ALL` groups by every non-aggregate select column |
| `histogram_numeric(x, n)`, `count_min_sketch` | Distribution | |

```sql
SELECT count(*) AS all_rows,                                -- 5
       count(amount) AS with_amount,                        -- 4
       count_if(status = 'shipped') AS shipped,             -- 3
       sum(amount) AS total,                                -- 445.75
       median(amount), mode(country),
       count(*) FILTER (WHERE country = 'AU') AS au_orders  -- 3
FROM orders;

SELECT customer,
       listagg(status, ', ') WITHIN GROUP (ORDER BY order_date) AS statuses,   -- ordered
       collect_list(order_id)                                    AS ids,        -- order not guaranteed
       max_by(status, order_date)                                AS latest_status,
       approx_count_distinct(country)                            AS countries
FROM orders GROUP BY customer;

SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY amount) AS p90_exact,
       approx_percentile(amount, 0.9)                      AS p90_approx
FROM orders;

SELECT country, customer, sum(amount) FROM orders GROUP BY ROLLUP (country, customer);
SELECT country, sum(amount) AS total FROM orders GROUP BY ALL;

-- Pivot rows to columns
SELECT * FROM (SELECT customer, status, amount FROM orders)
PIVOT (sum(amount) FOR status IN ('shipped', 'returned', 'pending'));
```

---

## 9. Window functions and `QUALIFY`

Syntax: `function OVER { window_name | (window_spec) }` where `window_spec` is `PARTITION BY`, `ORDER BY` and an optional frame. Aliases: `DISTRIBUTE BY` = `PARTITION BY`, `SORT BY` = `ORDER BY`.

| Group | Functions | Rule |
| --- | --- | --- |
| Ranking | `row_number`, `rank`, `dense_rank`, `ntile`, `percent_rank`, `cume_dist` | **Require `ORDER BY`; do not accept a frame clause** |
| Analytic | `lag`, `lead`, `first_value`, `last_value`, `nth_value` | Position based; `lag/lead` take an offset and default |
| Aggregate | `sum`, `avg`, `count`, `min`, `max`, `median` ... `OVER` | Cannot use `FILTER` when used as a window function; `DISTINCT` is unsupported in windows |

```sql
-- Latest order per customer, no subquery
SELECT * FROM orders
QUALIFY row_number() OVER (PARTITION BY customer ORDER BY order_date DESC) = 1;

-- Change versus previous order, with a default for the first row
SELECT order_id, order_date, amount,
       amount - lag(amount, 1, 0) OVER (ORDER BY order_date) AS change_vs_prev
FROM orders;

-- Running total and a 3-row moving average
SELECT order_id,
       sum(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       avg(amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)         AS moving_avg_3
FROM orders;

-- Named window, reused
SELECT order_id,
       row_number() OVER w AS rn,
       rank()       OVER w AS rnk
FROM orders
WINDOW w AS (PARTITION BY customer ORDER BY order_date);

-- last_value needs a widened frame
SELECT order_id,
       last_value(status) OVER (PARTITION BY customer ORDER BY order_date
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS final_status
FROM orders;

-- ROWS counts physical rows; RANGE groups ties and works on value distance
SELECT order_id,
       sum(amount) OVER (ORDER BY order_date RANGE BETWEEN INTERVAL 3 DAYS PRECEDING AND CURRENT ROW) AS last_3_days
FROM orders;
```

Errors to recognise: `MISSING_WINDOW_SPECIFICATION`, `WINDOW_FUNCTION_AND_FRAME_MISMATCH` (a frame on a ranking function), `DISTINCT_WINDOW_FUNCTION_UNSUPPORTED`.

---

## 10. Arrays, maps, structs and lambda functions

### Collections

| Function | Use | Trap |
| --- | --- | --- |
| `array(...)`, `sequence(a, b [, step])`, `array_repeat(x, n)` | Build | `sequence` works on numbers and dates |
| `size(a)` / `cardinality`, `array_size` | Length | `size(NULL)` is -1 in non-ANSI mode, NULL in ANSI mode |
| `array_contains(a, x)`, `array_position(a, x)` | Search | `array_position` is **1-based**, 0 if absent |
| `element_at(a, i)`, `a[i]`, `try_element_at` | Access | `a[i]` is **0-based**; `element_at` is **1-based**; out of range errors under ANSI unless `try_` |
| `array_distinct`, `array_union`, `array_intersect`, `array_except`, `arrays_overlap` | Set operations | |
| `array_append`, `array_prepend`, `array_insert`, `array_remove`, `array_compact`, `slice`, `flatten`, `array_join` | Edit | `array_join` skips NULL unless a replacement is given |
| `array_sort(a [, comparator])`, `sort_array(a [, asc])`, `array_min/max`, `shuffle`, `arrays_zip` | Order | |
| `map(k, v, ...)`, `map_from_arrays`, `map_keys`, `map_values`, `map_entries`, `map_concat`, `map_contains_key`, `str_to_map` | Maps | |
| `struct(...)`, `named_struct('a', 1, ...)` | Structs | `struct(*)` bundles all columns |

```sql
SELECT array(1, 2, 3, 3), array_distinct(array(1, 2, 3, 3));                     -- [1,2,3,3], [1,2,3]
SELECT array_contains(array(1, 2, 3), 2), array_position(array(10, 20, 30), 20); -- true, 2
SELECT array(10, 20, 30)[0], element_at(array(10, 20, 30), 1);                   -- 10, 10   (0-based vs 1-based)
SELECT slice(array(10, 20, 30, 40), 2, 2);                                       -- [20,30]
SELECT array_union(array(1, 2), array(2, 3)), array_intersect(array(1, 2), array(2, 3));
SELECT array_join(array('a', 'b'), '-');                                         -- a-b
SELECT map('a', 1, 'b', 2)['b'], map_keys(map('a', 1, 'b', 2));                   -- 2, ["a","b"]
SELECT named_struct('id', 1, 'name', 'alice').name;                              -- alice
```

### Lambda functions (higher-order)

Syntax: `param -> expr` or `(p1, p2) -> expr`. The expression cannot contain a subquery or a SQL UDF. Functions that take lambdas: `transform`, `filter`, `aggregate` (alias `reduce`), `exists`, `forall`, `map_filter`, `transform_keys`, `transform_values`, `zip_with`, `map_zip_with`, `array_sort`.

```sql
SELECT transform(array(1, 2, 3), x -> x * 2);                          -- [2,4,6]
SELECT transform(array(10, 20, 30), (x, i) -> x + i);                  -- [10,21,32]  (second parameter is the index)
SELECT filter(array(1, NULL, 3, 5, NULL), x -> x IS NOT NULL);         -- [1,3,5]
SELECT aggregate(array(1, 2, 3), 0, (acc, x) -> acc + x);              -- 6
SELECT aggregate(array(1, 2, 3), 0, (acc, x) -> acc + x, acc -> acc * 10);   -- 60   (final step)
SELECT exists(array(1, 2, 3), x -> x > 2), forall(array(1, 2, 3), x -> x > 0);   -- true, true
SELECT zip_with(array(1, 2), array(10, 20), (a, b) -> a + b);          -- [11,22]
SELECT map_filter(map('a', 1, 'b', 5), (k, v) -> v > 2);               -- {"b":5}
SELECT transform_values(map('a', 1, 'b', 2), (k, v) -> v * 10);        -- {"a":10,"b":20}
-- Custom sort: reverse-string order
SELECT array_sort(array('Hello', 'World'),
       (p1, p2) -> CASE WHEN p1 = p2 THEN 0 WHEN reverse(p1) < reverse(p2) THEN -1 ELSE 1 END);   -- [World, Hello]
```

---

## 11. JSON and VARIANT

Two ways to hold semi-structured data: a **JSON `STRING`** (parse each time) or the **`VARIANT`** type (parsed once, faster, schema-flexible). Prefer VARIANT for new tables.

| Function | Use | Trap |
| --- | --- | --- |
| `col:a.b[0]` | Path into a STRING of JSON **or** a VARIANT | Keys are case-sensitive; result is VARIANT/STRING until cast with `::` |
| `get_json_object(s, '$.a.b')`, `json_tuple(s, 'a', 'b')` | Older string extraction | Returns STRING |
| `from_json(s, 'a INT, b STRING')`, `to_json(x)`, `schema_of_json(s)` | JSON to struct and back | Needs a schema (DDL string or `schema_of_json`) |
| `json_array_length(s)`, `json_object_keys(s)` | Inspect | |
| `parse_json(s)`, `try_parse_json(s)` | STRING to VARIANT | `try_` returns NULL on bad JSON |
| `variant_get(v, '$.path', 'type')`, `try_variant_get(...)` | Typed extraction | Missing path returns NULL; bad cast raises `INVALID_VARIANT_CAST` (the `try_` form returns NULL) |
| `schema_of_variant(v)`, `schema_of_variant_agg`, `is_variant_null`, `to_variant_object` | Inspect and convert | |
| `variant_explode(v)`, `variant_explode_outer` | Explode a VARIANT array/object | |
| `from_xml`, `to_xml`, `xpath*` | XML | |

```sql
-- STRING path syntax
SELECT '{"user":{"name":"alice","tags":["a","b"]}}':user.name;                     -- "alice"
SELECT get_json_object('{"a":{"b":1}}', '$.a.b');                                  -- 1

-- Parse into a struct with an explicit schema
SELECT from_json('{"id":1,"name":"alice"}', 'id INT, name STRING').name;            -- alice
SELECT to_json(named_struct('id', 1, 'name', 'alice'));                             -- {"id":1,"name":"alice"}

-- VARIANT
WITH raw AS (
  SELECT parse_json('{"key": 123, "data": [4, {"a": "hello"}, "str"]}') AS v
)
SELECT variant_get(v, '$.data[1].a', 'string')   AS a,         -- hello
       variant_get(v, '$.missing', 'int')        AS missing,   -- NULL
       try_variant_get(v, '$.key', 'array<int>') AS bad_cast,  -- NULL (variant_get would raise an error)
       v:key::INT                                AS key_int    -- 123
FROM raw;

-- Explode a JSON array of objects into rows
SELECT item.sku, item.qty
FROM (SELECT from_json('{"items":[{"sku":"X1","qty":2},{"sku":"Y2","qty":5}]}',
                       'items ARRAY<STRUCT<sku: STRING, qty: INT>>') AS j) t
LATERAL VIEW explode(t.j.items) e AS item;

SELECT try_parse_json('{bad json');                                                 -- NULL
```

---

## 12. Generators and table-valued functions

| Function | Use | Trap |
| --- | --- | --- |
| `explode(arr or map)`, `explode_outer` | One row per element | `explode` **drops** rows whose array is NULL/empty; `_outer` keeps them |
| `posexplode`, `posexplode_outer` | Element plus position | Position is **0-based** |
| `inline(array_of_structs)`, `inline_outer` | Struct array to columns | |
| `stack(n, v1, v2, ...)` | Unpivot | `n` is the number of **rows** to produce |
| `range(start, end [, step])` | Number table | `end` is **exclusive** |
| `read_files(path, ...)` | Read files from storage/volumes | Options need `=>`; `_metadata` is not in `SELECT *` |
| `table_changes('tbl', start_version)` | Delta change data feed | Needs CDF enabled |
| `event_log`, `list_files`, `read_kafka`, `read_kinesis`, `remote_query`, `http_request` | Specialised sources | |
| `secret('scope', 'key')`, `list_secrets` | Secrets | Redacted in output |

```sql
SELECT explode(array('a', 'b'));                                         -- two rows
SELECT posexplode(array('a', 'b'));                                      -- (0,a), (1,b)
SELECT inline(array(struct(1, 'x'), struct(2, 'y')));                    -- columns col1, col2
SELECT stack(2, 'Q1', 10, 'Q2', 20) AS (quarter, revenue);               -- unpivot into 2 rows
SELECT * FROM range(1, 11, 2);                                           -- 1,3,5,7,9

-- LATERAL VIEW (older syntax) and LATERAL join (newer)
SELECT id, tag FROM (SELECT 1 AS id, array('a', 'b') AS tags) LATERAL VIEW explode(tags) t AS tag;

-- Files
SELECT * FROM read_files('s3://bucket/path', format => 'csv', schema => 'id int, ts timestamp, event string');
SELECT * EXCEPT (content), _metadata FROM read_files('/Volumes/my_catalog/my_schema/my_volume', format => 'binaryFile');
CREATE TABLE my_avro_data AS SELECT *, _metadata.file_path FROM read_files('gs://my-bucket/avroData');
CREATE OR REFRESH STREAMING TABLE avro_data AS SELECT * FROM STREAM read_files('gs://my-bucket/avroData', includeExistingFiles => false);

-- Change data feed
SELECT * FROM table_changes('main.sales.orders', 2);
```

`read_files` options worth knowing: `format` (`csv`, `json`, `parquet`, `avro`, `orc`, `xml`, `text`, `binaryFile`), `schema` (a DDL string), `schemaHints`, `inferColumnTypes` (default true), `partitionColumns`, and `schemaEvolutionMode => 'none'` (drops the default rescued-data column). `_metadata` holds `file_path`, `file_name`, `file_size`, `file_modification_time`, `file_block_start`, `file_block_length`.

---

## 13. Hash, context and miscellaneous

| Function | Returns |
| --- | --- |
| `hash(...)`, `xxhash64(...)` | Fast non-cryptographic 32-bit / 64-bit hash |
| `md5(x)`, `sha1(x)`, `sha2(x, 256)`, `crc32(x)`, `hmac(...)` | Digests |
| `uuid()` | Random UUID string |
| `base64`, `unbase64`, `hex`, `unhex`, `zstd_compress`, `zstd_decompress` | Encoding and compression |
| `aes_encrypt`, `aes_decrypt`, `try_aes_decrypt` | Encryption |
| `current_user()`, `session_user()`, `current_catalog()`, `current_schema()`, `current_metastore()`, `current_version()`, `version()` | Context |
| `is_member('group')`, `is_account_group_member('group')` | Group membership, used in **row filters and column masks** |
| `monotonically_increasing_id()`, `spark_partition_id()`, `input_file_name()` | Execution info (`input_file_name` is limited under Unity Catalog; prefer `_metadata`) |
| `typeof(x)`, `assert_true`, `raise_error` | Diagnostics |

```sql
SELECT md5('databricks'), sha2('databricks', 256), crc32('databricks'), hash(customer, country) FROM orders LIMIT 1;
SELECT uuid(), current_user(), current_catalog(), current_schema(), version();

-- A governance idiom: show a column only to members of a group
SELECT CASE WHEN is_account_group_member('finance') THEN amount ELSE NULL END AS amount FROM orders;
```

---

## 14. Geospatial: `ST_` and H3

`ST_` functions work on **`GEOMETRY`** (GA) and **`GEOGRAPHY`** (Public Preview). Applies to Databricks SQL and **Runtime 17.1+**; **not available on classic SQL warehouses**. Constructors set the SRID you pass, or **0** if you omit it. In Python or Scala notebooks, import with `from pyspark.databricks.sql import functions as dbf` (see file 03).

| Category | Functions |
| --- | --- |
| Import / export | `st_geomfromtext`, `st_geomfromwkt`, `st_geomfromwkb`, `st_geogfromtext`, `st_geomfromgeojson`, `st_astext`, `st_aswkb`, `st_asgeojson`, `st_asewkt`, `st_geohash` |
| Constructors / accessors | `st_point(x, y [, srid])`, `st_makeline`, `st_makepolygon`, `st_makeenvelope`, `st_x`, `st_y`, `st_xmin` ..., `st_npoints`, `st_geometrytype`, `st_dump`, `st_collect` |
| Measurements | `st_area`, `st_length`, `st_perimeter`, `st_distance`, `st_distancesphere`, `st_distancespheroid`, `st_azimuth` |
| Relationships | `st_contains`, `st_within`, `st_intersects`, `st_covers`, `st_touches`, `st_disjoint`, `st_equals`, `st_dwithin` |
| Processing | `st_buffer`, `st_centroid`, `st_envelope`, `st_convexhull`, `st_union`, `st_union_agg`, `st_intersection`, `st_difference`, `st_simplify`, `st_transform`, `st_setsrid`, `st_srid`, `st_isvalid` |

```sql
SELECT st_astext(st_point(1.0, 2.0));                                           -- POINT(1 2)
SELECT st_asewkt(st_point(1.0, 2.0, 4326));                                     -- SRID=4326;POINT(1 2)
SELECT st_contains(st_geomfromwkt('POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'), st_point(5, 5));   -- true
SELECT st_intersects(st_geomfromwkt('LINESTRING(0 0, 10 10)'), st_geomfromwkt('LINESTRING(0 10, 10 0)'));   -- true
SELECT st_astext(st_buffer(st_point(0, 0), 1.0));

-- Two different "distance" functions
SELECT st_distance(st_geomfromtext('POINT Z (0 0 300)'), st_geomfromtext('LINESTRING(-10 10,20 10)'));   -- 10.0
--   2D Cartesian, in the UNITS OF THE COORDINATES (degrees for lon/lat!)
SELECT round(st_distancesphere(st_geomfromtext('POINT M (2 3 100)'), st_geomfromtext('POINT ZM (6 7 23 1000)')), 3);   -- 627753.245
--   metres on a sphere; both inputs must be POINTS with the SAME SRID (else ST_DIFFERENT_SRID_VALUES)

-- Points within a polygon
SELECT s.store_id FROM stores s JOIN regions r ON st_contains(r.boundary, st_point(s.lon, s.lat));
```

**Exam traps:** `st_distance` returns **coordinate units**, not metres; use `st_distancesphere` for metres between lon/lat points. Longitude comes first in `st_point(x, y)`. Different SRIDs raise `ST_DIFFERENT_SRID_VALUES`.

### H3 (hex-grid indexing)

```sql
SELECT h3_longlatash3(100, 45, 6);                -- 604116085645508607   (longitude, latitude, resolution)
SELECT h3_longlatash3(-122.4783, 37.8199, 13);    -- 635714569676958015
SELECT h3_h3tostring(h3_longlatash3(151.2093, -33.8688, 8));           -- cell id as hex text
SELECT h3_toparent(h3_longlatash3(151.2093, -33.8688, 8), 5);          -- coarser cell
SELECT h3_kring(h3_longlatash3(151.2093, -33.8688, 8), 1);             -- the cell plus neighbours within 1 step
SELECT h3_distance(cell_a, cell_b);                                    -- grid distance in cells
```

Others: `h3_polyfillash3` (cells covering a polygon), `h3_pointash3`, `h3_boundaryaswkt`, `h3_isvalid`, `h3_resolution`, `h3_compact`/`h3_uncompact`, `h3_try_*` variants that return NULL instead of an error. **Longitude first** in `h3_longlatash3`.

---

## 15. Sketches and approximate analytics

Use sketches to compute distinct counts, quantiles and set operations on huge data, then **merge** partial results.

| Family | Aggregate | Combine | Estimate |
| --- | --- | --- | --- |
| HLL (distinct count) | `hll_sketch_agg(x)` | `hll_union_agg`, `hll_union` | `hll_sketch_estimate` |
| Theta (set ops) | `theta_sketch_agg` | `theta_union_agg`, `theta_intersection_agg`, `theta_difference` | `theta_sketch_estimate` |
| KLL (quantiles) | `kll_sketch_agg_double/float/bigint` | `kll_merge_agg_*`, `kll_sketch_merge_*` | `kll_sketch_get_quantile_*`, `kll_sketch_get_rank_*` |
| Top-K | `approx_top_k_accumulate` | `approx_top_k_combine` | `approx_top_k_estimate` |

```sql
SELECT hll_sketch_estimate(hll_sketch_agg(customer)) AS approx_customers FROM orders;
SELECT approx_top_k(country, 2) FROM orders;                      -- most frequent values with counts

-- Build a sketch per day, store it, merge later
WITH daily AS (SELECT order_date, hll_sketch_agg(customer) AS s FROM orders GROUP BY order_date)
SELECT hll_sketch_estimate(hll_union_agg(s)) AS distinct_customers_all_days FROM daily;
```

---

## 16. Not covered

| Area | Where to look |
| --- | --- |
| IP address functions (`ip_cidr_contains`, `ip_network`, `ip_host` ...) | [Built-in functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin) |
| Avro/CSV/XML helpers (`from_avro`, `to_csv`, `xpath`) | Same |
| `MATCH_RECOGNIZE` helpers (`first`, `last`, `next`, `prev`, `match_number`) | Same |
| Time-type functions (`time_diff`, `time_trunc`, `make_time`) | Same |
| `cloud_files_state`, `read_pubsub`, `read_pulsar`, `read_state_metadata` | Streaming/Auto Loader docs |
| Collations (`collate`, `collation`, `collations`) | String collation docs |
| `measure`, `session_window` | Metric views and streaming docs |

## 17. Ten you should be able to write from memory

```sql
SELECT * FROM t QUALIFY row_number() OVER (PARTITION BY k ORDER BY ts DESC) = 1;               -- latest per key
SELECT try_cast(col AS INT), try_divide(a, b) FROM t;                                          -- safe conversion
SELECT v:a.b[0]::STRING, variant_get(v, '$.a.b[0]', 'string') FROM t;                          -- VARIANT path
SELECT id, e.item FROM t LATERAL VIEW explode(arr) e AS item;                                  -- explode an array
SELECT date_trunc('MONTH', d), count_if(status = 'x') FROM t GROUP BY 1;                       -- monthly count
SELECT listagg(name, ', ') WITHIN GROUP (ORDER BY name) FROM t;                                -- ORDERED concatenation
SELECT transform(arr, x -> x * 2), filter(arr, x -> x > 0), aggregate(arr, 0, (a, x) -> a + x); -- lambdas
SELECT ai_classify(txt, '["a","b"]', MAP('version', '2.1')):response[0].value::STRING FROM t;  -- classify, read the label
SELECT ai_extract(txt, '["vendor","total"]', MAP('version', '2.1')):response FROM t;            -- extract fields
SELECT * FROM read_files('/Volumes/c/s/v/', format => 'csv', schema => 'id int, name string');  -- read files
```
