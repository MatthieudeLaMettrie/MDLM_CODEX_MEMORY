# Data and AI certification roadmap

Updated: 2026-09-23 (Australia/Sydney)

## Purpose and decision status

Career objective: hands-on Data / AI architect, with interest in enterprise delivery, consulting, multi-platform capability, and eventual leadership.

This document consolidates the certification discussion, including corrected claims and superseded recommendations. User-confirmed choices are distinguished from assistant recommendations. It is not an enrolment commitment or a guarantee of employment or salary.

## Existing qualifications and context

User reports:
- SnowPro Core, expiring January 2027.
- PL-300, AI-102, DP-600, DP-700.
- A credential described as "Gen AI"; exact issuer/title remains unspecified. Do not assume this is SnowPro Gen AI or Databricks GenAI.
- Databricks Data Engineer Associate.
- dbt course content completed and projects built; debugging is the main preparation weakness.

User explicitly wants dbt preparation in a separate task and this discussion focused on certification strategy. The separate task is "dbt certification preparation and debugging", ID 01a0c682-332f-7fa2-8a8a-ae93f9dad156.

The 2026-09-23 user update inserts AI-300 between AI-103 and the AI-500 / Databricks GenAI stage, superseding the earlier direct sequence. The prior SnowPro Advanced renewal proposal remains for 2028.

## Current roadmap: latest state takes precedence

Authoritative user update (2026-09-23): **after dbt, SnowPro GenAI -> AI-103 -> AI-300 -> AI-500 / Databricks GenAI**.

Study this as one continuous AI curriculum. Full resources, lab guidance and master notebook structure: [AI_STUDY_CURRICULUM.md](AI_STUDY_CURRICULUM.md).

| Sequence | Credential or activity | Status | Rationale |
|---|---|---|---|
| Current | dbt Analytics Engineering | Underway; primary focus | Detailed debugging and readiness work remains in its separate task. |
| Current (parallel) | SnowPro Specialty: Gen AI - study/prep only | Added 2026-09-23; runs alongside dbt rather than strictly after it | dbt debugging readiness is unscored, so starting Cortex study now protects the January 2027 Core renewal deadline against dbt slippage. Exam is still sat after dbt, per the locked order below. |
| 1 | SnowPro Specialty: Gen AI - sit exam | Locked next stage after dbt | Build GenAI concepts through Cortex; protect the January 2027 Core renewal deadline. |
| 2 | AI-103 | Locked | Apply common concepts to Foundry apps and agents; prerequisite credential for AI-500 Expert. |
| 3 | AI-300 | Locked, reinstated by user | Operate applications through CI/CD, Azure ML/Foundry, evaluation, monitoring and rollback. |
| 4 / 5 | AI-500 / Databricks GenAI | Locked final stage as written by user | Detailed learning order lists AI-500 then Databricks GenAI; exact final scheduling/choice within the pair remains unspecified. |
| Before actual Snowflake expiry in 2028 | SnowPro Advanced: Architect OR Data Engineer | Earlier renewal proposal retained; final choice pending | Match exam to architecture or engineering responsibilities. |
| Later | Other qualifications | Unscheduled | Add only for a concrete role, client or responsibility. |

Earlier calendar targets are provisional: no replacement exam dates were supplied, and adding AI-300 changes the direct AI-103-to-AI-500 schedule. Snowflake renewal dates remain a constraint.

The date of the 2028 Snowflake deadline depends on the actual 2026 renewal event, not automatically January 2029. Passing Specialty in Oct-Nov 2026 would normally place the next two-year expiry around Oct-Nov 2028.


## Recommended timetable (2026-09-23)

Assistant recommendation requested by user; windows are provisional, not bookings. This implements the user's continuous curriculum with AI-500 before Databricks GenAI.

| Timeframe | Certification | Recommendation and usefulness | Practical checkpoint |
|---|---|---|---|
| Now-Oct 2026 | dbt Analytics Engineering (primary) + SnowPro Specialty: Gen AI (parallel prep, exam not yet sat) | Finish dbt preparation if ready; do not let it jeopardize Snowflake renewal. Start SnowPro Cortex study and labs in parallel now, added 2026-09-23, so dbt slippage does not compress the exam-sitting window against the Jan 2027 Core deadline | dbt: diagnose project failures independently. SnowPro: Cortex concepts studied and labs started, not yet exam-ready |
| Oct-Dec 2026 | SnowPro Specialty: Gen AI (sit exam) | Sit the exam once dbt is done, drawing on prep already completed in parallel; window widened to Dec to keep a buffer before Jan 2027 Core expiry | Cortex retrieval/agent application with evaluation; exam passed with margin before Core expiry |
| Jan-Feb 2027 | AI-103 | Build on AI-102; develop Foundry applications and agents | Working Foundry app with tools and grounding |
| Mar-May 2027 | AI-300 | Keep in sequence for production ML/GenAI engineering | CI/CD, deployment, evaluation, monitoring and rollback |
| Jun-Sep 2027 | AI-500 | Main architecture milestone; extend operational foundations into multi-agent delivery | Justified orchestration, permissions, approvals and measured reliability |
| Oct 2027-Mar 2028 | Databricks GenAI Engineer Associate | Transfer the conceptual stack to a second AI delivery platform | Databricks RAG with lifecycle, serving and governance |
| Before actual Snowflake expiry in 2028 | SnowPro Advanced Architect or DE | Prefer Architect for architecture ownership; choose DE for pipeline-heavy work. Combine advancement and renewal | Experience and readiness aligned to chosen scope |

Keep GH-600, Databricks DE Professional/ML, AI security, AZ-104/AZ-305, AWS/GCP and AICD outside the scheduled core unless a concrete need changes priorities. Do not add exams between these stages. Dates can move with readiness; protect the actual Snowflake expiry and leave a retake buffer.

**Parallel-track update (2026-09-23):** the exam-sitting order remains dbt then SnowPro Specialty then AI-103, unchanged from the locked sequence. What changed is when SnowPro Specialty *preparation* begins: it now starts alongside dbt instead of waiting until dbt is finished, because dbt debugging readiness is unscored and a delay there would otherwise squeeze the SnowPro exam into a short window before the Jan 2027 Core renewal deadline. This was raised as a risk in the 2026-09-23 roadmap review (sessions/2026-09-23-roadmap-review-opinion.md) and accepted by the user the same day.

This sequence invests more study time than the earlier shortened plan. Its rationale is integrated capability: build -> operate -> architect -> implement on another platform. Reuse one project and one concept notebook to manage that opportunity cost. It does not imply guaranteed salary or job outcomes.


## Snowflake: Advanced Architect versus Data Engineer

| Dimension | Advanced: Architect | Advanced: Data Engineer |
|---|---|---|
| Scope | End-to-end flows, architecture meeting business/security/compliance requirements, integration/tool choices, performance, data sharing | Ingestion from lakes/APIs/on-premises, transformation, replication/sharing, near-real-time streams, scalable compute, performance metrics |
| Best fit | Owning platform designs and explaining architecture trade-offs | Building and operating production data pipelines |
| Career alignment | Data/solution architecture and architecture consulting | Senior DE, engineering lead and hands-on platform delivery |
| Candidate guidance | Two or more years of production Snowflake architecture experience | Two or more years of production DE experience |
| Recommendation | Preferred 2028 target if experience supports it | Choose if closer to actual work; not an inferior qualification |

Current Snowflake policy: certifications renew on a two-year cycle from the renewal event; higher-level certifications renew active lower-level ones. Advanced renews active Specialty and Core; Specialty renews active Core. The portal and specific credential's eligible continuing-education activities must be checked before booking. Current published Advanced exam fee is USD 375; Specialty USD 225. Future pricing/policy is not guaranteed.

No need to schedule both Advanced exams for the same renewal objective.

## Databricks: choose the capability needed

| Option | Added value | Decision |
|---|---|---|
| DE Professional | Production pipelines, streaming, cost/performance, governance, observability, CI/CD and deployment | Best additional DE option if Databricks engineering is central. No longer the default scheduled next exam once a Snowflake Advanced upgrade is planned. |
| GenAI Engineer Associate | Databricks-specific retrieval, agents, evaluation, serving and AI lifecycle tooling | Included in the user-locked AI-500 / Databricks GenAI final stage; detailed learning order follows AI-500. Reuse concepts and learn platform-specific implementations. |
| ML Associate | Feature engineering, training, tuning, evaluation, selection and deployment | Useful expansion into predictive ML: forecasting, classification, recommendation or anomaly detection. Pair with a modelling project. |
| ML Professional | Enterprise ML pipelines, distributed training, automated retraining, monitoring and rollout | Later, after production ML experience. Not a default next step. |

Snowflake Advanced DE and Databricks DE Professional are not equivalent or mutually substitutable. Deferring one is a study-time decision, not a claim that the platforms require identical knowledge.

## Conditional and deferred qualifications

- GH-600: optional for supervising coding agents in GitHub delivery workflows. Lower priority than core delivery objectives.
- AZ-104 -> AZ-305: retain for broader Azure infrastructure architecture. AI-500 does not replace networking, identity, resilience and cloud-design breadth. Azure Administrator Associate is required for Azure Solutions Architect Expert.
- SC-500: conditional on cloud/AI security implementation responsibility; broader than agent security alone.
- AB-100: conditional on Dynamics 365, Power Platform and Copilot Studio business-solution architecture. Technical architecture exists in this track; calling it nontechnical was wrong.
- SnowPro Advanced Architect: formerly deferred indefinitely, now a potential 2028 renewal upgrade.
- AWS ML Engineer Associate / GCP Professional ML Engineer: require a concrete platform opportunity. No third-cloud certification purely for coverage. AWS exam versions were transitioning when checked; verify current scope later.
- AICD Company Directors Course: later, for credible advisory/governance/board objectives, ideally sponsored. Successful assessment and eligible membership underpin GAICD. No guarantee of board access or fees.
- DAMA CDMP: data management/governance specialization if relevant. AICD corporate governance does not substitute for it.
- GH-200 and DP-750: not scheduled; no verified numerical overlap or market-recognition claim is retained.

## Market appetite and opportunity cost

Australian/Sydney market was used as a working assumption, not a user-confirmed location.

SEEK July 2026 reported:
- AI-skill references up 60.4% year-on-year.
- AI mentioned in 2.1% of all ads and 13.5% of ICT ads.
- Agentic AI references up 178.4%; this is growth in skill mentions, not proof of high absolute job volumes or demand for AI-500 badges.

Recruiter reports and example job listings support continued relevance of data engineering, cloud, AI and ML skills. No comprehensive vacancy census or causal certification salary analysis was performed. Do not claim a specific certification guarantees more demand or pay.

Decision rule:
1. Protect near-term renewal deadlines.
2. Keep the latest locked sequence: SnowPro GenAI -> AI-103 -> AI-300 -> AI-500 / Databricks GenAI.
3. Prefer incremental skills and usable project evidence over duplicative exams.
4. Select the next platform exam from actual work opportunities.
5. Retain time for delivery, architecture writing, networking and role progression.

Study effort estimates such as "2-3 weeks" or "3-month grind" are not established facts about this user's readiness. Avoid hard study deadlines based solely on such estimates.

## Salary planning: historical research snapshot, not a forecast

AUD annual permanent base salary, excluding superannuation and bonuses. These are approximate role-level planning bands from 2026 recruiter benchmarks, not personal offer estimates or certification premiums.

| Role positioning | Approximate base range | Required evidence |
|---|---|---|
| Senior Data / AI Engineer | A$150k-200k | Independent production delivery and operational ownership |
| Data / AI Solutions Architect | A$180k-220k | Architecture decisions, stakeholders, integration, security, cost and trade-offs |
| Experienced AI Architect | A$220k-250k | Repeated enterprise delivery and broader technical leadership |
| Head of Data / AI | A$220k-300k | Team, budget, strategy and organisational accountability; a separate leadership progression |

Robert Half Sydney Data Architect percentiles checked: A$168,950 / A$185,300 / A$212,550 (25th/50th/75th). Pearson Carter Australia AI Architect range: A$198k-253k, midpoint A$220k. Their populations and methods differ; do not treat these as a single statistical sample. Rebenchmark before negotiating. Current role, experience, pay and leadership scope remain unknown.

## Delivery evidence

Build a reference system or approved case study demonstrating:
- Data quality, modelling, lineage and grounding.
- Justified single-/multi-agent design and platform trade-offs.
- Evaluation datasets and measured results.
- Access controls, tool boundaries and approval flows.
- Deployment, rollback, observability and failure handling.
- Cost/latency measurement and business outcomes.

Use synthetic data or client-approved sanitized material publicly. Birrell, Metcash, FEI and PDP appeared in pasted external advice; detailed project ownership, implementation and commercial claims were not independently inspected.

## Corrections to earlier advice

- Databricks GenAI is vendor-specific, not vendor-neutral or a guarantee against platform lock-in.
- dbt skills can transfer across platforms; a badge alone does not make someone cloud-agnostic.
- AI-103's credential is currently required for the AI-500 Expert certification. Earlier advice describing only an informal sequence was incomplete. This does not establish a prerequisite to merely sit the exam.
- AI-300 is not fully replaced by AI-500; classical ML lifecycle is a major additional area.
- AB-100 is technical business-applications architecture, not simply a nontechnical track.
- AI-500 does not replace AZ-305's infrastructure scope.
- AICD and CDMP address different forms of governance.
- Claims about rare badge combinations, "moats", executive trust, an "80% overlap", small certified populations or automatic salary premiums lacked adequate evidence.
- GES-C02 was asserted in pasted advice but not verified; retrieved Snowflake catalog material showed GES-C01. Use the live registration guide rather than freezing an exam code.
- GCP or AWS is not automatically the best third cloud; choose based on opportunities.
- No exam alone turns an engineer into an enterprise architect.

## Sources

Official certification and renewal sources checked in this conversation (2026-09-22); revisit before booking:
- [dbt exam and samples](https://www.getdbt.com/certifications/analytics-engineer-certification-exam) - retrieved version 1.11, 65 questions, two hours, 65% pass mark; verify later.
- [Snowflake renewal](https://learn.snowflake.com/en/snowpro-continuing-education/)
- [Snowflake certification catalog](https://learn.snowflake.com/en/certifications/)
- [SnowPro Advanced Architect](https://learn.snowflake.com/en/certifications/snowpro-advanced-architect/)
- [SnowPro Advanced DE](https://learn.snowflake.com/en/certifications/snowpro-advanced-dataengineer-C02/)
- [AI-103](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-apps-and-agents-developer-associate/)
- [AI-500 credential and prerequisites](https://learn.microsoft.com/en-us/credentials/certifications/multi-agent-ai-solutions-expert/)
- [AI-500 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-500)
- [AI-300 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-300)
- [GH-600 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600)
- [AB-100](https://learn.microsoft.com/en-us/credentials/certifications/agentic-ai-business-solutions-architect/)
- [SC-500 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-500)
- [Azure Solutions Architect](https://learn.microsoft.com/en-us/credentials/certifications/azure-solutions-architect/)
- [Microsoft renewals](https://learn.microsoft.com/en-us/credentials/certifications/renew-your-microsoft-certification)
- [Microsoft retirements](https://learn.microsoft.com/en-us/credentials/support/credential-retirement) - AI-102 credential retired June 30, 2026; existing earned credential remains active until expiry.
- [Databricks DE Professional](https://www.databricks.com/learn/certification/data-engineer-professional)
- [Databricks GenAI March 2026 guide](https://www.databricks.com/sites/default/files/2026-03/Databricks-Certified-Generative-AI-Engineer-Associate-Exam-Guide-Mar26.pdf)
- [Databricks ML Associate](https://www.databricks.com/learn/certification/machine-learning-associate)
- [Databricks ML Professional](https://www.databricks.com/learn/certification/machine-learning-professional)
- [AWS ML Engineer Associate](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/)
- [Google ML Engineer guide](https://cloud.google.com/learn/certification/guides/machine-learning-engineer)
- [AICD course](https://www.aicd.com.au/courses-and-programs/all-courses/company-directors-course.html)
- [AICD graduate membership](https://www.aicd.com.au/membership/graduate.html)
- [DAMA CDMP](https://dama.org/certification/about-cdmp-certification/)

Market sources:
- [SEEK July 2026 dashboard](https://au.employer.seek.com/market-insights/article/seek-employment-dashboard-july-2026)
- [Hays September 2026 technology snapshot](https://www.hays.com.au/press-release/content/technology-snapshot-fy26-27)
- [Robert Half Sydney Data Architect](https://www.roberthalf.com/au/en/job-details/data-architect/sydney)
- [Pearson Carter 2026 Data and AI guide](https://www.pearsoncarter.com/hiring-guides/data-ai-2026)

## Next checkpoints

- Confirm exact issuer/title of existing "Gen AI" qualification.
- Confirm study capacity and actual 2026 Snowflake pass/expiry dates.
- Begin SnowPro Specialty: Gen AI (Cortex) study/labs now, in parallel with dbt, per the 2026-09-23 parallel-track update.
- Maintain PL-300, DP-600 and DP-700 through eligible renewal assessments.
- Keep detailed dbt practice in its separate task.
- After AI-103, complete AI-300 before the AI-500 / Databricks GenAI stage as requested on 2026-09-23.
- Use AI_STUDY_CURRICULUM.md for the continuous curriculum and master notebook; ML remains outside the locked sequence.
- Reassess Snowflake Architect vs DE well before the 2028 expiry.
- Obtain current role, experience, location and responsibilities before personal salary advice.
