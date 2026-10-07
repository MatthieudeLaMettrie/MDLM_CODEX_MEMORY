# dbt learning and certification preparation

**[Start the learning guide](dbt-study-guide/START_HERE.md)**

**[Semantic models and metrics: full practical course](SEMANTIC_MODELS_AND_METRICS_COURSE.md)** — 16 lessons using your FEI RSS lineage, latest and legacy YAML, a BigQuery lab, troubleshooting, 20 exercises and a capstone.

**[dbt Cloud + BigQuery setup and deployment field guide](DBT_BIGQUERY_CLOUD_GUIDE.md)** — a living record of this project's development and production setup, Git workflow, and resolved errors.

- [Core reference](dbt-study-guide/CORE_GUIDE.md): source-linked explanations across the exam domains, emphasizing troubleshooting.
- [Twenty debugging exercises](dbt-study-guide/PRACTICE.md): attempt before requesting hints; no answer key included.
- [Readiness plan](dbt-study-guide/READINESS.md): adapt the suggested 7–10 days to measured gaps.
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
