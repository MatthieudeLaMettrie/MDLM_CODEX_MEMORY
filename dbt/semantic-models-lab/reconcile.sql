-- Replace PROJECT.DATASET with the actual DEVELOPMENT relation location.
-- Manual BigQuery queries, not dbt models.
select
    count(distinct article_url) as articles_published,
    avg(article_length_chars) as avg_article_length,
    sum(article_length_chars) as total_article_characters,
    count(article_length_chars) as articles_with_length,
    safe_divide(count(article_length_chars), count(distinct article_url)) as length_coverage
from `PROJECT.DATASET.fct_rss_articles_lab`;

select
    published_date,
    count(distinct article_url) as articles_published,
    avg(article_length_chars) as avg_article_length
from `PROJECT.DATASET.fct_rss_articles_lab`
group by published_date
order by published_date;

select
    publisher,
    count(distinct article_url) as articles_published,
    avg(article_length_chars) as avg_article_length,
    sum(article_length_chars) as total_article_characters,
    count(article_length_chars) as articles_with_length,
    safe_divide(count(article_length_chars), count(distinct article_url)) as length_coverage
from `PROJECT.DATASET.fct_rss_articles_lab`
group by publisher
order by publisher;
