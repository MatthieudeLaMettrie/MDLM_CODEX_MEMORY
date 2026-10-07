# 04 — Debugging workbook: attempt before explanation

Twenty original scenarios. These are reasoning exercises, not actual exam questions. Code has not been run against your warehouse. Each case supplies its own assumptions; do not assume an adapter unless stated. If information is insufficient, identify exactly what evidence you need rather than inventing it.

For each case, reply with **diagnosis → evidence → smallest appropriate fix → verification → confidence (low/medium/high)**. Answers are intentionally absent. In this task, ask for a small hint, a stronger hint, or the solution after your attempt.

## Initial diagnostic: Cases 1–3

Allow about ten minutes total without documentation. These repeat the diagnostic already offered in the task so it is preserved in your workbook.

### Case 1

`models/staging/stg_orders.sql` contains:

```sql
{{ config(materialized='view', alias='orders_clean') }}
select order_id, customer_id, amount
from {{ source('raw', 'orders') }}
```

A downstream model contains:

```sql
select * from {{ ref('orders_clean') }}
```

dbt reports a dependency on a node named `orders_clean` that was not found. `stg_orders` is enabled and the source declaration is valid. Diagnose and repair the problem.

### Case 2

Assume a `merge`-capable adapter, one source row per `order_id`, and a nonempty target:

```sql
{{ config(materialized='incremental',
          incremental_strategy='merge', unique_key='order_id') }}
select order_id, status, updated_at
from {{ source('raw', 'orders') }}
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

| Location | order_id | status | updated_at |
|---|---:|---|---|
| Target | 101 | pending | 09:00 |
| Target | 102 | paid | 10:00 |
| Source | 101 | cancelled | 09:30 |
| Source | 102 | paid | 10:00 |

All times are on the same date. The correction to order 101 arrived after the previous run. The next run succeeds, but the target remains unchanged. Propose an immediate repair and a recurring processing approach, with explicit assumptions.

### Case 3

The graph is `stg_orders → int_orders → fct_orders`. All three are table models, all dependencies use `ref()`, and the development schema is empty. Deferral is off.

```shell
dbt run --select fct_orders
```

The warehouse reports that `int_orders` does not exist. Explain the failure and give the command you would use to build the required scope.

## Further practice

Use these after the diagnostic. Attempt each before looking up its topic in the reference guide. Some scenarios test code correctness; others test whether you choose the right investigation.

### Case 4

This properties file fails to parse with a YAML indentation error:

```yaml
version: 2
models:
  - name: fct_payments
      columns:
      - name: payment_id
        data_tests:
          - unique
```

Give the corrected structure. What would you run first to check the repair, and what would that check still not prove?

### Case 5

The project's name is `learning_shop`. `models/staging/stg_payments.sql` has no inline `config()`, and no resource YAML overrides apply. You expect it to be a table, but it remains a view.

```yaml
name: learning_shop
models:
  learning_shops:
    staging:
      +materialized: table
```

Which evidence would you inspect, what would you change, and how would you confirm the resolved configuration?

### Case 6

During project parsing, this code fails while accessing `results.columns`:

```sql
{% set results = run_query('select 1 as category_id') %}
{% set category_ids = results.columns[0].values() %}

select {{ category_ids[0] }} as category_id
```

Explain why an apparently valid SQL query does not prevent the error. Propose a repair that also handles the later expression when parsing does not have query results.

### Case 7

`int_accounts.sql` references `fct_activity`, and `fct_activity.sql` references `int_accounts`. The run fails before any warehouse model is built, reporting a cycle. A colleague suggests increasing threads.

Explain whether that proposal can address the observed failure. Describe the design information needed to choose a correct repair; do not arbitrarily remove a dependency without explaining what replaces it.

### Case 8

The requirement is: every invoice must have a non-negative, non-null amount. A developer writes this singular data test:

```sql
select invoice_id, amount
from {{ ref('fct_invoices') }}
where amount >= 0
```

The data contains amounts `20`, `0`, `-5` and `NULL`, one row each. Under the default failure threshold, predict which rows the test returns and what result dbt reports. Repair the test to match the full requirement.

### Case 9

A generic test has this configuration:

```yaml
config:
  severity: warn
  error_if: '>10'
  warn_if: '>0'
```

It reports 25 failures, yet the result is a warning. No warning-escalation flag is enabled. The developer expected an error above ten failures. Diagnose the mismatch and state the outcomes you would check at 0, 1, 10 and 11 failures after the repair.

### Case 10

The requirement is that every order has a non-null customer ID that exists in `dim_customers`. The only configured assertion is:

```yaml
data_tests:
  - relationships:
      arguments:
        to: ref('dim_customers')
        field: customer_id
```

The relationships test passes, but some orders have a null `customer_id`. Existing non-null customer IDs all match. What requirement is not yet established, and what would you add and verify?

### Case 11

A SQL model joins `ref('stg_orders')` as `o` to `ref('stg_customers')` as `c`. A unit test supplies a fixture for `stg_orders` only. It fails during compilation with an input/node-related message before comparing expected rows. Both model references are valid and enabled.

What should you inspect in the unit-test definition? Describe the minimal fixtures and an edge case that would make the join logic meaningfully testable.

### Case 12

An incremental model's target table exists but contains zero rows. Its source contains ten rows with non-null timestamps. It uses a supported `merge` strategy and this incremental filter:

```sql
{% if is_incremental() %}
where modified_at > (select max(modified_at) from {{ this }})
{% endif %}
```

The run succeeds and inserts no rows. Explain the behavior and propose a repair. Include separate verification for an empty target and a target with existing data.

### Case 13

A merge-based incremental model is configured with `unique_key='payment_id'`. The incoming batch contains two different rows for `payment_id=7` with distinct update timestamps. The warehouse returns an error indicating multiple source rows match a target row. The source may legitimately contain several events for the same payment.

Identify what must be decided about model grain and event ordering. Explain why the key configuration alone does not settle that decision. State the checks you would perform before and after a repair.

### Case 14

A snapshot uses `strategy: timestamp`, `unique_key: customer_id` and `updated_at: modified_at`. Between observations, customer 42's status changes from `active` to `closed`, but `modified_at` remains unchanged. The next snapshot run succeeds and no new version is observed.

Diagnose the missing history. Propose a durable design correction and explain what can and cannot be recovered about changes that were never observed.

### Case 15

CI downloads the production `manifest.json` into `target/`, then runs:

```shell
dbt build --select 'state:modified+' --state target --target-path target
```

The comparison behaves unexpectedly. Describe the sequence of artifact reads/writes that concerns you, how you would change the paths, and how you would prove the baseline was preserved.

### Case 16

A production schedule runs only:

```shell
dbt build --select 'state:modified+' --state artifacts/previous
```

No code or relevant configuration has changed since the saved manifest. New source rows arrive every hour. The scheduled job completes without updating the expected marts.

What does the selector measure? Explain how you would separate code-change CI from the recurring data-processing requirement.

### Case 17

`fct_sessions` depends on `int_sessions`. A correct production manifest is available. Production `int_sessions` contains a new row, while the existing development `int_sessions` table does not. Only `fct_sessions` is selected:

```shell
dbt run --select fct_sessions --defer --state artifacts/production
```

The new row is absent from the result. The SQL applies no filter that would exclude it. What relation would you inspect, and what choices could make the run use the intended data? State any tradeoff or assumption.

### Case 18

`int_costs` belongs to the `finance` group and has `access: private`. A model in the `marketing` group references it. Parsing rejects the reference. Both models are in the same project, and the warehouse role can select the physical relation.

Explain the failure and propose a correction that respects the intended ownership boundary. What design decision is needed before changing access?

### Case 19

`dim_accounts` has an enforced contract declaring `account_id` and `account_name`. A code change replaces `account_name` with `legal_name`, while the contract and downstream consumers are unchanged. The build fails its contract check. The rename is an intentional interface change used by another team.

Give an immediate diagnosis and outline a migration approach. Explain how you would check pinned and unpinned consumers before changing the canonical version.

### Case 20

A model calls `dbt_utils.generate_surrogate_key(...)`. It works on a developer's machine. A fresh CI runner checks out the same project revision, then runs `dbt build` directly. `packages.yml` declares `dbt_utils`, but no package installation step ran and the dependency directory is absent. CI reports the package/macro as undefined.

Diagnose and repair the CI flow. Identify which files or version information you would preserve to make subsequent installs reproducible. What would you verify after installation besides the absence of the original error?

## Before requesting a solution

You do not need a perfect answer. A useful attempt can say: “I believe the failure occurs during compilation because…, I would inspect…, and I am unsure whether…”. That gives us enough evidence to teach the missing reasoning step. Simply naming a command without explaining why it tests your hypothesis is not yet a complete diagnosis.
