# dbt: core concepts and troubleshooting

This guide targets the concepts relevant to the dbt Analytics Engineering exam currently listed as version 1.11. All examples are original teaching examples unless stated otherwise. They are not actual exam questions or warehouse-tested labs. Live source pages may include later features; read their version notes.

## 1. Understand the work before choosing a command

A dbt project combines transformation code, resource definitions, configuration and a dependency graph. SQL models describe a result set. Materializations decide how that result is represented in the warehouse. The adapter implements warehouse-specific behavior.

Keep four questions separate: What does the project define? Which resources did the command select? What relations does the compiled SQL refer to? What did the warehouse actually execute? Many debugging mistakes come from answering one of these questions with evidence about another.

| Stage | Evidence to inspect | What success establishes |
|---|---|---|
| Configuration and connection | Project/profile settings, selected target, connection error | The chosen environment is usable; it does not establish model correctness |
| Parsing and graph construction | YAML/Jinja errors, resource names, dependency messages | dbt can understand the project structure |
| Compilation | Rendered SQL and evaluated configuration | You can see what Jinja and relation references became |
| Materialization/execution | Executed SQL, adapter error, query history | The warehouse accepted the operation |
| Validation | Test results, business reconciliations, sample records | Specific assertions hold for the observed data |

An error's position in the log matters. A model downstream of a failing resource may be skipped without having a defect of its own. A successful SQL execution can still produce the wrong grain, omit late data, or multiply measures through a join.

For a failure, record the exact command, dbt and adapter versions, target, first relevant error, named resource and recent change. Classify the stage. Form a hypothesis that explains those observations. Choose one small investigation to disprove it. Change the original project file, then rerun the affected scope and a correctness check. Preserve useful evidence before another command overwrites artifacts.

Sources: [Debugging guide](https://docs.getdbt.com/guides/debug-errors), [dbt debug](https://docs.getdbt.com/reference/commands/debug), [dbt compile](https://docs.getdbt.com/reference/commands/compile).

## 2. Know which identity a name refers to

A resource has a dbt identity and can have a different warehouse identifier. `ref()` resolves a dbt model, seed or snapshot, contributes a dependency, and renders an environment-appropriate relation. An `alias` changes the warehouse identifier. It does not rename the resource used to identify a model in the project.

`source()` refers to a declared external input. Its arguments use the logical source and table names in YAML. `database`, `schema` and `identifier` map that declaration to the actual warehouse object. Declaring a source does not ingest or create its data.

```yaml
version: 2
sources:
  - name: commerce
    database: raw
    schema: app_public
    tables:
      - name: payments
        identifier: payment_events
```

```sql
select payment_id, amount
from {{ source('commerce', 'payments') }}
```

This declaration separates the name used in dbt code from the physical input table. During debugging, inspect the rendered relation rather than assuming it shares a name with the YAML declaration. Also check quoting and the role used by the run.

Hard-coding `production.some_schema.some_table` in a model can bypass environment-aware resolution and omit dependency information. A query that works in a SQL editor may use a different role, database, schema or existing object from the dbt run.

Sources: [ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref), [source](https://docs.getdbt.com/reference/dbt-jinja-functions/source), [source declarations](https://docs.getdbt.com/docs/build/sources), [alias](https://docs.getdbt.com/reference/resource-configs/alias).

## 3. Configuration, structure and model grain

Properties describe resources; configurations also control their behavior. Resource YAML can contain descriptions, columns, tests and a `config` section. `dbt_project.yml` can apply configurations across resources using their project/path hierarchy. SQL models can set configurations with `config()`.

When a model behaves unexpectedly, inspect all relevant configuration locations and its resolved configuration in the manifest. A setting written under the wrong project name or directory can look plausible while applying to no model. Also distinguish the profile name from the target name: the profile selects a connection configuration, and the target selects an output within it.

```yaml
name: learning_shop
version: '1.0'
config-version: 2
profile: learning_shop
model-paths: ['models']

models:
  learning_shop:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

This example establishes directory defaults; inspect more specific settings before predicting any particular model's materialization.

Before writing a transformation, state its grain in one sentence: for example, one row per payment, per customer, or per customer per day. Every join and aggregation must preserve or intentionally change that grain. An unexpectedly large result is often a relationship problem rather than a dbt configuration problem.

To investigate a join, count rows and distinct keys on each side before joining. Check whether the proposed key is unique on the expected side. Inspect a single duplicated key and trace its matching rows. Compare totals before and after the join. `distinct` is not evidence that the intended grain has been restored: it may hide duplicates without correcting measure inflation.

Source: [Configurations and properties](https://docs.getdbt.com/reference/configs-and-properties). The grain investigation is a general SQL debugging method used throughout this guide.

## 4. Materializations are operational choices

| Choice | What persists | Reason to use it | Question to ask when it fails |
|---|---|---|---|
| View | A query definition | Lightweight transformations and reuse | Is an expensive chain being recomputed at query time? |
| Table | A stored result rebuilt on a run | Faster consumption of expensive transformations | Has the model been rebuilt since the relevant input changed? |
| Incremental | A table updated using selected input and a strategy | Reduce repeated work for large datasets | Were the right rows selected and applied correctly? |
| Ephemeral | No separately queryable relation; logic is compiled into consumers | Small reusable intermediate logic | Are you expecting a physical table that should not exist? |
| Materialized view | A warehouse-managed object, where supported | Let the platform manage supported refresh behavior | Does this adapter/platform support the materialization and refresh settings? |

Do not choose an incremental model solely because it sounds faster. First establish correctness with a simpler full transformation, identify the expensive work, and define how updates, late arrivals and deletions should behave.

An ephemeral dependency is handled during compilation; a physical table dependency needs an existing relation or a build/deferral plan. This difference matters when reasoning about a clean development schema.

Seeds suit small, version-controlled reference inputs. They are a different resource type from models. Snapshots preserve observed historical versions of mutable records; an ordinary incremental table often represents a current or accumulated dataset instead. Avoid treating those two persistence goals as interchangeable.

Sources: [Materializations](https://docs.getdbt.com/docs/build/materializations), [Snapshots](https://docs.getdbt.com/docs/build/snapshots). Review adapter-specific support before choosing warehouse-managed materializations.

## 5. Reason about incremental correctness in three steps

An incremental model has three distinct decisions:

1. **Selection:** Which source records are included on this run?
2. **Matching:** Which existing target records correspond to those inputs?
3. **Application:** Does the selected strategy append, merge, replace partitions, or do something else?

Correct matching cannot repair a selection rule that excludes a needed record. A `unique_key` is matching configuration, not an automatic uniqueness test or a guarantee that incoming data is deduplicated. Validate the key and its null behavior separately.

`is_incremental()` is true when the model is configured as incremental, its target already exists as a table, and a full refresh is not being requested. Both branches of the model SQL must be valid. The first build and a later incremental run therefore exercise different paths.

For every incremental model, design fixtures for a first run, an unchanged rerun, a new record, a changed existing record, a late arrival, a boundary timestamp, a null timestamp, and an empty existing target. Add deletion and schema-change fixtures when they matter to the business requirement.

An empty target deserves attention: `max(timestamp_column)` can be null. In SQL, comparisons with null do not evaluate to true. A table can exist and still contain no rows, so target existence alone does not establish that a timestamp filter has a usable bound.

Late-arrival handling needs a documented lateness assumption. A bounded reprocessing window only covers changes inside that window. An ingestion timestamp or change feed may provide a different guarantee from event time. Choose a method that matches the source system's behavior, then verify it with known changes rather than relying on a successful run status.

Incremental strategies vary by adapter. Specify the strategy in a scenario before predicting its exact behavior. A source filter and an `incremental_predicates` target-scan restriction are not interchangeable. Reducing the range of possible target matches may improve performance but can change matching behavior if a relevant old record lies outside that range.

Schema evolution is also distinct from historical recalculation. Adding a new output column or changing an expression does not necessarily recompute old rows. `on_schema_change` handles aspects of target schema changes; it is not a general backfill of historical values. Decide whether a targeted repair or a rebuild is needed and assess downstream effects.

A strong verification compares the incremental result with a trusted full transformation over a small fixture. Check keys, affected values and aggregates; row count alone can miss a changed value or one missing row balanced by one duplicate.

Sources: [Incremental models](https://docs.getdbt.com/docs/build/incremental-models), [Incremental strategies](https://docs.getdbt.com/docs/build/incremental-strategy), [unique_key](https://docs.getdbt.com/reference/resource-configs/unique_key).

## 6. Snapshots: history has different rules

Snapshots implement a history of observed changes, typically as type-2 slowly changing dimensions. The configured key identifies the business record; multiple historical versions of that key are expected. A test asserting uniqueness of the business key across the entire snapshot history would conflict with that purpose.

The timestamp strategy relies on a trustworthy update timestamp. The check strategy compares configured columns. Timestamp is usually easier to maintain when an appropriate timestamp exists, but its correctness still depends on that timestamp advancing when relevant changes occur.

Each snapshot run observes the source at that point in time. If a value changes twice between observations, the intermediate state may never be captured. Increasing run frequency can reduce that gap; it cannot reconstruct unobserved history by itself.

YAML snapshot definitions are supported from 1.9 and are relevant to a 1.11 learning path. Current docs also contain later features; for example, inspecting snapshots through `dbt compile` is marked as a 1.12 addition. Do not assume every current snapshot command example applies to 1.11.

Before changing snapshot logic, inspect the key, strategy, current-row indicator and hard-delete configuration. Verify with a sequence of observations: initial state, one changed record, unchanged rerun, and a deletion if configured. Preserve the historical table when investigating; rebuilding only from current source data cannot recover missing history.

Source: [Snapshots](https://docs.getdbt.com/docs/build/snapshots).

## 7. Use tests to express the actual requirement

Data tests operate on data resources. A singular test is a SQL query that returns violating rows. A generic test is reusable SQL parameterized by a model, column or other arguments. Built-in generic tests include `not_null`, `unique`, `accepted_values` and `relationships`.

Unit tests exercise SQL model logic using controlled inputs and expected outputs. Use them for branching logic, joins, boundary dates and previously reported bugs. Passing a fixture test does not establish that today's production data satisfies a separate data-quality assertion.

```yaml
version: 2
models:
  - name: fct_payments
    columns:
      - name: payment_id
        data_tests:
          - not_null
          - unique
      - name: status
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['settled', 'reversed']
```

The `arguments` nesting shown above is supported in 1.11; current documentation identifies its availability from 1.10.5. Keep arguments separate from test `config` such as severity or thresholds.

Before implementing a test, write the allowed and disallowed cases in plain language. Consider nulls explicitly. Under SQL's three-valued logic, a comparison such as `amount < 0` does not select null amounts. Whether null should be allowed is a separate business decision that must be represented in the assertions.

For example, this original singular test enforces that a reported settled amount must be present and non-negative:

```sql
select payment_id, settled_amount
from {{ ref('fct_payments') }}
where settled_amount is null or settled_amount < 0
```

Under the normal nonzero-failure threshold, any returned record fails the assertion. More generally, test outcomes depend on `severity`, `error_if`, `warn_if` and possibly a custom failure calculation. For `severity: error`, the error condition is checked before the warning condition. For `severity: warn`, the error condition is skipped. Global warning escalation can still turn a warning into an error.

In `dbt build`, tests participate in dependency ordering. A relevant upstream test error can prevent downstream work. Unit tests occur before a model is materialized; its data tests follow materialization. Multi-parent tests and indirect selection introduce additional selection rules, so inspect the actual selection rather than assuming a model name implies a particular set of tests.

Test the test: include at least one known violating row in a small fixture and show that the assertion catches it. A test returning zero rows because it queried an empty relation may provide little evidence about the intended business rule.

Sources: [Data tests](https://docs.getdbt.com/docs/build/data-tests), [Unit tests](https://docs.getdbt.com/docs/build/unit-tests), [Test severity](https://docs.getdbt.com/reference/resource-configs/severity), [Build ordering](https://docs.getdbt.com/reference/commands/build).

## 8. Source freshness measures a different property

For the 1.11 workflow, use `dbt source freshness` for configured source freshness checks. `dbt test` and a successful model build do not by themselves establish that input data arrived on time. Current v2 documentation adds a broader top-level freshness command; do not substitute it blindly into a 1.11 exercise.

```yaml
version: 2
sources:
  - name: commerce
    config:
      loaded_at_field: ingested_at
      freshness:
        warn_after: {count: 2, period: hour}
        error_after: {count: 4, period: hour}
    tables:
      - name: payments
```

Investigate the selected source, inherited/table-specific configuration, timestamp meaning, timezone and maximum loaded timestamp. A freshness filter changes the freshness query's scanned records; it does not automatically change downstream model logic.

Freshness is not completeness. One recently loaded row can coexist with many missing expected rows. Combine freshness with volume or reconciliation checks when those are part of the requirement.

Sources: [Freshness configuration](https://docs.getdbt.com/reference/resource-configs/freshness), [Source command](https://docs.getdbt.com/reference/commands/source).

## 9. Jinja and SQL are two stages of reasoning

Jinja produces text and metadata that dbt uses to prepare warehouse work. SQL is then interpreted by the warehouse. A valid Jinja template can produce invalid SQL. A SQL syntax error may refer to a line in the generated query rather than the same line number in the source model.

Read the original and rendered model side by side. Check commas generated by loops, empty lists, quoting, branches and fully qualified relations. Make lasting repairs in the source model or macro, not an output file under `target/`.

During parsing, `execute` is false and warehouse query results are unavailable. Code that immediately dereferences a result from `run_query()` can fail at this stage. Guard logic requiring returned data, and provide a sensible parse-time fallback so dependency discovery and SQL generation remain coherent.

`execute` is not equivalent to “this command is materializing my model.” Compilation with a connection can evaluate `run_query()` and other introspective logic. Therefore `dbt compile` is not universally offline or free of side effects from user-written macros. `dbt parse` is the appropriate starting point when the goal is project parsing without warehouse execution.

Keep dependencies discoverable during parsing. A `ref()` hidden in an execution-only branch can require an explicit dependency declaration. A Jinja comment is removed by Jinja; it is not the same as a SQL comment containing an evaluated Jinja `ref()`.

For a macro, ask three questions: what arguments does it expect, what does it return or emit, and when does it execute? Inspect the generated text before treating the macro's name as evidence of its behavior.

Sources: [execute](https://docs.getdbt.com/reference/dbt-jinja-functions/execute), [run_query](https://docs.getdbt.com/reference/dbt-jinja-functions/run_query), [Dependency discovery with ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref), [Compilation](https://docs.getdbt.com/reference/commands/compile).

## 10. Choose the command and selection independently

| Command | Main purpose in this learning path |
|---|---|
| `dbt debug` | Check configuration/connection; different from the `--debug` logging flag |
| `dbt parse` | Parse the project and its graph |
| `dbt ls --select ...` | Inspect which resources match a selector |
| `dbt compile --select ...` | Inspect rendered SQL |
| `dbt run --select ...` | Materialize selected models |
| `dbt test --select ...` | Execute selected tests |
| `dbt seed` | Load seed resources |
| `dbt snapshot` | Run snapshot resources |
| `dbt build --select ...` | Build and test selected supported resources in dependency order |
| `dbt source freshness` | Evaluate configured source freshness in the 1.11 workflow |
| `dbt deps` | Install declared dbt package dependencies |

Selection describes a set of resources; it does not replace the command's resource-type behavior. A selected seed is not loaded by pretending it is a SQL model under `dbt run`.

| Selector | Meaning |
|---|---|
| `model_a` | The named resource |
| `+model_a` | It and its ancestors |
| `model_a+` | It and its descendants |
| `+model_a+` | It, ancestors and descendants |
| `1+model_a` | It and one level of parents |
| `@model_a` | It, its descendants, and the ancestors needed by those descendants |
| `tag:finance tag:daily` | Union of the two selections |
| `tag:finance,tag:daily` | Intersection of the two selections |

Quote combined selectors so the shell does not interfere. Predict the selected set on paper, then compare with `dbt ls`. In an empty schema, draw any additional parents required by selected downstream models. A dependency declared with `ref()` gives ordering information; it does not automatically mean every ancestor is selected by every command.

Sources: [Graph operators](https://docs.getdbt.com/reference/node-selection/graph-operators), [Set operators](https://docs.getdbt.com/reference/node-selection/set-operators), [Build](https://docs.getdbt.com/reference/commands/build), [Debug](https://docs.getdbt.com/reference/commands/debug).

## 11. State comparison and deferral solve different problems

State comparison asks which project resources differ from a saved manifest. Deferral asks where an eligible unselected upstream reference should resolve. You can use both together, but neither is a substitute for the other.

```shell
dbt ls --select "state:modified+" --state artifacts/production
dbt build --select "state:modified+" --defer --state artifacts/production
```

These example paths assume an independently saved production manifest. Keep the comparison directory separate from the current run's output path. Otherwise parsing can overwrite the baseline you intended to compare against.

For ordinary model references, deferral applies to an unselected node when the relation does not exist in the current environment, or when `--favor-state` is used. Selected nodes remain part of the current execution. Ephemeral models are not deferred as physical relations.

Consequently, an existing development relation can matter even when deferral is enabled. Inspect the actual rendered relation. Also check whether a multi-parent test joins development data with production data: mismatched filtering or sampling can create unexpected results across environments.

`state:modified` compares project definitions and relevant configuration, not new business records arriving in source tables. It is useful for code-change CI. Using it alone as a daily ingestion schedule can leave outputs stale when source data changes without a code change.

State behavior also has caveats for macro changes, large seeds, and variable-driven logic. Treat a saved manifest as an artifact with provenance: record the project revision, environment, dbt version and invocation that produced it. A manifest does not copy warehouse data or grant read access to referenced production relations.

Sources: [State](https://docs.getdbt.com/reference/node-selection/state-selection), [Defer](https://docs.getdbt.com/reference/node-selection/defer), [State comparison caveats](https://docs.getdbt.com/reference/node-selection/state-comparison-caveats).

## 12. Governance protects interfaces

A model contract specifies an expected output structure. With enforcement enabled, column names and data types must match the declared interface. Platform constraints may add guarantees, but support and enforcement differ by adapter and constraint type.

A structural contract does not prove that revenue is calculated correctly. Business meaning still needs tests, ownership, descriptions and consumer review. Changing a calculation without changing its column name/type can pass a contract while breaking a business expectation.

Model groups establish ownership boundaries. `private` models are referenceable within their group; `protected` models are accessible within the project (and the documented package context); `public` models expose an interface for broader references where supported. These settings govern dbt references. They are not substitutes for warehouse grants or user permissions.

Model versions help manage intentional interface changes. A pinned `ref('dim_account', version=1)` targets that version. An unpinned reference resolves to the configured latest version. Before changing `latest_version`, consider which consumers are pinned, which follow latest, and how they will migrate.

When a governance-related failure occurs, check the actual access boundary, materialization support, declared columns/types and referenced model version. Do not assume a warehouse permission change resolves a dbt parsing error about a private model.

Sources: [Contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts), [Model access](https://docs.getdbt.com/docs/mesh/govern/model-access), [Model versions](https://docs.getdbt.com/docs/mesh/govern/model-versions), [Versioned ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref).

## 13. Dependencies and reproducible environments

A dbt package is a dbt project whose resources can be incorporated into yours. That differs from a Python package, an adapter installation and a cross-project dependency on an already-managed public model.

When a macro works on a laptop but is undefined in CI, check the declared package, resolved version, installed dependencies, namespace and checkout revision. Inspect the installation step before editing the macro call at random.

`package-lock.yml` records resolved package versions. Committing it supports consistent installs. `dbt deps` normally honors an unchanged lock; `dbt deps --upgrade` intentionally resolves updates. A successful upgrade is not evidence that every changed macro still behaves the same way for your project.

`packages.yml` supports package declarations, including configurations using Jinja. `dependencies.yml` can express project dependencies and supported package declarations but has restrictions around dynamic configuration. Read the relevant workflow rather than renaming the file solely for consistency.

For a dependency change, review the package's compatibility guidance and changed behavior, install in development, compile affected consumers and validate their outputs. Record both dbt and adapter versions when comparing environments.

Sources: [Packages](https://docs.getdbt.com/docs/build/packages), [deps and lock files](https://docs.getdbt.com/reference/commands/deps).

## 14. Diagnose jobs with artifacts and environment evidence

CI asks whether a proposed code change works in an isolated setting. A production job also has to process the intended data on the required schedule. A green CI check does not prove that production credentials, input timing or every production branch of incremental logic will behave identically.

| Evidence | Useful question |
|---|---|
| `manifest.json` | Which resources, dependencies, configs and paths did dbt understand? |
| `run_results.json` | What statuses, timings and messages were recorded for this invocation? |
| `target/compiled/` | What did the model's Jinja render into? |
| `target/run/` and logs | What materialization or supporting SQL was executed? |
| Warehouse query history | Was time spent executing, queuing, scanning, spilling or waiting? |
| Freshness results | How recent was the configured source load timestamp? |

Use `unique_id` to connect run results to resource definitions in the manifest. Preserve artifacts for the same invocation; mixing files from different runs can produce misleading diagnoses. A current manifest contains project information beyond the resources selected by a particular run, so it is not itself an execution success report.

For a slow job, measure first. Find the critical path and slow nodes. Distinguish connection/setup time, compilation, warehouse queueing and execution. Examine expensive joins, scans, repeated transformations and materialization choices. Increase threads only after considering dependency parallelism and warehouse capacity; more threads cannot remove a serial dependency chain.

For a failed job, repair the earliest relevant failure, identify what was skipped, and rerun a scope that restores the intended outputs and validation. Explain why a rerun is safe under the model's logic and current input state; avoid assuming every custom hook or incremental strategy is idempotent.

Sources: [Manifest](https://docs.getdbt.com/reference/artifacts/manifest-json), [Run results](https://docs.getdbt.com/reference/artifacts/run-results-json), [Debugging](https://docs.getdbt.com/guides/debug-errors), [CI workflow](https://docs.getdbt.com/docs/deploy/continuous-integration).

## 15. Explain these distinctions without looking them up

You should be able to distinguish parse from compile, model identity from alias, a source from a model, `run` from `build`, a test failure from a warehouse error, selection from dependency ordering, state comparison from data-change detection, deferral from copying data, a contract from a business assertion, and incremental updates from snapshot history.

For each distinction, invent a small example, predict a command's behavior, identify the evidence that would confirm it, and describe a realistic failure. Then attempt the workbook. If you can state a definition but cannot make those predictions, that topic still needs practice.
