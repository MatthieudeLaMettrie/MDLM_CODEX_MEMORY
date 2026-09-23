# Project memory

Last updated: 2026-09-23

## Purpose and repository

This repository preserves context so future tasks can continue without relying on chat history.

- GitHub: https://github.com/MatthieudeLaMettrie/MDLM_CODEX_MEMORY
- AGENTS.md defines the continuity and publication workflow.
- MEMORY.md holds lasting context and priorities.
- sessions/ holds dated session summaries.
- VISUAL_GUIDE.md explains the setup from repository creation and GitHub Desktop to commits, pushes, and continuity, with diagrams.

## Decisions and preferences

- Read this file and the three most recent session notes before work.
- Record every session, including explanations and planning, before final responses. Update durable memory whenever lasting facts change.
- The user explicitly authorized committing and pushing session records and requested artifacts in this repository by default. Do not repeatedly ask for routine confirmation; tool permissions and later user overrides still apply.
- Use Australia/Sydney dates and unique note filenames for separate tasks.
- Notes are faithful summaries, not verbatim chat exports. This instruction-driven workflow is not a background capture service.
- Prefer beginner-friendly explanations with diagrams. Explain the full setup beginning with repository creation and GitHub Desktop.
- Exclude secrets and preserve unrelated changes.

## Current state

- Initial continuity files were committed and pushed to main as 06b7251; local and remote hashes matched.
- VISUAL_GUIDE.md documents the setup and ongoing workflow; README.md prominently links to it.
- sessions/2026-09-22-setup-guide-and-session-policy.md records this conversation's explanations and expanded recording policy.
- RUNTIME_STUDY_GUIDE.html is a standalone, offline study guide covering runtimes, Node.js/npm/npx, JavaScript and Python execution environments, examples and a self-check quiz; linked from README.md. HTML structure and interaction logic validated; browser visual preview was blocked by URL policy.
- The dbt collector includes nine offline tests. Current planning objective: Data / AI architect certification and career development.

## Certification and career planning

- Authoritative user update, 2026-09-23: after dbt, **SnowPro GenAI -> AI-103 -> AI-300 -> AI-500 / Databricks GenAI**.
- AI-300 is reinstated as a locked stage. This explicitly supersedes the earlier "AI-103 directly to AI-500" and "defer AI-300" decisions.
- Detailed user learning order places AI-500 before Databricks GenAI; preserve the slash in the short form because exact scheduling/choice within that final pair was not separately confirmed. Do not silently make Databricks GenAI conditional on projects again.
- Study as one continuous curriculum, reusing universal concepts and one master AI notebook across vendors. Full resource/lab guidance: [AI_STUDY_CURRICULUM.md](AI_STUDY_CURRICULUM.md).
- Primary sources: official SnowPro/Databricks guides, Microsoft AI-103/300/500 study guides and corresponding T00 courses; practical Cortex, Foundry/Azure ML and Databricks labs. SnowPro target split about 40% exam study / 60% labs; AI-300 requires a working CI/CD-to-rollback chain.
- Notebook topics: models, RAG, agents, lifecycle, governance, evaluation, monitoring, tools and deployment; compare Snowflake, Azure and Databricks without assuming feature equivalence.
- After dbt, next requested direction is a week-by-week SnowPro GenAI programme with current official modules, labs, original practice questions and a reusable project. No programme or notebook implementation has yet been created.
- Consolidated strategy/research: [CERTIFICATION_ROADMAP.md](CERTIFICATION_ROADMAP.md). New exact dates are not confirmed; do not impose the previous schedule unchanged.
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

## DataCertPrep review

- User owns www.datacert-prep.com and MatthieudeLaMettrie/DataCertPrep; requested content/curriculum/SEO analysis on 2026-09-23.
- Audit: sessions/2026-09-23-datacertprep-content-seo-audit-01a0cb68.md. Broad curriculum structures and file coverage are strong, but sampled AWS/Fabric/dbt inaccuracies, Copilot domain mapping, biased answer design and SEO defects need attention. No product changes were made.
- Fresh HTTP checks confirmed scoring-copy repairs and GH-300 update are deployed; do not repeat stale crawl findings as current defects. Sandbox tools failed with Windows 1907; approved escalated PowerShell worked.

## dbt preparation materials

- Published materials live under [dbt/README.md](dbt/README.md); learner entry point is [dbt/dbt-study-guide/START_HERE.md](dbt/dbt-study-guide/START_HERE.md).
- User completed courses and built projects; debugging is the weak spot and exam readiness is unassessed. Start with Cases 1–3, then tailor practice. Withhold answers until an attempt or request for help. Treat 7–10 days as a flexible window, not a readiness assumption.
- User chose a local Python collection workflow and guide writing/refinement in this task, without local AI installation. On 2026-09-22, public collection saved 1,558/1,573 discovered URLs; 15 gaps remain. Filtered study library contains 1,300 documents in 712 regenerable packets.
- Curated guide cites 34 official references and contains twenty original debugging cases plus a readiness plan. Official exam page listed dbt 1.11 when checked on 2026-09-22; live docs include later versions. Examples have not been warehouse-tested; enrolled dbt Learn lessons/transcripts were not collected.
- Git includes authored content, collector, nine tests, reading index, source metadata and historical coverage. Raw downloaded pages, generated packets and imports stay local and can be regenerated. No AI service or recurring automation configured.
- Task: 01a0c682-332f-7fa2-8a8a-ae93f9dad156. Publication session: sessions/2026-09-23-dbt-learning-guide-01a0c682.md. Keep broader roadmap decisions in their existing strategic records.
