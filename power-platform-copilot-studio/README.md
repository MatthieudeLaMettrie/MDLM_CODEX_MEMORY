# Power Platform and Copilot Studio: admin, agents on Fabric, MCP and flows

## Recommended study order

The filenames are numbered `01` to `14` so this order is visible in the GitHub folder.

| Step | File | What to do |
| ---: | --- | --- |
| **1** | [01_ADMIN_AND_ENVIRONMENTS.md](01_ADMIN_AND_ENVIRONMENTS.md) | Environment types, the inactivity cleanup (with the disabled-environment worked example), roles, licensing, Managed Environments, DLP, external models, and where Apps live. |
| **2** | [02_FABRIC_AND_DATA_AGENTS.md](02_FABRIC_AND_DATA_AGENTS.md) | Why Fabric is not a knowledge source, the Fabric data agent route for Copilot Studio and Foundry, Power BI semantic models, other databases, and the two-tenant (JB) case. |
| **3** | [03_MCP_CONNECTORS_AND_FLOWS.md](03_MCP_CONNECTORS_AND_FLOWS.md) | MCP authentication and OAuth configuration types, connectors, flows versus agent reasoning. |
| **4** | [04_AI_ENGINEER_PLAYBOOK.md](04_AI_ENGINEER_PLAYBOOK.md) | Platform choice, identity, ALM, governance, cost, quality, failure modes, and the JB readiness checklist. |
| **5** | [05_PRACTICE_CHECKS.md](05_PRACTICE_CHECKS.md) | Fourteen closed-book checks with answers and a lab. |
| **6** | [06_OFFICIAL_DOC_INDEX.md](06_OFFICIAL_DOC_INDEX.md) | The Microsoft Learn pages used, and what was not read. |
| **7** | [07_FOUNDRY_AGENT_WITH_FABRIC_TOOL.md](07_FOUNDRY_AGENT_WITH_FABRIC_TOOL.md) | Step-by-step: add the Fabric data agent tool to a Foundry agent in the new portal, test, code sample, MCP alternative, unattended-use caveat, troubleshooting. Do after step 2. |
| **8** | [08_FABRIC_ADMIN_AND_TENANT_CHECKLIST.md](08_FABRIC_ADMIN_AND_TENANT_CHECKLIST.md) | The same-tenant rule, the Fabric tenant settings to enable, capacity and region rules, permissions per user, authentication facts, one-page pre-flight. Read before any Fabric connection. |
| **9** | [09_FOUNDRY_PLATFORM_AND_SERVICES.md](09_FOUNDRY_PLATFORM_AND_SERVICES.md) | Foundry portal map, resource model, services you can add, why region matters, deployment types, roles, limits. |
| **10** | [10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md) | Every tool with examples, toolboxes, knowledge options, how to set up Azure AI Search and Foundry IQ step by step, memory and its model and region limits. |
| **11** | [11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md) | Guardrails (intervention points, risks, override rule), evaluations (approaches, evaluators, starter set), fine-tuning methods. |
| **12** | [12_JB_NEWSLETTER_FIELD_LOG.md](12_JB_NEWSLETTER_FIELD_LOG.md) | What actually happened building the JB agent: errors, fixes, what the agent revealed, open items. |
| **13** | [13_FOUNDRY_RESOURCE_IAM_AND_OPERATIONS_RUNBOOK.md](13_FOUNDRY_RESOURCE_IAM_AND_OPERATIONS_RUNBOOK.md) | Step-by-step runbook from the Foundry resource settings and region, through IAM roles, deployments, guardrails, Application Insights, evaluations and publishing, with the JB project's actual state. |
| **14** | [14_ACCESS_SETUP_FOUNDRY_AND_FABRIC.md](14_ACCESS_SETUP_FOUNDRY_AND_FABRIC.md) | Step-by-step access setup: Azure RBAC Foundry User and Fabric permissions (data agent sharing, warehouse, lakehouse, semantic model, SQL database, KQL), groups, RLS and CLS, testing, least-privilege plan. |

Steps 1–4 are the path; step 5 tests it; step 6 is a reference. Steps 7–12 are the Foundry and Fabric build: read 8 first, then 7, 9, 10 and 11; 12 is the worked example and 13 is the operations runbook (settings, IAM, monitoring, publishing). The loop is **study → try in a dev tenant → test yourself → repair misses**.

## Related material

- [Agents over Power BI semantic models: Desktop and Fabric setup](../guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md) for building the semantic model and data agent itself.
- [Azure Foundry RAG course](../learning/rag/AZURE_FOUNDRY_RAG_STUDY_COURSE.md) for Foundry and Azure AI Search.
- [API authentication guide](../guides/api/API_AUTHENTICATION_STUDY_GUIDE.md) for OAuth, keys and identity concepts.

## Status and limits

Started 2026-10-08 from a user session about a disabled Copilot Studio developer environment, then a request for a full admin and agent-building guide. Microsoft Learn pages were fetched on that date and are listed in file 06. **No Power Platform, Fabric, Foundry or Copilot Studio resource was created, changed or tested**; the lab is not run. Microsoft licensing, preview features and menu names change often, so recheck before acting. Statements marked **Unverified** are product knowledge, not read from a page. File 01 notes a conflict between the Fabric page (Microsoft 365 Copilot licence) and the Copilot Studio page (tenant plus user licences) that must be resolved against Microsoft's current licensing guide.

No tenant IDs, environment IDs, URLs of private environments or credentials are stored here.
