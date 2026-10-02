# Azure and GCP identity setup guide

User requested another part in MDLM_CODEX_MEMORY with step-by-step Azure Key Vault setup and service accounts/service principals or OAuth in GCP. Added guides/api/AZURE_GCP_IDENTITY_SETUP_GUIDE.md as Part 2, linked from the root README and Part 1 API guide.

Azure steps cover subscription/tenant choice, new vault, RBAC secret-reader/writer distinction, networking, harmless test secret, local AzureCliCredential read, Entra app/service principal and controlled client-secret example, managed identity on App Service and Fabric execution-identity caveats. GCP covers account creation, scoped BigQuery roles and Sheet sharing, local ADC impersonation, attached Cloud Run identity, federation overview, JSON-key fallback, full desktop Sheets OAuth setup and cached-token example, web-flow distinctions and Secret Manager.

Primary Microsoft/Google sources checked, including OAuth Testing seven-day refresh-token rule. Uses placeholder identifiers and protected external file paths; no credential values, actual resource creation, IAM edits, key generation, OAuth consent or live API calls. Explicitly distinguishes SELECT 1 job validation from dataset access, file sharing from project IAM, and service-account key JSON from OAuth client/token JSON.

Offline validation: Python fences compile without execution, PowerShell fences parse without execution, local links/internal anchors resolve and Git whitespace checks pass. Actual cloud integration remains untested. Durable notes/session also recorded in MDLM_AGY_MEMORY under standing instructions.
