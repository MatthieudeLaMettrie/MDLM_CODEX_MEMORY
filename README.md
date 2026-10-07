# MDLM_CODEX_MEMORY

Project memory and session records for continuing work across Codex tasks.

## Visual guide

**[Open the visual guide: from GitHub setup to session continuity](guides/continuity/VISUAL_GUIDE.md)**

The guide contains three diagrams, step-by-step setup instructions, and a glossary:

- Creating the repository, installing GitHub Desktop, cloning, and opening the project in Codex.
- How GitHub, your local folder, GitHub Desktop, and Codex fit together.
- How session notes and memory carry context into the next task.

## Study guides

- [Agents over Power BI semantic models: Desktop and Fabric setup](guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md) — both authoring paths, architecture diagrams, Prep for AI, Fabric IQ, instruction templates, permissions, Copilot Studio/Foundry connections, production deployment, and GCP/Snowflake/Databricks equivalents.

- [Databricks data engineering: 00–13 numbered course](databricks/README.md) — 16 lessons, executable development lab, ETL and medallion architecture, Delta/PySpark troubleshooting, Azure Synapse integration, bundles/orchestration, Unity Catalog volumes and managed/external storage, Lakeflow/DLT pipelines, fake-table CDF/CDC/Auto Loader examples, 28 incident exercises and capstone.

- [02 — dbt semantic models and metrics: practical course](dbt/dbt-study-guide/02_SEMANTIC_MODELS_AND_METRICS_COURSE.md) — FEI RSS examples, 16 lessons, both YAML specifications, reproducible BigQuery lab, queries, debugging and capstone. Follow the [00 → 06 numbered learning path](dbt/dbt-study-guide/README.md) for the full dbt sequence.

- [Data and dbt concepts: indexing, joins, React/Next.js, incremental strategies and freshness](guides/data-engineering/DATA_AND_DBT_CONCEPTS_GUIDE.md) — use cases, SQL/YAML examples, diagrams and platform distinctions.

- [Personal Access Tokens (PATs): what, how and why](guides/api/PERSONAL_ACCESS_TOKENS_GUIDE.md) — credential/transport distinctions, GitHub setup, Azure DevOps/GitLab examples, Databricks considerations, alternatives, rotation and practice questions.

- [Azure and GCP identity setup: Key Vault, service principals, service accounts and OAuth](guides/api/AZURE_GCP_IDENTITY_SETUP_GUIDE.md) — step-by-step console setup, permissions, local and hosted authentication, Google Sheets OAuth, connection checks and troubleshooting.

- [API authentication: passwords, keys, Bearer tokens, OAuth, cookies and Key Vault](guides/api/API_AUTHENTICATION_STUDY_GUIDE.md) — comparisons, sanitized MyTurn/Supabase and Fabric/Azure examples, diagrams, troubleshooting and practice questions.

- [Google Sheets to Snowflake using Fivetran](guides/data-engineering/google-sheets-snowflake-fivetran/README.md) — complete connection guide, public/private key generation, Snowflake scripts, validation, troubleshooting, and FEI RSS session evidence.

- [dbt Cloud with BigQuery: setup and deployment](dbt/DBT_BIGQUERY_CLOUD_GUIDE.md) — living field guide for connections, datasets, Git project paths, production jobs, and troubleshooting.

- [SnowPro Specialty: Gen AI (GES-C02) study guide and practice set](snowpro-genai/README.md) — official-blueprint coverage, syntax and billing sheets, a lab, 28 original questions, and Snowflake documentation links.

- [Azure Foundry SDK, Azure AI Search, and RAG study course](learning/rag/AZURE_FOUNDRY_RAG_STUDY_COURSE.md) — architecture, current Python agent calls, labs, and evaluation exercises.

- [GCP Agent Search, Gemini, ADK, and RAG study course](learning/rag/GCP_AGENT_SEARCH_RAG_STUDY_COURSE.md) — current naming, grounded Gemini and agent calls, labs, and evaluation.

- [AWS Bedrock Knowledge Bases, AgentCore, and RAG study course](learning/rag/AWS_BEDROCK_RAG_STUDY_COURSE.md) — managed and customer-managed paths, current agent integration, labs, and evaluation.

- [Gmail/Google Workspace: receive information@frenchexpatsinvestment.com in the existing inbox](guides/email/EMAIL_ALIAS_GUIDE.md) — step-by-step alias setup and delivery test.

- [dbt learning guide, debugging workbook and Python workflow](dbt/README.md) — source-linked reference, twenty exercises with answers withheld, and an adaptable readiness plan.

- [JavaScript and Python runtimes: Node.js, npm and npx](guides/programming/RUNTIME_STUDY_GUIDE.html) — download/open the HTML file in a browser for diagrams, examples, runtime comparisons and an interactive quiz. Works offline and includes print styling.

## Project records

- [Working instructions](AGENTS.md)
- [Current memory](MEMORY.md)
- [Certification roadmap and research findings](learning/certifications/CERTIFICATION_ROADMAP.md)
- [Locked continuous AI curriculum and resources](learning/certifications/AI_STUDY_CURRICULUM.md)
- [French Expats Investment ETF data project](projects/fei/ETF_DATA_FEI_PROJECT.md)
- [Session notes](sessions/)

## Folder map

- `learning/rag/` — Azure, GCP, and AWS RAG courses.
- `learning/certifications/` — AI curriculum and certification roadmap.
- `guides/` — continuity, email, programming, and data engineering guides.
- `projects/` — project-specific records.
- `dbt/`, `snowpro-genai/` and `databricks/` — numbered subject study collections.
- `sessions/` — dated session records.
