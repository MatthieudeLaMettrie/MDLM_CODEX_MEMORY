# Original GES-C02 practice set

28 original single-answer questions. Approximate domain weighting: 5 overview, 11 functions, 8 governance, 4 document processing. These are learning questions based on official objectives and documentation, **not** Snowflake practice-exam items or claimed real exam questions. Set a timer, answer before reading the key, and verify any disputed item in the linked docs. Syntax examples describe documented signatures as checked 2026-09-24; they were not run in an account.

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

### Review rule

For every miss, write one sentence explaining **why the chosen distractor is wrong** and one short SQL/API/privilege/cost example. Re-attempt missed items 24 hours later. Do not use a high score on this small set as proof of exam readiness; add the official practice exam and a live lab.
