# dbt study guide: numbered learning path

**Begin with [00 — Start here](00_START_HERE.md).** This folder brings together the core guide, semantic-model course, hands-on lab, practice and references, following the guide → lab → practice → reference structure used in the [SnowPro GenAI folder](../../snowpro-genai/README.md).

## Read and work in this order

| Order | Material | What to do |
|---|---|---|
| **00** | [Start here](00_START_HERE.md) | Choose your route; for general dbt preparation, attempt workbook Cases 1–3 first |
| **01** | [Core concepts and troubleshooting](01_CORE_GUIDE.md) | Learn resource naming, commands, materializations, tests, selection and debugging |
| **02** | [Semantic models and metrics course](02_SEMANTIC_MODELS_AND_METRICS_COURSE.md) | Follow the 16 lessons using your FEI RSS example; understand grain, entities, dimensions, metrics and both YAML formats |
| **03** | [BigQuery semantic-model lab](03_SEMANTIC_MODELS_LAB/README.md) | Work with synthetic articles, choose one YAML format, build in development and reconcile expected results |
| **04** | [Debugging practice workbook](04_PRACTICE.md) | Attempt the twenty core dbt cases; use lesson 15 of the semantic course for twenty additional metric exercises |
| **05** | [Readiness plan](05_READINESS.md) | Score your reasoning, target gaps and retest independently |
| **06** | [Official source references](06_SOURCES.md) | Investigate gaps; use the semantic course's own official reference library for metrics |
| **07** | [Publish metrics to business users](07_PUBLISH_TO_BUSINESS_USERS.md) | After lesson 12, connect Power BI or Excel/Google Sheets; provide category/date controls and publish a tested consumer experience |
| **08** | [Connect the Semantic Layer to six interfaces](08_CONNECT_SEMANTIC_LAYER_TO_TOOLS.md) | Locate definitions/data; follow the common setup and the Power BI, Excel, Google Sheets, Tableau, Data Studio or React/API steps |
| **09** | [Four additional RSS metrics](09_RSS_ADDITIONAL_METRICS.md) | Extend your supplied model with total/max body length, average title length and missing-category article count; reconcile nulls and duplicates |

The numbers describe the default learning sequence. Use references whenever you need them. The lab starts after course lesson 5 and accompanies lessons 6–10; you do not have to finish all 16 lessons before trying it.

## If you are here for semantic models and metrics

1. Open **02**, read lessons 1–5, then use **03** alongside lessons 6–10.
2. Finish lessons 11–14 for joins, BI consumption, deployment and debugging. Use **07** after lesson 12 for a business-user handoff and **08** for each tool's connection steps.
3. Attempt lesson 15's exercises, then complete lesson 16's FEI RSS capstone.
4. Return to **01** or **04** when a foundational dbt concept blocks you.

The semantic course has its own estimated 10–14-hour route, checkpoints and capstone rubric. The broader readiness plan is flexible and does not establish exam readiness merely from reading completion. Exercise answers remain withheld until you attempt them or request help.

## Supporting files and project setup

- [Progress log](progress.csv): record attempts, confidence and evidence.
- [Historical verification record](verification.json): scope of the original September 2026 collection checks.
- [dbt Cloud + BigQuery field guide](../DBT_BIGQUERY_CLOUD_GUIDE.md): project setup, credentials/targets and deployment history.
- [Public reading library and collector](../dbt-learning-flow/README.md): regenerate the wider documentation collection.

Core study materials were prepared in September 2026; the semantic course and lab were added on 7 October 2026. The examples have not been executed against your live warehouse. Read version and adapter notes before using them in an actual project.
