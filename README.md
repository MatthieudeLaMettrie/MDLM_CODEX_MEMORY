# MDLM_CODEX_MEMORY

Project memory and session records for continuing work across Codex tasks.

## Visual guide

**[Open the visual guide: from GitHub setup to session continuity](guides/continuity/VISUAL_GUIDE.md)**

The guide contains three diagrams, step-by-step setup instructions, and a glossary:

- Creating the repository, installing GitHub Desktop, cloning, and opening the project in Codex.
- How GitHub, your local folder, GitHub Desktop, and Codex fit together.
- How session notes and memory carry context into the next task.

## Study guides

- [Semantic layer vs semantic model: real-life scenarios](guides/data-engineering/SEMANTIC_LAYER_VS_SEMANTIC_MODEL_SCENARIOS.md) — nine scenarios (retail, bank, SaaS/dbt, hospital, multi-platform acquisition, airline, AI agent agency, small business, FEI RSS), layer-or-model quiz and ownership cheat sheet.

- [Semantic layer → AI agent → publishing: Databricks and Snowflake](guides/data-engineering/SEMANTIC_LAYER_AI_AGENTS_AND_PUBLISHING_GUIDE.md) — Genie Agent over a metric view and Cortex Agent over a semantic view, step by step; prerequisites and per-user permissions; publishing in-platform (Genie One/CoWork), Teams/M365 Copilot/Copilot Studio, SharePoint/website (iframe or API), Power BI/Tableau and cross-org sharing; rollout order and troubleshooting.

- [Semantic layers in Databricks and Snowflake: metric views vs semantic views](guides/data-engineering/SEMANTIC_LAYERS_DATABRICKS_SNOWFLAKE_GUIDE.md) — semantic layer vs semantic model, dim/fact relationships compared with Power BI and Tableau, one synthetic star schema built twice with known answers, vocabulary map (incl. dbt), grain-behaviour difference, Genie/Cortex Agent benchmark, deployment, tests, mistakes and exercises.

- [Agents over Power BI semantic models: Desktop and Fabric setup](guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md) — both authoring paths, architecture diagrams, Prep for AI, Fabric IQ, instruction templates, permissions, Copilot Studio/Foundry connections, production deployment, and GCP/Snowflake/Databricks equivalents.

- [Databricks data engineering: 00–16 numbered course](databricks/README.md) — 16 lessons, executable development lab, ETL and medallion architecture, Delta/PySpark troubleshooting, Azure Synapse integration, bundles/orchestration, Unity Catalog volumes and managed/external storage, Lakeflow/DLT pipelines, fake-table CDF/CDC/Auto Loader examples, screenshot-based retail CDC/CDF setup, operations/monitoring/optimisation with 15 worked incidents, 28 incident exercises and capstone.

- [02 — dbt semantic models and metrics: practical course](dbt/dbt-study-guide/02_SEMANTIC_MODELS_AND_METRICS_COURSE.md) — FEI RSS examples, 16 lessons, both YAML specifications, reproducible BigQuery lab, queries, debugging and capstone. Follow the [00 → 06 numbered learning path](dbt/dbt-study-guide/README.md) for the full dbt sequence.

- [Data and dbt concepts: indexing, joins, React/Next.js, incremental strategies and freshness](guides/data-engineering/DATA_AND_DBT_CONCEPTS_GUIDE.md) — use cases, SQL/YAML examples, diagrams and platform distinctions.

- [Python `os` and `sys`: what they are, why they matter, what to master](guides/api/PYTHON_OS_SYS_GUIDE.md) — environment variables, paths, files, interpreter diagnostics, argv/exit codes, streams, modern companions, seven tested examples, pitfalls and practice questions.

- [Personal Access Tokens (PATs): what, how and why](guides/api/PERSONAL_ACCESS_TOKENS_GUIDE.md) — credential/transport distinctions, GitHub setup, Azure DevOps/GitLab examples, Databricks considerations, alternatives, rotation and practice questions.

- [Azure and GCP identity setup: Key Vault, service principals, service accounts and OAuth](guides/api/AZURE_GCP_IDENTITY_SETUP_GUIDE.md) — step-by-step console setup, permissions, local and hosted authentication, Google Sheets OAuth, connection checks and troubleshooting.

- [API authentication: passwords, keys, Bearer tokens, OAuth, cookies and Key Vault](guides/api/API_AUTHENTICATION_STUDY_GUIDE.md) — comparisons, sanitized MyTurn/Supabase and Fabric/Azure examples, diagrams, troubleshooting and practice questions.

- [Google Sheets to Snowflake using Fivetran](guides/data-engineering/google-sheets-snowflake-fivetran/README.md) — complete connection guide, public/private key generation, Snowflake scripts, validation, troubleshooting, and FEI RSS session evidence.

- [dbt Cloud with BigQuery: setup and deployment](dbt/DBT_BIGQUERY_CLOUD_GUIDE.md) — living field guide for connections, datasets, Git project paths, production jobs, and troubleshooting.

- [SnowPro Specialty: Gen AI (GES-C02) study guide and practice set](snowpro-genai/README.md) — official-blueprint coverage, syntax and billing sheets, a lab, 28 original questions, and Snowflake documentation links.

- [Function reference: Fabric T-SQL, Databricks SQL and PySpark](functions-reference/README.md) — AI functions plus the functions worth knowing on each platform, with examples, traps, and a Snowflake/Fabric/Databricks/PySpark cross-walk; Snowflake's equivalents are in the SnowPro guide (files 09 and 10).

- [Power Platform and Copilot Studio: admin, agents on Fabric, MCP and flows](power-platform-copilot-studio/README.md) — 01–06 numbered path: environments and the inactivity cleanup (disabled developer environment worked example), licensing, DLP, external models, Fabric data agent via Copilot Studio and Foundry, Power BI semantic models, MCP authentication, flows, engineer playbook, JB checklist, 14 checks.

- [Azure Foundry SDK, Azure AI Search, and RAG study course](learning/rag/AZURE_FOUNDRY_RAG_STUDY_COURSE.md) — architecture, current Python agent calls, labs, and evaluation exercises.

- [GCP Agent Search, Gemini, ADK, and RAG study course](learning/rag/GCP_AGENT_SEARCH_RAG_STUDY_COURSE.md) — current naming, grounded Gemini and agent calls, labs, and evaluation.

- [AWS Bedrock Knowledge Bases, AgentCore, and RAG study course](learning/rag/AWS_BEDROCK_RAG_STUDY_COURSE.md) — managed and customer-managed paths, current agent integration, labs, and evaluation.

- [Gmail/Google Workspace: receive information@frenchexpatsinvestment.com in the existing inbox](guides/email/EMAIL_ALIAS_GUIDE.md) — step-by-step alias setup and delivery test.

- [dbt learning guide, debugging workbook and Python workflow](dbt/README.md) — source-linked reference, twenty exercises with answers withheld, and an adaptable readiness plan.

- [JavaScript and Python runtimes: Node.js, npm and npx](guides/programming/RUNTIME_STUDY_GUIDE.html) — download/open the HTML file in a browser for diagrams, examples, runtime comparisons and an interactive quiz. Works offline and includes print styling.

- [YouTube content planner: 50 short IT and AI video concepts](youtube-content/README.md) — Databricks, Snowflake, BigQuery, Fabric, dbt, Power BI, Claude, OpenAI, Gemini and cross-platform ideas, with priority, readiness, supporting guides, a sortable CSV and a production/safety checklist. Views are not guaranteed; demand was not checked.

## Project records

- [Working instructions](AGENTS.md)
- [Current memory](MEMORY.md)
- [Certification roadmap and research findings](learning/certifications/CERTIFICATION_ROADMAP.md)
- [Locked continuous AI curriculum and resources](learning/certifications/AI_STUDY_CURRICULUM.md)
- [French Expats Investment ETF data project](projects/fei/ETF_DATA_FEI_PROJECT.md)
- [Wonder Hollow website and YouTube](projects/wonder-hollow/README.md) — deployed SEO foundations, AI discovery decisions, YouTube priorities, access status and verified Firebase deployment runbook.
- [Session notes](sessions/)

## Folder map

- `learning/rag/` — Azure, GCP, and AWS RAG courses.
- `learning/certifications/` — AI curriculum and certification roadmap.
- `guides/` — continuity, email, programming, and data engineering guides.
- `projects/` — project-specific records.
- `dbt/`, `snowpro-genai/` and `databricks/` — numbered subject study collections.
- `youtube-content/` — YouTube video planner (50 concepts), production checklist and tracking CSV; separate from the study guides.
- `sessions/` — dated session records.
