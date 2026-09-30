# dbt source freshness, quality, and documentation request

The user requested a new BigQuery source and then a freshness check, data-quality test, and generated documentation in dbt Cloud. The project-specific source identifiers, timestamp column, update cadence, and quality rule were requested but not yet supplied.

Read-only inspection of private `MatthieudeLaMettrie/dbt_cert` found `models/Bronze/sources.yml` on `main` and `MatthieudeLaMettrie-patch-1`, defining `fei_sources` over `fei-website-f16b0.FEI_ADMIN_PORTAL.FEI_TRAFFIC_NAMED`. The patch branch also has `models/Bronze/fei_source_test.yml` with `not_null` and `accepted_values` for `action`. This is an existing source, not necessarily the new one the user wants checked. No project files or dbt Cloud settings were changed.

Current dbt documentation places source freshness under `config.freshness`, with optional `config.loaded_at_field` or `loaded_at_query`. `dbt freshness` evaluates it; `dbt build` does not perform source freshness automatically. A project-specific timestamp and threshold are needed before adding an accurate rule. Next: get the intended project/dataset/table, freshness timestamp and cadence, quality column/rule; then update the correct branch, run parse/test/freshness as possible, and generate docs.
