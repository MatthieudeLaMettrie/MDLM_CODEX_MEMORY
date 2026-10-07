# 03 — RSS semantic metrics lab

Read [02 — the course](../02_SEMANTIC_MODELS_AND_METRICS_COURSE.md), especially lessons 5–8, before copying files. Return to the [numbered learning path](../README.md) for the broader sequence. These are teaching assets, not a complete dbt project. The SQL is for BigQuery. No warehouse execution has been performed.

## Install in your existing development project

Use an isolated branch and development dataset. Check for name collisions: if your project already defines `articles_published` or `avg_article_length`, either use a separate lab project or consistently rename the lab metrics and all dependent references. Do not replace your live definitions just to run this example.

| File here | Destination in your dbt project |
|---|---|
| `rss_articles_lab.csv` | `seeds/rss_articles_lab.csv` |
| `fct_rss_articles_lab.sql` | `models/Gold/fct_rss_articles_lab.sql` |
| `time_spine_daily_lab.sql` | `models/Gold/time_spine_daily_lab.sql` |
| `time_spine_daily_lab.yml.example` | `models/Gold/time_spine_daily_lab.yml` |
| **Latest path:** `rss_latest.yml.example` | `models/Gold/rss_lab.yml` |
| **Legacy path:** `rss_legacy.yml.example` | `models/Gold/rss_lab.yml` |
| `rss_length_nonnegative.sql` | `tests/rss_length_nonnegative.sql` |
| `reconcile.sql` | Run manually in BigQuery after replacing `PROJECT.DATASET` |

Choose **one** semantic YAML alternative. The `.example` extension keeps alternatives from being accidentally parsed as dbt YAML here. Latest is for supported v1 Latest/v2/v1.12 environments; confirm the actual runtime. The daily time-spine YAML configuration requires dbt v1.9+ or a supported platform runtime. Extend existing model declarations rather than duplicating them if you reuse a model name.

If seed date/number inference is unexpected, inspect the loaded seed and configure its column types in your own project. The model casts DATE and INT64 explicitly. Blank length must become SQL NULL, not zero. The data uses a date already assigned under the lab's Sydney date policy; no timezone conversion is needed on this seed.

## Run in development

```shell
dbt seed --select rss_articles_lab
dbt build --select fct_rss_articles_lab time_spine_daily_lab
dbt test --select rss_length_nonnegative
dbt parse
```

In platform development, if commands are supported and your environment is configured:

```shell
dbt sl list metrics
dbt sl list dimensions --metrics articles_published
dbt sl validate
dbt sl query --metrics articles_published,avg_article_length,total_article_characters,articles_with_length,length_coverage
dbt sl query --metrics articles_published,avg_article_length --group-by metric_time__day
dbt sl query --metrics articles_published,avg_article_length --group-by article__publisher
```

For an independently installed/configured local MetricFlow environment, use `mf validate-configs`, `mf list metrics` and `mf query ...`. Consult runtime help for flags. Do not assume `dbt sl` is supplied by a plain dbt Core install. In Studio, do not add `--target dev` unless the profile actually has that output.

## Expected baseline

| Group | Count | Known lengths | Total chars | Mean chars | Length coverage |
|---|---:|---:|---:|---:|---:|
| All | 5 | 4 | 1,500 | 375 | 0.8 |
| Alpha | 3 | 3 | 600 | 200 | 1.0 |
| Beta | 2 | 1 | 900 | 900 | 0.5 |
| English | 3 | 3 | 1,200 | 400 | 1.0 |
| French | 2 | 1 | 300 | 300 | 0.5 |

Daily counts are 2, 2 and 1 on 1, 2 and 4 October. The baseline does not request time-spine filling; 3 October should be absent. Average ignores the missing length. A total over the publisher means is invalid; the overall average must be recomputed from article rows or additive total/known-length components.

## Extensions

1. Query language with the discovered qualified dimension name.
2. Add `join_to_timespine: true` and `fill_nulls_with: 0` to the **latest count metric**; bound the query to the sample period using supported filters and inspect 3 October. Do not zero-fill mean length.
3. Add the latest-format rolling/MTD definitions from course lesson 9 and query by day. Check calendar range and window boundaries in generated SQL.
4. Duplicate a URL deliberately and verify the uniqueness test fails; then restore it.
5. Replace synthetic inputs with a separate, explicitly mapped cleaned RSS model after agreeing its grain. Keep this deterministic lab as a regression reference.

These files support reproducible learning, but only execution in your actual environment can verify dbt compatibility and MetricFlow results. Source freshness and live ingestion are outside this synthetic lab.
