# AI Agentic Developer recruiter response

Date: 2026-10-07 (Australia/Sydney)
Task identifier: 01a114eb-3d00-72d0-b756-1739bbcdafaa

## Fabric IQ and cross-platform follow-up

User asked what Fabric IQ is and which GCP, Snowflake and Databricks tools serve comparable roles. They proposed model -> grounded data agent -> marketing/sales instructions -> Foundry/Copilot Studio through Fabric IQ -> testing, saying they had used the general workflow before.

Confirmed the broad sequence while adding model business preparation, direct agent testing and data-agent publishing before catalog connection; final consumer identity and channel/application testing remain necessary. Explained Fabric IQ as the broader business-context framework/workload, distinct from similarly named catalog/MCP integration tools. Ontology is optional for the semantic-model-backed reporting path, and either outer-agent product is optional.

Extended the existing guide with three instruction layers and illustrative marketing templates: model Prep for AI for DAX/business definitions, Fabric data-agent routing/presentation, and outer-agent tool-use/role behavior. Documented that DAX generation ignores agent-level instructions, persona prompts do not define measures or permissions, and causal explanations require evidence beyond observed change. Added acceptance-question examples without claiming live execution.

Compared functional counterparts using current primary documentation: GCP LookML plus Conversational Analytics (or direct BigQuery context) with API/A2A/ADK integration; Snowflake semantic views plus Cortex Analyst/Cortex Agents with REST or managed MCP; Databricks Unity Catalog semantics/metric views plus Genie Agents (formerly Genie Spaces), Conversation API and managed MCP. Distinguished SQL generation from orchestration/execution in Snowflake and broad Fabric IQ/ontology capabilities from the narrower reporting workflow. Updated README and durable memory. No tenant resources, agents, permissions or historical production claims were changed.

Validation: reviewed official vendor documentation and the guide changes; publication checks are recorded by Git history and the final response. Current names, preview status and integration availability are date-specific. Historical client rollout and exact personal implementation scope remain unconfirmed.

User additionally requested a production deployment section explaining where to publish after successful testing. Added section 14 covering Fabric workspace publication/sharing, direct M365 Copilot Agent Store (documented preview), Copilot Studio channels, and Foundry custom application/Teams/M365 routes. Included concrete steps, environment/source-binding checks, user authentication and release version behavior. Official Foundry docs now distinguish the current per-agent stable endpoint/identity from legacy Agent Applications; recorded this distinction rather than recommending legacy endpoint creation as the default. Foundry organization-wide publication requires Microsoft 365 administrator approval; this is a downstream product step, not permission to edit this guide. No live publication/deployment was attempted.

Local validation passed: git diff --check, 16 balanced Markdown fences, 14 numbered sections and review of the task-owned diff. No cloud execution was required or performed for the documentation change.

## Request and sources

User asked how to answer two recruiter questions using the local resume `Matthieu de La Mettrie Resume 3.docx` and position description `AI Agentic Developer PD.docx`: identify production enterprise agent deployments and personal implementation versus architecture; confirm willingness to remain hands-on in a developer role.

Read durable memory and the three latest filename-ordered session notes, checked repository state, and extracted all body paragraphs including tables from both supplied Word files. Used the documents skill for read-only source review. Source files were not edited or copied into Git. No recruiter message was sent.

## Findings and suggested response

- The resume explicitly describes the bilingual financial-media LLM pipeline and certification-prep SaaS as production/shipped systems. These support hands-on delivery claims, but are not evidence of Azure AI Foundry/Copilot Studio deployment to enterprise users.
- NSW Government copilots are described as developed using Copilot Studio and Azure AI Foundry with Fabric/external data, but rollout stage and detailed personal configuration/code scope are unspecified.
- Precision Data Partners' Fabric/Foundry newsletter workflow is described as designed and built, from ingestion and medallion layers through semantic grounding and CRM-ready HTML. The resume does not explicitly establish production enterprise use or user counts.
- Metcash Copilot Studio/Fabric Data Agents are described as evaluation. The Python Synapse reporting automation and automated unit tests give a concrete hands-on implementation example, separate from those agent evaluations.
- The PD explicitly specifies Level 1, assigned tasks, approved patterns, and working under senior developers/architects. A convincing response should acknowledge this reporting and decision structure, code review, testing, integration and maintenance, not only express general enthusiasm for AI.

Asked asynchronously for the rollout stage and personal implementation scope of the three Azure/Copilot examples. Do not invent production status, adoption numbers, dates, development percentages, or willingness as a confirmed personal preference before the user confirms it.

Prepared first-person wording for the user to review: distinguish each Azure project with explicit stage placeholders for NSW and Precision; state Metcash evaluation as described in the resume; explain personal implementation using the resume's developed/built evidence; separately cite production media/SaaS delivery. The second answer affirms comfort remaining hands-on, delivering defined backlog items under existing architecture/governance standards, testing/debugging/integrations and incorporating review feedback. This is suggested language, not a confirmed career commitment.

## Validation, limits and next steps

Cross-checked the response against both supplied documents. No external research was needed for this document-based drafting task. Deployment status, user adoption and precise personal contribution require the user's confirmation; the reply must leave those unknowns visibly marked instead of representing prototypes as production deployments. No lasting memory change is necessary because the unresolved project facts and proposed role preference are not confirmed.

Preserved concurrent work: initial modified MEMORY/dbt course/session files were committed by another task during this turn; later unrelated README, databricks assets and its session note remained outside this task's staging. Fetch initially failed because the sandbox cannot write `.git/FETCH_HEAD`; the approved escalated fetch succeeded. Review and publish only this note to current main under standing authorization; verify the push using remote branch evidence. Git history and the final reply provide publication evidence.

## Follow-up: simpler, realistic examples

User requested two or three simple, realistic examples using NSW Government, Metcash and Precision Data Partners, and explicitly confirmed personally creating a data agent for the newsletter at PDP. User also invited additional ideas. This confirms personal creation of that newsletter agent, but does not establish its rollout stage, enterprise adoption, or every implementation detail.

Prepared three descriptions: PDP newsletter generation from governed client data (confirmed project, supported by resume); NSW reporting copilot for natural-language questions over Fabric reporting datasets (resume-based use case, with specific configuration/testing tasks framed as suggested wording to use only if accurate); Metcash campaign analytics agent evaluation (resume-based evaluation, with example campaign questions proposed rather than asserted as implemented). Avoid fabricated production deployments, users, metrics or client outcomes. Explain that rollout stage still needs factual confirmation. Retain a concise hands-on-role answer covering coding, configuration, integrations, testing, and working within the team's architecture and review standards.

Added only the user's confirmed personal newsletter-agent work and unresolved rollout distinction to durable career context. Reviewed against the already extracted source documents; no external research, source-document edits or messaging to the recruiter. Existing Databricks task was committed during the preceding turn and is preserved. Publish this continuing note and relevant memory addition under standing authorization, then verify the remote contains the new commit.

## Follow-up: Desktop versus Fabric semantic models and agents

User asked whether the NSW reporting-agent scenario requires reports created in Fabric, or can use a model/report authored in Power BI Desktop, and requested architectures and step-by-step setup for both. Clarified that publishing a Desktop-authored model hosts it in the service; report authorship location does not dictate eligibility. Report and agent query the same published semantic model. A thin report uses its existing service model. These hosted integration patterns do not target an unpublished local PBIX.

Created guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md with both architectures and authoring paths, common capacity/tenant/region/permission prerequisites, model preparation, agent creation/validation/sharing, optional Copilot Studio and Foundry extensions, and precise recruiter wording. Linked it from README and updated durable memory. Used the visualization skill's static Mermaid guidance for four structural diagrams.

Checked current primary Microsoft documentation for Desktop publication, refresh, Fabric model creation, semantic-model/data-agent configurations, tenant settings, permissions, RLS, Copilot Studio harness variants and Foundry integrations. Key corrections: Power BI semantic models use DAX; model-specific query guidance must go in Prep for AI because data-agent instructions do not reach DAX generation; data-agent sample query pairs are unsupported for semantic models; consumers need model Read for these agent interactions rather than automatically requiring Build; RLS must be tested as actual restricted consumers. Source capacities must be in the same region as the data agent. Fabric no longer automatically creates default semantic models for new lakehouse/warehouse items.

Distinguished Fabric data agent (current concept docs call it generally available) from optional Foundry/Copilot Studio integrations and their documented preview/channel/harness limits. New Copilot Studio tool route uses Fabric IQ Data MCP; standard-harness route uses connected Agents. Current Foundry Fabric IQ uses catalog-selected MCP tools; older ID-based connection is an alternative. Avoid using old classic SDK examples as the new setup.

Earlier resume-based language grouped Foundry and Fabric agent terminology too loosely; clarified the actual component boundaries. User has not confirmed whether their PDP newsletter data agent is a Fabric-only or Foundry-orchestrated implementation. The technical setup guide is not evidence of prior NSW Government implementation, production rollout, or user adoption.

Validation is documentation/link/fence/diff review only. No tenant sign-in, capacity purchase/assignment, permissions changes, source refresh, Power BI publication, live DAX execution, agent configuration or deployment occurred. Tenant licensing, capacity, model storage mode, availability and actual user data remain uninspected. Record and publish only this guide/navigation/memory/session change to current main under standing authorization; verify publication against the remote. Preserve unrelated concurrent work.
