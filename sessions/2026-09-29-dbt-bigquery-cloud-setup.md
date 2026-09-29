# dbt Cloud and BigQuery setup and deployment

Date: 2026-09-29 (Australia/Sydney)

## Request and observed work

The user configured dbt Cloud project `TEST_ANALYTICS` against BigQuery project `fei-website-f16b0`, using a dedicated service account and Service Account JSON authentication. The conversation covered the distinction between service account JSON and Workload Identity Federation, dbt project versus Google Cloud project, BigQuery project/dataset/table versus dbt database/schema/model, and separate development and production datasets. The existing service account `dbt-fei-sa@fei-website-f16b0.iam.gserviceaccount.com` was visible in the user's screenshot. No key content was shared in this session.

The user created a dbt project `fei_dbt` with `Bronze`, `Silver`, and `Gold` model folders. `dbt_project.yml` configures matching folders but does not create them. The source is defined as `fei_sources.FEI_TRAFFIC_NAMED` in `sources.yml`, pointing to BigQuery table `fei-website-f16b0.FEI_ADMIN_PORTAL.FEI_TRAFFIC_NAMED`. A model initially sent bare `source(...)` to BigQuery, causing `Table-valued function not found: source`; changing it to `{{ source('fei_sources', 'FEI_TRAFFIC_NAMED') }}` resolved that issue.

A later run failed because dbt queried the source in US while the source dataset was in `australia-southeast1`. After the job location was corrected, the run failed because the old development dataset `dbt_mdelamettrie` was not found in that region. The user set their development credential Dataset to `dbt_fei_mdelamettrie`. A subsequent Studio `dbt build` was shown as successful.

The production environment `dbt_Prod_FEI` was configured with Service Account JSON and Dataset `DBT_FEI_PROD`. Its deploy job failed at `dbt deps` because dbt could not find `dbt_project.yml`. Screenshots established that the connected private Git repository `MatthieudeLaMettrie/dbt_cert` has `dbt_project.yml` at the **repository root** on `main`, while dbt Cloud's Project subdirectory was incorrectly set to `dbt_cert`. The user cleared that field and reported, “that was the issue.” The repository had a committed project initialization on `main`. The session did not include evidence of a completed production `dbt build` or resulting BigQuery object.

The user requested a Markdown or HTML record in `MDLM_CODEX_MEMORY` for these insights and future additions. Added the living guide at `dbt/DBT_BIGQUERY_CLOUD_GUIDE.md`, linked it from both READMEs, and updated durable memory.

Follow-up: the user asked to use Bronze, Silver, and Gold folders instead of staging, intermediate, and marts. Confirmed this is a valid dbt model layout and expanded the living guide with folder roles, `source()`/`ref()` flow, and the distinction between code folders and BigQuery datasets. The preference was recorded in durable memory.

Follow-up: the user asked to retain staging/intermediate/marts and `stg_`/`int_`/`dim_`/`fct_` terminology as well, and to explain how dbt Core reaches production. Added a side-by-side vocabulary map and a Core-only promotion/runner procedure, including an external `profiles.yml` example with separate `dev`/`prod` BigQuery targets. This is documentation, not a live Core deployment; no production runner was configured or executed.

## Decisions, limits, and next steps

- Develop and test in Studio, commit and sync code to the deployment branch, then run the production deploy job. Studio's Defer selector is not a production environment switch.
- Production job command: `dbt build`. Development single-model check: `dbt build --select fei_source_test`.
- Keep source and output datasets in the same BigQuery location for the view. Verify `DBT_FEI_PROD` exists in `australia-southeast1` and the service account can write to it.
- The user's GitHub screenshot showed `profiles.yml` in the repository. Its contents were not inspected. Check privately for embedded credentials and rotate any exposed key if found.
- Extend the living guide with dated observations and verified fixes as later work continues.

## Validation

Reviewed the user's screenshots and current dbt official documentation for BigQuery quickstart, model config, Studio, and deployment behavior. The guide records observed results and marks production completion as unverified. No dbt Cloud or BigQuery settings were modified by this task.
