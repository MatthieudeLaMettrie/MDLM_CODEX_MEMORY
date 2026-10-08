# SnowPro Specialty: Gen AI (GES-C02)

## Recommended study order

The filenames are numbered `01` to `07` so this order is visible in the GitHub folder.

| Step | File | What to do |
| ---: | --- | --- |
| **1** | [01_STUDY_GUIDE.md](01_STUDY_GUIDE.md) | Read the four exam domains, product choices, syntax traps, governance, and billing map. This is the main exam guide. |
| **2** | [02_COURSE_COMPANION.md](02_COURSE_COMPANION.md) | Follow the four-week route and its 13 units, labs, capstone, and recall checks. |
| **3** | [03_ENABLE_CORTEX_AND_RAG.md](03_ENABLE_CORTEX_AND_RAG.md) | Set up a test account/role, check AI Function access, and work through the Search and RAG lab while studying the related units. |
| **4** | [04_AI_ML_DEEP_DIVE.md](04_AI_ML_DEEP_DIVE.md) | Go deeper on functions, access, models, cost, guardrails, and evaluation. Focus first on topics you could not explain from steps 1–3. |
| **5** | [05_PRACTICE_EXAM.md](05_PRACTICE_EXAM.md) | Take the 28 original questions closed-book. Review every miss against the study guide and official docs, then take Snowflake's official practice exam separately. |
| **6** | [06_OFFICIAL_DOC_INDEX.md](06_OFFICIAL_DOC_INDEX.md) | Use the official C02 PDF's grouped source links to resolve a specific missed exam objective. |
| **7** | [07_AI_ML_DOC_ATLAS.md](07_AI_ML_DOC_ATLAS.md) | Use this broader 310-page documentation map when you need a particular Snowflake AI/ML topic. It is a reference index, not a cover-to-cover assignment. |
| **8** | [08_SEMANTIC_LAYER.md](08_SEMANTIC_LAYER.md) | Learn the semantic layer: what semantic views are, how to build, query, secure, deploy, and tune them, with a known-answer lab, exam traps, and 12 checks. Best read alongside course Unit 7 (step 2), before the practice exam. |

Step 8 was added after the numbered path existed, so its number does not reflect reading order: study it before step 5. Steps 6–7 are reference tools: open them whenever a question or lab exposes a gap. The core loop is **study → practise in Snowflake → test yourself → repair misses**. This material began on 2026-09-24 from the official Snowflake C02 study guide dated 2026-04-30, the supplied Snowflake GenAI course datasheet, and Snowflake documentation. It is an independent study aid, not an official Snowflake exam or a guarantee of a pass.

## Exam map

| Domain | Official weight | Practice questions |
| --- | ---: | ---: |
| 1. Snowflake for Gen AI overview | 18% | 1-5 (5/28) |
| 2. Snowflake Gen AI functions | 38% | 6-16 (11/28) |
| 3. Snowflake Gen AI governance | 29% | 17-24 (8/28) |
| 4. Document processing | 15% | 25-28 (4/28) |

The question counts approximate the blueprint with a 28-question set. The guide's five sample questions are **not** reproduced here. The official practice exam is linked from the [Snowflake practice exam page](https://learn.snowflake.com/en/certifications/snowpro-practice-exams/); use it separately.

## Study method

- Reproduce important syntax examples from memory and work through the small labs in a Snowflake test account. Repository SQL was checked against documentation but has **not** been run in a Snowflake account.
- Attempt the 28 questions before opening the answer key. For each miss, record the product choice, exact syntax or privilege, billing unit, and official documentation page.
- Revisit Snowflake's official study guide and current docs just before booking. Product names, prices, availability, and privilege rules can change.

The [course companion](02_COURSE_COMPANION.md) turns the two-day GenAI syllabus into 13 study units, a flexible four-week sequence, labs, a capstone, and ten closed-book checks. Its topic map is our interpretation; the course datasheet does not define C02 exam weights or promise exam coverage.

The [AI/ML deep dive](04_AI_ML_DEEP_DIVE.md) was checked on 2026-09-25 against the two user-supplied Snowflake documentation entry points and their linked official references. The [atlas](07_AI_ML_DOC_ATLAS.md) inventories the official Cortex, CoCo and Snowflake ML section indexes (111 + 76 + 94 pages), plus 29 linked ML Function and SQL reference pages. It can be regenerated with `python build_ai_ml_doc_atlas.py`. It is a page inventory; the deep dive is the synthesized learning material. Semantic-view pages (`/user-guide/views-semantic/`) sit outside the atlas's three section indexes, so the atlas does not list them. [08_SEMANTIC_LAYER.md](08_SEMANTIC_LAYER.md) cites them directly; it was checked against live docs on 2026-10-08.

The 2026-10-08 review rechecked the main guides against live documentation. It updated six redirected links to their canonical pages and corrected the YAML-versus-semantic-view statement. It also added the Analyst-to-Agents recommendation, the exact aggregate-function privilege exception, Agent inaccessible-tool behavior, routing-dependent AI Credit pricing, and `AI_PARSE_DOCUMENT` `extract_images`/`page_filter` details.

The source PDF is available from the user's supplied [Snowflake certification page](https://learn.snowflake.com/en/certifications/snowpro-GenAI-C02/?pdf_name=SnowProGenAIStudyGuideC02.pdf). The local downloaded PDF was read for its blueprint and links; it is not copied into this repository because the guide says it is for internal use only.

## Official training and additional reading

Snowflake's free [AI and Agents Learning Track](https://learn.snowflake.com/en/pages/ai-and-agents-learning-track/) lists these courses in this order. The exam-relevance column is **our mapping**, not a Snowflake claim that the course fully covers GES-C02.

| Track course | Public estimated effort | C02 use |
| --- | ---: | --- |
| 1. [CoCo Essentials](https://learn.snowflake.com/en/courses/OD-COCOESS/) | 4 hours | Domain 1 interface/product awareness; Domain 3 cost controls. Includes hands-on CoCo use. |
| 2. [Getting Started with CoCo Desktop](https://learn-sandbox.snowflake.com/en/courses/OD-COCODSK/) | 2 hours | Domain 1 Cortex Code/CoCo interface awareness. Its lab requires installing the desktop app and using a Snowflake trial account; optional for exam-focused study. |
| 3. [Snowflake x Gen AI: A Cool Collab](https://learn.snowflake.com/en/courses/OD-SXGA/) | 2 hours | Broad introduction. Public description uses an external OpenAI API; pair with current managed Cortex docs. |
| 4. [Snowflake X GenAI: LLM Functions](https://learn.snowflake.com/en/courses/OD-SXGA2/) | 4 hours | Domain 2 hands-on function introduction. Public description names older function surfaces; verify current `AI_` syntax. |
| 5. [Generative and Agentic AI for Executives](https://learn.snowflake.com/en/courses/OD-SXGAEX/) | 0.5 hour | Broad strategy and responsible-governance context; low priority for exact syntax/RBAC/billing questions. |

If you want an introductory Snowflake course alongside step 1, consider track modules 3 and 4. Add module 1 for CoCo familiarity and module 2 if you want the desktop workflow. The track's public descriptions do not establish complete coverage of the certification objectives or current SQL signatures.

Other official options: [Snowflake GenAI Training](https://learn.snowflake.com/en/courses/ILT-GENAI/) is a paid two-day/16-hour instructor-led course with labs. The [official SnowPro practice exams](https://learn.snowflake.com/en/certifications/snowpro-practice-exams/) follow the live exams' domain specifications and weightings; check purchase/access terms before starting, as Snowflake currently says an attempt must be completed within 24 hours and cannot be retaken once submitted. The earlier supplied `training.snowflake.com` catalog URL contained a login-session parameter and could not be read through the public web tool; stable public course pages are linked here.

A [BigDataPrep GES-C02 article](https://www.bigdataprep.com/2026/08/25/snowpro-specialty-gen-ai-ges-c02/) gives four weights and a broad feature map that agree with the official PDF. Its claims about question count, duration, passing score, and price were **not** independently confirmed from Snowflake's accessible certification page, so this repository does not treat them as exam rules. The article links to third-party practice material; the original questions here are based on the official blueprint and Snowflake documentation instead.
