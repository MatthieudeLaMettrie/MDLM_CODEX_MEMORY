# Project memory

Last updated: 2026-09-29

## Purpose and repository

This repository preserves context so future tasks can continue without relying on chat history.

- GitHub: https://github.com/MatthieudeLaMettrie/MDLM_CODEX_MEMORY
- AGENTS.md defines the continuity and publication workflow.
- MEMORY.md holds lasting context and priorities.
- sessions/ holds dated session summaries.
- guides/continuity/VISUAL_GUIDE.md explains the setup from repository creation and GitHub Desktop to commits, pushes, and continuity, with diagrams.

## Decisions and preferences

- Read this file and the three most recent session notes before work.
- Record every session, including explanations and planning, before final responses. Update durable memory whenever lasting facts change.
- The user explicitly authorized committing and pushing session records and requested artifacts in this repository by default. Do not repeatedly ask for routine confirmation; tool permissions and later user overrides still apply.
- Use Australia/Sydney dates and unique note filenames for separate tasks.
- Notes are faithful summaries, not verbatim chat exports. This instruction-driven workflow is not a background capture service.
- Prefer beginner-friendly explanations with diagrams. Explain the full setup beginning with repository creation and GitHub Desktop.
- Exclude secrets and preserve unrelated changes.

## Current state

- Repository layout (2026-09-28): root keeps README.md, MEMORY.md, and AGENTS.md; standalone guides and records are organized under `learning/rag/`, `learning/certifications/`, `guides/`, and `projects/`. Existing `dbt/`, `snowpro-genai/`, and `sessions/` remain in place. README.md is the navigation entry point.

- Initial continuity files were committed and pushed to main as 06b7251; local and remote hashes matched.
- guides/continuity/VISUAL_GUIDE.md documents the setup and ongoing workflow; README.md prominently links to it.
- sessions/2026-09-22-setup-guide-and-session-policy.md records this conversation's explanations and expanded recording policy.
- guides/programming/RUNTIME_STUDY_GUIDE.html is a standalone, offline study guide covering runtimes, Node.js/npm/npx, JavaScript and Python execution environments, examples and a self-check quiz; linked from README.md. HTML structure and interaction logic validated; browser visual preview was blocked by URL policy.
- guides/email/EMAIL_ALIAS_GUIDE.md explains how to receive information@frenchexpatsinvestment.com in the existing matthieu@frenchexpatsinvestment.com Gmail inbox using a same-domain Google Workspace user alias, and how to choose the sender in Outlook when using GWSMO. It distinguishes standard Outlook Gmail connections, where alias sending is not universally documented. The user corrected the new address from information@fei.com; actual account and Outlook configuration have not been checked.
- The dbt collector includes nine offline tests. Current planning objective: Data / AI architect certification and career development.

## Certification and career planning

- Azure Foundry/RAG study module: [AZURE_FOUNDRY_RAG_STUDY_COURSE.md](learning/rag/AZURE_FOUNDRY_RAG_STUDY_COURSE.md). It covers Azure AI Search, Foundry IQ versus Fabric IQ, current Foundry 2.x Python agent calls, indexing/retrieval, labs, and evaluation. Documentation-based; no Azure deployment was made.
- Matching GCP and AWS RAG modules: [GCP_AGENT_SEARCH_RAG_STUDY_COURSE.md](learning/rag/GCP_AGENT_SEARCH_RAG_STUDY_COURSE.md) and [AWS_BEDROCK_RAG_STUDY_COURSE.md](learning/rag/AWS_BEDROCK_RAG_STUDY_COURSE.md). GCP covers Agent Search (formerly Vertex AI Search), Gemini grounding and ADK; AWS covers Bedrock Knowledge Bases and AgentCore Gateway. Both have code, labs, and evaluation; neither was run in a cloud account.

- Authoritative user update, 2026-09-23: after dbt, **SnowPro GenAI -> AI-103 -> AI-300 -> AI-500 / Databricks GenAI**.
- AI-300 is reinstated as a locked stage. This explicitly supersedes the earlier "AI-103 directly to AI-500" and "defer AI-300" decisions.
- Detailed user learning order places AI-500 before Databricks GenAI; preserve the slash in the short form because exact scheduling/choice within that final pair was not separately confirmed. Do not silently make Databricks GenAI conditional on projects again.
- Study as one continuous curriculum, reusing universal concepts and one master AI notebook across vendors. Full resource/lab guidance: [AI_STUDY_CURRICULUM.md](learning/certifications/AI_STUDY_CURRICULUM.md).
- Primary sources: official SnowPro/Databricks guides, Microsoft AI-103/300/500 study guides and corresponding T00 courses; practical Cortex, Foundry/Azure ML and Databricks labs. SnowPro target split about 40% exam study / 60% labs; AI-300 requires a working CI/CD-to-rollback chain.
- Notebook topics: models, RAG, agents, lifecycle, governance, evaluation, monitoring, tools and deployment; compare Snowflake, Azure and Databricks without assuming feature equivalence.
- A flexible four-week SnowPro GenAI programme is now in [snowpro-genai/COURSE_COMPANION.md](snowpro-genai/COURSE_COMPANION.md), based on the user's five-page Snowflake GenAI instructor-led course datasheet (26F15): 13 units, labs, capstone, and ten retrieval checks. It maps course topics to C02 without treating the broader syllabus as the exam blueprint. A cross-vendor master notebook remains open.
- SnowPro GES-C02 study materials live under [snowpro-genai/README.md](snowpro-genai/README.md): four-domain guide, course companion, 28 original questions, staged-document/Search/Analyst/Agent mini-lab, 130 official resource-link entries extracted from the supplied 2026-04-30 PDF, and a mapped official AI and Agents Learning Track. Domain weights are 18/38/29/15. Live account labs and Snowflake SQL execution remain to be done. The supplied training catalog URL was session-gated, so stable public Snowflake course pages were used. The third-party BigDataPrep article agreed with the weights, but its exam mechanics were not independently verified.
- On 2026-09-25, added [snowpro-genai/AI_ML_DEEP_DIVE.md](snowpro-genai/AI_ML_DEEP_DIVE.md) for all 15 current AI Functions, privilege/model governance, guardrails, cost views, observability, and the broader Snowflake ML lifecycle. [snowpro-genai/AI_ML_DOC_ATLAS.md](snowpro-genai/AI_ML_DOC_ATLAS.md) inventories 310 reachable official pages (281 section-index pages plus 29 ML/SQL references); it is a heading-level inventory, not a deep review of every page. Its links now open normal Snowflake documentation pages; machine-readable `llms.txt`/`.md` URLs remain internal to the generator. Regeneration scripts are in the same folder. SQL has not been executed in a Snowflake account. Sessions: sessions/2026-09-25-snowflake-ai-ml-doc-deep-dive.md and sessions/2026-09-25-atlas-reader-links.md.
- [snowpro-genai/ENABLE_CORTEX_AND_RAG.md](snowpro-genai/ENABLE_CORTEX_AND_RAG.md) now gives the missing account/trial activation, roles/model governance, and end-to-end Cortex Search RAG lab, with PDF extension and troubleshooting. It was checked against current official docs on 2026-09-25 but not run in a Snowflake account. Session: sessions/2026-09-25-cortex-enablement-rag.md.
- Consolidated strategy/research: [CERTIFICATION_ROADMAP.md](learning/certifications/CERTIFICATION_ROADMAP.md). New exact dates are not confirmed; do not impose the previous schedule unchanged.
- User holds SnowPro Core (expires Jan 2027), PL-300, AI-102, DP-600, DP-700, Databricks DE Associate and an unspecified Gen AI credential. Do not guess its issuer.
- Goal: hands-on Data / AI architect. Balance delivery, market opportunities and study opportunity cost.
- Preserve Snowflake renewal: Specialty before Core expiry; use actual renewal date for 2028 deadline. Advanced Architect or DE considered for 2028; final choice pending and policy must be rechecked.
- Databricks DE Professional, ML, GH-600, AZ-104/AZ-305, security, third-cloud and AICD options remain unscheduled, not additions to the locked sequence.
- dbt projects built; debugging is weak spot. Prep task: 01a0c682-332f-7fa2-8a8a-ae93f9dad156. Keep this task strategic.
- Prior unsupported claims about vendor neutrality, rarity, commercial value and exam equivalence were corrected. Retain corrections without reviving obsolete recommendations.
- Salary research uses 2026 Australian/Sydney base-pay benchmarks excluding super/bonuses; location and personal salary context remain unconfirmed.
- User-supplied course dates, weights and product labels were saved as supplied, not freshly verified on 2026-09-23.
- Session: sessions/2026-09-23-continuous-ai-curriculum.md.

- Latest assistant recommendation: AI-500 before Databricks GenAI; target AI-103 Jan-Feb 2027, AI-300 Mar-May, AI-500 Jun-Sep, Databricks GenAI Oct 2027-Mar 2028. Provisional windows, not user-confirmed bookings. Full timetable in roadmap/curriculum.
- Accepted change, 2026-09-23: SnowPro Specialty: Gen AI *preparation* (Cortex study/labs) now starts in parallel with dbt, Now-Oct 2026, instead of only after dbt finishes; exam-sitting order is unchanged (dbt exam first, then SnowPro exam, widened to Oct-Dec 2026). Rationale: dbt debugging readiness is unscored, so slippage there would otherwise compress the SnowPro exam window against the Jan 2027 Core renewal deadline. Raised in the roadmap-review session and accepted the same day; see sessions/2026-09-23-roadmap-review-opinion.md and the updated table in CERTIFICATION_ROADMAP.md.

## DataCertPrep review

- User owns www.datacert-prep.com and MatthieudeLaMettrie/DataCertPrep; requested content/curriculum/SEO analysis on 2026-09-23.
- Audit: sessions/2026-09-23-datacertprep-content-seo-audit-01a0cb68.md. Broad curriculum structures and file coverage are strong, but sampled AWS/Fabric/dbt inaccuracies, Copilot domain mapping, biased answer design and SEO defects need attention. No product changes were made.
- Fresh HTTP checks confirmed scoring-copy repairs and GH-300 update are deployed; do not repeat stale crawl findings as current defects. Sandbox tools failed with Windows 1907; approved escalated PowerShell worked.

- Browser design follow-up completed: strong desktop styling; confirmed mobile header overflow (509px on 390px viewport) and squeezed DP-700 domain rows. Prioritize responsive fixes, clearer start-practice hierarchy and catalogue search. Evidence and scope are in the audit note and design-review/mobile-course-390.png; no product changes made.

## dbt preparation materials

- A living hands-on guide at [dbt/DBT_BIGQUERY_CLOUD_GUIDE.md](dbt/DBT_BIGQUERY_CLOUD_GUIDE.md) records the 2026-09-29 dbt Cloud + BigQuery setup for `TEST_ANALYTICS`: source `FEI_ADMIN_PORTAL.FEI_TRAFFIC_NAMED`, development dataset `dbt_fei_mdelamettrie`, production dataset `DBT_FEI_PROD`, BigQuery location `australia-southeast1`, and the Git deployment workflow. The connected private `dbt_cert` repository has `dbt_project.yml` at its root on `main`; Project subdirectory must be blank. The user reported this corrected project discovery. A completed production build remains unverified. Do not store service account keys in Git.
- The user prefers `models/Bronze`, `models/Silver`, and `models/Gold` as the dbt layer structure. Bronze wraps sources, Silver cleans and combines, Gold serves reporting. These are code folders; separate BigQuery datasets require explicit schema configuration. The living guide has the mapping and examples.

- Published materials live under [dbt/README.md](dbt/README.md); learner entry point is [dbt/dbt-study-guide/START_HERE.md](dbt/dbt-study-guide/START_HERE.md).
- User completed courses and built projects; debugging is the weak spot and exam readiness is unassessed. Start with Cases 1–3, then tailor practice. Withhold answers until an attempt or request for help. Treat 7–10 days as a flexible window, not a readiness assumption.
- User chose a local Python collection workflow and guide writing/refinement in this task, without local AI installation. On 2026-09-22, public collection saved 1,558/1,573 discovered URLs; 15 gaps remain. Filtered study library contains 1,300 documents in 712 regenerable packets.
- Curated guide cites 34 official references and contains twenty original debugging cases plus a readiness plan. Official exam page listed dbt 1.11 when checked on 2026-09-22; live docs include later versions. Examples have not been warehouse-tested; enrolled dbt Learn lessons/transcripts were not collected.
- Git includes authored content, collector, nine tests, reading index, source metadata and historical coverage. Raw downloaded pages, generated packets and imports stay local and can be regenerated. No AI service or recurring automation configured.
- Task: 01a0c682-332f-7fa2-8a8a-ae93f9dad156. Publication session: sessions/2026-09-23-dbt-learning-guide-01a0c682.md. Keep broader roadmap decisions in their existing strategic records.
