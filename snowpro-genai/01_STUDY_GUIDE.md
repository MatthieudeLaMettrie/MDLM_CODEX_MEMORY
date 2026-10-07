# SnowPro Gen AI GES-C02 study guide

Prepared 2026-09-24. Blueprint: Snowflake's *SnowPro Specialty: Gen AI Exam Study Guide*, last updated 2026-04-30, supplied as `SnowProGenAIStudyGuideC02.pdf`. Official documentation is the source of truth for syntax and current behavior. This guide prioritizes the exam blueprint while flagging changes in live docs. Product labels and charges can change before the test; recheck the [pricing](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing) and [AI cost governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) pages before booking.

For a module-by-module route based on the supplied Snowflake GenAI course datasheet, use the [course companion](02_COURSE_COMPANION.md). It adds guided labs, a capstone, and a distinction between the broader course syllabus and this exam blueprint.

For current coverage of all listed AI Functions, the complete access path, model RBAC, guardrails, cost-view changes, and Snowflake ML, use the [AI/ML deep dive](04_AI_ML_DEEP_DIVE.md) and its [documentation atlas](07_AI_ML_DOC_ATLAS.md).

For account/trial activation, role grants, model and regional checks, and a RAG walkthrough, use [Enable Cortex AI and build a RAG lab](03_ENABLE_CORTEX_AND_RAG.md).

## One-page memory sheet

| Need | Snowflake choice | Key distinction |
| --- | --- | --- |
| Generate a lesson, answer, or structured output | `AI_COMPLETE` | General generation; model, prompt, optional parameters/format |
| Extract named values from an invoice | `AI_EXTRACT` | Prompt/schema defines fields; accepts text or staged file |
| Preserve contract headings and tables as Markdown | `AI_PARSE_DOCUMENT` in `LAYOUT` mode | `OCR` returns text only and is default |
| Translate with unknown source language | `AI_TRANSLATE(text, '', 'en')` | Empty **source argument** triggers detection; the argument is not omitted |
| Search PDFs/knowledge base | Cortex Search | Hybrid keyword + vector retrieval and reranking; index has ongoing serving cost |
| Natural language to SQL over governed structured data | Cortex Analyst + semantic view | Verified queries and custom instructions improve correctness |
| Route between Search, Analyst, and tools | Cortex Agents | Orchestration cost plus underlying tool/compute costs |
| End-user chat with agents | Snowflake Intelligence in C02 blueprint | Live docs currently redirect this page to Snowflake CoWork |
| Bring a custom model | Model Registry; optionally Snowpark Container Services | Registry stores/version/deploys models; containers run custom services |
| Trace/evaluate outputs | AI Observability | Metrics, traces, logs, datasets and comparisons |

The exam weight is **18% / 38% / 29% / 15%** for Domains 1-4. Domain 2 plus Domain 3 account for 67% of the blueprint. The PDF says the domain outline is not exhaustive. Do not treat this guide as an exact future question bank.

## 1. Snowflake for Gen AI overview (18%)

### Choose the right surface

**Cortex AI functions** run managed AI operations in SQL and other supported interfaces. Use a task-specific function when it matches the task; use `AI_COMPLETE` for flexible generation. **Cortex Search** builds a managed search index over unstructured text and supports RAG. It combines vector retrieval, keyword search, and semantic reranking. **Cortex Analyst** turns questions into SQL using a semantic view or semantic model, with business meaning, relationships, metrics, verified queries, and custom instructions. **Cortex Agents** orchestrate tools, including Search and Analyst, for multi-step or mixed structured/unstructured questions. **Snowflake Intelligence** is the C02 name for the conversational user interface. Its linked documentation now redirects to **Snowflake CoWork**; learn the exam name and verify current product naming at booking. [AISQL overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) · [Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) · [Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst) · [Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) · [CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork)

Decision drill: a PDF support bot starts with staged files → parse/chunk → Search → optionally an agent to compose answers with citations. A sales metric question starts with a semantic view and Analyst. A question requiring both a policy PDF and live sales metrics needs an Agent with Search and Analyst tools. `AI_COMPLETE` alone has no retrieval or semantic layer merely because it receives a prompt.

**RAG flow:** ingest documents; parse (`LAYOUT` if structure matters); chunk at boundaries that preserve meaning; embed/index; retrieve; rerank; place only relevant snippets and source metadata into the prompt; generate and evaluate. A larger chunk may retain context but consume more prompt tokens and reduce retrieval precision. A smaller chunk may split facts across passages. Keep a stable document ID, page, and citation metadata. Search supports multi-index configurations; each indexed text column and its embeddings may add cost. [Search overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) · [Search costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-costs) · [Vector embeddings](https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings)

```sql
-- Illustrative Search service after DOC_CHUNKS and a refresh warehouse exist.
CREATE OR REPLACE CORTEX SEARCH SERVICE policy_search
  ON chunk_text
  ATTRIBUTES document_id
  WAREHOUSE = search_refresh_wh
  TARGET_LAG = '1 day'
  EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
  AS (SELECT chunk_text, document_id FROM doc_chunks);
```

`ON` selects text to search; `ATTRIBUTES` makes a column usable for filtering; the warehouse refreshes the index, and `TARGET_LAG` expresses freshness. Creating a service builds an index and can incur cost immediately. [Search create example](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#example-create-and-query-a-cortex-search-service)

```sql
-- Preview retrieval after the service is ready.
SELECT PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
  'MY_DB.MY_SCHEMA.POLICY_SEARCH',
  '{"query":"refund deadline","columns":["chunk_text","document_id"],"limit":3}'
))['results'] AS results;
```

The Search preview helper takes a fully qualified service name and JSON query; it is distinct from `AI_COMPLETE`. [Search preview example](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#preview-the-service)

**Semantic layer:** a semantic view defines entities, dimensions, facts, metrics, joins, and business synonyms. A Verified Query Repository supplies reviewed question-to-SQL examples. Custom instructions constrain generation but do not replace permissions or verified definitions. Suggested questions guide users. Semantic Views Autopilot can help create a view, but it needs review. YAML specifications and SQL semantic views are distinct representations. [Semantic view overview](https://docs.snowflake.com/en/user-guide/views-semantic/overview) · [YAML specification](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec) · [Verified queries](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/verified-query-repository) · [Custom instructions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/custom-instructions)

Analyst REST request shape (credentials and endpoint omitted deliberately):

```json
{
  "messages": [{"role": "user", "content": [{"type": "text", "text": "Net sales by region?"}]}],
  "semantic_view": "MY_DB.MY_SCHEMA.SALES_SEMANTIC_VIEW"
}
```

The request needs one supported semantic-model/view field; a multi-turn request includes relevant message history. [Analyst REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api)

**Interfaces and models:** AI Studio, SQL, REST APIs, Cortex Code in Snowsight and CLI, Agents, and Model Context Protocol (MCP) are different ways to build or invoke capabilities. Snowflake Model Registry handles custom model lifecycle; Snowpark Container Services provides containerized compute/services with image repositories, compute pools, and service specifications. Know that importing/logging a model is separate from invoking it. Fine-tuning and provisioned throughput are specialized options, not prerequisites for ordinary inference. [Model Registry](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview) · [Container Services](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview) · [Cortex Code CLI](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-cli) · [MCP](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)

The blueprint also names **Cortex Knowledge Extensions**, which make curated knowledge available to Cortex applications, and Cortex Code CLI **commands/session management**. Know the roles of these features and check the CLI reference for exact commands, because command sets are versioned and may move faster than the exam PDF. [Knowledge Extensions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview) · [Cortex Code CLI commands](https://docs.snowflake.com/en/user-guide/cortex-code/cli-reference#commands) · [session management](https://docs.snowflake.com/en/user-guide/cortex-code/cli-reference#session-management)

**Context window and routing:** the context window limits material sent to and produced by a model. Use retrieval and concise history to control tokens. Cross-region inference is an **account-level** choice via `CORTEX_ENABLED_CROSS_REGION`; customer data remains stored in the account region while the inference payload may travel transiently within the configured boundary. Check availability, latency, residency, and model support. `SHOW PARAMETERS LIKE 'CORTEX_ENABLED_CROSS_REGION' IN ACCOUNT;` is a useful diagnostic. [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) · [Model availability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)

**File-location detail from the reported exam experience:** the current CoWork page says a file uploaded directly to chat is saved to the **user stage/personal stage**, accessible in that thread, and cleaned up when the thread is deleted or expires. This is distinct from files an application developer uploads to a named internal or external stage for AI functions or Search. The C02 blueprint uses the name Snowflake Intelligence. [CoWork file upload](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork#zero-setup-file-upload) · [Internal stage types](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage)

## 2. Snowflake Gen AI functions (38%)

### Task-to-function table

| Function | Use | Syntax fact to remember |
| --- | --- | --- |
| `AI_COMPLETE` / older `SNOWFLAKE.CORTEX.COMPLETE` | Generate text, analyze supported files, structured output | Model first, then prompt; options depend on input form |
| `AI_CLASSIFY` | Classify into supplied categories | Categories are an array with at least two unique values |
| `AI_EXTRACT` | Extract named facts from text or file | Input then `responseFormat`; file via `TO_FILE` |
| `AI_PARSE_DOCUMENT` | OCR/layout extraction from staged docs | FILE object; optional object with `mode`, `page_split` |
| `AI_SENTIMENT` | Sentiment | Task-specific, not arbitrary generation |
| `AI_SUMMARIZE`, `AI_SUMMARIZE_AGG` | One item or an aggregate of rows | Choose row or aggregate scope deliberately |
| `AI_TRANSLATE` | Language translation | `''` in source slot auto-detects source |
| `AI_EMBED` | Vector from text/image | Embedding model and input; returns `VECTOR` |
| `AI_SIMILARITY` | Managed similarity across inputs | Compare inputs; distinguish from vector SQL functions |
| `AI_FILTER`, `AI_AGG` | Semantic filtering and aggregation | AI-assisted table operations; cost depends on processed inputs |
| `AI_TRANSCRIBE` | Audio/video transcription | File on stage |
| `AI_REDACT` | PII redaction | Verify output and governance fit |
| `AI_COUNT_TOKENS` | Estimate token count | Helper; does not itself invoke generation |
| `TO_FILE`, `PROMPT`, split-text helpers | Pass staged files, construct prompts, chunk text | Support a larger workflow |

[AI functions overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) · [all function references](https://docs.snowflake.com/en/sql-reference/functions-all)

### Syntax traps: rehearse these

```sql
-- General generation. Choose a model available in your account/region.
SELECT AI_COMPLETE('llama3.3-70b', 'Draft a short lesson on RAG.');

-- The second argument is still required: '' means detect the source language.
SELECT AI_TRANSLATE('Bonjour le monde', '', 'en');
SELECT AI_TRANSLATE('Hello world', 'en', 'fr');

-- Task-specific extraction from a staged document.
SELECT AI_EXTRACT(
  file => TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'invoice.pdf'),
  responseFormat => {
    'vendor': 'What is the vendor name?',
    'total': 'What is the total amount?'
  }
);

-- Parsing returns JSON text by default; PARSE_JSON makes fields queryable.
SELECT PARSE_JSON(AI_PARSE_DOCUMENT(
  TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'contract.pdf'),
  {'mode': 'LAYOUT', 'page_split': TRUE}
)) AS parsed;

SELECT AI_EMBED('snowflake-arctic-embed-l-v2.0', 'refund policy');
```

These examples follow the documented signatures but were not executed in a Snowflake account. `AI_TRANSLATE(text, 'en')` is **not** the documented two-argument form. `AI_TRANSLATE` requires text, source-language slot, and target language; auto-detection is requested by passing `''` in the source slot. Older `SNOWFLAKE.CORTEX.TRANSLATE` has the same three-argument pattern. SQL `TRANSLATE` without the Cortex namespace performs character substitution, not language translation. [AI_TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/ai_translate) · [legacy Cortex TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/translate-snowflake-cortex) · [SQL TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/translate)

`AI_COMPLETE` single-string syntax starts with `(model, prompt [, model_parameters, response_format, show_details])`; multimodal and prompt-object forms differ. For constrained JSON, use the documented structured-output `response_format` on the appropriate form. Prompting for JSON in plain text is less reliable than a schema. `AI_CLASSIFY(input, categories [, config])` needs at least two unique categories. `AI_EXTRACT` accepts a response-format object, question array, or other supported schema; it is better for specific fields than a broad content conversion. [AI_COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-string) · [structured outputs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/complete-structured-outputs) · [AI_CLASSIFY](https://docs.snowflake.com/en/sql-reference/functions/ai_classify) · [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract)

The PDF includes legacy `SNOWFLAKE.CORTEX.TRY_COMPLETE(model, prompt_or_history [, options])`, which returns `NULL` instead of raising an error when completion fails. Current docs favor `AI_COMPLETE`; it can return `NULL` by default on processing errors or an object with `value` and `error` when `return_error_details => TRUE` is supported for the chosen input form. Check which function and failure behavior a question names. [TRY_COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/try_complete-snowflake-cortex) · [AI_COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/ai_complete)

For vectors, remember **higher** cosine similarity or inner product can mean more similar, while **lower** L1/L2 distance means closer. Compare like dimensions and embedding models; normalization can affect inner product behavior. Know `VECTOR_COSINE_SIMILARITY`, `VECTOR_INNER_PRODUCT`, `VECTOR_L1_DISTANCE`, `VECTOR_L2_DISTANCE`, `VECTOR_NORMALIZE`, `VECTOR_TRUNCATE`, and vector aggregates (`SUM`, `MIN`, `MAX`, `AVG`). [Vector types](https://docs.snowflake.com/en/sql-reference/data-types-vector) · [vector embeddings](https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings)

### Application and pipeline decisions

For chat, store conversation history in application state or use a service with thread support; send relevant prior turns in the `messages` array when the chosen API expects it. Memory preserves context, but increases tokens and may carry stale or sensitive text. Streamlit can provide a UI. A container runtime may be needed for particular Agent API calls; check the current [Agent limitations](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) rather than assuming any Streamlit runtime works. [Analyst REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api) · [Streamlit](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)

For batch enrichment, apply functions to selected rows, keep outputs and source IDs, and evaluate quality before broad execution. Use a model sized to accuracy, latency, context, region, and cost. A larger model is not automatically the right choice. Provisioned throughput addresses predictable high-volume workloads with separate capacity economics. For a custom open-source model, the Container Services flow is: image repository → Docker image → compute pool → service spec/service; Model Registry manages model versions and deployment. [Choosing a model](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#choosing-a-model) · [Provisioned Throughput](https://docs.snowflake.com/en/user-guide/snowflake-cortex/provisioned-throughput) · [SPCS tutorial](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/tutorial-1#create-a-service)

## 3. Governance, access, cost and observability (29%)

### Permission model

Separate **account-level AI Function privilege**, **Snowflake database role**, **model access**, **object privilege**, and **data/tool privilege**. Current docs require `USE AI FUNCTIONS ON ACCOUNT` or `USE AI FUNCTION <name> ON ACCOUNT` plus `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.AI_FUNCTIONS_USER` for most function calls; the aggregate functions have a documented exception to review. `USE AI FUNCTIONS` and broad `CORTEX_USER` access are granted to `PUBLIC` by default in documented setups. `AI_FUNCTIONS_USER` covers scalar functions but excludes `AI_AGG` and `AI_SUMMARIZE_AGG`; `CORTEX_EMBED_USER`, `CORTEX_ANALYST_USER`, and `CORTEX_AGENT_USER` support narrower capability access. Database roles are granted to account roles, then account roles to users. API requests need authentication plus relevant role/object access. [Cortex privileges](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access) · [Analyst access](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst#access-control-requirements) · [Agent setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup)

**Model-control version trap:** the April C02 PDF names the account-level `CORTEX_MODELS_ALLOWLIST` and application roles. Current Snowflake docs call the allowlist **legacy, planned for removal**, and recommend per-model RBAC/application roles. Since August 2026, the only permitted change to the allowlist is setting it to `'None'`; while both mechanisms operate, either can permit access. Learn both terms for exam recognition, but for a real deployment check the current account state and grant the intended model application roles. [Privileges and model access](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access)

```sql
-- Illustrative grant; run only with an authorized administrator role.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE APP_AGENT_ROLE;
-- Agent callers also need USAGE on the database, schema, agent and warehouse,
-- plus privileges on the Search/Analyst/custom tools the agent may use.
```

Search creation requires embedding entitlement, `CREATE CORTEX SEARCH SERVICE` on its schema, `SELECT` on source objects, and warehouse `USAGE` for refresh. Querying requires `USAGE` on the service and containing database/schema. Search services use **owner's rights**; granting `USAGE` may expose indexed content beyond the caller's direct source-table access, so design services around appropriate data boundaries. Agent calls use the caller's **default role** under the documented setup and need access to tools, agent, and default warehouse. Check the Agent setup page for exact current handling when a tool is inaccessible. [Search access](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) · [Agent setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup)

### Billing map: answer the unit and the extra costs

Snowflake's live pricing page distinguishes **AI Credits** from **Platform Credits**. The April 2026 exam PDF lists older usage views, so use current pricing for real decisions and learn the blueprint's vocabulary. Avoid memorizing a dollar rate; contract and routing affect price. [Pricing](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing) · [Search costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-costs) · [cost governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance)

| Capability | Current billing basis | Extra cost or trap |
| --- | --- | --- |
| Cortex Agents | Orchestration model tokens, AI Credits | Tool calls add Analyst/Search/custom compute and possibly other services; one user prompt is not one flat charge |
| Cortex Analyst via Agent | Token-based Agent path | Generated SQL execution uses a warehouse |
| Standalone Cortex Analyst API | Per 1,000 messages, legacy Platform Credit path | Generated SQL execution uses a warehouse; **different** from Analyst through Agent |
| Cortex Search | Index serving per GB-month plus embedding tokens on insert/update | Refresh warehouse, stored index, and possible cloud services; serving can cost money even with zero queries |
| AI functions | Generally model/function-specific tokens, AI Credits | Input/output treatment differs by function; warehouse running time can add cost |
| `AI_PARSE_DOCUMENT` | Pages, with mode-dependent rate | It is a page-billed exception to the generic token mental model |
| Snowpark Container Services | Compute pool service time plus other associated resources | Model Registry storage/deployment and warehouse activity may add costs |
| Provisioned Throughput | Reserved throughput/capacity model | Evaluate utilization against on-demand usage |

For functions that generate text, account for **input and output** tokens; embeddings/similarity are commonly input-oriented. Image/audio token equivalence and structured output can change totals. Estimate with `AI_COUNT_TOKENS` where supported, sample inputs, and cap output length. `AI_COUNT_TOKENS` itself has warehouse compute rather than the same model-inference token charge. Avoid using a larger warehouse to speed managed model inference without evidence. [AISQL costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-cost) · [AI_COUNT_TOKENS](https://docs.snowflake.com/en/sql-reference/functions/ai_count_tokens)

**Cost history gotcha:** `SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY` is the official guide's sample-answer view for daily `AI_SERVICES` consumption. Current service-specific analysis adds `CORTEX_AGENT_USAGE_HISTORY`, `CORTEX_ANALYST_USAGE_HISTORY` (if available for the route), `CORTEX_SEARCH_DAILY_USAGE_HISTORY`, and `CORTEX_AI_FUNCTIONS_USAGE_HISTORY`; check the current matrix for actual names, retention, start dates, and service types. Older views such as `CORTEX_AISQL_USAGE_HISTORY` and `CORTEX_FUNCTIONS_USAGE_HISTORY` can be legacy/deprecation paths. **Do not sum overlapping views blindly**: the cost-governance page flags Search embedding totals also appearing in AI-function views. [Cost history matrix](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) · [METERING_DAILY_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/metering_daily_history)

```sql
-- Blueprint-style daily AI_SERVICES rollup. Verify current service types too.
SELECT usage_date, service_type, credits_used
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
WHERE service_type = 'AI_SERVICES'
ORDER BY usage_date DESC;

-- Current feature-level investigations, subject to the view's latency/retention:
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AGENT_USAGE_HISTORY LIMIT 10;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY LIMIT 10;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_SEARCH_DAILY_USAGE_HISTORY LIMIT 10;
```

**Safety and availability:** use least privilege, model allowlists, governed stages, data masking/row policies as appropriate, `AI_REDACT` for PII workflows, prompt and retrieved-context controls, and output evaluation. Guardrails help but do not guarantee correctness or eliminate bias. Cross-region inference can move the inference payload transiently; assess residency and model availability. [Governance](https://docs.snowflake.com/en/guides-overview-govern) · [cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) · [AI_REDACT](https://docs.snowflake.com/en/sql-reference/functions/ai_redact)

**Observability:** capture traces and event-table data, curate ground truth, compare versions, and evaluate retrieval/answer correctness rather than only accepting fluent answers. Distinguish LLM-as-judge scores from deterministic checks. For text-to-SQL, inspect generated SQL, execution, and verified query match. For RAG, check retrieval relevance, groundedness, and answer correctness. Evaluations themselves consume model/warehouse/storage resources. [AI Observability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability) · [evaluate apps](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/evaluate-ai-applications) · [Agent evaluations](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-evaluations)

The C02 blueprint explicitly names the **TruLens SDK** as one implementation route. Recognize it alongside Snowflake AI Observability's evaluation metrics, tracing, comparisons, logs, and event tables; the SDK is a tool for recording/evaluating applications, not a substitute for a test dataset or access controls. [AI Observability concepts](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability)

## 4. Document processing (15%)

Documents for AI functions are stored in an **internal or external stage**, referenced through a FILE object such as `TO_FILE('@DB.SCHEMA.STAGE', 'path.pdf')`. Use a suitable encryption configuration and stage privileges. `AI_PARSE_DOCUMENT` defaults to `OCR` and returns extracted plain text; `LAYOUT` preserves structural text as Markdown, including tables. `page_split => TRUE` creates per-page output for supported formats. The current reference documents `page_filter` with zero-based inclusive start and exclusive end; the April blueprint names `page_limit`, so treat that as a version-drift checkpoint and inspect the reference before relying on a particular option. [AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document) · [parsing guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/parse-document)

As checked in the current parsing guide, `AI_PARSE_DOCUMENT` accepts files up to **100 MB** and **2,000 pages**; supported types include PDF, PPTX, DOCX, JPEG/JPG, PNG, TIFF/TIF, HTML, and TXT. `AI_EXTRACT` has its own limits (including a 100 MB file limit and a documented 125-page error threshold), so do not transfer a limit from one function to the other. An image counts as a page for `AI_PARSE_DOCUMENT`; HTML/TXT billing counts each 3,000-character chunk as a page. Recheck these operational limits at exam time. [Parsing requirements and costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/parse-document#input-requirements) · [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract)

`AI_EXTRACT` targets specific fields or questions from text or a file and returns structured data; it is the invoice-field choice. `AI_PARSE_DOCUMENT(LAYOUT)` is the searchable-contract-text choice. To build a pipeline, list staged files with a directory table, parse/extract, store result with file ID and status, chunk/embeddings as needed, then index with Search. Streams capture table changes; tasks schedule processing. Check errors and file constraints before retrying. `GET_PRESIGNED_URL(@stage, 'path' [, expiry_seconds])` issues a short-lived pre-signed URL; `BUILD_SCOPED_FILE_URL` produces a Snowflake scoped URL whose validity follows the persisted-query-result period (currently 24 hours). Calling privileges differ by stage type and by whether a view/procedure owner is involved. [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract) · [GET_PRESIGNED_URL](https://docs.snowflake.com/en/sql-reference/functions/get_presigned_url) · [BUILD_SCOPED_FILE_URL](https://docs.snowflake.com/en/sql-reference/functions/build_scoped_file_url) · [streams](https://docs.snowflake.com/en/user-guide/streams-intro) · [data pipelines](https://docs.snowflake.com/en/user-guide/data-pipelines-intro) · [troubleshooting](https://docs.snowflake.com/en/user-guide/snowflake-cortex/document-ai/troubleshooting)

### Mini-lab: make the distinctions real

1. In a test database, create an encrypted named internal stage with a directory table, upload a few synthetic PDFs, and confirm `LIST @stage`/directory metadata. Use test documents without personal data.
2. Run `AI_PARSE_DOCUMENT` in `OCR` and `LAYOUT` on the same table-heavy PDF; compare content and per-page output. Run `AI_EXTRACT` for a few invoice fields. Record failures and the relevant limits from the function pages.
3. Chunk the parsed text, build a Cortex Search service, and compare retrieval for a keyword query versus a paraphrase. Track initial embedding, refresh warehouse, storage, and idle serving usage.
4. Define a small semantic view over structured invoice rows; add one verified query and one custom instruction. Ask a question through Analyst, then combine Analyst and Search in an Agent if your account and privileges permit.
5. Inspect query history and feature usage views; measure answer accuracy, cost, latency, permissions, and whether any retrieved text exposed data outside the intended audience. Clean up the test service and compute pool when done.

See the [source index](06_OFFICIAL_DOC_INDEX.md) for official Snowflake resource URLs embedded in the supplied PDF's four domain resource sections; the core links above were individually checked during this pass, while the larger index is an extraction for follow-up reading.
