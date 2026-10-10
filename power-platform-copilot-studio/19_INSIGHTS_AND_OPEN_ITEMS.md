# Insights and open items (sessions of 2026-10-08 to 2026-10-10)

Durable lessons from the JB newsletter agent work on Foundry. Facts marked *verified* were seen working in this tenant; others are from Microsoft Learn or are assumptions and are labelled.

## Verified in this tenant
- **Fabric notebook has no `az login` or managed identity.** Use `DeviceCodeCredential(tenant_id=...)` and open https://login.microsoft.com/device. `DefaultAzureCredential` fails there.
- **SDK:** `azure-ai-projects` 2.x (tested 2.8.0) is not compatible with 1.x. Use `AIProjectClient`, `agents.create_version`, `get_openai_client(agent_name=...)`, `conversations.create`, `responses.create`.
- **`TypeError: process() takes no keyword arguments`** = old Brotli decoder. Fix: `%pip install -U brotli` (confirmed), or send `Accept-Encoding: identity`.
- **Test scripts must never write to the live agent name.** A script that called `create_version` on `jbnewsletteragentv1` created version 8 and made it the served version, which caused a 404 DeploymentNotFound. Use a separate test agent name.
- **Pinning a version:** in the portal set Active version to a fixed version (v7). The endpoint then has `version_selector = {"version_selection_rules": [{"type": "FixedRatio", "agent_version": "7", "traffic_percentage": 100}]}`.
- **Deleting a version:** `project.agents.delete_version(agent_name, agent_version)` works. `examples/foundry_delete_agent_version.py` does a dry run by default and refuses to delete the pinned version (or the latest when nothing is pinned). Version 8 was deleted this way on 2026-10-09 and the portal list confirmed it.
- Local demo app (`examples/foundry_agent_web_demo_app.py`) works as the signed-in user. A hardened version exists (`examples/hardened_app/`, 14 mocked unit tests) but has not been run against a real tenant or deployed.

## Access and identity
- Foundry Owner and subscription Contributor do **not** allow creating role assignments. That needs Owner, User Access Administrator or Role Based Access Control Administrator (`Microsoft.Authorization/roleAssignments/write`).
- **Monitor "Setup incomplete"** means the project managed identity lacks: Reader on the App Insights resource, Foundry User on the Foundry account (`jb-pdp-newsletter-eus2`), Log Analytics Reader on the workspace only if it requires workspace permissions, Privileged Monitoring Data Reader only for protected tables. A JB/PDP admin must assign these (scope: `rg-pdp-ai-project`, subscription PDP PROJECT). Source: Microsoft Learn evaluation-permissions page.
- A published Agent Application needs **Foundry User** for callers; Foundry Agent Consumer only covers the project agent endpoint.
- Do not give public or shared-account access to an agent that can reach the contact table (personal data). Visitor sign-in (Easy Auth) plus an allow-list is the minimum; whether the Fabric tool works under a managed identity is **unverified** (docs say service principals are unsupported), so run `examples/foundry_identity_test.py` first.
- The Foundry account API key is full access: never put it in an app or in git.

## Foundry portal pages seen
- Account `jb-pdp-newsletter-eus2`: eastus, S0, public network access enabled. Project `jb-newsletter` (default, created 2026-08-19). Connected resources: `JB_Data_Agent_Fabric` and an App Insights connection.
- AI Gateway (Preview, Azure API Management) is not enabled; not needed while the hardened app has its own limits.

## Open items, in suggested order
1. Verify the agent's answers against the warehouse (an answer of 0 houses last week looked suspicious; check `property_type` labels and table `gld_market_listing`).
2. Add guardrails and exclude the contact table or its personal columns from what the agent can read.
3. Build an evaluation set, then enable scheduled analysis in Monitor once the roles above are assigned.
4. Ask an admin for the Monitor role assignments (message template in session note item 17/this folder's doc 13).
5. Create the Entra registrations (doc 18), run the identity test, then deploy the hardened app.
6. Remove subscription-level Contributor from guest consultants where not needed.
7. Unverified: per-visitor on-behalf-of route, Teams per-user identity, memory supported region.
