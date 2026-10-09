# Original GES-C02 practice set

32 original single-answer questions (28 blueprint-weighted plus a 4-question supplement on newer functions). Approximate domain weighting of the first 28: 5 overview, 11 functions, 8 governance, 4 document processing. These are learning questions based on official objectives and documentation, **not** Snowflake practice-exam items or claimed real exam questions. Set a timer, answer before reading the key, and verify any disputed item in the linked docs. Syntax examples describe documented signatures as checked 2026-09-24; they were not run in an account.

Questions 33-49 are a **supplement on the semantic layer** at the end of this file ([08_SEMANTIC_LAYER.md](08_SEMANTIC_LAYER.md)); they sit outside the 28-question blueprint weighting.

## Questions

### Domain 1: overview

**1.** A support bot must retrieve relevant passages from thousands of policy PDFs before drafting an answer. Which component primarily supplies the managed retrieval index? A. Cortex Analyst B. Cortex Search C. Model Registry D. AI Observability

**2.** A user asks, “What were net sales by region last quarter?” The source is governed relational tables and business definitions. Which component directly turns that natural-language request into SQL grounded in a semantic view? A. Cortex Analyst B. `AI_PARSE_DOCUMENT` C. Cortex Search D. `AI_TRANSCRIBE`

**3.** A question requires a policy PDF passage and a computed sales metric. What is the most fitting orchestration layer? A. `AI_EMBED` alone B. Cortex Agents with Search and Analyst tools C. Model Registry alone D. A larger warehouse alone

**4.** A user directly uploads a PDF into the C02-era Snowflake Intelligence chat interface. Where does the current successor documentation say the upload is saved? A. A public S3 bucket B. The user's personal/user stage C. The Model Registry D. A semantic view

**5.** An administrator sets `CORTEX_ENABLED_CROSS_REGION` to permit a broader inference region. Which statement matches the documentation? A. The setting is per SQL query only B. All source tables permanently move to the inference region C. It is an account-level parameter; inference payload may be transmitted transiently D. It changes only the warehouse size

### Domain 2: functions

**6.** Which documented call requests automatic source-language detection? A. `AI_TRANSLATE('Hola', 'en')` B. `AI_TRANSLATE('Hola', '', 'en')` C. `AI_TRANSLATE('', 'Hola', 'en')` D. `TRANSLATE('Hola', '', 'en')`

**7.** A developer wants to generate a lesson plan from a prompt. Which is the most direct function? A. `AI_EXTRACT` B. `AI_COMPLETE` C. `AI_REDACT` D. `VECTOR_L2_DISTANCE`

**8.** Which function best extracts `vendor`, `invoice_number`, and `total` according to labeled questions from a staged invoice PDF? A. `AI_EXTRACT` B. `VECTOR_NORMALIZE` C. `AI_TRANSLATE` D. `AI_SENTIMENT`

**9.** Which helper creates a FILE object from a stage and relative path for functions that accept a file? A. `PROMPT` B. `TO_FILE` C. `AI_COUNT_TOKENS` D. `GET_PRESIGNED_URL`

**10.** Which is the documented minimum for `AI_CLASSIFY` categories? A. One category B. Two unique categories C. A semantic view D. A PDF

**11.** A SQL call must return a vector representation of text using a named embedding model. Which function? A. `AI_EMBED(model, input)` B. `AI_COMPLETE(input, model)` C. `AI_PARSE_DOCUMENT(file, model)` D. `AI_TRANSLATE(input, model)`

**12.** For two vectors from the same embedding model, a smaller value of which metric indicates they are closer? A. `VECTOR_COSINE_SIMILARITY` B. `VECTOR_INNER_PRODUCT` C. `VECTOR_L2_DISTANCE` D. Token count

**13.** The developer wants JSON output constrained by a declared schema rather than a plain prompt that says “return JSON.” Which `AI_COMPLETE` mechanism addresses this? A. `response_format` with a supported JSON schema B. `page_split` C. `CORTEX_ENABLED_CROSS_REGION` D. `GET_PRESIGNED_URL`

**14.** A team needs to keep context across several chat turns. What is the main role of the prior-message history sent to a chat-capable model/API? A. It stores Snowflake credentials B. It carries relevant conversation context C. It eliminates token charges D. It automatically creates a Search index

**15.** Which function handles speech-to-text from a staged audio/video file? A. `AI_TRANSCRIBE` B. `AI_SENTIMENT` C. `AI_EMBED` D. `AI_AGG`

**16.** A team needs to run its own packaged model service in Snowflake rather than call only a managed AI function. Which infrastructure is central to containerized service execution? A. Snowpark Container Services compute pool, image repository, and service spec B. Verified Query Repository C. Cortex Search reranker only D. `METERING_DAILY_HISTORY`

### Domain 3: governance

**17.** A user can call a Cortex Agent object but the role lacks privileges for one of its Search tools. What must be addressed? A. Increase `max_tokens` B. Grant the needed tool/service privileges to the calling role under the documented agent permission model C. Fine-tune the LLM D. Change `AI_TRANSLATE` source language

**18.** Which role is the broad covered-AI-feature entitlement described in Snowflake docs? A. `SNOWFLAKE.CORTEX_USER` B. `SYSADMIN` always C. `SNOWFLAKE.CORTEX_SEARCH_OWNER` D. `PUBLIC` alone

**19.** A Search service has no queries today but remains resumed. Which cost can still accrue? A. No cost at all B. Serving compute based on indexed data size/time C. Only per-message Analyst billing D. Only Python package download fees

**20.** A direct standalone Cortex Analyst API request and an Analyst tool call through an Agent use which current billing distinction? A. Both always flat-rate per warehouse hour B. Standalone API is per 1,000 messages; Agent route is token-based, and generated SQL can add warehouse cost C. Neither can incur warehouse cost D. Search index size alone determines both

**21.** A Cortex Agent invokes Search and a custom SQL tool. What is the safest cost estimate? A. Count only one agent message B. Add orchestration tokens, underlying Search/tool costs, and any warehouse compute C. Count only stored PDFs D. Count only `AI_EMBED` input tokens

**22.** Which view was the official April 2026 guide's sample-answer choice for **daily** `AI_SERVICES` credit consumption? A. `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` B. `SNOWFLAKE.INFORMATION_SCHEMA.METERING_HISTORY` C. `SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY` D. `SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AGENT_USAGE_HISTORY`

**23.** Why should Search and AI-function usage-history totals not always be added directly? A. Search has no embedding work B. Search embedding charges can appear in both feature views C. `METERING_DAILY_HISTORY` is a text column D. All views are disabled by default

**24.** A role has `USAGE` on a Cortex Search service but not `SELECT` on every source row. Which design concern matters? A. Search always rechecks source row grants for the caller B. Search uses owner's rights, so service access can expose indexed content; scope and grant the service carefully C. `AI_SENTIMENT` automatically masks rows D. Only account admins can query any service

### Domain 4: document processing

**25.** The goal is to retain headings and table structure from a contract as searchable Markdown. Which call is appropriate? A. `AI_PARSE_DOCUMENT` with `mode='LAYOUT'` B. `AI_TRANSLATE` with source `''` C. `AI_PARSE_DOCUMENT` with default `OCR` because it preserves all layout D. `VECTOR_L1_DISTANCE`

**26.** What is the documented default mode when `AI_PARSE_DOCUMENT` options do not specify a mode? A. `LAYOUT` B. `OCR` C. `EXTRACT` D. `TRANSCRIBE`

**27.** When `page_split` is true for a supported document, what changes? A. The function generates a semantic view B. Output has a `pages` array with per-page content/index C. It disables all billing D. It removes the need for a stage

**28.** A pipeline must process newly arrived staged files and keep structured invoice fields for analytics. Which design aligns with Snowflake components? A. Stage/directory metadata → `AI_EXTRACT` → persist results; streams/tasks can orchestrate downstream table changes B. `AI_COMPLETE` alone without file reference or storage C. A public URL to each file as the only source of truth D. A semantic view that automatically parses all PDFs without a function

### Supplement: evaluation, sentiment and fine-tuning

**29.** A team wants a repeatable quality score for an `AI_COMPLETE` classification prompt against 500 labeled rows. Which feature fits? A. `AI_FUNCTION_EVALUATION` B. `AI_COUNT_TOKENS` C. `AI_SIMILARITY` D. `AI_REDACT`

**30.** Which meter appears for an `AI_FUNCTION_OPTIMIZATION` run, in addition to Cortex inference tokens? A. Search serving B. `SERVERLESS_EXPERIMENTS` C. Per-1,000 Analyst messages D. Page-based parsing

**31.** `AI_SENTIMENT(text, ['Cost','Quality'])` returns `unknown` for `Cost`. What does that mean? A. Cost was neutral B. Cost was not mentioned C. The call failed D. Cost was mixed

**32.** What must the training query of `SNOWFLAKE.CORTEX.FINETUNE('CREATE', ...)` return? A. `input` and `label` columns B. `prompt` and `completion` columns C. A single VARIANT column D. An embedding VECTOR

---

## Answer key and why

| # | Answer | Reason and official documentation |
| ---: | :---: | --- |
| 1 | B | Search is the managed retrieval service. [Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) |
| 2 | A | Analyst creates SQL grounded in a semantic view/model. [Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst) |
| 3 | B | Agents orchestrate Search for unstructured and Analyst for structured data. [Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) |
| 4 | B | Direct chat uploads go to the user's stage and have thread-linked cleanup. [CoWork upload](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork#zero-setup-file-upload) |
| 5 | C | Account-level routing affects transient inference payload, while source data stays in the account region. [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) |
| 6 | B | The empty **second** argument selects auto-detection; target remains required. [AI_TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/ai_translate) |
| 7 | B | `AI_COMPLETE` is general-purpose generation. [AI_COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/ai_complete) |
| 8 | A | `AI_EXTRACT` takes a file and response format specifying fields/questions. [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract) |
| 9 | B | `TO_FILE(stage, path)` produces the file reference. [TO_FILE](https://docs.snowflake.com/en/sql-reference/functions/to_file) |
| 10 | B | At least two unique categories are required. [AI_CLASSIFY](https://docs.snowflake.com/en/sql-reference/functions/ai_classify) |
| 11 | A | `AI_EMBED` takes model then input and returns `VECTOR`. [AI_EMBED](https://docs.snowflake.com/en/sql-reference/functions/ai_embed) |
| 12 | C | L2 is a distance, minimized for nearer vectors. [VECTOR_L2_DISTANCE](https://docs.snowflake.com/en/sql-reference/functions/vector_l2_distance) |
| 13 | A | Use the supported structured-output `response_format`. [Structured outputs](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-structured-outputs) |
| 14 | B | Relevant prior messages maintain multi-turn context, with token tradeoffs. [Analyst REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api) |
| 15 | A | `AI_TRANSCRIBE` handles staged media transcription. [AISQL](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) |
| 16 | A | Container Services needs images, compute pool, and a service spec/service. [SPCS tutorial](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/tutorial-1#create-a-service) |
| 17 | B | Agent access and tool access are separate privileges; inspect current policy for inaccessible tools. [Agent setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup) |
| 18 | A | `CORTEX_USER` is the broad entitlement; narrower database roles exist. [Agent setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup) |
| 19 | B | Search serving accrues while service is resumed, even without queries. [Search costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-costs) |
| 20 | B | Direct Analyst and Agent-integrated Analyst use different pricing paths; SQL execution adds warehouse cost. [Pricing](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing) |
| 21 | B | Agent orchestration and tool costs add together. [Agents cost](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents#cost-considerations) |
| 22 | C | The official guide marks this as its daily-metering answer; current service-specific views supplement it. [Daily metering](https://docs.snowflake.com/en/sql-reference/account-usage/metering_daily_history) |
| 23 | B | Search embeddings can overlap AI-functions history. [Cost governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) |
| 24 | B | Search uses owner's rights; grant service access with indexed content in mind. [Search access](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) |
| 25 | A | `LAYOUT` yields structural Markdown; `OCR` is text only. [AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document) |
| 26 | B | `OCR` is the documented default. [AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document) |
| 27 | B | `page_split` produces indexed per-page content for supported formats. [AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document) |
| 28 | A | Stages hold files; `AI_EXTRACT` extracts fields; streams/tasks can orchestrate processing. [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract) · [streams](https://docs.snowflake.com/en/user-guide/streams-intro) |
| 29 | A | Evaluation scores a function against a labeled dataset. [AI_FUNCTION_EVALUATION](https://docs.snowflake.com/en/sql-reference/functions/ai_function_evaluation) |
| 30 | B | Experiments run on serverless compute metered as `SERVERLESS_EXPERIMENTS`, plus inference tokens. [AI_FUNCTION_OPTIMIZATION](https://docs.snowflake.com/en/sql-reference/functions/ai_function_optimization) |
| 31 | B | `unknown` means not mentioned; it is distinct from `neutral`. [AI_SENTIMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_sentiment) |
| 32 | B | The training query returns `prompt` and `completion`. [FINETUNE CREATE](https://docs.snowflake.com/en/sql-reference/functions/finetune-create) |

### Review rule

For every miss, write one sentence explaining **why the chosen distractor is wrong** and one short SQL/API/privilege/cost example. Re-attempt missed items 24 hours later. Do not use a high score on this small set as proof of exam readiness; add the official practice exam and a live lab.

---

## Supplement: semantic layer (questions 33-49)

17 extra single-answer questions on semantic views, based on [08_SEMANTIC_LAYER.md](08_SEMANTIC_LAYER.md) and the linked Snowflake pages, checked 2026-10-09. They mostly map to Domain 1, with some Domain 3 (privileges). They are original learning questions, not Snowflake exam items. Answer first, then check the key below. Assume the lab view `SALES_SV` from file 08 where a view is named.

**33.** How do YAML and SQL DDL relate for semantic views? A. YAML creates a stage-based semantic model and DDL creates a semantic view, so they are different object types B. YAML is only for Cortex Analyst and DDL is only for SQL queries C. They are two authoring formats that produce the same kind of semantic view object D. DDL is deprecated in favour of YAML

**34.** Which function must wrap a defined metric when you query the view name with standard SQL, for example `SELECT region, ___(net_sales) FROM SALES_SV GROUP BY region`? A. `AGG` B. `SUM` C. `METRIC` D. `SEMANTIC_VIEW`

**35.** Which combination is **not** allowed in a single `SEMANTIC_VIEW(...)` clause? A. `DIMENSIONS` and `METRICS` B. `DIMENSIONS` and a `WHERE` filter on a dimension C. `METRICS` and a derived metric D. `FACTS` and `METRICS`

**36.** Why does `DIMENSIONS order_lines.product METRICS orders.order_count` fail? A. `product` is a private dimension B. The dimension's table has a finer grain than the metric's table C. Facts are required in the same clause D. `AGG()` is missing

**37.** A role has `SELECT` on `SALES_SV` but no privilege on the base tables. It runs `SELECT * FROM SEMANTIC_VIEW(SALES_SV METRICS orders.order_count)`. What happens? A. It fails: `SELECT` on every base table is required B. It fails: `REFERENCES` on the view is required C. It works only if the role owns the view D. It works: semantic views run with owner's rights, so `SELECT` on the view suffices

**38.** The same role asks a Cortex Agent, which has `SALES_SV` as an Analyst tool, a sales question and gets no usable answer. Which explanation fits the documentation? A. The Agent runs generated SQL against the physical tables as the user's default role, which therefore needs base-table access B. Agents cannot use semantic views C. The role needs `AI_FUNCTIONS_USER` D. `MAX_STALENESS` is not set

**39.** Which DDL clause tells Cortex Analyst to reject, or ask a clarifying question about, certain user questions? A. `AI_SQL_GENERATION` B. `AI_VERIFIED_QUERIES` C. `AI_QUESTION_CATEGORIZATION` D. `COMMENT`

**40.** What must the SQL in a verified query use? A. Physical table names only B. Cortex Search service names C. Dimension names only D. The logical table and column names defined in the semantic view

**41.** Which statement about a derived metric is correct? A. It omits the logical-table prefix and can combine metrics from different tables B. It must be prefixed with the table that owns the first metric C. It can aggregate other metrics, such as `SUM(orders.order_count)` D. It can be used inside a regular (non-derived) metric

**42.** How do you convert a legacy stage-based YAML model into a semantic view, validating first? A. `ALTER SEMANTIC VIEW ... SET YAML` B. Call `SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML` with `TRUE` as the third argument to validate, then call it again to create C. `GRANT` the stage file to the view D. Rename the stage file to `.sv.yaml`

**43.** How do masking and row access policies interact with semantic views? A. They can be attached directly to semantic-view dimensions B. Semantic views ignore them C. They cannot be set on semantic-view attributes, but policies on the base tables and columns propagate and are enforced D. They apply only to Cortex Agents, not SQL queries

**44.** What is true of sample values defined on a dimension? A. They are stored as metadata, are not masked by masking policies, and are visible through `GET_DDL` to roles with `REFERENCES` or `OWNERSHIP` B. They are masked by any masking policy on the column C. They are visible only to `ACCOUNTADMIN` D. They are not stored in the view

**45.** Materializations have been added to a semantic view, but Agent latency is unchanged. Why? A. `MAX_STALENESS` is below 120 seconds B. Agents need an `IMMUTABLE WHERE` condition C. Materializations apply only to facts D. Materializations speed up semantic SQL (the `SEMANTIC_VIEW` clause or standard SQL on the view), whereas Agent and Analyst queries run physical SQL on the base tables

**46.** When is attaching a Cortex Search service to a semantic-view dimension recommended? A. Numeric measure columns B. High-cardinality text columns, such as product or customer names C. Date columns D. Long free-text notes

**47.** An Agent has several semantic views as tools. Which statement is correct? A. It joins across the views when it needs to B. The views must share one description C. Each view is queried independently, with no joins across views, and distinct descriptions help it choose D. Only one semantic view per Agent is supported

**48.** What privileges let a provider share a semantic view through a share? A. `GRANT REFERENCES` and `GRANT SELECT` on the semantic view to the share B. `USAGE` on the view only C. Semantic views cannot be shared D. Sharing works only via a stage

**49.** In the Cortex Analyst REST API, which field passes a native semantic view, as opposed to a legacy staged YAML model? A. `semantic_model_file` B. `semantic_view` C. `semantic_stage` D. `view_name`

### Supplement answer key

| # | Answer | Reason and official documentation |
| ---: | :---: | --- |
| 33 | C | YAML and DDL have near-complete feature parity and produce the same object. The legacy distinction is the stage-based model. [YAML vs DDL](https://docs.snowflake.com/en/user-guide/views-semantic/yaml-vs-ddl) |
| 34 | A | Defined metrics must be passed to `AGG()` in standard SQL. `SUM` of a metric would be an aggregation of a metric. [Querying](https://docs.snowflake.com/en/user-guide/views-semantic/querying) |
| 35 | D | You cannot specify `FACTS` and `METRICS` in the same clause. [SEMANTIC_VIEW](https://docs.snowflake.com/en/sql-reference/constructs/semantic_view) |
| 36 | B | The dimension's table must be related to the metric's table and have an equal or coarser grain. Use `SHOW SEMANTIC DIMENSIONS ... FOR METRIC`. [Querying](https://docs.snowflake.com/en/user-guide/views-semantic/querying) |
| 37 | D | Querying needs only `SELECT` on the semantic view, as with standard views. [Querying privileges](https://docs.snowflake.com/en/user-guide/views-semantic/querying) |
| 38 | A | Agents run with the default role and generate physical SQL, so the role also needs base-table access. [Dev best practices](https://docs.snowflake.com/en/user-guide/views-semantic/best-practices-dev) · [Agent setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup) |
| 39 | C | `AI_QUESTION_CATEGORIZATION` governs question handling. `AI_SQL_GENERATION` governs the SQL. [Custom instructions](https://docs.snowflake.com/en/user-guide/views-semantic/custom-instructions) |
| 40 | D | Verified SQL uses logical names, not the underlying dataset's. [Verified queries](https://docs.snowflake.com/en/user-guide/views-semantic/verified-query-repository) |
| 41 | A | A derived metric is view-scoped, so you omit the table name. It cannot aggregate metrics, and only another derived metric may use it. [SQL guide](https://docs.snowflake.com/en/user-guide/views-semantic/sql) |
| 42 | B | Passing `TRUE` as the third argument validates without creating. Conversion is one file at a time. [SQL guide](https://docs.snowflake.com/en/user-guide/views-semantic/sql) |
| 43 | C | Policies cannot be set on semantic-view attributes but propagate from base tables. [Dev best practices](https://docs.snowflake.com/en/user-guide/views-semantic/best-practices-dev) |
| 44 | A | Metadata is not covered by masking policies, so non-sensitive sample values are advised. [Dev best practices](https://docs.snowflake.com/en/user-guide/views-semantic/best-practices-dev) |
| 45 | D | Cortex Analyst, Agent and CoWork queries that run physical SQL do not benefit. [Materializations](https://docs.snowflake.com/en/user-guide/views-semantic/materializations) |
| 46 | B | Use Search for high-cardinality text (roughly more than 10 distinct values). Avoid it for numeric, date and paragraph text. [Modeling](https://docs.snowflake.com/en/user-guide/views-semantic/best-practices-modeling) |
| 47 | C | Agents do not join across separate semantic views; distinct descriptions improve selection. [Modeling](https://docs.snowflake.com/en/user-guide/views-semantic/best-practices-modeling) |
| 48 | A | Grant both `REFERENCES` and `SELECT` on the view to the share. [Sharing](https://docs.snowflake.com/en/user-guide/views-semantic/sharing-semantic-views) |
| 49 | B | `semantic_view` takes the fully qualified view name; `semantic_model_file` is the legacy staged YAML path. [Analyst REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api) |
