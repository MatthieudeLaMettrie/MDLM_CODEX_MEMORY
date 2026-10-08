# Admin and environments

Checked against Microsoft Learn on 2026-10-08. Part of the [Power Platform / Copilot Studio guide](README.md). Nothing here was executed in a tenant; every procedure is taken from the cited pages.

## The three admin surfaces

| Surface | URL | What you do there |
| --- | --- | --- |
| Microsoft 365 admin center | admin.microsoft.com | Buy and assign Copilot Studio licences. Allow Anthropic as an AI provider. |
| Power Platform admin center (PPAC) | admin.powerplatform.microsoft.com | Environments, environment groups, data policies (DLP), tenant settings, Managed Environments, Generative AI settings. |
| Copilot Studio | copilotstudio.microsoft.com | Build agents. Pick the environment first; everything you build lives in it. |

An environment is the container for agents, flows, connections and the Dataverse database. It belongs to one Entra tenant and one geography. Anything built in it can only use data sources deployed in the same environment ([overview](https://learn.microsoft.com/en-us/power-platform/admin/environments-overview)).

## Environment types

| Type | Purpose | Key limits |
| --- | --- | --- |
| Production | Permanent work. | Needs 1 GB free database capacity to create. Full control. |
| Sandbox | Dev and test. Copy and reset available. | Full control. |
| Trial | Short tests. | Expires after 30 days. One per user. |
| Developer | Personal, single-owner use. | Limited control. Security groups cannot be assigned. |
| Default | Shared by all users. | Every licensed user is a maker. Not for production. |
| Dataverse for Teams | Created by Teams apps. | Limited admin settings. |

Use Developer for learning. Use Sandbox or Production for anything shared (for example the JB agent).

## Worked example: a "Disabled" developer environment

Seen on 2026-10-08: environment **PDP Copilot Development** (Developer, Australia) showed State **Disabled**. History showed a **Disable** operation, *Initiated by SYSTEM*, on 2026-10-03, status Succeeded. The red banner about "adding Managed Environments" was a separate failed call and did not cause the disable.

Cause: automatic inactivity cleanup ([source](https://learn.microsoft.com/en-us/power-platform/admin/automatic-environment-cleanup)).

| Day (no activity) | Developer env | Managed developer env |
| --- | ---: | ---: |
| Warning emails | 23 and 27 | 53 and 57 |
| Disabled | 30 | 60 |
| Deletion warnings (days after disable) | 7 and 11 | 7 and 11 |
| Deleted (days after disable) | 15 | 15 |
| Recovery window after delete | 7 days | 7 days |

This environment was disabled on 10/3, so deletion is due about **10/18/2026** unless re-enabled.

**Re-enable:** PPAC → Manage → Environments → select the environment → **Re-enable environment**. Once an environment is disabled, *Trigger environment activity* is not shown; re-enabling is the only action. It needs an admin role (Global, Power Platform or Dynamics 365 administrator). Your screenshot's command bar showed only Delete and History, so refresh first and check the role.

**Recover a deleted one:** Environments → **Recover deleted environments** → select → **Recover** (7 days).

**What counts as activity:** launching an app, running a flow (including scheduled runs), chatting with an agent, creating or editing an app, flow, agent or custom connector, and environment operations such as copy or reset. Home-page visits and opening the designer do not count. You cannot turn the cleanup off. The *Last activity* column in the environment list updates once a day. Warnings go to the environment's system administrators and its creator.

## Roles

| Role | Where | Can do |
| --- | --- | --- |
| Global admin, Power Platform admin, Dynamics 365 admin | Entra | Create environments (when restricted), enable Managed Environments, re-enable environments. |
| Environment Admin | Environment | Manage all resources in that environment, set DLP, add makers. |
| Environment Maker | Environment | Create apps, flows, connections, custom connectors. |
| System Administrator | Dataverse | Full control of the database. Not automatically given to Power Platform admins in the default environment. |

Environment Admin and Maker do not grant access to the Dataverse data. That is a separate Dataverse security role.

To limit who can create environments: PPAC → Manage → Tenant settings → choose *Developer*, *Production* or *Trial environment assignments* → **Only specific admins** → Save. Environments created earlier stay manageable by their creators ([source](https://learn.microsoft.com/en-us/power-platform/admin/control-environment-creation)).

## Licensing (Copilot Studio)

From the [admin licensing page](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing):

1. **Tenant licence** ("Copilot Studio" in the M365 admin center). Bought by an admin. Cannot be assigned to a user.
2. **User licence** ("Copilot Studio User License", under Add-ons). Assign it to each person who builds or manages agents. Group-based assignment through an Entra security group is supported.
3. People who only *use* a published agent need no special licence.
4. **Guest users of your tenant cannot access Copilot Studio.** To build in another organisation's tenant you need a member account there, not a B2B guest.
5. **Trial:** you can build and test in the test chat but **cannot publish**. Self-service trial sign-up can be switched off with the `AllowAdHocSubscriptions` flag.
6. **Teams plan** (inside some Microsoft 365 plans): classic orchestration, Teams channel only, Dataverse for Teams environments, no premium connectors, no generative orchestration. Fabric data agents need generative orchestration, so this plan is not enough ([comparison](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions)).
7. Capacity is pooled across the tenant; per-agent consumption is visible, not tenant-level.

**Conflict to resolve:** the Fabric page says builders need a *Microsoft 365 Copilot licence and a user licence*, while the Copilot Studio page lists the tenant plus user licences above. Check the current Microsoft Copilot Studio Licensing Guide before buying anything for JB.

Forecast cost with the [agent usage estimator](https://microsoft.github.io/copilot-studio-estimator/). Per-credit prices were not verified for this guide.

## Managed Environments

Enable: PPAC → Environments → the **...** next to the environment → **Enable Managed Environments** ([source](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-enable)). Requires the Power Platform Administrator or Dynamics 365 Administrator role; Environment Admin is not enough. Dataverse is required for production, sandbox and trial types; developer environments do not need it. Gives usage insights, sharing limits, data-policy controls and a 60-day inactivity window for developer environments. The source and destination must match before copy or restore.

## Data policies (DLP)

Copilot Studio reaches external systems through Power Platform connectors, so a data policy that blocks a connector also blocks MCP servers and tools built on it ([source](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)). Plan this before blaming an agent when a tool fails to appear.

## External models (Claude and others)

From the [external model page](https://learn.microsoft.com/en-us/power-platform/admin/allow-llm-generative-responses) and the [subprocessor page](https://learn.microsoft.com/en-us/microsoft-365/copilot/connect-to-ai-subprocessor):

1. M365 admin center → Copilot → Settings → **AI providers operating as Microsoft subprocessors** → Anthropic → save and choose users. Needs AI Administrator or Global Administrator. The default differs by region: on in most commercial regions, off by default for EU/EFTA and UK.
2. PPAC → Environment groups → Rules → **External Models** (or the environment itself) → enable the model family.
3. If the toggle is visible but greyed, step 1 was not completed.
4. For cross-region processing: Environment → **Generative AI features** → Edit → **Move data across regions**. Data already moved cannot be pulled back by clearing the box.
5. Anthropic models in Copilot Studio are currently outside EU Data Boundary commitments, and FedRAMP is not achieved for them.

## Where are "Apps"?

Power Apps are not part of Copilot Studio. They are built at make.powerapps.com in the same environment, and the environment page lists them under **Resources → Power Apps**. The Copilot Studio left navigation shown in the screenshots (Home, Agents, Workflows) has no Apps item. I did not find documentation saying it should. If you cannot see apps, check the maker portal first, then your Power Apps licence and environment role.

## Troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Environment *Disabled*, History says SYSTEM | Inactivity cleanup | Re-enable within 15 days. |
| No *Re-enable* button | Missing admin role, or page needs refresh | Role in Entra; reload. |
| Cannot create an environment | Creation restricted to admins, or under 1 GB capacity | Tenant settings; capacity. |
| Model toggle greyed | Anthropic not allowed in M365 admin center | Step 1 above. |
| Tool or MCP server missing or blocked | Data policy | PPAC data policies. |
| Cannot publish | Trial licence | Standalone licence or pay-as-you-go. |
| Guest cannot open Copilot Studio | Guests unsupported | Create a member account. |
