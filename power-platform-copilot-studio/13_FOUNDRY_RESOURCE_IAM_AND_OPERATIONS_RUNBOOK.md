# Foundry runbook: resource settings, IAM, deployments, guardrails, monitoring, evaluation, publishing

Checked against Microsoft Learn on 2026-10-09 and against seven screenshots of the user's own Foundry project. Part of the [Power Platform / Copilot Studio guide](README.md). Nothing was changed by the assistant. **No IDs, e-mail addresses or person names are recorded**; people are described by role only.

Read order: this file is the operations runbook. Concepts live in [09](09_FOUNDRY_PLATFORM_AND_SERVICES.md), [10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md) and [11](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md); the build story is [12](12_JB_NEWSLETTER_FIELD_LOG.md).

## Part A. Read the resource settings (Manage, Resource details)

Path: Foundry portal, top bar **Manage**, left nav **Resource details**. The page shows the **parent resource** (the Foundry resource). **Project details** shows the project.

| Field seen | Value pattern | What to check |
| --- | --- | --- |
| Name | `jb-pdp-newsletter-eus2` | The suffix `eus2` is only a name. Do not read the region from it. |
| **Location** | **eastus** (East US) | The real region. See Part B. |
| Pricing tier | S0 | Standard. |
| Public network access | Enabled | Fine for a prototype; disable plus private endpoints for production (some portal features then need the SDK or CLI). |
| Resource group, Subscription | Named in the portal | Roles inherit from these scopes (Part C). |
| **Tenant ID** | A GUID | Must equal the Fabric `ctid` (see [08](08_FABRIC_ADMIN_AND_TENANT_CHECKLIST.md)). |
| Endpoint, API key | Shown | Keys bypass RBAC: anyone with the key has full access. Prefer Microsoft Entra authentication and do not paste keys into notes. |
| **My permission** | Foundry Owner, full access | Your effective role on this resource. |
| Tabs | Projects, Users, Connected resources, Admin-connected models | Projects list shows one default project, also in eastus. |

Left nav also has **Quota** and **AI Gateway**.

## Part B. What the region means for this project

Region **East US** was confirmed from the resource details (it replaces the earlier guess of East US 2 from the name).

| Capability | East US result | Source |
| --- | --- | --- |
| Agents, Responses API | Supported | [limits and regions](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions) |
| Fabric data agent tool, MCP, AI Search, code interpreter, web search, A2A, OpenAPI, SharePoint | Supported | same table |
| Computer use | Not supported in East US (supported in East US 2, Central US and a few others) | same table |
| **Memory (preview)** | **Not supported.** The memory region list has East US 2 but not East US. This explains the portal message "Memory is not available in this project region". | [memory page](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory) |
| Model availability | Per model; check the deployment catalogue | [model regions](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability) |

Options if memory is needed: create a new Foundry resource and project in a memory-supported region (for example East US 2, Sweden Central, Australia East), redeploy models, recreate connections and tools. Region cannot be changed on an existing resource. Memory also needs an Azure OpenAI chat model plus an embedding model in that region.

If the data must stay inside a geography, also check deployment type: Global Standard may process prompts in any region ([09](09_FOUNDRY_PLATFORM_AND_SERVICES.md)).

## Part C. IAM: who can do what

### C1. The scopes and the roles in play

Scopes from widest to narrowest: subscription, resource group, Foundry resource, project, individual agent. A role assigned at a wider scope is **inherited**. The Foundry portal shows inherited roles as "Inherited access, View only"; change them in the Azure portal.

Foundry roles ([source](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry)):

| Role (formerly) | Build in project | Manage models | Publish agents | Assign roles | Call agent endpoints |
| --- | --- | --- | --- | --- | --- |
| Foundry Agent Consumer | no | no | no | no | yes |
| Foundry User (Azure AI User) | yes | no | no | no | yes |
| Foundry Project Manager | yes | no | yes | Foundry User only | yes |
| Foundry Account Owner | no | yes | no | Foundry User, ACR, monitoring roles | no |
| Foundry Owner | yes | yes | yes | Foundry User, ACR, monitoring roles | yes |
| Azure **Owner** | no (control plane only) | yes | yes | any role | no |
| Azure **Contributor** | no | yes | no | no | no |

Role definition IDs (use IDs in code, names were renamed): Foundry User `53ca6127-db72-4b80-b1b0-d745d6d5456d`; Foundry Owner `c883944f-8b7b-4483-af10-35834be79c4a`; Foundry Account Owner `e47c6f54-e4a2-4754-9501-8e0985b135e1`; Foundry Project Manager `eadc314b-1a2d-4efa-be10-5d325db5065e`; Foundry Agent Consumer `eed3b665-ab3a-47b6-8f48-c9382fb1dad6`.

Do **not** use roles starting "Cognitive Services" (except Cognitive Services Usages Reader at subscription scope for quota views) and do **not** use Azure AI Developer for Foundry work.

### C2. What the project's Users tab showed (roles only)

| Principal | Role | Scope | Access type |
| --- | --- | --- | --- |
| The JB account owner (member of the host tenant) | Owner | Subscription | Inherited |
| Two consultants (guest accounts, `#EXT#`) | **Contributor** | Subscription | Inherited |
| The same two consultants | **Foundry Owner** | Resource group | Inherited |

Reading it:
1. The Foundry resource sits in **JB's tenant**. The consultants are **B2B guests** there and still have full Foundry access through Azure RBAC. Guests are blocked from Copilot Studio ([01](01_ADMIN_AND_ENVIRONMENTS.md)) but not from Foundry.
2. Foundry Owner already covers build, deploy, publish and role assignment. **Contributor at subscription scope is extra and broad** (can create and delete resources across the subscription). Candidate to remove.
3. Everything is inherited; nothing is assigned directly at resource or project scope.

### C3. Recommended target model for this project

| Persona | Role | Scope |
| --- | --- | --- |
| Subscription owner | Owner | Subscription (no change) |
| Lead builder(s) | Foundry Project Manager (publish, build) or keep Foundry Owner if they also manage models | Foundry resource |
| Other builders | Foundry User | Project (plus Reader on the resource) |
| People who only chat with the agent | Foundry Agent Consumer | Project, or the single agent |
| Project managed identity | Foundry User | Foundry resource |
| Agent identity (prompt agent calling tools) | Foundry User | Project |
| Finance or audit viewers | Reader | Resource |

Additional roles by task: Cognitive Services Usages Reader (subscription) to see quota; Log Analytics Reader on Application Insights to view traces (Part G); Search Index Data Contributor and Search Service Contributor for Azure AI Search ([10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md)).

### C4. How to assign (three ways)

**Foundry portal:** Manage, Project details (or Resource details), **Users** tab, **Add user**. Shown only if you can assign roles.

**Azure portal:** open the Foundry resource, **Access control (IAM)**, **Add**, **Add role assignment**, choose the role, **Members**: user, group or service principal (or managed identity), select, **Review + assign**. Use **Check access** to verify. Wait a few minutes.

**Azure CLI** (needed for Foundry Agent Consumer at project or agent scope, because the Azure portal only assigns it at account scope):

```azurecli
az role assignment create --role "eed3b665-ab3a-47b6-8f48-c9382fb1dad6" \
  --assignee-object-id "<principalId>" --assignee-principal-type User \
  --scope "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>/projects/<project>"
# agent scope: append /agents/<agentName>
```

Rules of thumb: prefer groups over individuals; guests need a **group or direct assignment in the host tenant**; remove access by deleting the assignment in IAM; API keys ignore all of this.

### C5. Verify

1. Resource, Access control (IAM), **Check access**, search each user, the project managed identity and the agent identity.
2. Confirm Foundry User on the **resource** scope for the managed identity: model inference needs it at account scope; a project-only assignment does not authorise inference.
3. Test as a low-privilege user: open the agent endpoint and the Playground.

## Part D. Model deployments (what exists, what is missing)

The Guardrails table listed three deployments: `claude-opus-5`, `claude-opus-5-5` and `text-embedding-3-small`. There is **no GPT chat deployment**, which causes three visible gaps:

| Gap | Where it showed |
| --- | --- |
| Optimization has no model | Agent, **Optimize** tab: "No supported optimization model. Deploy a supported model (for example GPT-5)". |
| AI-assisted evaluators need a judge model | Evaluations need an Azure OpenAI connection with a GPT deployment such as `gpt-4.1-mini` ([evaluation page](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluate-generative-ai-app)). |
| Memory needs an Azure OpenAI chat model | Plus a supported region (Part B). |

Steps to add one: **Build**, **Models** (or the Optimize tab's **Deploy a model**), pick a GPT model available in East US, choose a deployment type (Global Standard is pay per token and may process outside the region), name it, set quota. Deploying needs control-plane rights: Foundry Owner, Foundry Account Owner, or Contributor. Check **Manage, Quota** first. Some GPT-5 models need registration for access.

## Part E. Guardrails (Operate, Compliance)

Path: top bar **Operate**, left nav **Compliance**, tab **Guardrails** (preview). Filters: subscription, project, date range. Tabs beside it: Policies, Security posture, Data security and governance.

State seen (per model deployment, all three the same):

| Control | State |
| --- | --- |
| Content harms | On |
| Jailbreak | On (prompt only) |
| Indirect prompt injections | **Off** |
| Spotlighting | Off |
| Profanity (blocklist) | Off |
| Protected materials code | Off |
| Protected materials text | On (completion only) |

These are the **model-level** (default) settings. Remember from [11](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md): an agent uses its own guardrail if one is assigned, which completely replaces the model's.

Step by step:
1. **Guardrails** in the Build left nav (or Operate, Compliance), create a guardrail. Needs Foundry Account Owner or Owner.
2. Add controls for the agent: user input and output for harm categories and prompt attacks; **tool call and tool response** for indirect attacks (injected text in tool results) and PII (the data agent can return personal data).
3. Choose action **Annotate and block** (the only option for agents).
4. **Assign** the guardrail to `jbnewsletteragentv1` (agent Playground, Guardrail section) and to the deployments you want.
5. Test with a blocked-style prompt and a normal prompt; check Traces.
6. Do not rely on Spotlighting or Groundedness for agents (not supported there).

## Part F. Monitoring: Application Insights (Agent, Insights or Monitor, Settings)

The Monitor settings dialog showed everything disabled: App Insights resource **Not connected**, Insights, Recurring evaluations, Scheduled red teaming runs, Evaluation alerts.

Steps ([tracing setup](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-setup)):
1. In the banner or **Settings**, choose **Connect**, then search or **create new** Application Insights resource. (Alternative: Manage, Project details, Connected resources.) Extra Azure Monitor charges apply.
2. Server-side tracing turns on automatically after connecting; generate agent traffic; allow a few minutes.
3. Grant **Log Analytics Reader** to people who must read traces, on the Application Insights resource (and the linked Log Analytics workspace for workspace-scoped queries). Add **Privileged Monitoring Data Reader** for protected content.
4. For trace-based and scheduled evaluation, give the **project managed identity** Reader on Application Insights ([evaluation permissions](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/evaluation-permissions)); if Entra-only ingestion is used the ingesting identity needs Monitoring Metrics Publisher.
5. Then enable, in order: Insights, Recurring evaluations, Evaluation alerts, Scheduled red teaming.

**Privacy notice in the dialog:** traces may contain personal data and customer content. Anyone with Log Analytics Reader on the connected resource can read them. For this agent, answers can include contact details from Fabric, so restrict that role.

## Part G. Evaluations (Evaluations, Create)

The wizard in the screenshot has six steps: **1 Target** (Agent, Model, Dataset), **2 Scope**, **3 Frequency**, **4 Data**, **5 Criteria**, **6 Review**. The agent target list showed the prompt agent with a version picker (v7 selected). Frequency is the recurring option (one-off or scheduled), which also needs Application Insights and the project managed identity roles above.

Steps:
1. Prerequisites: the GPT judge deployment (Part D) and Foundry User on the project and resource.
2. Target: Agent, tick the agent and the version.
3. Scope: individual turns for tool debugging; full conversations (preview) for end-to-end.
4. Frequency: once while building; recurring after go-live.
5. Data: your known-answer dataset (CSV or JSONL with `query` and optional `ground_truth`), synthetic data, or existing traces.
6. Criteria: Tool Call Accuracy, Groundedness, Relevance, Task Adherence, plus the four safety evaluators; compare answers to the warehouse by hand.
7. Review and submit; open results from the Evaluation list; repeat after every instruction, tool, model or guardrail change.

Evaluation jobs use Entra: if an evaluation calls a deployment, **Foundry User at the account scope** is required.

## Part H. Publishing (agent Details, Publish dropdown)

The Details page offers **Publish** with: Set up routine, Preview web app, Teams and Microsoft 365 Copilot, Details. The agent shows **Running**, **Active version Latest (version 7)**, an **Entra agent identity** and **blueprint**, a **Responses protocol** endpoint ("People with Azure RBAC permissions can access"), an A2A protocol option, and channels (Teams and Microsoft 365 Copilot unpublished, Preview web app active, Routines).

Facts and cautions ([agent applications](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/agent-applications), [publish](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot)):
1. **Who can publish:** Foundry Project Manager (minimum) on the Foundry resource, or Foundry Owner. A disabled Publish button usually means a missing resource-scope role. (One docs page lists Foundry User; treat the stricter reading as safe.)
2. **Identity changes on publish.** Before publishing all agents share the project's agent identity; a published agent gets its **own** identity. **Reassign every downstream permission** (search, storage, any tool backend) to the new identity or tool calls fail.
3. **Who can invoke a published agent:** Foundry Agent Consumer covers the plain project endpoint but the docs say it does not grant invoking an Agent Application; use **Foundry User** on the Agent Application resource for callers.
4. **Teams and Microsoft 365 channel access:** *Just you* applies BotServiceRbac (only people with the Azure permission to call the agent); *People in your organization* applies BotServiceTenant (anyone in the tenant). Choose deliberately for data-bearing agents.
5. **Per-user Fabric access through Teams:** community reports say publishing to Microsoft 365 Copilot uses the Activity Protocol, which may not forward the user's OAuth token, so per-user identity passthrough may not work. Unverified in official docs; test with a non-author before announcing. If it fails, the published agent would query Fabric as a fixed identity (not supported for the Fabric tool) or fail.
6. **Routines** (scheduled runs) run unattended and so face the same identity question.
7. Guests in JB's tenant can build in Foundry, but they cannot use Copilot Studio.

## Part I. Closing checklist for this project

- [ ] Region confirmed East US; decide whether memory justifies a new resource in a supported region.
- [ ] Remove or justify subscription-level Contributor for the two guest builders.
- [ ] Add Foundry User for the project managed identity on the resource (verify in Check access).
- [ ] Deploy a GPT judge model (also unblocks Optimize).
- [ ] Create an agent guardrail with tool call, tool response and PII controls; assign to the agent.
- [ ] Connect Application Insights; limit Log Analytics Reader; then enable Insights and evaluation alerts.
- [ ] Run an evaluation on the known-answer set; repeat after changes.
- [ ] Before publishing: grant roles to the published identity, choose channel access mode, test as a non-author.
- [ ] Keep the API key out of code and notes; use Entra authentication.
