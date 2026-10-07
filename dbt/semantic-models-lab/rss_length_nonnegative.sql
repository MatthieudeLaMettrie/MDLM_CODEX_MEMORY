-- A singular dbt data test: returning any row fails the test.
-- NULL is allowed by the metric contract; negative values are not.
select article_url, article_length_chars
from {{ ref('fct_rss_articles_lab') }}
where article_length_chars < 0
