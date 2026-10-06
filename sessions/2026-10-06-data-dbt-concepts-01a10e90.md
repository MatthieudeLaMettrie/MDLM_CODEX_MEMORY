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

## Follow-up: simpler web explanation and automatic timestamps

User requested pushing to the same repository, an explanation of React/Next.js as if aged ten using the supplied freeCodeCamp article, and clarification on whether dbt automatically creates freshness timestamps or requires a timestamp column.

- Verified the initial guide was already on remote main at 733d2e7.
- Read the linked article (3 April 2023) and checked current primary React, Next.js and dbt documentation. Added the LEGO shop analogy and an exam-practice website example. Qualified the article's backend-only, React browser-only, always-faster SSR and built-in authentication claims.
- Clarified that freshness checks do not create source columns. The table need not contain a timestamp if supported metadata or an audit query provides one. A real time signal remains necessary.
- Added an explicit BigQuery table model using current_timestamp() as dbt_processed_at, explaining table/view/incremental timing and why a Friday transformation can stamp Monday's stale source rows as Friday. This measures processing rather than source arrival.
- Updated the existing guide and durable memory. SQL examples reviewed, not executed; no live warehouse or source schema changes made. Reviewed Git diff and whitespace before publishing the follow-up under standing authorization.

## Follow-up: concrete React and Next.js examples

User still did not understand the comparison and requested definitions, reasons for using each, and five very simple examples per tool. Interpreted “React vs React” as React versus Next.js from the immediate conversation context and stated the assumption.

Added a plain explanation that both are code tools, JavaScript is the language, React builds reusable interactive interfaces, and Next.js provides the surrounding website framework using React. Added exactly five React examples (like count, basket total, quiz feedback, local filtering, reused product cards) and five Next.js examples (page addresses, product routes, shared layout, prepared blog content, server-handled contact form). Explicitly explained overlap and developer responsibilities, avoiding an exclusive frontend/backend or browser/server split. Updated this same guide; no application code or live service changes. Reviewed the diff and whitespace before publication. No additional durable memory change needed.

## Follow-up: kitchen analogy

User asked to define React and Next.js using a kitchen analogy. Added React as reusable recipes/tools for assembling visible dishes, and Next.js as an organised restaurant kitchen using those React tools plus order routing, preparation and server work. Used a pizza customiser versus menu/order pages and order handling as the concrete example. Kept the developer as the cook and clarified the complementary roles. Documentation only; no durable memory change needed. Reviewed the diff and whitespace before committing and pushing the same guide and session note.

## Follow-up: React dashboard and Fabric Gold

User asked whether React could be the dashboard frontend with Fabric Warehouse Gold as backend, and whether the connection is just an API. Checked current official Fabric connectivity, GraphQL overview/setup/React authentication, Warehouse security and Power BI embedding documentation.

Added two architecture diagrams and a bounded sales-query/JSON example. Distinguished the analytical data store from the application API: browser-to-custom API uses HTTPS; custom server-to-Warehouse uses a SQL driver, TDS and Entra identity. Explained Fabric's managed GraphQL API as an alternative to writing a custom service, its SPA/PKCE user sign-in and permissions, optional Next.js server routes, and Power BI embedding. Recommended evaluating managed GraphQL for suitable read-only internal queries and a custom API for tailored metrics/caching/access rules. Not a user-approved implementation choice.

Kept application secrets server-side and explained that a shared service principal does not automatically convey each user's identity to the database. Advised Gold aggregates, bounded queries and data-as-of time. Updated the existing guide and memory; examples are conceptual, not executed. No Fabric workspace, Entra app, permissions or React app was created or changed. Diff and whitespace reviewed before publication.

## Follow-up: freshness placement and YAML layout

User requested more explanation of freshness: model SQL versus model YAML, all configuration locations, loaded_at_field selection, and per-model versus per-stage YAML best practice.

Checked current primary dbt freshness/source/model config and property references, v2 command/upgrade docs and staging structure guidance. Extended the existing guide with source YAML defaults/table overrides, source project defaults, v2 model YAML and SQL examples, config precedence, version boundaries, and view/ephemeral limitations. Distinguished age thresholds from build_after orchestration settings and file location from the resource being checked.

Explained loaded_at_field as an existing timestamp column/expression in the checked source/model, MAX-based age calculation, source/model renames, ingestion versus business clocks, and why freshness does not create columns. Recommended a hybrid growing-project layout: sources per source system, shared defaults in dbt_project.yml, model properties beside SQL; short folder/group files remain valid for the small learning project. No migration was selected by the user.

Updated durable memory and reviewed examples/diff/whitespace. Examples are documentation only, not compiled or warehouse-tested; the user's current runtime/adapter capabilities have not been inspected. No live dbt project, model or warehouse changes made. Publish guide and records under standing authorization.
