# Snowflake AI/ML documentation atlas

Generated 2026-09-25 from Snowflake's official `llms.txt` section indexes.
This is a **page inventory**, not a claim that every page is examined in depth or that every detail is on the GES-C02 exam.
Each entry was fetched to check availability and read its Markdown headings. Use the [deep-dive guide](AI_ML_DEEP_DIVE.md) for the synthesized study notes.
The first three sections come from live official section indexes; the final two add ML Function and SQL reference pages linked by the user's entry points. Run `python build_ai_ml_doc_atlas.py` to refresh.

| Collection | Indexed pages |
| --- | ---: |
| [Snowflake Cortex](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llms.txt) | 111 |
| [Snowflake CoCo](https://docs.snowflake.com/en/user-guide/cortex-code/llms.txt) | 76 |
| [Snowflake ML](https://docs.snowflake.com/en/developer-guide/snowflake-ml/llms.txt) | 94 |
| [AI/ML overview and ML Functions](https://docs.snowflake.com/en/guides-overview-ai-features.md) | 7 |
| [SQL AI Function references](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql.md) | 22 |

Unique pages: **310**. Fetch failures: **0**.

## Snowflake Cortex

[Official section index](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llms.txt)

| Page | First section headings | Fetch |
| --- | --- | --- |
| [Access control and authentication](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup.md) | Access control and authentication; API access roles; User requirements | OK |
| [Agent skills](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-skills.md) | Agent skills; How skills work; Skill sources | OK |
| [Agent toolsets](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-toolsets.md) | Agent toolsets; How agent toolsets work; Configure an agent toolset | OK |
| [AI cost management and governance](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance.md) | AI cost management and governance; Usage views; Budget features | OK |
| [AI Observability Tutorial](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/tutorial.md) | AI Observability Tutorial | OK |
| [AI Observability with Snowflake Cortex](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability.md) | AI Observability with Snowflake Cortex; What is AI observability?; Where to start | OK |
| [AI_COMPLETE with documents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-complete-document-intelligence.md) | AI_COMPLETE with documents; Processing documents with AI_COMPLETE; Chart Q&A example | OK |
| [Analytical search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-analytical-search.md) | Analytical search; How analytical search works; Analytical search vs. traditional RAG | OK |
| [Artifacts in Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/artifacts.md) | Artifacts in %sf-intelligence%; Artifact types; Interactive tables and charts | OK |
| [Automations in Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/automations.md) | Automations in %sf-intelligence%; How automations work; Create an automation | OK |
| [Batch Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/batch-cortex-search.md) | Batch Cortex Search; Syntax; Parameters | OK |
| [Build agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/build-agents.md) | Build agents; Agent structure; Prerequisites | OK |
| [CKE document access history](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-access-history.md) | CKE document access history; Prerequisites; Understand document IDs | OK |
| [Coding Agent](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-coding-agent.md) | Coding Agent; Quickstart; Included tools | OK |
| [Copy `arctic-extract` models between databases, schemas, and accounts](https://docs.snowflake.com/en/user-guide/snowflake-cortex/copy-arctic-extract-models.md) | Copy arctic-extract models between databases, schemas, and accounts; Copy models between databases and/or schemas within an account; Copy models between accounts | OK |
| [Cortex Agent code execution tool](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-code-execution-tool.md) | Cortex Agent code execution tool; How the code execution tool works; Enabling the code execution tool | OK |
| [Cortex Agent evaluations](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-evaluations.md) | Cortex Agent evaluations; Access control requirements; Prepare an evaluation dataset | OK |
| [Cortex Agent versioning](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-versioning.md) | Cortex Agent versioning; How agent versioning works; Live versions | OK |
| [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents.md) | Cortex Agents; Overview; Key concepts | OK |
| [Cortex Agents Compact API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-compact.md) | Compact a Cortex Agent conversation; Endpoint; Compaction modes | OK |
| [Cortex Agents for Microsoft Teams and Microsoft 365 Copilot](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-teams-integration.md) | Cortex Agents for Microsoft Teams and Microsoft 365 Copilot; Introduction; Regional availability and limitations | OK |
| [Cortex Agents REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-rest-api.md) | Cortex Agents REST API; Create Cortex Agent; Describe Cortex Agent | OK |
| [Cortex Agents Run API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-run.md) | Cortex Agents Run API; Agent run request with agent object; Agent run without an agent object | OK |
| [Cortex Agents shared resource budgets](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-shared-budgets.md) | Cortex Agents shared resource budgets; How shared resource-level budgets work; Set up a shared resource-level budget | OK |
| [Cortex AI Function Evaluation and Optimization](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-function-studio.md) | Cortex AI Function Evaluation and Optimization; Workflow overview; Create | OK |
| [Cortex AI Functions: Audio](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-audio.md) | Cortex AI Functions: Audio; AI_TRANSCRIBE; Examples | OK |
| [Cortex AI Functions: Documents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-documents.md) | Cortex AI Functions: Documents; Document functions; Use cases | OK |
| [Cortex AI Functions: Image extraction with AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/user-guide/snowflake-cortex/image-extraction.md) | Cortex AI Functions: Image extraction with AI_PARSE_DOCUMENT; Using AI_PARSE_DOCUMENT to extract images; Examples | OK |
| [Cortex AI Functions: Images](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-images.md) | Cortex AI Functions: Images; Input requirements; Analyze images | OK |
| [Cortex AI Functions: Multimodal](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-multimodal.md) | Cortex AI Functions: Multimodal; Supported media types and functions; Examples | OK |
| [Cortex AI Gateway](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-gateway.md) | Cortex AI Gateway; Capabilities; Access control | OK |
| [Cortex AI Guardrails](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-guardrails.md) | Cortex AI Guardrails; Overview; Configure Cortex AI Guardrails | OK |
| [Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst.md) | %cortex-analyst%; Overview; Understanding Semantic Views | OK |
| [Cortex Analyst administrator monitoring](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/admin-observability.md) | %cortex-analyst% administrator monitoring; Accessing logs; Querying logs with SQL | OK |
| [Cortex Analyst evaluations](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst-evaluations.md) | %cortex-analyst% evaluations; Access control requirements; Prepare an evaluation set | OK |
| [Cortex Analyst REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api.md) | %cortex-analyst% REST API; Send message; Send feedback | OK |
| [Cortex Knowledge Extensions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview.md) | Cortex Knowledge Extensions; Overview; How CKE works | OK |
| [Cortex Playground](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-playground.md) | Cortex Playground; Required privileges; Get started with the Cortex Playground | OK |
| [Cortex REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api.md) | Cortex REST API; Monitor usage; Choose your API | OK |
| [Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview.md) | Cortex Search; Overview; When to use Cortex Search | OK |
| [Cortex Search tutorials](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/overview-tutorials.md) | Cortex Search tutorials | OK |
| [Cost considerations for Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-cost.md) | Cost considerations for Cortex AI Functions; Warehouse sizing; Track costs for AI services | OK |
| [Cost management for Cortex AI Gateway](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-gateway/cost-management.md) | Cost management for Cortex AI Gateway; Monitor gateway usage; Choose a spending control | OK |
| [Create and manage agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-manage.md) | Create and manage agents; Create an agent; Add tools | OK |
| [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference.md) | Cross-region inference; How it works; Choosing a routing option | OK |
| [Customize charts in Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/chart-customization.md) | Customize charts in %sf-intelligence%; Overview; Agent-level customization | OK |
| [Customizing Cortex Search scoring](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring.md) | Customizing Cortex Search scoring; Numeric boosts and time decays; Reranking | OK |
| [Document generation in Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/document-generation.md) | Document generation in %sf-intelligence%; Prerequisites; Supported formats | OK |
| [Document Processing Playground](https://docs.snowflake.com/en/user-guide/snowflake-cortex/document-processing-playground.md) | Document Processing Playground; Required privileges; Get started with the Document Processing Playground | OK |
| [Evaluate applications with TruLens](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens.md) | Evaluate applications with TruLens; Evaluation workflow; Map span attributes for metrics | OK |
| [Extracting information from documents with AI_EXTRACT](https://docs.snowflake.com/en/user-guide/snowflake-cortex/document-extraction.md) | Extracting information from documents with AI_EXTRACT; Extraction quality; Question optimization for extracting information | OK |
| [Feedback REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-feedback-rest-api.md) | Feedback REST API; Collect feedback about a Cortex Agent; View feedback for Cortex Agents | OK |
| [Fine-tuning (Snowflake Cortex)](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-finetuning.md) | Fine-tuning (Snowflake Cortex); Overview; Cost considerations | OK |
| [Fine-tuning `arctic-extract` models](https://docs.snowflake.com/en/user-guide/snowflake-cortex/arctic-extract-finetuning.md) | Fine-tuning arctic-extract models; Syntax; Dataset requirements | OK |
| [Get started with Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-get-started.md) | Get started with Cortex Agents; Let CoCo walk you through it; What the manual walkthrough builds | OK |
| [Getting started with Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/getting-started.md) | Getting started with %sf-intelligence%; Prerequisites; Create a database, schema, and tables and load data from AWS S3 | OK |
| [Governance and availability](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability.md) | Governance and availability; Cross-region inference; Model availability | OK |
| [Improve literal search to enhance Cortex Analyst responses](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/cortex-analyst-search-integration.md) | Improve literal search to enhance Cortex Analyst responses; Semantic search over sample values; Semantic search using Cortex Search Service | OK |
| [Inaccessible tool handling](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling.md) | Inaccessible tool handling; Where to set the field; Access modes | OK |
| [Inference with Cortex AI Gateway](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-gateway/inference.md) | Inference with Cortex AI Gateway; Gateway endpoint; Pricing | OK |
| [Integrate tools and data](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/integrate-tools.md) | Integrate tools and data; Use the Snowflake-managed MCP server to connect to your agents from external MCP clients | OK |
| [Managing Cortex AI Function costs with Account Usage](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-func-cost-management.md) | Managing Cortex AI Function costs with Account Usage; Usage history view; Basic usage monitoring | OK |
| [MCP Connectors](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp-connectors.md) | MCP Connectors; Overview; Set up supported MCP connectors | OK |
| [Models and regional availability for Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-regional-availability.md) | Models and regional availability for Cortex AI Functions; Choosing a model; Model restrictions | OK |
| [Monitor Cortex Agent requests](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-monitor.md) | Monitor Cortex Agent requests; Observability vs evaluations (Cortex Agents); Terminology | OK |
| [Monitor Cortex Search requests](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor.md) | Monitor Cortex Search requests; Information collected in request logs; Enable request logging | OK |
| [Multi-tenancy for Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-multi-tenancy.md) | Multi-tenancy for Cortex Agents; How multi-tenancy works; Session attributes | OK |
| [Observability for Cortex AI Gateway](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-gateway/observability.md) | Observability for Cortex AI Gateway; How traces are structured; Send client traces to the gateway | OK |
| [Onboarding questions in Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/suggested-questions-feature.md) | Onboarding questions in %cortex-analyst%; How onboarding questions work; How to configure onboarding questions | OK |
| [Opt out of Snowflake AI features](https://docs.snowflake.com/en/user-guide/snowflake-cortex/opting-out.md) | Opt out of Snowflake AI features; Opt out of default features; Revoke access to opt-in features | OK |
| [Optimize an existing semantic view or model with verified queries](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/analyst-optimization.md) | Optimize an existing semantic view or model with verified queries; Prerequisites; Use optimization | OK |
| [Overview of Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork.md) | Overview of %sf-intelligence%; Key capabilities; How it works | OK |
| [Parsing documents with AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/user-guide/snowflake-cortex/parse-document.md) | Parsing documents with AI_PARSE_DOCUMENT; Processing modes; Examples | OK |
| [Privileges and model access for Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access.md) | Privileges and model access for Cortex AI Functions; Cortex LLM privileges; Control model access | OK |
| [Provisioned Throughput](https://docs.snowflake.com/en/user-guide/snowflake-cortex/provisioned-throughput.md) | Provisioned Throughput; Overview; Access control requirements | OK |
| [Query a Cortex Search Service](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service.md) | Query a Cortex Search Service; Parameters; Syntax | OK |
| [Reference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/reference.md) | Reference; SQL commands and API reference; Supported models and regions | OK |
| [Replicate a Cortex Search Service](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-replication.md) | Replicate a Cortex Search Service; Create a replicated Cortex Search Service using a replication group; Create a replicated Cortex Search Service using a failover group | OK |
| [Resource budgets for Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-resource-budgets.md) | Resource budgets for Cortex Agents; How resource budgets work; Create a tag | OK |
| [Resource budgets for Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-resource-budgets.md) | Resource budgets for Cortex Search; How resource budgets work; Create a tag | OK |
| [Resource budgets for Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/cowork-resource-budgets.md) | Resource budgets for %sf-intelligence%; How resource budgets work; Create a tag | OK |
| [Routing Mode for Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/cortex-analyst-routing-mode.md) | Routing Mode for Cortex Analyst; Benefits of Routing Mode; How it works | OK |
| [Secure agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-secure.md) | Secure agents; How secure agents work; Create a secure agent | OK |
| [Share Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-sharing.md) | Share Cortex Agents; Requirements; Set a Cortex Agent as shared | OK |
| [Snowflake AI Observability Reference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/reference.md) | Snowflake AI Observability Reference; Dataset and attributes; Evaluation metrics | OK |
| [Snowflake AI pricing](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing.md) | Snowflake AI pricing; AI Credits compared to Platform Credits; AI Credit price | OK |
| [Snowflake Cortex AI Functions (including LLM functions)](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql.md) | Snowflake Cortex AI Functions (including LLM functions); Available functions; Performance considerations | OK |
| [Snowflake CoWork shared resource budgets](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/cowork-shared-budgets.md) | %sf-intelligence% shared resource budgets; How shared resource-level budgets work; Set up a shared resource-level budget | OK |
| [Snowflake-managed MCP server](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp.md) | Snowflake-managed MCP server; Overview; MCP server security recommendations | OK |
| [Threads API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-threads-rest-api.md) | Threads API; Create thread; Describe thread | OK |
| [Trace and monitor applications with TruLens](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens.md) | Trace and monitor applications with TruLens; Get started; Tracing vs evaluation | OK |
| [Troubleshooting](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/troubleshooting.md) | Troubleshooting; Common issues and solutions; Performance optimization | OK |
| [Tutorial 1: Build a simple search application with Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/tutorials/cortex-search-tutorial-1-search.md) | Tutorial 1: Build a simple search application with Cortex Search; Introduction; Step 1: Setup | OK |
| [Tutorial 1: Providers set up and test a CKE](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/setup-test-cke-tutorial.md) | Tutorial 1: Providers set up and test a CKE; Introduction; Step 1: Create Snowflake objects | OK |
| [Tutorial 2: Build a simple chat application with Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/tutorials/cortex-search-tutorial-2-chat.md) | Tutorial 2: Build a simple chat application with Cortex Search; Introduction; Step 1: Setup | OK |
| [Tutorial 2: Consumer interfaces with a CKE in a Streamlit chatbot](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/query-cortex-search-service-tutorial.md) | Tutorial 2: Consumer interfaces with a CKE in a Streamlit chatbot; Introduction; Step 1. Set up your environment | OK |
| [Tutorial 3: Add a CKE to Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/add-cke-to-snowflake-cowork-tutorial.md) | Tutorial 3: Add a CKE to %sf-intelligence%; Step-by-step instructions | OK |
| [Tutorial 3: Build a PDF chatbot with Cortex Search](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/tutorials/cortex-search-tutorial-3-chat-advanced.md) | Tutorial 3: Build a PDF chatbot with Cortex Search; Introduction; Step 1: Setup | OK |
| [Tutorial: Answer questions about time-series revenue data with Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/tutorials/tutorial-1.md) | Tutorial: Answer questions about time-series revenue data with Cortex Analyst; Introduction; Step 1: Setup | OK |
| [Tutorials](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-knowledge-extensions/overview-tutorials.md) | Tutorials | OK |
| [Understanding cost for Cortex Search Services](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-costs.md) | Understanding cost for Cortex Search Services; Cost categories; Managing indexing costs | OK |
| [Use case examples](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/templates.md) | Use case examples | OK |
| [Use Cortex Search with Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-agents.md) | Use Cortex Search with Cortex Agents; Use cases; Connect Cortex Search to an agent | OK |
| [Use threads with the Cortex Agent REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-threads.md) | Use threads with the Cortex Agent REST API; Start a new thread and use it with Agent Run; Read the returned message IDs | OK |
| [User access and settings for agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents.md) | User access and settings for agents; Customize the %sf-intelligence% interface; User privileges and access control | OK |
| [User skills in Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-cowork/user-skills.md) | User skills in %sf-intelligence%; Prerequisites; How user skills work | OK |
| [Using Cortex AI Functions with Python and Snow CLI](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-programmatic-use.md) | Using Cortex AI Functions with Python and Snow CLI; Call Cortex AI Functions in Snowpark Python; Summarize reviews per product | OK |
| [Vector embedding REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api/embed-api.md) | Vector embedding REST API; Setting up authentication; Setting up authorization | OK |
| [Vector Embeddings](https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings.md) | Vector Embeddings; Text embedding models; About vector similarity functions | OK |
| [Visualization policies for chart customization in Snowflake CoWork](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-viz-policies.md) | Visualization policies for chart customization in %sf-intelligence%; How it works; Where to define policies | OK |
| [Working with temporary agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-temporary.md) | Working with temporary agents; Overview; Creating a temporary agent | OK |

## Snowflake CoCo

[Official section index](https://docs.snowflake.com/en/user-guide/cortex-code/llms.txt)

| Page | First section headings | Fetch |
| --- | --- | --- |
| [Agent mode and Plan mode](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/agent-mode-and-plan-mode.md) | Agent mode and Plan mode; Overview; Agent mode | OK |
| [Agent view and Editor view](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/agent-view-and-editor-view.md) | Agent view and Editor view; Views at a glance; Agent view | OK |
| [Agentic Browser](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/agentic-browser.md) | Agentic Browser; Agent view vs Editor view; Opening the browser | OK |
| [Agentic Notebook](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/agentic-notebook.md) | Agentic Notebook in CoCo Desktop; Prerequisites; How the agent works with your notebook | OK |
| [Agents](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/agents.md) | Agents in CoCo Desktop; When to use agents; Launching an agent | OK |
| [Automations](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/automations.md) | Automations; What automations are good for; Quick start | OK |
| [Building apps](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/building-apps.md) | Building apps; Prerequisites; Supported frameworks | OK |
| [Cloud Agents](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-snowsight/cloud-agents.md) | Cloud Agents; What's enabled; How to use it | OK |
| [CoCo automations in CLI and Snowsight (*Preview*)](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-automations.md) | CoCo automations in CLI and Snowsight (Preview); Overview; How automations work | OK |
| [CoCo CLI](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-cli.md) | CoCo CLI; Install CoCo CLI; Connect to Snowflake | OK |
| [CoCo CLI Agent Client Protocol (ACP) support](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-acp.md) | CoCo CLI Agent Client Protocol (ACP) support; Supported ACP clients; Prerequisites | OK |
| [CoCo CLI agent tools](https://docs.snowflake.com/en/user-guide/cortex-code/tools.md) | CoCo CLI agent tools; File tools; Shell tools | OK |
| [CoCo CLI bundled skills](https://docs.snowflake.com/en/user-guide/cortex-code/bundled-skills.md) | CoCo CLI bundled skills; Getting started; Development and applications | OK |
| [CoCo CLI cloud sandbox](https://docs.snowflake.com/en/user-guide/cortex-code/cloud-sandbox.md) | CoCo CLI cloud sandbox; When to use cloud mode; Starting a cloud session | OK |
| [CoCo CLI extensibility](https://docs.snowflake.com/en/user-guide/cortex-code/extensibility.md) | CoCo CLI extensibility; Skills; Subagents | OK |
| [CoCo CLI keyboard shortcuts](https://docs.snowflake.com/en/user-guide/cortex-code/keyboard-shortcuts.md) | CoCo CLI keyboard shortcuts; Input shortcuts; View shortcuts | OK |
| [CoCo CLI Model Context Protocol (MCP) support](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-mcp.md) | CoCo CLI Model Context Protocol (MCP) support; Transport types; Managing MCP servers | OK |
| [CoCo CLI plugins](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-plugins.md) | CoCo CLI plugins; What a plugin contributes; Plugin layout | OK |
| [CoCo CLI reference](https://docs.snowflake.com/en/user-guide/cortex-code/cli-reference.md) | CoCo CLI reference; Starting CoCo; CLI options | OK |
| [CoCo CLI sandbox](https://docs.snowflake.com/en/user-guide/cortex-code/sandbox.md) | CoCo CLI sandbox; Platform support; Enabling the sandbox | OK |
| [CoCo CLI Settings](https://docs.snowflake.com/en/user-guide/cortex-code/settings.md) | CoCo CLI Settings; Configuration files; Environment variables | OK |
| [CoCo CLI workflow examples](https://docs.snowflake.com/en/user-guide/cortex-code/workflows.md) | CoCo CLI workflow examples; Use cases: Data discovery and querying; Use cases: Building Cortex Agents | OK |
| [CoCo Desktop](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/index.md) | CoCo Desktop; Access control requirements; What's new | OK |
| [CoCo in Snowsight](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-snowsight.md) | CoCo in Snowsight; Overview; Use cases and benefits | OK |
| [Code mode](https://docs.snowflake.com/en/user-guide/cortex-code/code-mode.md) | Code mode; Enable code mode; What changes in code mode | OK |
| [Configure default model settings](https://docs.snowflake.com/en/user-guide/cortex-code/configure-model-settings.md) | Configure default model settings; Prerequisites; Create the database and schema | OK |
| [Context management](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/context-management.md) | Context management; See the token breakdown; Compact a conversation | OK |
| [Cortex Code changelog](https://docs.snowflake.com/en/user-guide/cortex-code/changelog.md) | Cortex Code changelog; 1.1.87 (Sep 14, 2026); 1.1.78 (Sep 7, 2026) | OK |
| [Cortex Code Desktop release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/index.md) | Cortex Code Desktop release notes; Version history | OK |
| [Cortex Code Desktop v1.14.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-14-0.md) | Cortex Code Desktop v1.14.0 release notes; Headlining: Plugins; Highlights | OK |
| [Cortex Code Desktop v1.15.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-15-0.md) | Cortex Code Desktop v1.15.0 release notes; The Glow-Up: UI/UX overhaul; Highlights | OK |
| [Cortex Code Desktop v1.15.1 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-15-1.md) | Cortex Code Desktop v1.15.1 release notes; Highlights; Notable fixes | OK |
| [Cortex Code Desktop v1.16.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-16-0.md) | Cortex Code Desktop v1.16.0 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.17.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-17-0.md) | Cortex Code Desktop v1.17.0 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.18.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-18-0.md) | Cortex Code Desktop v1.18.0 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.19.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-19-0.md) | Cortex Code Desktop v1.19.0 release notes; What's new; Security fixes | OK |
| [Cortex Code Desktop v1.19.1 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-19-1.md) | Cortex Code Desktop v1.19.1 release notes; What's new; Security and trust | OK |
| [Cortex Code Desktop v1.20.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-20-0.md) | Cortex Code Desktop v1.20.0 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.20.2 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-20-2.md) | Cortex Code Desktop v1.20.2 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.21.0 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-21-0.md) | Cortex Code Desktop v1.21.0 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.21.1 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-21-1.md) | Cortex Code Desktop v1.21.1 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.21.2 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-21-2.md) | Cortex Code Desktop v1.21.2 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.21.3 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-21-3.md) | Cortex Code Desktop v1.21.3 release notes; What's new; Security and trust | OK |
| [Cortex Code Desktop v1.21.4 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-21-4.md) | Cortex Code Desktop v1.21.4 release notes; What's new; Reliability and fixes | OK |
| [Cortex Code Desktop v1.21.5 release notes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/release-notes/v1-21-5.md) | Cortex Code Desktop v1.21.5 release notes; What's new | OK |
| [Cortex Code in Claude Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-claude-code.md) | Cortex Code in Claude Code; How it works; Prerequisites | OK |
| [Cortex Code in Snowsight changelog](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-snowsight/changelog.md) | Cortex Code in Snowsight changelog; September 2026; August 2026 | OK |
| [Cortex Code in your code editor](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-in-your-editor.md) | Cortex Code in your code editor; Ways to use Cortex Code in your editor; Monitor usage | OK |
| [Cost controls for CoCo](https://docs.snowflake.com/en/user-guide/cortex-code/cost-controls.md) | Cost controls for CoCo; Cost control options; Budgets | OK |
| [Daily credit usage limits for CoCo](https://docs.snowflake.com/en/user-guide/cortex-code/credit-usage-limit.md) | Daily credit usage limits for CoCo; How credit limits work; CoCo CLI limits | OK |
| [Data visualization](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/data-visualization.md) | Data visualization in CoCo Desktop; How you get visualizations; Supported visualizations | OK |
| [dbt integration](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/dbt-integration.md) | dbt integration in CoCo Desktop; Getting started; Project Action Bar | OK |
| [FAQ](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/faq.md) | FAQ; Does CoCo Desktop require WSL on Windows?; Why do I get "Not a valid Python interpreter"? | OK |
| [Hooks](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/hooks.md) | Hooks; Hook events; Managing hooks | OK |
| [Installation, onboarding, and authentication](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/onboarding-and-authentication.md) | Installation, onboarding, and authentication; Onboarding and sign in; Default warehouse | OK |
| [Instruction files](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/instruction-files.md) | Instruction files; Supported file names; File locations | OK |
| [Managed settings](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/managed-settings.md) | Managed settings; Permission patterns; Examples | OK |
| [Managed settings (organization policy)](https://docs.snowflake.com/en/user-guide/cortex-code/managed-settings.md) | Managed settings (organization policy); How managed settings work; File locations | OK |
| [MCP Connectors](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-snowsight/mcp-connectors.md) | MCP Connectors; How it works; Connecting to MCP Connectors | OK |
| [MCP support in CoCo Desktop](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/mcp-support.md) | CoCo Desktop Model Context Protocol (MCP) support; Transport types; Managing MCP servers | OK |
| [Memory](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/memory.md) | Memory; How memory works; Manage memory | OK |
| [Navigation](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/navigation.md) | Navigation; Switching between Agent and Editor views; Agent view | OK |
| [Observability](https://docs.snowflake.com/en/user-guide/cortex-code/observability.md) | Observability; What's tracked; Product feedback | OK |
| [Overview of Snowflake CoCo](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code.md) | Overview of Snowflake CoCo; Core experiences; More information | OK |
| [Permission modes](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/permission-modes.md) | Permission modes; Approval modes at a glance; Default Approvals | OK |
| [Personalization](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/personalization.md) | Personalization; Open the Personalization page; Custom instructions | OK |
| [Plugins in CoCo Desktop](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/plugins.md) | Plugins in CoCo Desktop; What plugins contain; Open the Agent Settings panel | OK |
| [Security](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/security.md) | Security; The trust model; Recommended security baseline | OK |
| [Security best practices for CoCo CLI](https://docs.snowflake.com/en/user-guide/cortex-code/security.md) | Security best practices for CoCo CLI; Credentials; Roles & access | OK |
| [Semantic code search](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/semantic-code-search.md) | Semantic code search; How it works; Consent | OK |
| [Share skills and plugins](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-skill-plugin-sharing.md) | Share skills and plugins; Overview; How it works | OK |
| [Skills](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/skills.md) | Skills in CoCo Desktop; Prerequisites; Open the Agent Settings panel | OK |
| [Skills and Plugins](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-snowsight/skills-and-plugins.md) | Skills and Plugins; Requirements; Built-in skills | OK |
| [SQL Playground](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/sql-playground.md) | SQL Playground in CoCo Desktop; Prerequisites; Open the SQL Playground | OK |
| [Using Apache Airflow™ with CoCo CLI](https://docs.snowflake.com/en/user-guide/cortex-code/airflow.md) | Using Apache Airflow™ with CoCo CLI; Capabilities; Prerequisites | OK |
| [Using CoCo CLI with other data platforms](https://docs.snowflake.com/en/user-guide/cortex-code/data-platforms.md) | Using CoCo CLI with other data platforms; Prerequisites; AWS Glue | OK |

## Snowflake ML

[Official section index](https://docs.snowflake.com/en/developer-guide/snowflake-ml/llms.txt)

| Page | First section headings | Fetch |
| --- | --- | --- |
| [Access control requirements for ML Jobs](https://docs.snowflake.com/en/developer-guide/snowflake-ml/ml-jobs/access-control-requirements.md) | Access control requirements for ML Jobs; Setting Up a New Environment; Using an Existing Environment | OK |
| [Advanced feature engineering](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering.md) | Advanced feature engineering; Overview of feature patterns; Online features | OK |
| [Agentic ML with Snowflake CoCo](https://docs.snowflake.com/en/developer-guide/snowflake-ml/agentic-ml.md) | Agentic ML with Snowflake CoCo; Using the machine-learning skill; Subskills | OK |
| [Autocapture inference logs for realtime inference](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/auto-capture-inference-logs.md) | Autocapture inference logs for realtime inference; Prerequisites and model version compatibility; Activate Auto Capture | OK |
| [Batch inference jobs](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/batch-inference-jobs.md) | Batch inference jobs; When to use batch inference; Limitations | OK |
| [Bring your own model types via serialized files](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/bring-your-own-model-types.md) | Bring your own model types via serialized files; Defining model context by keyword arguments; Initialize ModelContext with an in-memory model object | OK |
| [CatBoost](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/catboost.md) | CatBoost; Examples; Load dataset | OK |
| [Container Runtime on multi-node clusters](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime-multi-node.md) | Container Runtime on multi-node clusters; Prerequisites; Running a workload on a multi-node cluster | OK |
| [Create pipelines and deploy them](https://docs.snowflake.com/en/developer-guide/snowflake-ml/create-pipelines-deploy.md) | Create pipelines and deploy them; Overview; Develop | OK |
| [Creating or connecting to a feature store](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/create.md) | Creating or connecting to a feature store | OK |
| [CUDA-X Libraries in Snowflake ML](https://docs.snowflake.com/en/developer-guide/snowflake-ml/nvidia-cuda-x-libraries.md) | CUDA-X Libraries in Snowflake ML; NVIDIA CUDA-X Libraries for Data Science; Use Cases | OK |
| [Custom Runtime Images](https://docs.snowflake.com/en/developer-guide/snowflake-ml/custom-runtime-images.md) | Custom Runtime Images; Overview; Workflow: Create and use a custom runtime image | OK |
| [Deploy models for real-time inference (REST API)](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/real-time-inference-rest-api.md) | Deploy models for real-time inference (REST API); How it works; reg is a snowflake.ml.registry.Registry object | OK |
| [Distributed training](https://docs.snowflake.com/en/developer-guide/snowflake-ml/distributed-training.md) | Distributed training; Snowflake ML distributed training; Load data | OK |
| [Engineer features](https://docs.snowflake.com/en/developer-guide/snowflake-ml/transform-data.md) | Engineer features; Load your data locally into a Pandas DataFrame; Define preprocessing steps | OK |
| [Example feature patterns](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/examples.md) | Example feature patterns; Per-row features; Per-group features | OK |
| [Example workflows](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/real-time-inference-examples.md) | Example workflows; Deploy an XGBoost model for CPU-powered inference; your model training code here output of which is a trained xgb_model | OK |
| [Examples and Quickstarts](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/examples-and-quickstarts.md) | Examples and Quickstarts; Beginner Quickstart; xgboost model, CPU inference in Snowpark Container Services | OK |
| [Feature Development Lifecycle](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/feature-development-lifecycle.md) | Feature Development Lifecycle; Prerequisites; 1. Initialize a project | OK |
| [Feature groups](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/feature-groups.md) | Feature groups; Primary keys and join behavior; Define and register a feature group | OK |
| [Find Feature Store objects](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/feature-store-ui.md) | Find Feature Store objects | OK |
| [Force plots](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-explainability-visualization/force-plots.md) | Force plots; Required arguments; Optional arguments | OK |
| [Gateway monitoring & A/B testing](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing.md) | Gateway monitoring & A/B testing; A/B testing workflow; Gateway configuration for A/B tests | OK |
| [Getting Started: Quickstarts](https://docs.snowflake.com/en/developer-guide/snowflake-ml/quickstart.md) | Getting Started: Quickstarts | OK |
| [Hugging Face pipeline](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/hugging-face.md) | Hugging Face pipeline; Model Registry API; model: snowflake.ml.model.ModelVersion | OK |
| [Influence sensitivity plots](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-explainability-visualization/influence-sensitivity-plots.md) | Influence sensitivity plots; Required arguments; Optional arguments | OK |
| [Ingest API reference](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/online-feature-store-ingest-api-reference.md) | Ingest API reference; Endpoint; Request headers | OK |
| [Keras](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/keras.md) | Keras; Examples; Load dataset | OK |
| [LightGBM](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/lightgbm.md) | LightGBM; Examples; Load dataset | OK |
| [Load and write data](https://docs.snowflake.com/en/developer-guide/snowflake-ml/load-data.md) | Load and write data; Load structured data from Snowflake tables; Create DataConnector from a Snowflake table | OK |
| [Manage packages in notebooks on Container Runtime](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime-package-management.md) | Manage packages in notebooks on Container Runtime; Prerequisite; View all packages installed in a notebook environment | OK |
| [Managing models with the Snowflake Model Registry](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-management.md) | Managing models with the Snowflake Model Registry; Governance; Model lifecycle management | OK |
| [ML Lineage: Trace ML data flow](https://docs.snowflake.com/en/developer-guide/snowflake-ml/ml-lineage.md) | ML Lineage: Trace ML data flow; Limitations; Required privileges | OK |
| [ML Observability: Monitoring model behavior over time](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-observability.md) | ML Observability: Monitoring model behavior over time; ML Observability workflow; Prerequisites | OK |
| [MLFlow](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/mlflow.md) | MLFlow; Example | OK |
| [Model Explainability](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-explainability.md) | Model Explainability; Supported model types; Logging models with background data | OK |
| [Model explainability visualizations](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-explainability-visualization.md) | Model explainability visualizations | OK |
| [Model Inference in Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/inference-overview.md) | Model Inference in Snowflake; When to choose | OK |
| [Model Training and Inference](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/modeling.md) | Model Training and Inference; Generating tables for training; Generating Snowflake Datasets for training | OK |
| [Monitoring and Observability](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/monitoring.md) | Monitoring and Observability; Prerequisites; Offline Refresh | OK |
| [Notebooks on Container Runtime](https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs.md) | Notebooks on Container Runtime; Overview; Prerequisites | OK |
| [Parallel Hyperparameter Optimization (HPO) on Container Runtime](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-hpo.md) | Parallel Hyperparameter Optimization (HPO) on Container Runtime; Optimize a model's hyperparameters; API reference | OK |
| [Pre-processing and post-processing with models](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/custom-processing-with-models.md) | Pre-processing and post-processing with models; In-memory scikit-learn models and pipelines; Step 1: Import the Iris dataset | OK |
| [Process data with custom logic across partitions](https://docs.snowflake.com/en/developer-guide/snowflake-ml/process-data-across-partitions.md) | Process data with custom logic across partitions; DataFrame mode: Process data by column partitions; Check overall status | OK |
| [Prophet](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/prophet.md) | Prophet; Data Format Requirements; Example | OK |
| [Python APIs for Snowflake ML](https://docs.snowflake.com/en/developer-guide/snowflake-ml/snowpark-ml.md) | Python APIs for Snowflake ML; Using Snowflake ML in Snowflake Notebooks; Using Snowflake ML in Snowsight Worksheets | OK |
| [PyTorch](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/pytorch.md) | PyTorch; Example; Define a simple neural network for classification | OK |
| [Query API reference](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/online-feature-store-query-api-reference.md) | Query API reference; Endpoint; Request headers | OK |
| [Replicating and sharing features](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/replication-sharing.md) | Replicating and sharing features; Replicating a feature store; Sharing a feature store | OK |
| [Run an experiment to compare and select models](https://docs.snowflake.com/en/developer-guide/snowflake-ml/experiments.md) | Run an experiment to compare and select models; Access control requirements; Create an experiment | OK |
| [Scale an application using Ray](https://docs.snowflake.com/en/developer-guide/snowflake-ml/scale-application-ray.md) | Scale an application using Ray; Connect to the pre-existing Ray cluster within the Snowflake environment; Scaling your Ray cluster | OK |
| [scikit-learn](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/scikit-learn.md) | scikit-learn; Example; create a session and set DATABASE and SCHEMA | OK |
| [Sentence Transformer](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/sentence-transformer.md) | Sentence Transformer; 1. Initialize the model; This example uses the 'all-MiniLM-L6-v2' model, which is a popular | OK |
| [Service Management & Scaling](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/service-management.md) | Service Management & Scaling; Managing services; Scaling services | OK |
| [Serving online features](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/online-feature-store.md) | Serving online features; How the Online Feature Store works; Enabling online serving for feature views | OK |
| [Snowflake Container Runtime](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime-ml.md) | Snowflake Container Runtime; Overview; Execution environment | OK |
| [Snowflake Container Runtime CPU Version 2.3](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/cpu/2_3.md) | Snowflake Container Runtime CPU Version 2.3 | OK |
| [Snowflake Container Runtime CPU Version 2.4](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/cpu/2_4.md) | Snowflake Container Runtime CPU Version 2.4 | OK |
| [Snowflake Container Runtime CPU Version 2.5](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/cpu/2_5.md) | Snowflake Container Runtime CPU Version 2.5 | OK |
| [Snowflake Container Runtime CPU Version 2.6](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/cpu/2_6.md) | Snowflake Container Runtime CPU Version 2.6; Added; Changed | OK |
| [Snowflake Container Runtime CPU Version 2.7](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/cpu/2_7.md) | Snowflake Container Runtime CPU Version 2.7; Added; Changed | OK |
| [Snowflake Container Runtime CPU Version 2.8](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/cpu/2_8.md) | Snowflake Container Runtime CPU Version 2.8; Added; Changed | OK |
| [Snowflake Container Runtime CPU Version 2.9 (Latest)](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/cpu/2_9.md) | Snowflake Container Runtime CPU Version 2.9 (Latest); Added | OK |
| [Snowflake Container Runtime GPU Version 2.3](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/gpu/2_3.md) | Snowflake Container Runtime GPU Version 2.3 | OK |
| [Snowflake Container Runtime GPU Version 2.4](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/gpu/2_4.md) | Snowflake Container Runtime GPU Version 2.4 | OK |
| [Snowflake Container Runtime GPU Version 2.5](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/gpu/2_5.md) | Snowflake Container Runtime GPU Version 2.5 | OK |
| [Snowflake Container Runtime GPU Version 2.6](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/gpu/2_6.md) | Snowflake Container Runtime GPU Version 2.6; Added; Changed | OK |
| [Snowflake Container Runtime GPU Version 2.7](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/gpu/2_7.md) | Snowflake Container Runtime GPU Version 2.7; Added; Changed | OK |
| [Snowflake Container Runtime GPU Version 2.8](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/gpu/2_8.md) | Snowflake Container Runtime GPU Version 2.8; Added; Changed | OK |
| [Snowflake Container Runtime GPU Version 2.9 (Latest)](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases/gpu/2_9.md) | Snowflake Container Runtime GPU Version 2.9 (Latest); Added | OK |
| [Snowflake Container Runtime release notes](https://docs.snowflake.com/en/developer-guide/snowflake-ml/container-runtime/releases.md) | Snowflake Container Runtime release notes; Snowflake Container Runtime on CPU compute; Snowflake Container Runtime on GPU compute | OK |
| [Snowflake Datasets](https://docs.snowflake.com/en/developer-guide/snowflake-ml/dataset.md) | Snowflake Datasets; Installation; Required privileges | OK |
| [Snowflake Feature Store](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/overview.md) | Snowflake Feature Store; How does it work?; Getting started | OK |
| [Snowflake Feature Store access control model](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/rbac.md) | Snowflake Feature Store access control model; Access control setup in Python; Access control setup in SQL | OK |
| [Snowflake ML Jobs](https://docs.snowflake.com/en/developer-guide/snowflake-ml/ml-jobs/overview.md) | Snowflake ML Jobs; Prerequisites; Run a Snowflake ML job | OK |
| [Snowflake ML Model Development](https://docs.snowflake.com/en/developer-guide/snowflake-ml/modeling.md) | Snowflake ML Model Development; Train and tune your models; Develop your code | OK |
| [Snowflake ML: End-to-End Agentic Machine Learning](https://docs.snowflake.com/en/developer-guide/snowflake-ml/overview.md) | Snowflake ML: End-to-End Agentic ML; Agentic ML; Model Training | OK |
| [Snowflake Model Registry](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview.md) | Snowflake Model Registry; Required privileges; Current limitations | OK |
| [Snowflake Model Registry user interface](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/snowsight-ui.md) | Snowflake Model Registry user interface; Model details; Deploy user models | OK |
| [Snowflake Multi-Node ML Jobs](https://docs.snowflake.com/en/developer-guide/snowflake-ml/ml-jobs/distributed-ml-jobs.md) | Snowflake Multi-Node ML Jobs; Prerequisites; Writing code for multi-node jobs | OK |
| [Snowflake Native Batch Inference (SQL)](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/native-batch-inference-sql.md) | Snowflake Native Batch Inference (SQL); Where to run a model?; Inference from Python | OK |
| [Snowpark ML](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/snowpark-ml.md) | Snowpark ML; Example | OK |
| [Specifying model signatures](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-signature.md) | Specifying model signatures; Inferring a signature; Supply a signature for every function the model exposes, in this case only predict. | OK |
| [Stable Endpoints & API Reference](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference.md) | Stable Endpoints & API Reference; Stable Endpoints with Snowflake Gateway; Managing Model Upgrades | OK |
| [TensorFlow](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/tensorflow.md) | TensorFlow; Examples; Define a simple TensorFlow module | OK |
| [Train models](https://docs.snowflake.com/en/developer-guide/snowflake-ml/train-models.md) | Train models; Train with open source; Get the active Snowpark session | OK |
| [Train models across data partitions](https://docs.snowflake.com/en/developer-guide/snowflake-ml/train-models-across-partitions.md) | Train models across data partitions; Training a model with MMT; Example: sales_data with columns: region, feature1, feature2, feature3, target | OK |
| [Troubleshooting](https://docs.snowflake.com/en/developer-guide/snowflake-ml/inference/real-time-inference-troubleshooting.md) | Troubleshooting; Monitor SPCS deployments; Package conflicts | OK |
| [Using built-in model types](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/overview.md) | Using built-in model types | OK |
| [Using partitioned models](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/partitioned-models.md) | Using partitioned models; Defining and logging the model; Partitioned model inference | OK |
| [Violin Plots](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-explainability-visualization/violin-plots.md) | Violin Plots; Required arguments; Optional arguments | OK |
| [Working with entities](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/entities.md) | Working with entities; Creating an entity; Listing entities | OK |
| [Working with feature views](https://docs.snowflake.com/en/developer-guide/snowflake-ml/feature-store/feature-views.md) | Working with feature views; Creating a Snowflake-managed feature view; Creating an external feature view | OK |
| [XGBoost](https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/built-in-models/xgboost.md) | XGBoost; Example | OK |

## AI/ML overview and ML Functions

[Official section index](https://docs.snowflake.com/en/guides-overview-ai-features.md)

| Page | First section headings | Fetch |
| --- | --- | --- |
| [Snowflake AI and ML](https://docs.snowflake.com/en/guides-overview-ai-features.md) | Snowflake AI and ML; Use of Snowflake AI features; AI/ML model update process | OK |
| [ML Functions](https://docs.snowflake.com/en/guides-overview-ml-functions.md) | ML Functions; Time-Series Functions; Other Analysis Functions | OK |
| [Anomaly Detection](https://docs.snowflake.com/en/user-guide/ml-functions/anomaly-detection.md) | Anomaly Detection (Snowflake ML Functions); Overview; About the Algorithm for Anomaly Detection | OK |
| [Classification](https://docs.snowflake.com/en/user-guide/ml-functions/classification.md) | Classification (Snowflake ML Functions); About the Classification Model; Preparing for Classification | OK |
| [Forecasting](https://docs.snowflake.com/en/user-guide/ml-functions/forecasting.md) | Time-Series Forecasting (Snowflake ML Functions); Quickstart to forecasting; Dive deeper into forecasting | OK |
| [Top Insights](https://docs.snowflake.com/en/user-guide/ml-functions/top-insights.md) | Top Insights (Snowflake ML Functions); About Top Insights; Required privileges | OK |
| [Time-series preprocessing](https://docs.snowflake.com/en/user-guide/ml-functions/preprocessing.md) | Dealing with real-world data in Time-Series Forecasting; Specifying event frequency; Filling in values for missing time steps | OK |

## SQL AI Function references

[Official section index](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql.md)

| Page | First section headings | Fetch |
| --- | --- | --- |
| [AI_COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/ai_complete.md) | AI_COMPLETE; Syntax; Error behavior | OK |
| [AI_COMPLETE-SINGLE-STRING](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-string.md) | AI_COMPLETE (Single string); Syntax; Arguments | OK |
| [AI_COMPLETE-SINGLE-FILE](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-single-file.md) | AI_COMPLETE (Single image); Syntax; Arguments | OK |
| [AI_COMPLETE-PROMPT-OBJECT](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-prompt-object.md) | AI_COMPLETE (Prompt object); Syntax; Arguments | OK |
| [AI_COMPLETE-STRUCTURED-OUTPUTS](https://docs.snowflake.com/en/sql-reference/functions/ai_complete-structured-outputs.md) | AI_COMPLETE (Structured outputs); Using AI_COMPLETE with type literals; Using AI_COMPLETE with JSON schemas | OK |
| [AI_CLASSIFY](https://docs.snowflake.com/en/sql-reference/functions/ai_classify.md) | AI_CLASSIFY; Region availability; Syntax | OK |
| [AI_FILTER](https://docs.snowflake.com/en/sql-reference/functions/ai_filter.md) | AI_FILTER; Region availability; Syntax | OK |
| [AI_AGG](https://docs.snowflake.com/en/sql-reference/functions/ai_agg.md) | AI_AGG; Syntax; Arguments | OK |
| [AI_EMBED](https://docs.snowflake.com/en/sql-reference/functions/ai_embed.md) | AI_EMBED; Syntax; Arguments | OK |
| [AI_MULTI_EMBED](https://docs.snowflake.com/en/sql-reference/functions/ai_multi_embed.md) | AI_MULTI_EMBED; Syntax; Arguments | OK |
| [AI_EXTRACT](https://docs.snowflake.com/en/sql-reference/functions/ai_extract.md) | AI_EXTRACT; Syntax; Arguments | OK |
| [AI_SENTIMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_sentiment.md) | AI_SENTIMENT; Syntax; Arguments | OK |
| [AI_SUMMARIZE](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize.md) | AI_SUMMARIZE; Syntax; Arguments | OK |
| [AI_SUMMARIZE_AGG](https://docs.snowflake.com/en/sql-reference/functions/ai_summarize_agg.md) | AI_SUMMARIZE_AGG; Syntax; Arguments | OK |
| [AI_SIMILARITY](https://docs.snowflake.com/en/sql-reference/functions/ai_similarity.md) | AI_SIMILARITY; Syntax; Arguments | OK |
| [AI_TRANSCRIBE](https://docs.snowflake.com/en/sql-reference/functions/ai_transcribe.md) | AI_TRANSCRIBE; Syntax; Arguments | OK |
| [AI_PARSE_DOCUMENT](https://docs.snowflake.com/en/sql-reference/functions/ai_parse_document.md) | AI_PARSE_DOCUMENT; Syntax; Arguments | OK |
| [AI_REDACT](https://docs.snowflake.com/en/sql-reference/functions/ai_redact.md) | AI_REDACT; Syntax; Arguments | OK |
| [AI_TRANSLATE](https://docs.snowflake.com/en/sql-reference/functions/ai_translate.md) | AI_TRANSLATE; Syntax; Arguments | OK |
| [AI_COUNT_TOKENS](https://docs.snowflake.com/en/sql-reference/functions/ai_count_tokens.md) | AI_COUNT_TOKENS; Syntax; Arguments | OK |
| [PROMPT](https://docs.snowflake.com/en/sql-reference/functions/prompt.md) | PROMPT; Syntax; Arguments | OK |
| [TO_FILE](https://docs.snowflake.com/en/sql-reference/functions/to_file.md) | TO_FILE; Syntax; Arguments | OK |
