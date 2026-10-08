# Snowflake AI/ML deep dive: functions, governance and operations

Checked 2026-09-25 against [Snowflake AI and ML](https://docs.snowflake.com/en/guides-overview-ai-features), [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql), current SQL references, and the linked product guides. The [documentation atlas](07_AI_ML_DOC_ATLAS.md) inventories all 281 pages in Snowflake's Cortex, CoCo, and Snowflake ML section indexes, plus 29 linked ML Function and SQL reference pages, and records their headings. This document synthesizes the pages needed to make product, syntax, security, cost, and evaluation decisions; the atlas is a navigation map, not a promise that every indexed feature is tested on GES-C02. Use the [exam guide](01_STUDY_GUIDE.md) for official C02 domain weights and the [course companion](02_COURSE_COMPANION.md) for labs.

## 1. Choose the correct Snowflake surface

| Goal | Surface | What makes it distinct |
| --- | --- | --- |
| Enrich many rows with a specific AI task | Cortex AI Functions in SQL/Python | Managed functions optimized for throughput and batch processing |
| Low-latency model inference from an app | Cortex REST API | Interactive inference endpoint; application owns prompt and state |
| Retrieve facts from changing text | Cortex Search | Managed search index; hybrid retrieval and reranking |
| Ask natural-language questions of structured business data | Cortex Analyst (now recommended as a Cortex Agent tool) | Generates SQL from a semantic view/model; review SQL and metric definitions. See [the semantic layer](08_SEMANTIC_LAYER.md) |
| Route a question among Search, Analyst and tools | Cortex Agents | Managed planning, tool calls, and final response; caller/tool permissions matter |
| Give business users an Agent chat interface | Snowflake CoWork | Conversational surface, formerly called Snowflake Intelligence in older material |
| Assist a developer with Snowflake code and workflows | Snowflake CoCo | Snowsight, Desktop, CLI; formerly Cortex Code in older material |
| Share licensed indexed knowledge | Cortex Knowledge Extension | A Cortex Search service shared through a listing |
| Customize behavior with examples | Cortex Fine-tuning | Trains an adapter; does not refresh changing source facts |
| Train and operate a custom ML model | Snowflake ML | Feature Store, training, experiments, Model Registry, serving, monitoring |
| Forecast, detect anomalies, classify rows without custom code | ML Functions | Snowflake-managed traditional ML models over structured data |

Snowflake separates **Cortex AI features** from **Snowflake ML**. Cortex focuses on LLM-powered functions, Search, Analyst, Agents, and assistants; Snowflake ML covers model development and lifecycle. The distinction helps answer “which product?” questions. [AI/ML overview](https://docs.snowflake.com/en/guides-overview-ai-features) · [ML Functions](https://docs.snowflake.com/en/guides-overview-ml-functions) · [Snowflake ML](https://docs.snowflake.com/en/developer-guide/snowflake-ml/overview)

Other surfaces in the documentation tree: **Cortex AI Gateway** is a preview, account-level route for client inference with access control, trace and cost attribution; `USAGE` on it does not grant access to the underlying model, and request/response payload logging must be treated as sensitive if enabled. It is distinct from the Snowflake ML gateway used for model-serving traffic. **Snowflake-managed MCP server** exposes Snowflake resources to external MCP clients; **MCP connectors** let Snowflake Agents call remote tools. **Provisioned Throughput** reserves managed inference capacity for a term and charges allocated PTUs even when idle, so compare it with on-demand demand before reserving. [Cortex AI Gateway](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-gateway) · [managed MCP server](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp) · [MCP connectors](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp-connectors) · [Provisioned Throughput](https://docs.snowflake.com/en/user-guide/snowflake-cortex/provisioned-throughput)

## 2. Cortex AI Functions: exact task and argument shape

The Snowflake function-reference sidebar (checked 2026-10-09) lists **18 `AI_` entries**: the 15 task functions in the table below, `AI_COUNT_TOKENS`, and two preview, experiment-based quality tools, `AI_FUNCTION_EVALUATION` and `AI_FUNCTION_OPTIMIZATION` (see the quality subsection in section 4). It also lists the older `SNOWFLAKE.CORTEX.FINETUNE` and `SNOWFLAKE.CORTEX.SENTIMENT` entries and a **Helper functions** group (`PROMPT`, `TO_FILE`, `SPLIT_TEXT_RECURSIVE_CHARACTER`, `AGENT_RUN`, `DATA_AGENT_RUN`, `THREAD_MESSAGES`). Runnable examples for every one are in [09_AI_FUNCTION_EXAMPLES.md](09_AI_FUNCTION_EXAMPLES.md). Some functions or modalities may be in preview; check each reference and [regional availability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-regional-availability). The table shows the core signature, omitting some optional error-handling arguments for readability. Follow each reference before execution.

| Function | Core call or input | Output / exam distinction |
| --- | --- | --- |
| [`AI_COMPLETE`](https://docs.snowflake.com/en/sql-reference/functions/ai_complete) | Text form: `AI_COMPLETE(model, prompt [, model_parameters, response_format, show_details])` | General generation. File and prompt-object forms have different signatures; structured output uses a schema/SQL type rather than hoping for JSON in prose. |
| [`AI_CLASSIFY`](https://docs.snowflake.com/en/sql-reference/functions/ai_classify) | `AI_CLASSIFY(input, categories [, config])` | Classifies text/image/document into at least two unique categories; descriptions/examples add prompt tokens. |
| [`AI_FILTER`](https://docs.snowflake.com/en/sql-reference/functions/ai_filter) | `AI_FILTER(input)` | Boolean decision; usable in predicates. |
| [`AI_AGG`](https://docs.snowflake.com/en/sql-reference/functions/ai_agg) | `AI_AGG(expr, instruction)` | Prompt-driven aggregation across rows beyond a single-model context window. |
| [`AI_EMBED`](https://docs.snowflake.com/en/sql-reference/functions/ai_embed) | `AI_EMBED(model, input)` | Returns VECTOR for text or supported image; compare only compatible vectors/models. |
| [`AI_MULTI_EMBED`](https://docs.snowflake.com/en/sql-reference/functions/ai_multi_embed) | `AI_MULTI_EMBED(model, input [, options])` | Multimodal vectors with segment metadata for text/image/audio/video workflows. |
| [`AI_EXTRACT`](https://docs.snowflake.com/en/sql-reference/functions/ai_extract) | `AI_EXTRACT(text_or_file, responseFormat)` | Pulls requested fields/questions as structured output. Text and FILE forms have different named options. |
| [`AI_SENTIMENT`](https://docs.snowflake.com/en/sql-reference/functions/ai_sentiment) | `AI_SENTIMENT(text [, categories])` | Overall or aspect-level sentiment as an object; `unknown` is distinct from neutral. |
| [`AI_SUMMARIZE`](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize) | `AI_SUMMARIZE(text_or_file)` | One text/file summary. For many rows, use aggregate form. |
| [`AI_SUMMARIZE_AGG`](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize_agg) | `AI_SUMMARIZE_AGG(expr)` | General summary across rows; `AI_AGG` adds a custom instruction. |
| [`AI_SIMILARITY`](https://docs.snowflake.com/en/sql-reference/functions/ai_similarity) | `AI_SIMILARITY(input1, input2 [, config])` | Similarity score for two texts or two images; current reference says text-versus-image pairing is unsupported. |
| [`AI_TRANSCRIBE`](https://docs.snowflake.com/en/sql-reference/functions/ai_transcribe) | `AI_TRANSCRIBE(audio_file [, options])` | Transcribes staged media; options can request word or speaker segments/timestamps. |
| [`AI_PARSE_DOCUMENT`](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document) | `AI_PARSE_DOCUMENT(file_object [, options])` | `OCR` text is default; `LAYOUT` preserves structure, and optional image extraction requires layout. Page billed. |
| [`AI_REDACT`](https://docs.snowflake.com/en/sql-reference/functions/ai_redact) | `AI_REDACT(input [, categories] [, return_error_details] [, mode])` | Redact detected PII or use detect mode to return spans; not a substitute for RBAC. |
| [`AI_TRANSLATE`](https://docs.snowflake.com/en/sql-reference/functions/ai_translate) | `AI_TRANSLATE(text, source_language, target_language)` | Pass `''` for automatic source detection. The source argument is still present. |

**Helpers:** [`TO_FILE`](https://docs.snowflake.com/en/sql-reference/functions/to_file) makes a FILE object from a staged path; [`AI_COUNT_TOKENS`](https://docs.snowflake.com/en/sql-reference/functions/ai_count_tokens) estimates tokens with function/model-specific forms; [`PROMPT`](https://docs.snowflake.com/en/sql-reference/functions/prompt) constructs prompt objects. A local file path is not automatically a Snowflake FILE object. [Functions overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql)

### Syntax worth reproducing from memory

```sql
SELECT AI_TRANSLATE('Bonjour', '', 'en');
SELECT AI_CLASSIFY('The package arrived late', ['shipping', 'billing']);
SELECT AI_AGG(review_text, 'Summarize recurring delivery problems')
  FROM customer_reviews;
SELECT AI_PARSE_DOCUMENT(
  TO_FILE('@MY_DB.MY_SCHEMA.DOC_STAGE', 'policy.pdf'),
  {'mode': 'LAYOUT', 'page_split': TRUE}
);
```

The last two examples require your own table/stage, privileges, supported region, and may incur charges. `AI_COMPLETE` has separate [single-string](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-string), [single-file](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-file), and [prompt-object](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-prompt-object) forms. `show_details` changes its return shape. A supplied response format can return an object; adding “return JSON” to text alone does not enforce a schema. The general reference documents an optional `return_error_details` final argument, which changes errors into a value/error object for supported forms. [Structured output](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-structured-outputs)

### Choose between lookalikes

- **`AI_EXTRACT` vs `AI_PARSE_DOCUMENT`:** asked for named invoice fields → Extract; asked for a document's full text/structure before chunking → Parse. `OCR` is plain text; `LAYOUT` includes structure such as tables. The current parser uses `page_filter` with zero-based start-inclusive/end-exclusive ranges; the older C02 PDF names `page_limit`. [Extract](https://docs.snowflake.com/en/sql-reference/functions/ai_extract) · [Parse](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document)
- **`AI_SUMMARIZE` vs `AI_SUMMARIZE_AGG` vs `AI_AGG`:** one item → Summarize; general many-row summary → Summarize Agg; instruction-specific many-row insight → AI Agg. [Summarize](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize) · [Agg](https://docs.snowflake.com/en/sql-reference/functions/ai_agg)
- **`AI_EMBED` vs Search:** Embed produces a vector; Search creates and serves a managed retrieval index. `AI_SIMILARITY` compares pairs but does not build a search service. [Embeddings](https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings) · [Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
- **SQL functions vs REST:** Functions favor batch enrichment/throughput on table rows; REST favors interactive latency. SQL calls may still use a warehouse, so avoid scanning every row while experimenting. [AI Functions overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) · [Cortex REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api)

### Multimodal and file handling

The current overview includes text and image classification/completion, document parsing/extraction, audio/video transcription, and multimodal embedding. Supported type, model, size, duration, and region depend on the **individual function**, not on a blanket “Cortex supports files” claim. Stage the file, create a FILE reference, and check that function's limits. `AI_SIMILARITY` currently does not compare a text input to an image input. The Document Processing Playground is a UI for comparing extraction, Markdown layout, and OCR output; its upload limits differ from underlying function limits. [Multimodal guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-multimodal) · [Document functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-documents) · [Playground](https://docs.snowflake.com/en/user-guide/snowflake-cortex/document-processing-playground)

## 3. Governance: follow the whole access path

For AI Functions, think **account privilege AND database role**. Users need `USE AI FUNCTIONS ON ACCOUNT` or a specific `USE AI FUNCTION <name> ON ACCOUNT` privilege, plus `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.AI_FUNCTIONS_USER` where applicable. The blanket privilege and `CORTEX_USER` are granted to `PUBLIC` by default in documented setups. `AI_FUNCTIONS_USER` is narrower, is not granted to `PUBLIC` by default, and covers scalar functions, **not** `AI_AGG` or `AI_SUMMARIZE_AGG`. The privilege page also states the reverse exception: a role with `USE AI FUNCTIONS` but without `CORTEX_USER` can still call `AI_AGG` and `AI_SUMMARIZE_AGG`. The account privilege and role are separate gates. [AI Function privileges](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access)

| Gate | Test question | Current answer |
| --- | --- | --- |
| Account/function privilege | Can the role invoke this AI function at all? | Blanket `USE AI FUNCTIONS` or a per-function grant; blanket access still wins if a narrower grant is revoked. |
| Snowflake database role | Which AI capability does the role hold? | `CORTEX_USER` broad; `AI_FUNCTIONS_USER` scalar functions; `CORTEX_EMBED_USER` embeddings/Search creation. |
| Model permission | Is this model available to this role? | Prefer model RBAC/application roles in `SNOWFLAKE.MODELS`; also check region and rollout state. |
| Data/stage permission | Can the caller read rows or staged files? | Ordinary object, stage and FILE privileges still apply. |
| Product object permission | Can the caller use Agent/Search/semantic resources? | Agent and Search `USAGE`, containing database/schema, and tool-specific access. |
| Compute permission | Can required queries/tools run? | Warehouse `USAGE`; Agent setup uses the user's **default** role and default warehouse. |

The [model-access page](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access) calls `CORTEX_MODELS_ALLOWLIST` legacy and says it can only be changed to `'None'` from August 2026, with removal planned later. Model RBAC is the forward path. A role may gain model access through either mechanism while both operate, and `ACCOUNTADMIN` bypasses restrictions; test with a non-admin role and no secondary roles. Learn the old parameter name for C02 recognition, but design current grants around RBAC. Model availability also depends on region and lifecycle. [Regional availability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-regional-availability) · [cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)

**Agents:** `SNOWFLAKE.CORTEX_AGENT_USER` is narrower than `CORTEX_USER`. Callers need `USAGE` on database, schema, Agent, and default warehouse, plus their tools. The Agent docs explicitly use the user's **default role**, which can differ from the active worksheet role. `MONITOR` lets a role view threads/logs/traces; `MODIFY` is for updates; `CREATE AGENT` is a schema privilege. Revoking imported privileges on the `SNOWFLAKE` database from `PUBLIC` also removes access to other shared objects such as Account Usage views, so evaluate that broader effect. [Agent access control](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup)

**Search:** creating a managed-embedding service needs schema `CREATE CORTEX SEARCH SERVICE`, source `SELECT`, refresh warehouse `USAGE`, and embedding entitlement. Querying needs `USAGE` on the service and its database/schema. A Search service executes with its owner's rights, so a consumer's service access can expose indexed rows the consumer could not query from the source table directly; design separate services and source filters for distinct audiences. A Search result/citation is not proof of correctness. [Search access and behavior](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)

**Data and residency:** Snowflake says customer data is not used to train models made available to the customer base and AI models run inside its perimeter except as customers elect. Cross-region inference can route an inference payload to another permitted region while account storage remains in the home region; this is a policy and data-residency decision, not just a latency switch. Review supported regions/models and the `CORTEX_ENABLED_CROSS_REGION` parameter. Apply masking, row policies, stage privileges, scoped file URLs and least privilege where the data demands them. [AI/ML overview](https://docs.snowflake.com/en/guides-overview-ai-features) · [cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)

**Guardrails are layered, with different purposes.** `AI_REDACT` addresses PII in text. The `guardrails` option on `AI_COMPLETE` invokes Cortex Guard to filter harmful responses and adds a separate scan charge. The account `AI_SETTINGS` configuration provides prompt-injection/jailbreak protection for CoCo, CoWork, and Agents; it scans tool output and has its own token-based charge and usage view. Neither option grants privileges, guarantees factual accuracy, or replaces output evaluation. [AI_REDACT](https://docs.snowflake.com/en/sql-reference/functions/ai_redact) · [AI_COMPLETE Cortex Guard](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-string) · [Cortex AI Guardrails](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-guardrails)

## 4. Meter every layer, then observe quality

| Feature | Current primary meter | Additional cost to remember |
| --- | --- | --- |
| AI Functions | Model/function token usage in AI Credits | Prompt overhead, warehouse runtime; `AI_PARSE_DOCUMENT` is page billed |
| `AI_EXTRACT` on documents | Input/output tokens; documentation counts each processed page as 970 input tokens | Response format text also counts |
| `AI_COMPLETE` with Cortex Guard | Generation input/output tokens | Separate Guard input-token scan |
| Search | Continuous serving by indexed GB/month; embeddings on changes | Refresh warehouse and storage |
| Agents / CoWork | Orchestration tokens in AI Credits | Tool calls and generated SQL warehouse execution |
| Standalone Analyst API | Per 1,000 messages, legacy Platform Credit path | Warehouse running generated SQL |
| Analyst through Agent | Agent token-based AI Credit path | Warehouse and other invoked tools |
| Cortex Fine-tuning | Training on a legacy Platform Credit path | Later inference is separately billed |
| `AI_FUNCTION_EVALUATION` / `AI_FUNCTION_OPTIMIZATION` (preview) | Serverless compute metered as `SERVERLESS_EXPERIMENTS` | Plus Cortex inference tokens for every AI call the experiment makes |
| ML Functions / custom Snowflake ML | Training, inference/compute and stored model assets | Container/runtime/service resources as used |

For token accounting, [AI Function costs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-cost) says generation usually bills input **and** output, while embedding/similarity bill input. Classification labels, descriptions and examples are repeated input for each record. The page currently states audio equivalence of 50 tokens per second and treats pages processed by `AI_EXTRACT` as 970 input tokens per page; these are operational details to recheck before use. `AI_COUNT_TOKENS` adds warehouse work but no model-inference token charge. Snowflake recommends a warehouse no larger than MEDIUM for AI Function calls because a larger one does not speed the managed model. [AI pricing](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing)

**Usage-view drift:** the dedicated function-cost page still names `CORTEX_FUNCTIONS_USAGE_HISTORY` and `CORTEX_FUNCTIONS_QUERY_USAGE_HISTORY`, while the newer [AI cost-governance matrix](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) marks those views for deprecation and points to `CORTEX_AI_FUNCTIONS_USAGE_HISTORY`. For current reporting, use the matrix's service-type, date and overlap notes. `CORTEX_AGENT_USAGE_HISTORY`, `CORTEX_SEARCH_DAILY_USAGE_HISTORY`, `SNOWFLAKE_COWORK_USAGE_HISTORY`, standalone Analyst history, and `CORTEX_AI_GUARDRAILS_USAGE_HISTORY` each answer a different question. Search embeddings can appear in AI Function history, so summing views directly can double-count. `METERING_DAILY_HISTORY` can answer the older blueprint's daily `AI_SERVICES` question, but current AI Credit reporting needs the modern view matrix. Budgets alert/react periodically; per-user quotas are the built-in blocking control and can overshoot briefly. [Cost governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance)

**Measure and improve a function's quality (preview).** `AI_FUNCTION_EVALUATION` scores an AI function against a labeled Snowflake **dataset** with a chosen metric (`exact_match`, `fuzzy_match`, `contains_match`, `redaction_match`, `llm_judge`, `custom`) and reports an aggregate score plus cost and tokens. `AI_FUNCTION_OPTIMIZATION` searches for a better prompt/model configuration of an existing function (one `AI_COMPLETE` call, up to 1,000 dataset rows, one metric per run), reports a quality-versus-cost frontier, and lets you promote a winning run with `CREATE AI FUNCTION ... FROM EXPERIMENT`. Both are experiments: `CREATE EXPERIMENT ... TYPE = '...' FROM SPECIFICATION $$ yaml $$;` then `EXECUTE EXPERIMENT <name>;`. Needs `CREATE EXPERIMENT` on the schema and `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.AI_FUNCTIONS_USER`. Billing: serverless compute metered as `SERVERLESS_EXPERIMENTS` **plus** Cortex inference tokens. Neither changes the original function. Examples: [09_AI_FUNCTION_EXAMPLES.md](09_AI_FUNCTION_EXAMPLES.md#17-ai_function_evaluation-preview).

Observe **quality as well as spend**. Native Agent/CoWork monitoring exposes threads, traces and evaluations; Analyst has evaluations and SQL/log review; Search has request monitoring. Custom RAG/agent apps can use TruLens to send traces and evaluations to Snowflake AI Observability. Keep a fixed test set with expected evidence, SQL, answer, role, cost and latency, then rerun it after model, semantic-view, prompt, tool or source changes. [AI Observability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability) · [Agent monitoring](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-monitor) · [Analyst evaluations](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst-evaluations) · [TruLens](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens)

## 5. ML beyond the GenAI specialty blueprint

**ML Functions** give analyst-friendly forecasting, anomaly detection, classification and Top Insights over structured data. Forecasting and anomaly detection are time-series tasks; classification and Top Insights do not require a time series. Training/inference consume compute and model assets consume storage. This is Snowflake ML knowledge, but the C02 guide is centered on GenAI. [ML Functions](https://docs.snowflake.com/en/guides-overview-ml-functions)

**Custom Snowflake ML lifecycle:** prepare data and features → train/tune (Notebooks on Container Runtime, ML Jobs, or supported workflows) → compare experiments → log/version in Model Registry → deploy for inference (including model serving on Snowpark Container Services where appropriate) → monitor drift/performance and explainability → trace lineage. The Feature Store provides reusable, refreshed feature views for batch/online retrieval and helps reduce training-serving skew. Model Registry manages versions, grants, and deployment; merely logging a model is not the same as running inference. [Snowflake ML overview](https://docs.snowflake.com/en/developer-guide/snowflake-ml/overview) · [Feature Store](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/overview) · [Model Registry](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview) · [ML Jobs](https://docs.snowflake.com/en/developer-guide/snowflake-ml/ml-jobs/overview) · [ML Observability](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-observability)

**Adaptation decision:** prompt changes fix simple instruction/style failures; retrieval fixes changing knowledge; semantic-view corrections fix metric/join errors; fine-tuning may help stable behavior patterns after evaluation. Custom model development is a separate ML lifecycle with training data, features, deployment, monitoring and costs. [Cortex Fine-tuning](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-finetuning)

## 6. Closed-book checks

1. A role has `SNOWFLAKE.CORTEX_USER` but an administrator revoked `USE AI FUNCTIONS` from `PUBLIC`. What other grant might it need to call `AI_CLASSIFY`?
2. Why might a per-function revocation fail to block `AI_COMPLETE`?
3. Which has a custom instruction: `AI_AGG` or `AI_SUMMARIZE_AGG`?
4. What does `AI_TRANSLATE(text, '', 'en')` do, and how many required arguments does it still have?
5. For a document, distinguish `AI_EXTRACT`, `AI_PARSE_DOCUMENT(OCR)`, and `AI_PARSE_DOCUMENT(LAYOUT)`.
6. Why can `USAGE` on a Search service reveal data a user cannot select from its source table?
7. Why can an Agent fail after you switch to a powerful worksheet role?
8. Name the AI Function usage view favored by the current cost-governance matrix. Why is summing it with Search history unsafe?
9. Which controls PII text, harmful `AI_COMPLETE` output, and prompt injection in Agent tool outputs?
10. Which Snowflake capability manages reusable ML features, which versions models, and which monitors model drift?
11. What is the difference between `AI_FUNCTION_EVALUATION` and `AI_FUNCTION_OPTIMIZATION`, and what two things do both bill for?
12. `AI_SENTIMENT` returned `unknown` for the aspect `Cost`. Does that mean neutral? How does `SNOWFLAKE.CORTEX.SENTIMENT` differ in return type?

<details>
<summary>Answers</summary>

1. The account-level `USE AI FUNCTIONS` grant or `USE AI FUNCTION AI_CLASSIFY`, as well as the applicable database role.
2. A blanket `USE AI FUNCTIONS` grant still permits it; the blanket and per-function grants have an OR relationship.
3. `AI_AGG(expr, instruction)`; `AI_SUMMARIZE_AGG(expr)` is a general aggregate summary.
4. Auto-detects the source language and translates into English; text, source, and target remain required.
5. Targeted structured fields; plain extracted text; structure-preserving Markdown, respectively.
6. Search uses owner-rights behavior and serves indexed content through the service privilege.
7. Agent permissions use the user's default role and default warehouse, not merely the worksheet's active role.
8. `CORTEX_AI_FUNCTIONS_USAGE_HISTORY`; Search embedding costs can appear in both histories.
9. `AI_REDACT`; Cortex Guard via `AI_COMPLETE` options; account-level Cortex AI Guardrails via `AI_SETTINGS`, respectively.
10. Feature Store; Model Registry; ML Observability.
11. Evaluation *scores* an existing function against labeled data; optimization *searches* for a better prompt/model and lets you promote a winner. Both bill serverless compute (`SERVERLESS_EXPERIMENTS`) plus Cortex inference tokens.
12. No. `unknown` means the aspect was not mentioned; `neutral` means it was mentioned without leaning either way. The older function returns one FLOAT from -1 to 1 (English only), not an object with aspects.

</details>

## Reading order and limits

For C02, study [Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) → [function privileges](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access) → [pricing/cost governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) → [Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) → [Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst) → [Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) → [documents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-documents) → [practice questions](05_PRACTICE_EXAM.md). Use the [atlas](07_AI_ML_DOC_ATLAS.md) to branch into any product detail. The atlas is an inventory of 310 linked pages, not 310 individually validated product claims. SQL examples here were checked against references but not executed in a Snowflake account. Product status, regional support, pricing and SQL signatures can change after this review.
