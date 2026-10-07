# 00 — Start here: your dbt learning guide

Prepared 22 September 2026. Designed for someone who has completed dbt courses and built projects, with extra emphasis on debugging and evidence of readiness.

Organized into a numbered learning path on 7 October 2026. Open the [folder overview](README.md) for the complete **00 → 08** sequence. For semantic models and metrics specifically, start with [02 — the course](02_SEMANTIC_MODELS_AND_METRICS_COURSE.md), then work through [03 — the BigQuery lab](03_SEMANTIC_MODELS_LAB/README.md) alongside its lessons. Use [07 — publication](07_PUBLISH_TO_BUSINESS_USERS.md) and [08 — tool connections](08_CONNECT_SEMANTIC_LAYER_TO_TOOLS.md) when preparing the business-user interface.

## Start with an attempt

Before reading the core explanations, attempt Cases 1–3 in [04 — the practice workbook](04_PRACTICE.md). Spend about ten minutes. Reply in this task with your diagnosis, evidence, fix, verification and confidence. Answers are intentionally withheld; ask for a hint or solution when you want one.

## Your materials

| Material | Use it for |
|---|---|
| [01 — Core guide](01_CORE_GUIDE.md) | Connected explanations, command choices, examples, source links and common failure mechanisms |
| [02 — Semantic models and metrics course](02_SEMANTIC_MODELS_AND_METRICS_COURSE.md) | Sixteen FEI RSS lessons, diagrams, YAML formats, metric queries, troubleshooting and capstone |
| [03 — BigQuery semantic-model lab](03_SEMANTIC_MODELS_LAB/README.md) | Synthetic article data, SQL/YAML alternatives and expected results |
| [04 — Practice workbook](04_PRACTICE.md) | Twenty deliberate-fault scenarios; diagnosis before hints or answers |
| [05 — Readiness plan](05_READINESS.md) | A flexible 7–10 day sequence, marking rubric and retest criteria |
| [06 — Source provenance](06_SOURCES.md) | Official references and retrieval dates; metrics references are also in 02 |
| [Progress log](progress.csv) | Record attempts, hints, confidence and evidence of improvement |
| [Collected reading index](../dbt-learning-flow/guide/START_HERE.md) | Browse the wider source library by topic |
| [Coverage report](../dbt-learning-flow/data/coverage.json) | Inspect unsuccessful URLs and collection limitations |
| [Workflow instructions](../dbt-learning-flow/README.md) | Repeat collection and regenerate source packets |

## What is verified, and what remains open

The current [official exam page](https://www.getdbt.com/certifications/analytics-engineer-certification-exam) lists dbt 1.11, 65 questions, two hours and a 65% passing score. Its seven domains are model development/optimization, governance, debugging, pipeline troubleshooting/optimization, tests, external dependencies and state. This guide maps to those domains; it does not invent topic weights or claim to reproduce the exam.

The public documentation collection discovered 1,573 URLs and saved 1,558 after the full run and retry, with 15 unsuccessful URLs recorded. The collection includes broader documentation and blog/reference material. It is not proof that every page on the website was discovered, and it does not include your enrolled dbt Learn lessons or unavailable video transcripts.

The core guide is a curated synthesis of the relevant official references, not a claim that every downloaded page has been individually summarized or fact-checked. Source links accompany each topic. Live docs include changes after 1.11; later-version examples have been kept out of the core command path where identified. Check version badges and adapter support when following a live link.

The Python collection and HTML fallback have passed offline checks and live sample runs. The teaching examples and fault scenarios have been reviewed as text but have not been executed against your warehouse. Once you supply your adapter and dbt runtime, we can turn the weak areas into executable labs.

## How to use it

Use a loop of attempt → targeted reading → explanation in your own words → verification → delayed retest. Do not read the full library sequentially. Begin with the diagnostic and spend most of the practice time on whichever reasoning steps fail: identifying the stage, interpreting evidence, choosing a repair, or proving correctness.

No answer key has been included in this guide. The main reference naturally teaches concepts used in the workbook, so do the diagnostic first if you want an honest baseline.
