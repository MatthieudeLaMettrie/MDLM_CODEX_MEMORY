# Data and dbt concepts explained

Date: 2026-10-06 (Australia/Sydney)
Task identifier: 01a10e90-69e7-7212-a132-a2f1bff48763

## Request

Explain through use cases and appropriate diagrams: indexing versus partitioning versus clustering and column selection; full versus cross join; Next.js versus React; dbt incremental strategies and when to use them; dbt freshness configuration, field choice and alternatives without timestamps.

## Work and decisions

- Read MEMORY.md, the three most recent session notes, AGENTS.md and repository state. Working tree was clean on main.
- Checked official PostgreSQL, BigQuery, Snowflake, React, Next.js and dbt documentation.
- Used the visualization skill's static Mermaid guidance. No interactive artifact was necessary for these structural diagrams.
- Created guides/data-engineering/DATA_AND_DBT_CONCEPTS_GUIDE.md, linked it from README.md and added its availability to durable memory.
- Used orders/customers/events as consistent examples and separated physical layout columns, change detection, row matching, event windows and freshness clocks.
- Highlighted Snowflake insert_overwrite's whole-table replacement, unlike BigQuery partition replacement; merge uniqueness and deletion limitations; full join duplicate multiplication; server/client rendering distinctions; dbt v1 versus v2 freshness commands.
- Covered timestamp-free alternatives: ingestion instrumentation, supported warehouse metadata with its caveats, successful-load audit queries and the limits of counts/checksums.

## Validation and limits

Reviewed authored SQL/YAML, join outputs, diagram structure, links and Git diff. Examples are illustrative and have not been compiled in a dbt project or executed against a warehouse. No user's live database, dbt version/adapter or website was inspected or changed. Current dbt documentation includes v2 features; the guide labels version boundaries and preserves v1 source examples.

## Publication and next steps

Publish only the guide, README link, memory update and this session note to current main under standing authorization. Git output and the final response provide publication evidence. Future exercises can be tailored to the user's actual adapter and installed dbt version; no clarification is required for this conceptual explanation.

Initial push was rejected because remote main had advanced. Fetched remote history, reread updated memory and the three latest prior notes, and rebased the unpublished commit onto it. Resolved README/MEMORY conflicts by retaining remote additions and adding this guide; adopted the remote guides/data-engineering folder organization. No concurrent work was discarded.
