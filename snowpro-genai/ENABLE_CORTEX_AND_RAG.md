# Enable Cortex AI and build a RAG lab

Checked against Snowflake documentation on 2026-09-25. This practical companion to the [GES-C02 study guide](STUDY_GUIDE.md) uses instructional SQL templates. Replace account-specific names and recheck current documentation. No Snowflake account was available to run these examples.

## Account, billing, and access

Snowflake's [AI pricing page](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing) describes consumption charges; it does not list a separate general Cortex AI Functions subscription to activate. On a **self-service trial**, however, AI features are disabled by default. Adding a credit card in Snowsight **Admin → Billing** enables them without ending or upgrading the trial. A suspended trial needs reactivation/upgrade before queries can run. [Trial-account rules](https://docs.snowflake.com/en/user-guide/admin-trial-account)

Check the access path in order:

1. **Active account and supported region/model.** Inspect the effective `CORTEX_ENABLED_CROSS_REGION` value. Cross-region inference may send inference payloads outside the home region, so routing is a data-residency decision. [Cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)
2. **Function privilege.** The caller needs `USE AI FUNCTIONS ON ACCOUNT` or the specific `USE AI FUNCTION <name> ON ACCOUNT` privilege.
3. **Snowflake database role.** The caller also needs `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.AI_FUNCTIONS_USER` for scalar AI functions. `AI_FUNCTIONS_USER` excludes `AI_AGG` and `AI_SUMMARIZE_AGG`; the [privilege page](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access) notes an aggregate-function exception, so check it for that grant design.
4. **Model entitlement.** A permitted model via model RBAC or the legacy allowlist fallback, plus regional availability. Model names and roles change.
5. **Ordinary access.** `USAGE` on the selected warehouse/database/schema, plus table, stage, file, or product-object access as needed.

The blanket `USE AI FUNCTIONS` and `SNOWFLAKE.CORTEX_USER` are documented as granted to `PUBLIC` by default. A new restricted role cannot isolate access while users inherit these broad grants. An administrator must review existing users and workloads before any account-wide revocation. Per-function and blanket grants have an **OR** relationship: revoking a per-function grant does nothing if the blanket grant remains. [Function privileges](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access)

### Inspect before changing access

```sql
SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE();
SHOW GRANTS TO ROLE PUBLIC;
SHOW GRANTS TO ROLE <your_role>;
SHOW PARAMETERS LIKE 'CORTEX_ENABLED_CROSS_REGION' IN ACCOUNT;
SHOW APPLICATION ROLES LIKE 'CORTEX-MODEL%' IN APPLICATION SNOWFLAKE;
-- ACCOUNTADMIN can audit the default all-model bootstrap:
SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC;
```

Review inherited roles as well as direct grants. The all-model bootstrap may come through application role `SNOWFLAKE.PUBLIC`, distinct from account role `PUBLIC`. Current Snowflake docs call `CORTEX_MODELS_ALLOWLIST` legacy and say only setting it to `'None'` is permitted from August 2026. Model RBAC is the forward path; removing the bootstrap requires Snowflake's documented stored procedure, not a raw revoke from account `PUBLIC`. `ACCOUNTADMIN` can bypass model restrictions, so verify with a non-admin role and `USE SECONDARY ROLES NONE`. [Model RBAC and bootstrap](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access#control-model-access)

### Example dedicated scalar-function role

An `ACCOUNTADMIN` can adapt this after `GENAI_WH` and `GENAI_LAB.PUBLIC` exist. Replace `<learner_user>` and object names. This limits the role's **direct** grants; it only limits effective AI access if broad inherited grants have been removed as part of an account-wide policy.

```sql
USE ROLE ACCOUNTADMIN;
CREATE ROLE IF NOT EXISTS GENAI_FUNCTION_LAB;
GRANT USE AI FUNCTION AI_TRANSLATE ON ACCOUNT TO ROLE GENAI_FUNCTION_LAB;
GRANT USE AI FUNCTION AI_COMPLETE ON ACCOUNT TO ROLE GENAI_FUNCTION_LAB;
GRANT DATABASE ROLE SNOWFLAKE.AI_FUNCTIONS_USER TO ROLE GENAI_FUNCTION_LAB;
GRANT USAGE ON WAREHOUSE GENAI_WH TO ROLE GENAI_FUNCTION_LAB;
GRANT USAGE ON DATABASE GENAI_LAB TO ROLE GENAI_FUNCTION_LAB;
GRANT USAGE ON SCHEMA GENAI_LAB.PUBLIC TO ROLE GENAI_FUNCTION_LAB;
GRANT ROLE GENAI_FUNCTION_LAB TO USER <learner_user>;
```

If model RBAC is restricted, grant a model application role that appears in `SHOW APPLICATION ROLES`, for example `GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-LLAMA3.1-70B" TO ROLE GENAI_FUNCTION_LAB;` when that model is supported. Then test with the learner's role:

```sql
USE SECONDARY ROLES NONE;
USE ROLE GENAI_FUNCTION_LAB;
USE WAREHOUSE GENAI_WH;
SELECT AI_TRANSLATE('Bonjour', '', 'en');
-- Choose a model actually available to this role and region.
SELECT AI_COMPLETE('llama3.1-70b', 'Explain RAG in one sentence.');
```

The empty **source-language argument** triggers detection in `AI_TRANSLATE`; the function still takes three arguments. [AI_TRANSLATE reference](https://docs.snowflake.com/en/sql-reference/functions/ai_translate)

### Other feature gates

| Feature | Additional setup and roles |
| --- | --- |
| Cortex Search | Creator of a managed-embedding service: `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.CORTEX_EMBED_USER`, schema `CREATE CORTEX SEARCH SERVICE`, source `SELECT`, refresh warehouse `USAGE`, and required change tracking. Consumer: service and containing database/schema `USAGE`. [Search privileges](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#required-privileges) |
| Cortex Analyst | Confirm `ENABLE_CORTEX_ANALYST = TRUE`; if it is `FALSE`, `ACCOUNTADMIN` can set it to `TRUE` under account policy. The caller needs `SNOWFLAKE.CORTEX_ANALYST_USER` or broader `CORTEX_USER`, plus the governed semantic resource/data and warehouse access for generated SQL. Check the [Analyst access guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst) and [feature controls](https://docs.snowflake.com/en/user-guide/snowflake-cortex/opting-out). |
| Cortex Agents | `SNOWFLAKE.CORTEX_AGENT_USER` or broader `CORTEX_USER`; schema `CREATE AGENT` for creators. The **user's default role and default warehouse**, plus Agent/database/schema and tool privileges, govern calls; an active worksheet role alone is insufficient. [Agent access](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup) |
| Fine-tuning | Separate schema `CREATE MODEL`, training requirements, and training/inference costs. [Fine-tuning](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-finetuning) |

For Analyst specifically, inspect the account setting first. If it is disabled and the administrator approves access, the documented account parameter can be set to `TRUE`; grant its narrower database role to a user-facing account role:

```sql
SHOW PARAMETERS LIKE 'ENABLE_CORTEX_ANALYST' IN ACCOUNT;
-- ACCOUNTADMIN, only if the feature is disabled and approved:
ALTER ACCOUNT SET ENABLE_CORTEX_ANALYST = TRUE;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_ANALYST_USER TO ROLE <analyst_role>;
```

For governance, approve model/region access and data classification; limit table, stage, Search, and Agent privileges; inspect `PUBLIC` inheritance; and monitor spend. [Budgets, shared resource budgets, and per-user quotas](https://docs.snowflake.com/en/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) differ by feature. Quotas can block per-user use shortly after a limit; budgets are evaluated periodically and are not instantaneous hard caps. Check the [pricing page](https://docs.snowflake.com/en/user-guide/snowflake-cortex/pricing) and [cost section](AI_ML_DEEP_DIVE.md) for the product used.

## RAG: retrieve, then generate from evidence

**Retrieval-augmented generation (RAG)** uses relevant retrieved text as context for a generation model. A typical Snowflake path is **stage documents → parse → chunk with source IDs → Cortex Search index → retrieve → `AI_COMPLETE` or Agent → cited answer → evaluate**. Search retrieves; `AI_COMPLETE` generates but does not automatically retrieve; Analyst generates SQL for structured business questions; Agents can orchestrate Search and Analyst. [Search and RAG overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)

### Minimal text lab

Assume an administrator has provisioned `GENAI_LAB.PUBLIC` and `GENAI_WH`. For a separate lab role, an `ACCOUNTADMIN` can adapt these grants; substitute `<learner_user>`. The creator owns the new table/service, so this role can read the table it creates. It needs the AI Function and model access described above to generate an answer. Creating Search builds an index and incurs charges.

```sql
USE ROLE ACCOUNTADMIN;
CREATE ROLE IF NOT EXISTS GENAI_RAG_LAB;
GRANT USAGE ON DATABASE GENAI_LAB TO ROLE GENAI_RAG_LAB;
GRANT USAGE ON SCHEMA GENAI_LAB.PUBLIC TO ROLE GENAI_RAG_LAB;
GRANT USAGE ON WAREHOUSE GENAI_WH TO ROLE GENAI_RAG_LAB;
GRANT CREATE TABLE ON SCHEMA GENAI_LAB.PUBLIC TO ROLE GENAI_RAG_LAB;
GRANT CREATE CORTEX SEARCH SERVICE ON SCHEMA GENAI_LAB.PUBLIC TO ROLE GENAI_RAG_LAB;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_EMBED_USER TO ROLE GENAI_RAG_LAB;
GRANT USE AI FUNCTION AI_COMPLETE ON ACCOUNT TO ROLE GENAI_RAG_LAB;
GRANT DATABASE ROLE SNOWFLAKE.AI_FUNCTIONS_USER TO ROLE GENAI_RAG_LAB;
GRANT ROLE GENAI_RAG_LAB TO USER <learner_user>;
```

The AI Function grants above still inherit any broader `PUBLIC` access. Check the selected generation and embedding models' availability for this account and role. For pre-existing source tables, grant the service creator `SELECT` on those tables and satisfy [change-tracking requirements](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#required-privileges).

```sql
USE ROLE GENAI_RAG_LAB;
USE DATABASE GENAI_LAB;
USE SCHEMA PUBLIC;
USE WAREHOUSE GENAI_WH;

CREATE OR REPLACE TABLE RAG_DOC_CHUNKS (
  DOC_ID VARCHAR,
  CHUNK_TEXT VARCHAR
);
INSERT INTO RAG_DOC_CHUNKS VALUES
  ('policy-1', 'Refund requests must be submitted within 30 days of purchase.'),
  ('policy-2', 'Approved refunds return to the original payment method.'),
  ('policy-3', 'Delivery address changes must be requested before dispatch.');

CREATE OR REPLACE CORTEX SEARCH SERVICE RAG_POLICY_SEARCH
  ON CHUNK_TEXT
  ATTRIBUTES DOC_ID
  WAREHOUSE = GENAI_WH
  TARGET_LAG = '1 day'
  EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
  AS (SELECT CHUNK_TEXT, DOC_ID FROM RAG_DOC_CHUNKS);

SELECT PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
  'GENAI_LAB.PUBLIC.RAG_POLICY_SEARCH',
  '{"query":"What is the refund deadline?","columns":["CHUNK_TEXT","DOC_ID"],"limit":3}'
))['results'] AS RESULTS;
```

The Search service uses warehouse compute for build/refresh, embeds text, and charges for serving and storage while active. `TARGET_LAG` is a desired freshness interval, not transactional freshness. Inspect the retrieved snippets first: if the deadline is missing, fix the data/chunks, query, filters, or index before asking the model. [Search create/query example](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#example-create-and-query-a-cortex-search-service) · [Search query reference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service)

Pass retrieved `CHUNK_TEXT` and `DOC_ID` to `AI_COMPLETE` in an application or worksheet. Example prompt after retrieval:

```text
Answer using only the evidence below. Cite DOC_ID after each claim.
If the evidence does not answer the question, say "I don't know based on these documents."
Question: What is the refund deadline?
Evidence:
[policy-1] Refund requests must be submitted within 30 days of purchase.
[policy-2] Approved refunds return to the original payment method.
```

Expected grounded answer: “Refund requests must be submitted within 30 days of purchase [policy-1].” A citation is not proof; verify that the cited chunk supports the statement. An Agent connected to Search can combine retrieval and response generation but still needs tool privileges and evaluation.

### Extend to PDFs

1. Upload non-sensitive test PDFs to a named internal stage. A local Windows path is not directly a Snowflake FILE object.
2. Parse with `AI_PARSE_DOCUMENT(TO_FILE('@db.schema.stage', 'file.pdf'), {'mode':'LAYOUT'})` when structure matters; `OCR` is default. Preserve extracted text/Markdown, document path, page, and citation metadata.
3. Chunk at headings/paragraphs. Snowflake's [PDF chatbot tutorial](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/tutorials/cortex-search-tutorial-3-chat-advanced) shows a complete stage → parse → `SPLIT_TEXT_MARKDOWN_HEADER` → Search → chat example.
4. Create Search over those chunks, then grant `USAGE` by audience. Search executes with the **owner's rights**; service access can reveal indexed content even when the caller lacks source-table `SELECT`. Separate services or filter the source query for distinct audiences. [Search access model](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#required-privileges)
5. Test answerable, unanswerable, stale, and access-denied questions. Check retrieval relevance, unsupported claims, citations, latency, token use, and cost. Retrieved documents are untrusted input: embedded instructions must not override the task or privileges. Apply appropriate masking/redaction and [guardrails](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-guardrails).

**Exam recall:** Search is managed retrieval/indexing; `AI_EMBED` alone creates a vector, not a service; `AI_COMPLETE` alone has no live document context; Analyst is for governed structured-data questions; Agents route among tools. RAG quality depends on parsing, chunks, retrieval, access, grounding, citations, and evaluation.

## Troubleshooting

| Symptom | Check first |
| --- | --- |
| AI unavailable on a trial | Trial activation in Admin → Billing, account status, region/product availability. |
| Function permission error | Account/function privilege **and** database role; inherited `PUBLIC` grants. |
| Model unavailable | Region, cross-region setting, model application roles/bootstrap/allowlist; test without an admin secondary role. |
| Search creation fails | Embedding entitlement, schema create privilege, source `SELECT`, refresh warehouse `USAGE`, change tracking and source-query constraints. |
| Search works for creator only | Consumer's service and database/schema `USAGE`; review what indexed rows that audience may see. |
| Agent fails despite worksheet role | User's **default** role and warehouse, Agent `USAGE`, and every required tool permission. |

No live account test was performed. Recheck the linked official documentation before applying account-wide grants, routing, or spend controls.
