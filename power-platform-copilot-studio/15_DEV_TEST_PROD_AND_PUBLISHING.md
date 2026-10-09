# Dev, test, prod and publishing (Teams, Slack, website, third parties)

Checked against Microsoft Learn on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Nothing here was executed; CLI and REST snippets are templates. Sources: [Foundry agent applications](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/agent-applications), [publish to Teams and Microsoft Copilot](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot), [Copilot Studio channels](https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-fundamentals-publish-channels), [solutions](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-overview), [export and import](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-import-export), [Azure Bot Service channels](https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-connect-bot-to-azure-bot-service-channels).

## 1. The principle

Three stages, each isolated, each with its own identity and data:

| Stage | Purpose | Who touches it | Data |
| --- | --- | --- | --- |
| **Dev** | Build and iterate fast | Builders | Sample or masked data |
| **Test (UAT)** | Prove quality, security and access before release | Builders plus a few real users | Production-like, least privilege |
| **Prod** | Serve real users | Nobody edits by hand; release by promotion only | Real data |

Rules: promote the same artefact, never rebuild by hand; configuration (IDs, URLs, connections) changes per stage, logic does not; every release has an evaluation run and a rollback.

## 2. Foundry agents (prompt or hosted)

### 2.1 Environment layout

| Option | Layout | Use when |
| --- | --- | --- |
| **A. One resource, one project per stage** | Foundry resource with `dev`, `test`, `prod` projects | Small team; cheapest. Weak isolation: models and quotas shared. |
| **B. One resource per stage (recommended for prod)** | `rg-...-dev`, `-test`, `-prod`, each with its own resource, project, model deployments, App Insights | Real separation of RBAC, quota, network, cost |

Fabric side: a data agent per stage over a matching workspace (dev workspace on sample data, prod workspace on real data). The Fabric tool takes a **workspace ID and artifact ID**, so these are per-stage configuration values. Do not point dev at prod data. Region and same-tenant rules still apply ([08](08_FABRIC_ADMIN_AND_TENANT_CHECKLIST.md)).

### 2.2 Step by step

1. **Source control first.** Keep the agent definition as code in Git: instructions text, tool definitions, model name, guardrail config, evaluation dataset and the publish script. The portal is for exploring; the repo is the source of truth. Foundry versions are immutable, but they live in the project, not in your Git history.
2. **Dev.** Build in the dev project. Each save creates a new immutable version (limit 1,000 per agent; delete old ones). Use Playground and Traces. Use the dev data agent and dev workspace.
3. **Pin before testing.** The default is "Always use latest": every save changes what the endpoint serves. Pin the version under test (Publish dropdown, Active version, or the `version_selector` PATCH).
4. **Quality gate.** Run the known-answer evaluation set ([11](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md)): relevance, groundedness, tool-call accuracy, safety, plus a few red-team prompts and a PII probe. Record pass thresholds. This needs a judge model (an Azure OpenAI GPT deployment; JB has none yet).
5. **Promote to test.** Re-create the agent in the test project from the repo (SDK or REST) with test settings: test data agent IDs, test connection names, test model deployment name. Do not copy-click.
6. **Test as real roles, never as owner.** Use a member of `agent-users` (see [14](14_ACCESS_SETUP_FOUNDRY_AND_FABRIC.md) Part 3): correct answers, denied tables denied, no PII leak, tool errors handled, latency and cost acceptable. Run the same evaluation set again and compare.
7. **Security review.** Guardrail with tool-call and tool-response points plus PII control; remove web search unless needed; narrow data agent sources; App Insights on with trace access limited.
8. **Approve.** A named approver signs off on the evaluation report and the access list.
9. **Promote to prod.** Same script against the prod project and prod IDs. Pin the approved version. Foundry Project Manager (at account scope) is the minimum to publish.
10. **Publish the stable endpoint** (section 4). The published agent gets its **own new identity**: reassign every role it needs (Foundry User on the project for tools, plus anything it reads). Tool calls that worked in dev fail with authorization errors otherwise.
11. **Smoke test in prod** with a real non-admin user, then announce.
12. **Operate.** Monitor tab, traces, scheduled evaluation, cost alerts, quota alerts. A new version is rolled out by updating the version selector or deployment, not by republishing the channel.
13. **Rollback.** Point the version selector (or the deployment) back to the previous pinned version. Keep the last two good versions undeleted.

### 2.3 CI/CD sketch

Pipeline in GitHub Actions or Azure DevOps with OIDC federated credentials (no stored secrets):

```text
pull request -> lint prompts, unit tests on tool glue code
merge to main -> deploy to dev -> run evaluation set (fail below threshold)
manual approval -> deploy to test -> run evaluation + access tests
manual approval (change record) -> deploy to prod -> pin version -> smoke test
```

Use per-stage variables for resource names, project endpoints, model deployment names and Fabric workspace and data agent IDs. Infrastructure (resource, project, deployments, role assignments, App Insights, Bot Service) belongs in Bicep or Terraform.

## 3. Copilot Studio agents and workflows (standard harness)

Copilot Studio uses Power Platform **environments** and **solutions**, not Foundry projects. Applies to agents licensed and permitted in your tenant (note: JB has no Copilot Studio licences, so this path is for other clients and for the PDP tenant).

### 3.1 Environments

Dev (developer or sandbox), Test (sandbox), Prod (production; Managed Environments recommended). Create DLP policies per environment group ([01](01_ADMIN_AND_ENVIRONMENTS.md)). Prod makers should be few; prod is imported, not edited.

### 3.2 Step by step

1. In **Dev**, create a **custom solution** (agents land in the default solution otherwise). Set it as the preferred solution. Add the agent, its flows, topics, connection references and **environment variables**.
2. Use **environment variables** for anything that differs by stage (URLs, workspace IDs, mailbox, SharePoint site) and **connection references** for connectors, so imports can bind new connections without editing flows.
3. Run **Add required objects** on the agent, flows and environment variables so the solution is complete. Import fails mostly because a required component is missing; download the log file to see which.
4. Custom connectors must be imported **before** the connection references and agent that use them.
5. **Export** the **unmanaged** solution from Dev and import it as **managed** into Test and Prod. Docs note that you cannot export a managed solution, so always export from the unmanaged Dev source. Do not hand-edit managed components in Prod (use the "see solution layers" view to remove an unmanaged layer if someone did).
6. Prefer **Power Platform pipelines** (solution explorer, Pipelines) to automate Dev, Test, Prod; or Azure DevOps and GitHub Actions with the Power Platform build tools and service principals.
7. After each import, do these by hand (they are not carried across): configure **end-user authentication** again, bind connections and set environment variable values, check knowledge sources and custom topics came across (docs say some might not), re-add the icon and channel details, then **Publish** (an imported agent cannot be shared until published).
8. Not exported: topic and node comments; conversation, CDS bot and environment IDs. Topics with a period in their name block export.
9. Test in Test with real roles, then promote the same solution file to Prod. Keep the exported solution zip (versioned) as the release artefact, in Git or a release store.
10. **Publish** again after each change. New content reaches users in the next session; Teams may take up to an hour, and `start over` forces a new session.
11. **Workflows** (agent flows, Power Automate cloud flows) move in the same solution. Use connection references and service accounts for unattended flows; turn flows on after import.
12. Rollback: keep the previous managed solution version and import it over the top (update, not upgrade, if you need to be conservative); there is no one-click revert.

## 4. Publishing: where and how

### 4.1 Decision table

| Target | From Foundry | From Copilot Studio |
| --- | --- | --- |
| **Teams** | Publish dialog, Teams and Microsoft Copilot (creates Azure Bot Service and a Teams app package) | Channels, Teams and Microsoft Copilot |
| **Microsoft 365 Copilot** | Same publish dialog | Same channel |
| **Slack** | No built-in button. Use your own bot or a relay on Azure Bot Service calling the published agent endpoint | Azure Bot Service channels via a relay bot (developer work), Slack channel on the bot |
| **Your website** | Call the Agent Application endpoint from your backend and build your own chat UI | Custom Website channel (embed) or Demo Website for internal feedback only |
| **Mobile or custom app** | Same backend call | Direct Line / mobile channel |
| **Other third parties (WhatsApp, Facebook, Telegram, Twilio, email and so on)** | Own bot layer, or workflow tool calling the endpoint | Built-in WhatsApp and Facebook channels; others via Azure Bot Service |
| **Another agent or tool** | A2A or MCP | Connected agents, MCP |
| **Automation (n8n, Logic Apps, Power Automate)** | HTTP call to the Responses endpoint with Entra token | Agent flows or HTTP |

### 4.2 Foundry: publish the Agent Application (stable endpoint)

Prerequisites: Foundry Project Manager on the **resource** scope (the Publish button is greyed out if it is only on the project); a pinned, tested version.

1. Portal: **Publish** to create an **Agent Application** (own URL, own Entra agent identity and blueprint, own RBAC, ARM resource). Or REST: `PUT .../projects/{project}/applications/{app}` with `displayName` (required; omitting it gives an opaque 400) and `agents`, then `PUT .../applications/{app}/agentdeployments/{dep}` with `deploymentType: Managed`, protocol `Responses` version `1.0`, and the agent name and version.
2. One active deployment per application, 100% of traffic. Publishing a new version to the same application switches all traffic at once. There is no canary; get gradual rollout by running two applications and routing in front.
3. **Reassign roles to the new agent identity.**
4. Callers need **Foundry User** (or a custom role with `Microsoft.CognitiveServices/accounts/AIServices/applications/invoke/action`) on the **Agent Application**. **Foundry Agent Consumer does not grant invoke on Agent Applications**, even though it works on a project-level agent endpoint. This corrects the assumption in [14](14_ACCESS_SETUP_FOUNDRY_AND_FABRIC.md) Part 1 that Agent Consumer is enough for end users: it is right for the project endpoint only.
5. API keys are not supported; use Entra tokens for `https://ai.azure.com`.
6. **Only the stateless Responses API** is exposed on applications (`POST /responses`). No conversations, files or vector store APIs. Your client or backend must store the history and resend it.
7. **One protocol at a time**: Responses (REST, website backends) or Activity (Teams and Microsoft 365). Publishing to Teams switches the application to the Activity protocol. The same application cannot serve both at once, so create separate applications for a website backend and for Teams.
8. Cost model: publisher pays for the deployed infrastructure, not per call. Add your own metering if you charge users.

### 4.3 Foundry: Teams and Microsoft 365 Copilot

1. Register `Microsoft.BotService` in the subscription. You need Azure Bot Service Contributor (or Contributor/Owner) on the resource group; Foundry roles do not grant it. Foundry User on the project.
2. Pin the active version (the endpoint keeps serving it).
3. Publish, **Teams and Microsoft Copilot**. Fill name, 3-part version, short and long description, developer, optional website, terms, privacy (HTTPS). No secrets in metadata.
4. Choose scope:
   - **Just you**: `BotServiceRbac`, no admin approval; shows under **Your agents**; share by link; participants need Foundry permissions on the project.
   - **People in your organization**: `BotServiceTenant`, a Microsoft 365 admin approves at the Microsoft 365 admin center, then it appears under **Built by your org** for all tenant users.
5. Alternative: **Download & customize** to get a manifest zip, edit user-facing metadata only (never the generated IDs) and upload it as a custom or org app in Teams.
6. Updating: to ship a new agent version, change the version selector (no republish). To change name, descriptions or URLs, use the update display properties item in the Publish dropdown.
7. Data note: Microsoft 365 and Teams process and store the agent metadata and responses under their own compliance terms; check this with the client first.
8. Projects with public network access disabled cannot publish from the portal; use the REST route with `enable_m365_public_endpoint`.
9. **Open for JB:** whether the Fabric tool still receives the signed-in user's identity when called through Teams (it runs as the user in the portal) is **unverified**; a community report says the channel may not forward the OAuth token. Test with a non-admin user before promising per-user data access.

### 4.4 Copilot Studio: Teams, Microsoft Copilot, SharePoint, website

1. **Publish** first (confirm). Authentication: **Authenticate with Microsoft** is on by default and automatic for Teams, Power Apps and Microsoft Copilot; **Authenticate manually** for other channels (needed to keep sign-in and user-credential tools); **No authentication** lets anyone with the link chat and blocks tools that use user credentials.
2. Start with **Open the agent in Teams** for yourself, then **Make the agent available to others**. Do not widen availability before testing in the published form.
3. **Demo Website**: for stakeholder feedback only, not for customers.
4. **Custom Website**: Channels, Custom Website, copy the iframe or snippet; with manual authentication configure the identity provider and secrets.
5. Admins can restrict channels with **Agent access channels** in the Power Platform admin center and DLP policies; a blocked channel appears greyed with an information icon.
6. Known limits: attachments are not processed (text only); Teams shows at most six suggested actions; satisfaction survey is text-only in Teams.

### 4.5 Slack and other Azure Bot Service channels

Copilot Studio does not have a one-click Slack channel. The documented route is a **relay bot**:

1. Create (or reuse) an Azure Bot Service bot (v4 SDK) that relays messages between the external channel and the Copilot Studio agent over **Direct Line**. Microsoft provides a relay bot sample (not production ready).
2. In Copilot Studio, Settings, Channels, copy the agent **Token Endpoint**. The relay maps each Slack conversation to a Direct Line conversation and refreshes tokens.
3. Deploy the bot to Azure and enable the Slack channel (and others: Telegram, Twilio, Line, Email and so on) in the bot's Channels blade, following the Azure Bot Service channel instructions.
4. Developer expertise is required; handle token refresh, idle conversation cleanup, rate limits and response parsing (cards to Slack blocks).
5. For a Foundry agent in Slack, the same pattern applies: a Slack app (Events API or Bolt) or a Bot Service bot that calls the Agent Application Responses endpoint with a service identity, stores history, and posts replies. Check the Slack workspace admin approves the app and scopes. Your relay's identity, not the Slack user, then calls Foundry: you lose per-user Fabric access (see 4.7).

### 4.6 Website (custom front end)

Never call Foundry from browser JavaScript with a token you embed.

```text
Browser chat UI -> your backend (authenticates the visitor) -> Foundry Agent Application (Responses) -> reply
```

1. Backend uses a managed identity or service principal with **Foundry User on the Agent Application**.
2. Backend stores history per visitor and resends it (stateless endpoint).
3. Add rate limiting, bot protection, input and output filtering, abuse logging, a data retention policy and a visible AI disclosure.
4. For Copilot Studio, use the Custom Website channel instead, with manual authentication if visitors must sign in.
5. Public website agents must not use the Fabric tool over private warehouse data without a design for who the data is shown to.

### 4.7 The identity question (read before choosing a channel)

| Path | Who the data call runs as | Consequence |
| --- | --- | --- |
| Foundry portal Playground / SDK as a signed-in user | The user (OBO) | Fabric RLS and CLS apply |
| Published endpoint called by a backend or Slack relay | The service identity of the caller or agent | One identity for everyone; per-user rules are lost; grant that identity least privilege |
| Teams via Bot Service | Unverified (see 4.3 item 9) | Test before promising |
| Scheduled newsletter (unattended) | No user | The docs say service principals are not supported for the Foundry Fabric tool; use a signed-in service account pattern, a direct MCP/API call with a service principal token, or a pipeline that queries the warehouse and passes the result to the agent. Decide with the client |

Decision rule: if answers depend on who is asking, keep calls as the user (Teams with OBO, Copilot Studio connected agent). If every user may see the same data, a service identity with a narrow data source is acceptable.

## 5. Release checklist (copy per release)

- [ ] Agent definition and evaluation dataset in Git, version tagged
- [ ] Passed evaluation thresholds in test; report stored
- [ ] Tested as non-admin with correct and denied cases
- [ ] Guardrail on (tool call, tool response, output, PII); web search decision made
- [ ] Data agent sources narrowed; sensitive tables denied
- [ ] Version pinned; rollback version identified
- [ ] Agent identity roles reassigned after publish
- [ ] Callers granted invoke on the Agent Application (Foundry User), not just Consumer
- [ ] Channel scope and approver confirmed (Teams admin approval, Slack workspace approval, CORS and domain for the website)
- [ ] App Insights, alerts and cost budget on; trace access restricted
- [ ] Data residency and Microsoft 365 data handling reviewed with the client
- [ ] Runbook and owner named; support path for users
- [ ] Post-release smoke test with a real user, then review traces after 24 hours

## 6. Application to the JB newsletter agent (proposal)

1. Today everything is in one project (`jb-newsletter`) with "Always use latest": treat it as dev. Create test and prod projects (or resources) when the agent is stable, with matching Fabric workspaces and data agents.
2. Decide the delivery pattern first: interactive (editors ask questions in Teams) or unattended (scheduled newsletter). It decides identity (4.7).
3. Add a GPT judge deployment, guardrail and App Insights before the first formal test.
4. Pin a tested version, publish to Teams with scope "Just you", test with an editor account, then request organization scope.
5. Slack and a public website are not needed for a newsletter and would remove per-user data access; leave them out unless JB asks.

## 7. Unverified items

- Teams per-user identity flow into the Fabric tool.
- Whether preview Foundry features (Fabric tool, Activity protocol, Optimize) are allowed in JB's production policy.
- Exact Foundry CI/CD tooling beyond REST and SDK (azd templates or Foundry-specific GitHub actions were not checked).
- Licensing for Copilot Studio at JB (none today).
