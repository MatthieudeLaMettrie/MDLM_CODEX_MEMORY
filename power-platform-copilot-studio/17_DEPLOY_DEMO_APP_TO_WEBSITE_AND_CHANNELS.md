# From local demo to a real website, SharePoint, Teams and Slack

Written 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Builds on [15](15_DEV_TEST_PROD_AND_PUBLISHING.md) and [16](16_SDK_AGENTS_DEV_TEST_PROD.md) and on the working local demo `examples/foundry_agent_web_demo_app.py`. Command snippets are templates and were **not run**. Items marked *(general knowledge)* were not checked against docs in this session.

## 1. What the local demo is, and why it cannot just be uploaded

The demo is a FastAPI page that calls the Foundry agent **as the person who signed in with a device code**. A real site has many visitors and no device-code sign-in, so three things must change: who the visitors are, whose identity calls Foundry and Fabric, and where it runs.

## 2. Decide the identity first (this decides everything else)

| Pattern | Calls Foundry as | Fabric data agent tool | Verdict |
| --- | --- | --- | --- |
| **A. Visitor signs in (Entra) and the backend calls Foundry on their behalf (on-behalf-of token exchange)** | Each visitor | Runs as that visitor, so row and column security apply | Best for editors and internal staff. **Unverified** that the Foundry agent endpoint accepts an exchanged user token and that the Fabric tool then works; test first. |
| **B. Backend uses its own managed identity** | The app | The Foundry docs say service principals are **not supported** for the Fabric tool, so it is expected to fail | Do not assume it works. Test with one call before building around it. |
| **C. One shared "service user" account** | A normal user | Works, as in the demo | Not recommended: shared account, MFA and Conditional Access problems, everyone sees the same data. |
| **D. Skip the Fabric tool on the web path** | Managed identity | The backend queries the warehouse itself (SQL or the Fabric data agent MCP/API with a service-principal token, which the Fabric MCP page allows for direct clients) and gives results to the model | Works unattended; you own the SQL safety (read-only, allow-listed views). |

Data governance: the data belongs to JB, so host the site in **JB's Azure subscription and tenant**, with JB's approval, not on Metcash or PDP infrastructure.

## 3. Prepare the app for production

1. Replace `DeviceCodeCredential` with `DefaultAzureCredential()` (managed identity in Azure) for pattern B or D, or an on-behalf-of credential for pattern A.
2. Add visitor authentication in front: Azure Container Apps or App Service **built-in authentication** (Entra), restricted to your tenant, a group or named users *(general knowledge)*.
3. Render answers properly: the demo shows raw markdown (`**bold**`, table pipes) and citation markers like `【4:0†source】`. Use a markdown renderer with an HTML sanitiser in the page and strip the citation markers server-side.
4. Add rate limiting, request size limits, structured logging (no secrets, no full answers if they contain personal data), a health endpoint, and an error page.
5. Store the conversation ID per signed-in user on the server side, not only in browser memory.
6. Keep `host 0.0.0.0` only inside the container; the platform terminates HTTPS.
7. Add the guardrail, evaluation set and instructions fixes first ([11](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md), [12](12_JB_NEWSLETTER_FIELD_LOG.md)); the agent can reach a contact table with personal data.

## 4. Deploy to Azure (Container Apps; App Service is the alternative)

Template commands; replace names; run in JB's subscription with a role that can create resources.

```bash
# requirements.txt: fastapi, uvicorn, azure-ai-projects>=2.3.0, azure-identity, brotli
# Dockerfile
#   FROM python:3.12-slim
#   WORKDIR /app
#   COPY requirements.txt . && RUN pip install -r requirements.txt
#   COPY . .
#   CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]

az group create -n rg-jb-agent-web -l eastus
az containerapp env create -n jb-agent-env -g rg-jb-agent-web -l eastus
az containerapp up -n jb-agent-web -g rg-jb-agent-web --environment jb-agent-env \
  --source . --ingress external --target-port 8000
az containerapp identity assign -n jb-agent-web -g rg-jb-agent-web --system-assigned
# give the app permission to call the agent (role id = Foundry User)
az role assignment create --role 53ca6127-db72-4b80-b1b0-d745d6d5456d \
  --assignee <app-principal-id> --scope <foundry-project-or-resource-scope>
```

Then: set environment variables (tenant, endpoint, agent name; no secrets in the image), turn on **Authentication** (Microsoft identity provider, require sign-in, single tenant), add Application Insights, and set a custom domain. Put the active agent version pin in place before go-live. Use CI/CD (GitHub Actions with OIDC) so deployments are repeatable ([15](15_DEV_TEST_PROD_AND_PUBLISHING.md) section 2.3).

Optional hardening: Azure Front Door with WAF, private networking to Foundry, managed-identity-only access, budget alerts, an agent kill switch.

## 5. Channels

### 5.1 Public or internal website
The deployed Container App URL is the site. For a public audience, pattern A does not apply; use pattern D or a heavily restricted agent without private data, with bot protection and rate limits.

### 5.2 SharePoint (embedded) *(general knowledge)*
- **Embed web part (iframe):** add the Embed web part to a page and paste the app URL. Site admins may need to allow the domain under the site's HTML field security setting. Your app must permit framing: send `Content-Security-Policy: frame-ancestors https://*.sharepoint.com` and do not send `X-Frame-Options: DENY`. Entra sign-in inside an iframe can be blocked by browser or Conditional Access settings; test early or use a "open in new tab" link.
- **SPFx web part:** a custom web part that calls your API with the user's SharePoint token (more work, cleaner sign-in).
- **Copilot Studio SharePoint channel:** only if the Copilot Studio standard-harness agent exists; JB has no licences today ([01](01_ADMIN_AND_ENVIRONMENTS.md), [15](15_DEV_TEST_PROD_AND_PUBLISHING.md) 4.4).

### 5.3 Teams
- **Easiest:** publish the Foundry agent from the portal (Details, Channels, Teams and Microsoft 365 Copilot). Scope "Just you" needs no admin approval; "People in your organization" needs Microsoft 365 admin approval ([15](15_DEV_TEST_PROD_AND_PUBLISHING.md) 4.3). The agent identity changes on publish; reassign its roles. **Unverified:** whether the Fabric tool runs as the Teams user.
- **Tab:** add your website as a Teams personal tab (an app manifest pointing at the URL) so the same web page shows inside Teams *(general knowledge)*.
- **Custom bot:** Teams SDK / Microsoft 365 Agents SDK bot via Azure Bot Service calling your backend.

### 5.4 Slack
No built-in route. Create a Slack app (Events API or Bolt), verify the Slack signing secret, call your backend, reply asynchronously. The backend sees a Slack user, not a Fabric identity, so pattern A is unavailable; use only for data everyone in the channel may see. The workspace admin must approve the app.

### 5.5 Other (WhatsApp, email, mobile)
Same shape: a gateway or bot that calls your backend; see [16](16_SDK_AGENTS_DEV_TEST_PROD.md) section 9.

## 6. Order of work for JB

1. Run the **identity test**: deploy a tiny version with a managed identity and call the agent. Record whether the Fabric tool works (pattern B). If not, test the on-behalf-of path (A).
2. If neither works, choose pattern D (own SQL or MCP) or keep access interactive through the Foundry Playground, the preview web app or Teams.
3. Add guardrail, evaluation set, instructions, pinned version.
4. Pilot with 2 to 3 editors; review traces and cost.
5. Then widen (SharePoint embed, Teams tab); leave Slack and a public site out unless JB asks.

## 7. Unverified

- Foundry agent endpoint with an on-behalf-of user token, and the Fabric tool under it.
- Managed identity with the Fabric tool (docs say service principals are unsupported).
- SharePoint, Teams tab and Container Apps authentication specifics (general knowledge, not read here).
- Costs and quotas.

## 8. Addendum: how to run the identity test, and why not a public shared-account site

**Identity test without deploying anything.** A managed identity behaves like a service principal for this test, so test locally with a service principal:
1. JB admin creates an app registration in JB's tenant (guest consultants usually cannot) and a client secret; the secret goes in environment variables or Key Vault, never in code or the repo.
2. Azure: give the service principal Foundry User on the project.
3. Fabric: JB admin enables the tenant setting that lets service principals use Fabric APIs (scope it to a security group), adds the service principal to that group, then shares the published data agent and the source items with it.
4. Run the demo's call using `ClientSecretCredential(tenant_id, client_id, client_secret)` instead of `DeviceCodeCredential`.
5. Read the result: answer plus a `fabric_dataagent_preview_call` item means service identity works for the Fabric tool; an unauthorized or tool error means it does not (the docs say service principals are not supported for this tool, so an error is expected).
The on-behalf-of (user token exchange) test needs a small web app with Entra sign-in and is a second step.

**Public or "anyone" access with a shared service account: do not.** The agent can reach the warehouse including a contact table with personal data; a shared identity removes per-user row and column security, anyone can run up model cost (Claude Opus class pricing), prompt injection can steer the agent into revealing data, and a shared user account breaks MFA and Conditional Access. Use authenticated users (Entra group) for internal use. For a public audience build a separate agent over curated, public-only data with no warehouse tool, rate limits and bot protection.
