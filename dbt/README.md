# dbt learning and certification preparation

**[Start the numbered learning path: 00 → 07](dbt-study-guide/README.md)**

**[02 — Semantic models and metrics: full practical course](dbt-study-guide/02_SEMANTIC_MODELS_AND_METRICS_COURSE.md)** — 16 lessons using your FEI RSS lineage, latest and legacy YAML, a [03 — BigQuery lab](dbt-study-guide/03_SEMANTIC_MODELS_LAB/README.md), troubleshooting, 20 exercises and a capstone.

**[dbt Cloud + BigQuery setup and deployment field guide](DBT_BIGQUERY_CLOUD_GUIDE.md)** — a living record of this project's development and production setup, Git workflow, and resolved errors.

- [00 — Start here](dbt-study-guide/00_START_HERE.md): orientation and diagnostic.
- [01 — Core reference](dbt-study-guide/01_CORE_GUIDE.md): source-linked explanations across the exam domains, emphasizing troubleshooting.
- [04 — Twenty debugging exercises](dbt-study-guide/04_PRACTICE.md): attempt before requesting hints; no answer key included.
- [05 — Readiness plan](dbt-study-guide/05_READINESS.md): adapt the suggested 7–10 days to measured gaps.
- [06 — Official references](dbt-study-guide/06_SOURCES.md): source provenance for the core guide.
- [07 — Publish metrics to business users](dbt-study-guide/07_PUBLISH_TO_BUSINESS_USERS.md): Power BI and spreadsheet category/date filtering, deployment, sharing and alternatives.
- [Collection workflow](dbt-learning-flow/README.md): repeatable Python collector with Markdown/HTML support.
- [Public reading index](dbt-learning-flow/guide/START_HERE.md) and [coverage report](dbt-learning-flow/data/coverage.json).

Prepared from official sources on 22 September 2026. The exam page listed dbt 1.11; live documentation includes newer features. The original collection saved 1,558 of 1,573 discovered URLs. Nine workflow tests passed. The guide cites 34 official references; it is a curated synthesis, not an individually reviewed summary of every downloaded page.

Enrolled dbt Learn lessons were not collected. Teaching examples have not been executed against the learner's warehouse, and readiness has not yet been assessed.

## Run the offline checks

From `dbt/dbt-learning-flow`:

```shell
python -m unittest -v test_flow.py test_html.py test_build.py
```

## Refresh the public documentation

```shell
python dbt_learning.py collect --delay 0.25 --build
```

Python 3.10+ is required; collection and tests use only the standard library. Raw downloaded pages, synthesis packets, imports and optional model outputs stay out of Git. The collector can regenerate them locally. No scheduled task or AI service has been configured.
