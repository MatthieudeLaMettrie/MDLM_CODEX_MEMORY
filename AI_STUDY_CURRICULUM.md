# Continuous AI curriculum

Saved: 2026-09-23 (Australia/Sydney)
Authority: user-supplied plan explicitly requested for durable memory. This supersedes the earlier advice to defer AI-300 and proceed directly from AI-103 to AI-500.

## Locked sequence after dbt

**SnowPro GenAI -> AI-103 -> AI-300 -> AI-500 / Databricks GenAI**

The user's detailed learning sequence puts AI-500 before Databricks GenAI. Preserve the slash in the short form: exact scheduling or choice within the final pair is not separately confirmed. Both are covered by this curriculum; do not silently drop either or insert DE Professional.

Study as one continuous AI curriculum, reusing concepts and a cross-platform project rather than treating these as unrelated exams. New fixed dates were not supplied; earlier dates are provisional and must accommodate AI-300.

## Recommended timetable (2026-09-23)

Assistant recommendation requested by user; windows are provisional, not bookings. This implements the user's continuous curriculum with AI-500 before Databricks GenAI.

| Timeframe | Certification | Recommendation and usefulness | Practical checkpoint |
|---|---|---|---|
| Now-Oct 2026 | dbt Analytics Engineering | Finish current preparation if ready; do not let it jeopardize Snowflake renewal | Diagnose project failures independently |
| Oct-Nov 2026 | SnowPro Specialty: Gen AI | First AI stage; learn Cortex and renew active Core before Jan 2027 under current policy | Cortex retrieval/agent application with evaluation |
| Jan-Feb 2027 | AI-103 | Build on AI-102; develop Foundry applications and agents | Working Foundry app with tools and grounding |
| Mar-May 2027 | AI-300 | Keep in sequence for production ML/GenAI engineering | CI/CD, deployment, evaluation, monitoring and rollback |
| Jun-Sep 2027 | AI-500 | Main architecture milestone; extend operational foundations into multi-agent delivery | Justified orchestration, permissions, approvals and measured reliability |
| Oct 2027-Mar 2028 | Databricks GenAI Engineer Associate | Transfer the conceptual stack to a second AI delivery platform | Databricks RAG with lifecycle, serving and governance |
| Before actual Snowflake expiry in 2028 | SnowPro Advanced Architect or DE | Prefer Architect for architecture ownership; choose DE for pipeline-heavy work. Combine advancement and renewal | Experience and readiness aligned to chosen scope |

Keep GH-600, Databricks DE Professional/ML, AI security, AZ-104/AZ-305, AWS/GCP and AICD outside the scheduled core unless a concrete need changes priorities. Do not add exams between these stages. Dates can move with readiness; protect the actual Snowflake expiry and leave a retake buffer.

This sequence invests more study time than the earlier shortened plan. Its rationale is integrated capability: build -> operate -> architect -> implement on another platform. Reuse one project and one concept notebook to manage that opportunity cost. It does not imply guaranteed salary or job outcomes.


## Resource plan

| Certification | Primary resource | Hands-on resource | Approach |
|---|---|---|---|
| SnowPro Specialty: Gen AI | Official SnowPro GenAI certification page/guide | Snowflake Cortex AI docs, Cortex Search and Cortex Agents tutorials | Learn universal GenAI concepts through Cortex |
| AI-103 | Official Microsoft AI-103 study guide | AI-103T00: Develop AI apps and agents on Azure | Follow blueprint and build with Foundry |
| AI-300 | Official Microsoft AI-300 study guide | AI-300T00: Operationalize machine learning and generative AI solutions | Lab-heavy MLOps/GenAIOps with GitHub Actions, Azure ML, Azure CLI and Bicep |
| AI-500 | Official Microsoft AI-500 study guide | AI-500T00 and Microsoft multi-agent learning paths | Build a production-oriented multi-agent system |
| Databricks GenAI Engineer Associate | Official exam guide and AI Prep Guide | Databricks Academy, AI Search, Model Serving and MLflow labs | Build and deploy a substantial RAG application |

## SnowPro Specialty: Gen AI

- Start with the official certification guide and map the blueprint to implementation.
- Prefer Snowflake AI documentation and practical labs over generic exam videos.
- Cortex Search exercises: search application, chatbot and PDF-RAG application.
- Complete at least one Cortex Agents tutorial combining structured and unstructured data.
- Suggested study allocation: approximately 40% exam-specific preparation, 60% hands-on Cortex.
- Learn embeddings, retrieval, model selection, agents, evaluation and governance as reusable concepts.

## AI-103

- Use the official study guide as the blueprint.
- Complete AI-103T00.
- Prior AI-102 knowledge should help with familiar services; move faster only where mastery is demonstrated.
- Spend extra time on Foundry, agents, tools, knowledge/RAG, memory, model selection and Python SDKs.
- User-supplied snapshot describes GenAI/agentic section as 30-35% and the course as four-day-equivalent; verify current weighting and course details before study scheduling.
- Connect the Snowflake concepts to Azure implementations rather than restarting conceptual study.

## AI-300

- Mandatory stage in the newly saved plan; no longer a deferred option.
- Use the official guide and AI-300T00, not generic GenAI courses alone.
- Cover traditional ML lifecycle as well as GenAIOps.
- Practise Azure ML, Foundry, GitHub Actions, Azure CLI and Bicep.
- Build the full operational chain: GitHub -> CI/CD -> Azure ML/Foundry -> deployment -> evaluation -> monitoring -> rollback.
- Include secure/scalable infrastructure, lifecycle management, versioning, automated checks and release controls.
- Objective: stronger production engineering, not just exam familiarity.

## AI-500

- Use the official study guide, AI-500T00 and multi-agent learning paths.
- Prepare for architecture, development, evaluation/monitoring, security/governance and deployment.
- Practise Foundry, Python, Azure infrastructure, MCP, RAG and orchestration frameworks such as LangGraph.
- User-supplied plan says AI-500T00 becomes available 2026-09-30; this was not reverified when saving.
- Illustrative capstone: supervisor agent -> data/research/document/analytics agents -> MCP/tool layer -> human approval -> monitoring -> security -> deployment.
- Agent topology is an example, not a requirement to force every use case into multiple agents. Document why each component is needed.
- Demonstrated system behavior and production controls matter more professionally than an isolated exam pass.

## Databricks GenAI Engineer Associate

- Preparation order: official exam guide -> related training -> official AI Prep Guide -> recheck guide and fill gaps.
- Cover application design, data preparation, development, deployment, governance, evaluation and monitoring.
- Practise the platform's search, Model Serving, MLflow and Unity Catalog capabilities.
- Build RAG applications and LLM chains; connect Delta data to retrieval, then deploy and evaluate the application.
- Study model lifecycle integration with access control, lineage and governance.
- "AI Search" and other product labels are preserved from the supplied plan; check current documentation naming and exact exam version before labs.
- Reuse the earlier conceptual foundation while learning platform-specific behavior.

## Master AI study notebook

Create one durable notebook organized by universal concepts, not exam or vendor. The following is the user's conceptual comparison, not a claim of exact feature equivalence.

| Universal concept | Snowflake | Azure | Databricks |
|---|---|---|---|
| Models | Cortex models | Foundry models | Foundation Model APIs |
| RAG | Cortex Search | Azure AI Search / Foundry | AI Search |
| Agents | Cortex Agents | Foundry Agents | Databricks Agents |
| Model lifecycle | Model Registry | Azure ML | MLflow |
| Governance | Snowflake RBAC | Azure RBAC | Unity Catalog |
| Evaluation | Cortex evaluation | Foundry Evaluation | MLflow evaluation |
| Monitoring | Snowflake observability | Azure Monitor / Application Insights | MLflow / Databricks monitoring |
| Tools | Cortex functions | Foundry tools / MCP | Tools/functions |
| Deployment | Snowpark / Native | Azure / Foundry | Model Serving |

For each concept, retain the definition, design trade-offs, vendor implementation, lab/code reference, failure cases, evaluation evidence, security implications and cost notes. The goal is to reuse learning and reduce duplicated preparation; the amount of time saved is not guaranteed.

## Learning progression

1. SnowPro GenAI: learn the common GenAI foundation through Cortex.
2. AI-103: implement those concepts in Microsoft Foundry.
3. AI-300: deploy, evaluate, monitor and operate the applications.
4. AI-500: develop production multi-agent architecture.
5. Databricks GenAI: apply the conceptual stack with Databricks retrieval, MLflow, Model Serving and Unity Catalog.

## Official starting points

Existing verified reference links from the earlier roadmap:
- [Snowflake certification catalog](https://learn.snowflake.com/en/certifications/)
- [Snowflake documentation](https://docs.snowflake.com/)
- [AI-103 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-103)
- [AI-300 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-300)
- [AI-500 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-500)
- [Databricks GenAI March 2026 guide](https://www.databricks.com/sites/default/files/2026-03/Databricks-Certified-Generative-AI-Engineer-Associate-Exam-Guide-Mar26.pdf)

This update saves the user's chosen curriculum; it is not a fresh verification of course availability, exam percentages, product names or version-specific features. Follow links from the current official guides for training and latest versions.

## Next action

After dbt, prepare a week-by-week SnowPro GenAI programme with exact current modules, labs, documentation chapters, original practice questions and a reusable cross-platform GenAI project. This is a future task, not already created or completed. Detailed dbt preparation remains in its separate task.
