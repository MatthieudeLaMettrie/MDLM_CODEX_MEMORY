# Cortex AI enablement and RAG guide

Date: 2026-09-25 (Australia/Sydney)

## Request and finding

The user asked whether the SnowPro GenAI guide explained how to enable Cortex AI/AI Functions from subscription or trial status through governance and specific roles, and whether it included RAG. The existing study guide did cover the RAG pipeline, Search syntax, and individual privileges, but activation was scattered and there was no single account-to-RAG walkthrough. This session adds one.

## Research and changes

- Rechecked current official Snowflake documentation for trial accounts, AI pricing, AI Function privileges and model RBAC, cross-region inference, Search privileges and creation/query syntax, Agent default-role requirements, Analyst opt-in, cost governance, and the PDF chatbot tutorial.
- Added `snowpro-genai/ENABLE_CORTEX_AND_RAG.md`. It explains self-service trial credit-card activation without ending the trial; consumption billing rather than a documented general Cortex Functions subscription; account/function privilege plus Snowflake database role; `PUBLIC` defaults; model-role/bootstrap and regional checks; dedicated scalar-function and Search lab role templates; separate gates for Search, Analyst (parameter and `CORTEX_ANALYST_USER`), Agents, and fine-tuning; cost controls; a synthetic Search retrieval lab; a grounded prompt/citation example; PDF ingestion extension; security/evaluation/troubleshooting.
- Linked the new chapter from `snowpro-genai/README.md` and `snowpro-genai/STUDY_GUIDE.md`, and updated `MEMORY.md`.

## Validation and limits

- Compared the role-grant and Search SQL shapes with official Snowflake examples and checked the working-tree diff and links. The SQL is an instructional template using placeholder account objects and was not executed against a Snowflake account.
- Account-wide `PUBLIC` or model-bootstrap revocation is intentionally described as an administrator policy change rather than a learner step, because it can affect other users. The current model allowlist is legacy, and regional availability/pricing can change.
- Next hands-on check: run the synthetic RAG lab in a test account with a non-admin role, then update any account-specific findings or changed syntax.
