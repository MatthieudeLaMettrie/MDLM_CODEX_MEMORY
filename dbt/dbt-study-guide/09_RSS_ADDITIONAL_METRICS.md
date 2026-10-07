# 09 — Four additional RSS metrics

Prepared **8 October 2026** from your supplied YAML and BigQuery schema screenshot. Continue from [02 — semantic models and metrics](02_SEMANTIC_MODELS_AND_METRICS_COURSE.md); use [08 — connections](08_CONNECT_SEMANTIC_LAYER_TO_TOOLS.md) when publishing them.

## 1. Columns confirmed by the screenshot

The selected relation is `fei_rss_source_brz` in dataset `DBT_FEI_PROD`. The screenshot shows these nullable fields:

| Column | BigQuery type | Use |
|---|---|---|
| `Date_Published` | DATE | Existing semantic publication-day dimension |
| `Article_Title` | STRING | New title-length metric |
| `Content` | STRING | Body-length metrics |
| `Categories` | STRING | Existing dimension and missing-category logic |
| `URL` | STRING | Existing article entity and distinct counting |
| `Date` | STRING | Not used as an analytical date in these examples |

This is schema evidence, not evidence of current row values, uniqueness or metric results. Your latest YAML already defines four metrics; the four below extend that list to eight. These use the same embedded simple-metric format as your model. Confirm your runtime supports that format. [dbt simple metrics](https://docs.getdbt.com/docs/build/simple).

## 2. What the four new metrics calculate

| Metric | Formula over selected input rows | Useful question |
|---|---|---|
| `total_article_content_chars` | `SUM(LENGTH(Content))` | How much stored article content is in this selection? |
| `max_article_length` | `MAX(LENGTH(Content))` | What is the length of the longest stored article body? |
| `avg_article_title_length` | `AVG(LENGTH(Article_Title))` | How long are the headlines on average? |
| `articles_missing_categories` | Distinct non-null URLs on rows whose category is null or trims to empty | Which selection has uncategorized articles? |

For STRING columns, BigQuery `LENGTH` counts characters. Stored spaces, line breaks and markup count too; this is neither a word count nor a rendered-text measurement. [BigQuery string functions](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions).

## 3. Paste these entries into your existing metrics list

Append these four entries **inside the existing `fei_rss_source_brz.metrics` list**, immediately after `articles_published_selected_categories`. Keep your existing `metrics:` key and its four entries. The indentation below matches your supplied model:

```yaml
      - name: total_article_content_chars
        label: Total Article Content (chars)
        description: Sum of stored body character lengths across selected model rows.
        type: simple
        agg: sum
        expr: length(Content)

      - name: max_article_length
        label: Longest Article Length (chars)
        description: Maximum stored body character length across selected model rows.
        type: simple
        agg: max
        expr: length(Content)

      - name: avg_article_title_length
        label: Average Article Title Length (chars)
        description: Average stored title character length across selected model rows.
        type: simple
        agg: average
        expr: length(Article_Title)

      - name: articles_missing_categories
        label: Articles Missing Categories
        description: Distinct non-null URLs on rows with null, empty or whitespace-only categories.
        type: simple
        agg: count_distinct
        expr: |
          CASE
            WHEN Categories IS NULL OR TRIM(Categories) = '' THEN URL
            ELSE NULL
          END
```

The last expression returns URL for qualifying rows and NULL for the others; `count_distinct` counts only the qualifying non-null URLs. `TRIM` handles surrounding whitespace, including the line breaks shown in your earlier category sample. A non-empty `Bonds & Fixed Income` remains categorized. [BigQuery aggregate functions](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions).

The CASE expression belongs in `expr` and references physical columns. A semantic `filter` or command `--where` uses names such as `Dimension('article__categories')`. This distinction avoids your earlier dbt1005 error from `Dimension('Categories')`.

No new semantic dimension is required for these expressions. Arbitrary title filtering in a consuming tool would require a separately modeled dimension; calculating a title-length metric does not automatically expose a title filter.

The [complete example YAML](examples/rss-additional-metrics/fei_rss_source_brz.yml) includes your other two models, the original four RSS metrics and these four additions. It is a reference copy, not a second model declaration to add alongside the existing one. Merge into the real dbt project's current property file, or replace that file only if it matches the supplied content and has no other definitions to preserve.

## 4. Query and filter them

After saving the actual project changes, run the supported validation commands in your environment:

```shell
dbt parse
dbt sl validate
dbt sl query --metrics total_article_content_chars,max_article_length,avg_article_title_length,articles_missing_categories
```

All four inherit your `agg_time_dimension: date_published`. This defines the publication clock; it does not automatically restrict them to the last seven days. Your existing last-seven-days metric's filter is local to that metric.

For a category breakdown:

```shell
dbt sl query --metrics total_article_content_chars,max_article_length,avg_article_title_length --group-by article__categories
```

For Investing/Shares on 1–7 October inclusive:

```shell
dbt sl query --metrics total_article_content_chars,max_article_length,avg_article_title_length --where "{{ Dimension('article__categories') }} IN ('Investing', 'Shares') AND {{ TimeDimension('article__date_published', 'day') }} >= '2026-10-01' AND {{ TimeDimension('article__date_published', 'day') }} < '2026-10-08'"
```

For missing categories over that same date range, keep the query free of a selected-category condition:

```shell
dbt sl query --metrics articles_missing_categories --where "{{ TimeDimension('article__date_published', 'day') }} >= '2026-10-01' AND {{ TimeDimension('article__date_published', 'day') }} < '2026-10-08'"
```

A query filter for Investing/Shares removes uncategorized rows before the conditional count. It therefore returns zero for an ungrouped missing-category count on that selection; an empty grouped query may return no row. This metric is useful as a quality view with all categories, or with only a date filter.

## 5. Reconcile the calculations with SQL

Save the following as an analysis in the real dbt project. This expresses the four unfiltered formulas; MetricFlow's generated SQL can use a different query structure:

```sql
select
    sum(length(Content)) as total_article_content_chars,
    max(length(Content)) as max_article_length,
    avg(length(Article_Title)) as avg_article_title_length,
    count(distinct case
        when Categories is null or trim(Categories) = '' then URL
        else null
    end) as articles_missing_categories
from {{ ref('fei_rss_source_brz') }}
```

Apply equivalent WHERE/GROUP BY clauses when comparing a filtered/grouped semantic query. Use the actual model relation if running directly in BigQuery; a dbt `ref` is not raw BigQuery SQL.

### Synthetic arithmetic example

These invented rows illustrate the rules, not values from your table:

| URL | Content | Article_Title | Categories |
|---|---|---|---|
| A | `12345` | `ABC` | Investing |
| B | `1234567890` | `News` | NULL |
| B | `1234567890` | `News` | NULL |
| C | empty string | empty string | spaces/line breaks only |
| D | NULL | NULL | Shares |
| NULL | `zz` | `X` | empty string |

Results: total body length **27**, longest body **10**, average title length **12 / 5 = 2.4**, and missing-category distinct articles **2** (B and C).

The repeated B contributes twice to the sum and average but once to the distinct count. The null-URL row contributes its body/title lengths but cannot contribute to the article count. This follows your existing row-based length metric; `primary` entity metadata does not deduplicate rows. If your business definition requires one row per article, establish that grain upstream and reconcile all length metrics afterward.

## 6. Interpretation and publishing checks

- NULL bodies/titles are ignored by the length aggregates; an empty string contributes zero. Without explicit filling, SUM/MAX/AVG return NULL when there are no non-null inputs. An ungrouped distinct count returns zero when no qualifying non-null URL exists.
- Missing-category count means a URL has at least one qualifying row in the selection. If duplicate rows disagree on category, the same URL can appear both as categorized and uncategorized; the metric does not prove all its rows lack a category.
- Title average uses non-null title rows, not `articles_published` as a denominator. Do not average group averages to create a combined total.
- Maximum length gives a numeric length, not the associated title or URL. Retrieving the actual longest article needs a detail query.
- Query totals at the requested grain. Do not assume exported distinct counts can be summed across overlapping groups. See [guide 07](07_PUBLISH_TO_BUSINESS_USERS.md).
- After local validation/reconciliation, deploy the updated semantic artifacts so the tools in [guide 08](08_CONNECT_SEMANTIC_LAYER_TO_TOOLS.md) can discover the new metrics.

The definitions, YAML structure, local arithmetic and links were checked here. No live dbt parse, semantic query, warehouse SQL or deployment was executed.
