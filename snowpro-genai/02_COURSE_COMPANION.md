# Snowflake GenAI course companion for GES-C02

Prepared 2026-09-24 from the five-page *Snowflake GenAI* instructor-led course datasheet supplied as `standard_genai_datasheet_24J23.pdf` (course code 26F15, two days), the official GES-C02 study guide, and the Snowflake documentation linked below. This is an independent learning plan. The course syllabus is **not** the exam blueprint: it includes broader product and implementation topics. For the exam's exact domain objectives and 18% / 38% / 29% / 15% weights, use the [four-domain guide](01_STUDY_GUIDE.md).

## How to use this companion

Work each unit in order. For every product, be able to explain **when to use it, what input it accepts, what permission it needs, what it bills, and how to check the result**. Write those five answers from memory before opening the docs. Use a test account and synthetic data for labs; many features consume credits when enabled. Where the datasheet names a feature but gives no API detail, the links below point to current docs rather than inventing course content.

If time is short, prioritize units 2–4, 6–8, 11–12, and the [syntax/billing sections](01_STUDY_GUIDE.md) of the exam guide. The other units broaden architectural understanding and cover syllabus topics that may support scenario questions. Do the [28-question practice set](05_PRACTICE_EXAM.md) only after the first closed-book pass.

| Course topic | Main C02 domain | Required result |
| --- | --- | --- |
| GenAI, LLMs, AI Data Cloud, cross-region, REST, container services | 1; 3 | Choose the right Snowflake surface and explain residency |
| AI Functions, prompting, multimodal analytics | 2 | Select function and recall argument shape and billing unit |
| CoCo | 1; 3 | Distinguish developer assistant from end-user agent chat |
| Document Processing Playground and pipelines | 4; 2 | Choose OCR, layout parsing, or extraction |
| Search, Analyst, Agents, Knowledge Extensions | 1; 2; 3 | Design a governed structured/unstructured answer path |
| CoWork | 1; 3 | Explain agent deployment and direct file uploads |
| Fine-tuning, observability, security, cost | 1; 3 | Select adaptation strategy, evaluate, and meter |

## A flexible four-week route

This is a sequence, **not** a fixed booking schedule. Compress or extend it around dbt preparation. Move on when the exit check is passed.

| Phase | Read and build | Exit check |
| --- | --- | --- |
| Week 1: foundations and functions | Units 1–4; run simple AI functions on synthetic rows; compare OCR, layout and field extraction | Explain each function's input/output, exact `AI_TRANSLATE` argument count, and page versus token billing |
| Week 2: retrieval and analytics | Units 5–7; stage documents, create Search; define a semantic view; try Analyst | Answer one document question with source citation and one metric question with reviewed SQL |
| Week 3: agents and governance | Units 8–12; connect Search and Analyst in an Agent; review permissions, traces and usage | Explain a mixed-data answer, every charged component, and where a direct CoWork upload lives |
| Week 4: proof and repair | Unit 13 capstone; take official practice exam and the [original practice set](05_PRACTICE_EXAM.md); maintain error log | Resolve every miss against an official reference; reproduce syntax and billing map without notes |

### 1. Enterprise GenAI foundations

An LLM predicts output from a prompt and context; it does not acquire a live view of your tables by default. Ground it with retrieved evidence or a governed tool. RAG is the usual pattern for changing documents: ingest → parse → chunk → index → retrieve → generate with citations → evaluate. A semantic view gives Analyst business meaning for structured SQL. An Agent can choose among tools and combine their results. Account privileges govern access at each step.

The datasheet also calls out REST APIs, cross-region support, and LLMs on Snowpark Container Services. Distinguish managed Cortex inference from a custom model deployed in a container. Cross-region inference controls **where inference can run**, while account data stays stored in its home region; the inference payload can be routed transiently according to the account setting. Check `CORTEX_ENABLED_CROSS_REGION`, regional model availability, residency requirements, and latency before choosing a model. [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) · [Model Registry](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview) · [Snowpark Container Services](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview) · [Cortex REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api)

**Check:** A support-policy PDF changes daily. Explain why fine-tuning a model is a poor first response to stale policy answers, and sketch the retrieval path instead.

### 2. Cortex AI Functions and prompt design

Group functions by task, rather than memorizing one generic LLM call:

| Task | Function or surface | Decision cue |
| --- | --- | --- |
| Free-form generation or structured response | `AI_COMPLETE` | Set model, prompt and, where supported, output format/options |
| Translate | `AI_TRANSLATE` | Three arguments: text, source, target; an empty source string enables detection |
| Summarize / sentiment / classify | `AI_SUMMARIZE_AGG`, `AI_SENTIMENT`, `AI_CLASSIFY` and related task functions | Prefer specific function when task matches; distinguish row-level from aggregate work |
| Embed or compare text | `AI_EMBED`, `AI_SIMILARITY` | Representation/relevance, not natural-language explanation |
| Extract document fields | `AI_EXTRACT` | Specify questions or schema; returns structured values |
| Parse document text | `AI_PARSE_DOCUMENT` | `OCR` plain text versus `LAYOUT` structured Markdown |

Prompt recipe: specify the task, input boundary, output schema, evidence rule, and fallback for insufficient evidence. For example: “Return `{decision, evidence_id}` as JSON. Use only the supplied policy excerpts. If no excerpt answers the question, set `decision` to `unknown`.” Then test adversarial and empty evidence, as well as a normal case. A prompt is an instruction to the model, **not** an access-control boundary. [AI Functions overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) · [AI_COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/ai_complete) · [AI_TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/ai_translate) · [AI_COUNT_TOKENS](https://docs.snowflake.com/en/sql-reference/functions/ai_count_tokens)

**Syntax trap:** `AI_TRANSLATE('Bonjour', '', 'en')` asks Snowflake to detect French. The current reference does not describe a two-argument form that omits the source argument. Recheck exact signatures just before the exam.

**Lab:** Run one task-specific function and one `AI_COMPLETE` prompt on the same ten synthetic support rows. Record output quality, input/output token estimates, and whether a warehouse or other resource was used. Change only one prompt factor at a time.

### 3. Multimodal analytics

Multimodal means a task can use more than plain text, such as image or document content. The correct path depends on the desired result: parse a scanned form to text, extract named fields, or provide an image/file to a model function that supports that input. Do not infer support for a file type or size from another function: `AI_EXTRACT` and `AI_PARSE_DOCUMENT` have distinct limits. Check model, function, region, stage, and file requirements before a lab. [AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql) · [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract) · [AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document)

**Check:** A scanned receipt needs vendor, date, and total as columns. Select extraction. A long policy PDF needs preserved headings for retrieval. Select layout parsing, then chunking and Search.

### 4. Intelligent Document Processing

Use the [Document Processing Playground](https://docs.snowflake.com/en/user-guide/snowflake-cortex/document-processing-playground) in Snowsight (AI & ML → AI Studio) to preview `AI_EXTRACT`, `AI_PARSE_DOCUMENT` layout Markdown, and OCR text, then copy the generated SQL or Python snippet. The UI is an exploration surface, not the production pipeline. Local Playground uploads require a personal database and have a 50 MB UI limit; stage uploads follow their own path. The Playground accepts up to ten documents. Those limits are **not** interchangeable with the underlying functions' limits.

Production pattern: put source files in a governed internal or external stage; identify files via directory metadata; pass a FILE object such as `TO_FILE('@DB.SCHEMA.STAGE','invoice.pdf')`; parse or extract; persist output plus source path, page, status, and processing time; retry failures; chunk text if building Search. Streams and tasks can make the pipeline incremental. Keep raw document access and Search index access aligned with the intended audience. [Parsing guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/parse-document) · [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract) · [directory tables](https://docs.snowflake.com/en/user-guide/data-load-dirtables) · [streams and tasks](https://docs.snowflake.com/en/user-guide/data-pipelines-intro)

**Lab:** With a synthetic two-page invoice, compare the Playground's Text, Markdown, and Extraction tabs. Write down one fact layout retains that OCR flattens, and one field extraction makes easier than full-text parsing. Then run the copied snippet in a worksheet and inspect the result type.

### 5. Snowflake CoCo

**CoCo** is Snowflake's assistant for developing and operating Snowflake work. Current docs describe Snowsight, Desktop, and CLI experiences. It can help author SQL and notebooks, explore schemas, and work on local code (Desktop/CLI). It does not replace a deployed Cortex Agent or a semantic view. Review suggested SQL, file changes, and privileges before applying them. CoCo billing is token based for account usage; local development can also trigger ordinary Snowflake compute/storage charges. The C02 blueprint may still use the older name *Cortex Code*. [CoCo overview](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) · [CLI reference](https://docs.snowflake.com/en/user-guide/cortex-code/cli-reference) · [CoCo cost controls](https://docs.snowflake.com/en/user-guide/cortex-code/cost-controls)

**Check:** A data engineer asks an assistant to debug a local dbt project: CoCo Desktop or CLI fits. A business user asks a governed sales question through a published agent: CoWork fits.

### 6. Cortex Search

Search builds an index over selected text, then supports retrieval with keyword and semantic signals and reranking. Source data and a refresh warehouse feed the index. The `ON` column is searched; `ATTRIBUTES` can be filtered; `TARGET_LAG` expresses desired freshness. Include source ID, page, and permitted citation metadata in the indexed result. Test both exact keywords and paraphrases, then inspect whether the cited chunk actually supports the answer. A service can incur serving charges even when no one asks questions. [Search overview and create/query syntax](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) · [Search cost](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-costs)

**Lab:** Build a small Search service over three synthetic policies with a document ID and category attribute. Compare top results for “refund deadline” and “how long do I have to return an item?” Record precision, source ID, index size, refresh work, and idle serving usage. Review the [Search example in the exam guide](01_STUDY_GUIDE.md).

### 7. Cortex Analyst and the semantic layer

Analyst converts a natural-language **structured-data** question into SQL using a semantic view/model. Define business metrics, dimensions, entities/relationships, synonyms, and verified questions. Review generated SQL and result values; a fluent explanation can accompany an incorrect join or grain. Custom instructions guide behavior but do not grant access. For a time-series metric, check time grain, filters, denominator and metric definition. Current docs recommend reaching Analyst through a **Cortex Agent** (semantic view as an Analyst tool) rather than the standalone API; the C02 blueprint still uses the Analyst framing. [Analyst overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst) · [semantic views](https://docs.snowflake.com/en/user-guide/views-semantic/overview) · [verified query repository](https://docs.snowflake.com/en/user-guide/views-semantic/verified-query-repository)

**Lab:** Work through the [semantic-layer lab](08_SEMANTIC_LAYER.md#4-build-one-lab-with-known-answers). It uses a three-table synthetic star schema with hand-calculated answers. Query it with `SEMANTIC_VIEW(...)` and with `AGG()`, trigger the grain error, then ask "net sales by month for completed orders" through an Agent or Analyst. Review the generated SQL against the expected results. Add one verified query for a business phrase that was ambiguous.

### 8. Cortex Agents and MCP

An Agent plans a response and calls configured tools: Analyst for governed structured data, Search for unstructured evidence, and optionally custom, code, or connector tools. It can converse with no tools, but then it has no account-data retrieval. Design tool descriptions so selection is unambiguous, give the caller only necessary access, and test wrong-tool, missing-permission, prompt-injection, and no-answer cases. Check the trace and citations before exposing it to users. [Agents overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) · [agent setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup) · [monitoring](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability)

MCP is a protocol for tool discovery and invocation. Snowflake can **serve** Snowflake resources as tools through a managed MCP server, or an Agent/CoWork can **consume** tools from an external MCP server through a connector. These are different directions. External connectors add integration, authentication, privilege, and third-party tool risk; a tool call can perform an action, so grant least privilege. For business-data clients, Snowflake recommends exposing a governed Agent as the MCP tool instead of giving a client unrestricted direct SQL. [Snowflake-managed MCP server](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp) · [MCP connectors](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp-connectors)

**Lab:** Give an Agent one Search service and one semantic view. Ask (1) a policy-only question, (2) a sales-only question, (3) a question combining both. Trace the chosen tool sequence and confirm that each final claim has the right evidence.

### 9. Snowflake CoWork and uploaded files

CoWork is the business-user conversation surface for Agents. Publishing/visibility and using an Agent are separate concerns: the user needs Agent access; admins can curate which Agents appear in the CoWork object. The C02 PDF calls this experience **Snowflake Intelligence**; current docs use **Snowflake CoWork** in navigation while some SQL object names still say `SNOWFLAKE INTELLIGENCE`. [CoWork overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork) · [agent visibility](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents)

**Reported exam detail:** a file uploaded **directly into a CoWork chat** is saved in the user's personal stage and associated with that thread, then cleaned up when the thread is deleted or expires. That is different from a file deliberately placed in a named/external stage to build a document pipeline or Search index. [CoWork zero-setup file upload](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork#zero-setup-file-upload)

**Check:** If an Agent exists but does not appear in CoWork, investigate Agent `USAGE` and CoWork visibility configuration before rebuilding the Search index.

### 10. Cortex Knowledge Extensions

A Cortex Knowledge Extension (CKE) is a **Cortex Search service shared through a listing** (Marketplace, private, or organizational). A provider creates a Search service over its text and shares it; a consumer uses that indexed knowledge in a RAG application while the provider retains content protections and can manage trial/monetization settings. Think “share a governed retrieval resource,” not “train a shared model.” [CKE overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview)

**Check:** A research publisher wants customers' assistants to cite licensed articles without handing over the entire source table. A CKE is worth investigating. An internal support team indexing its own private PDFs normally starts with a regular Search service.

### 11. Fine-tuning and adaptation choices

Start with the cheapest change that addresses the failure: improve a prompt for wording/format; use retrieval for changing facts; improve the semantic view or verified queries for wrong business SQL; evaluate fine-tuning when repeated examples show a stable task-specific behavior gap. Cortex Fine-tuning creates a customized adapter from a supported base model; training and later inference have separate charges. It does not automatically refresh knowledge from a changing policy table. Check supported model, region, training data and privileges before scheduling a job. [Cortex Fine-tuning](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-finetuning)

**Check:** “The bot ignores a stable required output style” suggests prompt tests, then perhaps fine-tuning. “The answer used last month's policy” suggests retrieval freshness and citations, not fine-tuning first.

### 12. Observability, governance and cost

Evaluate with a small golden set: question, expected evidence, expected answer or SQL, allowed role, and failure mode. Track answer correctness, groundedness, retrieval relevance, latency, tokens, tool path, refusals, and cost per useful answer. Native Cortex Agents have their own traces/evaluations. **TruLens** instruments custom RAG/agent applications and sends traces/evaluation results into Snowflake AI Observability; it is not required just to monitor a native Agent. [AI Observability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability) · [TruLens integration](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens)

Security checklist for an answer path: caller role → database/schema and source access → Search/semantic-view/Agent privileges → model access and regional routing → prompt and retrieved-data boundaries → output review → audit. Search can expose indexed content to a role with service `USAGE` under its documented owner-rights behavior, so segment services by audience. Guardrails, redaction, masking and row policies mitigate different risks; none replaces testing. [Search access](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) · [AI governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) · [Guardrails](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-guardrails)

| Path | Meter to recall | Also inspect |
| --- | --- | --- |
| CoCo / CoWork / Agent | Model tokens, generally AI Credits | Invoked tools and ordinary compute/storage |
| Standalone Analyst API | Per 1,000 messages, legacy Platform Credit path | Warehouse executing generated SQL |
| Analyst through Agent | Agent token-based path | Warehouse for generated SQL and other invoked tools |
| Search | Continuous serving by indexed GB/month; embedding tokens on insert/update | Refresh warehouse, index storage, query activity |
| AI functions | Model/function-dependent tokens, generally AI Credits | Warehouse work; input and output tokens where applicable |
| `AI_PARSE_DOCUMENT` | Pages processed, mode-dependent AI Credit rate | Stage storage and downstream work |
| Fine-tuning | Training tokens on a legacy Platform Credit path; later inference tokens separately | Model use and any supporting compute |

Use the current [pricing page](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing) for rates, not a memorized number. For cost totals, follow the [current usage-view matrix](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance). `CORTEX_AGENT_USAGE_HISTORY`, `CORTEX_AI_FUNCTIONS_USAGE_HISTORY`, `CORTEX_SEARCH_DAILY_USAGE_HISTORY`, and `SNOWFLAKE_COWORK_USAGE_HISTORY` answer different questions. Do not add overlapping views blindly: Search embedding can also appear in AI-functions history. Budgets help track spend; per-user quotas are the documented built-in blocking control. A larger warehouse does not inherently make managed inference faster.

**Cost drill:** An Agent receives one question, calls Search, asks Analyst for SQL, executes the SQL, then generates a response. List the possible charges in order: Agent orchestration tokens, Search serving/embedding related usage as applicable, Analyst route usage, warehouse SQL execution, and any function or other tool invoked. Explain why “one prompt = one charge” is false. Distinguish the Search service's continuing idle serving charge from the per-request costs.

### 13. Capstone: an answerable, auditable support assistant

Build this only with synthetic data and a test role. Save a short design/measurement note in your own lab repo or notebook.

1. Create three policy documents with different refund rules and ten synthetic orders with dates, regions and amounts. Record ground-truth answers to ten questions: four policy, four metric, two mixed.
2. Upload policies to a governed stage. Compare Playground OCR, Markdown layout and field extraction. Persist parsed text with document ID and page. Capture a deliberate parsing failure and the error message.
3. Build a Search service over chunks with document ID and page. Test an exact keyword, paraphrase and no-answer question. Confirm citation links point to the correct source.
4. Define a semantic view for orders. Add one verified query. Ask Analyst for monthly net sales and review the SQL and arithmetic.
5. Create an Agent with the Search service and semantic view. Ask the two mixed questions and inspect the tool trace. Test a role that lacks one tool and record actual behavior.
6. Compare answers with your ground truth. Record accuracy, unsupported claims, latency and all cost components. Review role grants, cross-region setting, guardrail behavior and usage views. Remove charge-bearing test services when finished.

For exact SQL shapes, see the [exam guide](01_STUDY_GUIDE.md), and use each linked reference immediately before executing: product syntax and feature availability change. No SQL in this repository has been executed in a Snowflake account.

## Closed-book retrieval questions

1. Which product generates SQL from a governed business metric definition, and which product retrieves matching document passages?
2. What argument value enables source-language detection in `AI_TRANSLATE`, and can the source argument be omitted in the documented signature?
3. When would you use `AI_PARSE_DOCUMENT(LAYOUT)` instead of `AI_EXTRACT`?
4. What three expenses should you consider when creating a Cortex Search service even if query volume is low?
5. What changes when Analyst is called through an Agent rather than through the standalone API?
6. Where does a file uploaded directly in CoWork chat reside? Is that the same location as a production named stage?
7. What is the distinction between a managed MCP server and an external MCP connector?
8. Why does a CKE resemble Search more than fine-tuning?
9. When is TruLens appropriate, and when can you use native Agent monitoring?
10. For a bot that cites an obsolete policy, what should you inspect before considering fine-tuning?

<details>
<summary>Answer key</summary>

1. Analyst with a semantic view; Search for document retrieval.
2. Empty string `''`; the documented call still has text, source and target arguments.
3. Layout parsing preserves document structure as Markdown for downstream reading/retrieval; extraction returns targeted structured fields.
4. Embedding on inserts/updates, continuous index serving, and refresh warehouse; account for index storage too.
5. Agent-path token billing and orchestration/tool costs replace the standalone per-message Analyst path; SQL warehouse charges still apply.
6. The user's personal stage, associated with the thread; no, production stages are separate governed objects.
7. The managed server exposes Snowflake tools to MCP clients; a connector lets Snowflake Agents/CoWork call an external MCP server.
8. A CKE is a shared Cortex Search service/listing for retrieval, not adjusted model weights.
9. TruLens for a custom application needing exported traces/evaluations; native Agent monitoring for Snowflake Cortex Agents.
10. Document freshness, ingestion/refresh lag, retrieval result, citation and prompt grounding.

</details>

## Source and version notes

- The supplied datasheet is a **course topic list**, with no exam weights or exact SQL signatures. The [official C02 PDF](https://learn.snowflake.com/en/certifications/snowpro-GenAI-C02/?pdf_name=SnowProGenAIStudyGuideC02.pdf) remains the exam map. The 26F15 datasheet adds CoCo, CoWork, MCP, CKE, fine-tuning and TruLens detail that may be broader than the C02 tested scope.
- Product names drift: *Snowflake Intelligence* in the April 2026 blueprint corresponds to current CoWork documentation; *Cortex Code* appears in the blueprint while current product docs say CoCo. Some current SQL object names still retain earlier names. Read the actual question's wording and check live references for operations.
- Pricing, region availability, privilege requirements and function parameters can change. Recheck the [pricing page](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing), [AI Functions reference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql), and [official documentation index](06_OFFICIAL_DOC_INDEX.md) just before booking.
