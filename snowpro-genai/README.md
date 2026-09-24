# SnowPro Specialty: Gen AI (GES-C02)

Start with [the study guide](STUDY_GUIDE.md), then take [the original practice set](PRACTICE_EXAM.md) closed-book. Use [the official documentation index](OFFICIAL_DOC_INDEX.md) to investigate misses. This material was prepared on 2026-09-24 from the official Snowflake C02 study guide dated 2026-04-30 and current Snowflake documentation. It is an independent study aid, not an official Snowflake exam or a guarantee of a pass.

## Exam map

| Domain | Official weight | Practice questions |
| --- | ---: | ---: |
| 1. Snowflake for Gen AI overview | 18% | 1-5 (5/28) |
| 2. Snowflake Gen AI functions | 38% | 6-16 (11/28) |
| 3. Snowflake Gen AI governance | 29% | 17-24 (8/28) |
| 4. Document processing | 15% | 25-28 (4/28) |

The question counts approximate the blueprint with a 28-question set. The guide's five sample questions are **not** reproduced here. The official practice exam is linked from the [Snowflake practice exam page](https://learn.snowflake.com/en/certifications/snowpro-practice-exams/); use it separately.

## How to use this

1. Read the four domain chapters and reproduce the syntax examples from memory.
2. Build the small lab in the guide using a Snowflake account, keeping costs and privileges in view. Examples here were checked against documentation but have **not** been run in a Snowflake account.
3. Attempt all 28 questions before opening the answer key. For each miss, write the product choice, exact syntax or privilege, billing unit, and the linked documentation page.
4. Revisit Snowflake's official study guide and current docs just before booking. Snowflake products, names, pricing, availability, and privilege rules change.

The source PDF is available from the user's supplied [Snowflake certification page](https://learn.snowflake.com/en/certifications/snowpro-GenAI-C02/?pdf_name=SnowProGenAIStudyGuideC02.pdf). The local downloaded PDF was read for its blueprint and links; it is not copied into this repository because the guide says it is for internal use only.

## Official training and additional reading

The supplied `training.snowflake.com` course-catalog URL contains a login-session parameter and could not be read through the public web tool. The stable public [Snowflake course catalog](https://learn.snowflake.com/en/courses/) and the study guide point to these courses:

- [Snowflake GenAI Training](https://learn.snowflake.com/en/courses/ILT-GENAI/) — paid instructor-led, two days/16 estimated hours, with labs. Useful if you want guided practice; not required by the blueprint.
- [Snowflake x Gen AI: A Cool Collab](https://learn.snowflake.com/en/courses/OD-SXGA/) — free, two-hour introductory module. Its public description uses an external OpenAI API, so pair it with current managed Cortex docs.
- [Snowflake X GenAI: LLM Functions](https://learn.snowflake.com/en/courses/OD-SXGA2/) — free, about four hours. Its public description names older function surfaces; check current `AI_` syntax in the study guide and linked reference pages.
- [Official SnowPro practice exams](https://learn.snowflake.com/en/certifications/snowpro-practice-exams/) — Snowflake says these follow the live exams' domain specifications and weightings. Check purchase/access terms before starting; the page currently says an attempt must be completed within 24 hours and cannot be retaken once submitted.

The user also supplied a [BigDataPrep GES-C02 article](https://www.bigdataprep.com/2026/08/25/snowpro-specialty-gen-ai-ges-c02/). Its four weights and broad feature map agree with the official PDF. Its claims about question count, duration, passing score, and price were **not** independently confirmed from Snowflake's accessible certification page, so this repository does not treat them as exam rules. The article links to third-party practice material; the original questions here are based on the official blueprint and Snowflake documentation instead.
