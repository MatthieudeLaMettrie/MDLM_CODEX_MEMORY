{{ config(materialized='table') }}

select
    cast(article_url as string) as article_url,
    cast(published_date as date) as published_date,
    cast(publisher as string) as publisher,
    cast(language as string) as language,
    cast(article_length_chars as int64) as article_length_chars
from {{ ref('rss_articles_lab') }}
