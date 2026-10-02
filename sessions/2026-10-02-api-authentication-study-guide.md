# API authentication study guide

User requested a Markdown study guide in MDLM_CODEX_MEMORY comparing API connection/authentication methods, using supplied MyTurn/Supabase Bearer-versus-cookie and Fabric Key Vault/Foundry examples. Credentials in the prompt were excluded entirely; rotation of exposed password/private keys was advised, not performed.

Added guides/api/API_AUTHENTICATION_STUDY_GUIDE.md and linked it from README.md. Covers issuance versus transport versus storage, Basic versus password login, API keys, Bearer/JWT, OAuth code + PKCE and client credentials, OIDC, managed identity, Supabase session refresh, diagnostic SSR-cookie adaptation, explicit secret fallback, Claude Foundry key/Entra, deployment-based Azure OpenAI and ACS SDK construction. Includes comparison tables, Mermaid diagrams, troubleshooting, labs and twelve questions with answers.

Official documentation checked: IETF, Supabase and SSR source, Microsoft Learn and Anthropic Foundry docs. Current Foundry Claude guidance uses https://ai.azure.com/.default. Fabric documentation describes current-user getSecret, a limited list of getToken audience keys and lack of direct DefaultAzureCredential support; scheduled identity must be verified, not assumed. Original inline-key expression short-circuits vault retrieval.

Earlier AGY note reports Supabase password-login success and non-JSON Bearer response from /api/listings/filter-options. Cookie success and /api/listings behavior remain unverified. No live API calls, login, secret retrieval, email, cloud changes or credential rotation executed for this task.

Validation: Python fenced examples compiled without execution; guide structure, internal heading anchors, local navigation links and Git whitespace checked. Placeholder-only artifacts and staged changes reviewed before publication. Memory category and session also recorded in MDLM_AGY_MEMORY under standing instructions.

## Follow-up: os and sys

User requested adding os/sys libraries. Added section 11 and its contents link: standard-library imports, os.environ versus os.getenv, string/default semantics, PowerShell configuration inheritance, RESOURCES and os.path/pathlib, sys.executable/version/platform, sys.path versus PATH, sys.argv/sys.exit and argparse. Connects examples to API configuration and explains notebook/runtime differences. Official Python documentation checked; all fenced Python examples compile and heading links resolve; Git whitespace checked. No secrets read or API calls executed.
