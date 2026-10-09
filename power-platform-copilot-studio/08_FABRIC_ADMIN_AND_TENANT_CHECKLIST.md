# Fabric admin settings and the same-tenant rule

Checked against Microsoft Learn on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Consolidates every prerequisite found so far for exposing a Fabric data agent to Foundry, Copilot Studio or any MCP client. Nothing was changed in any tenant.

## The same-tenant rule (most common blocker)

| Pair | Rule | Source |
| --- | --- | --- |
| Fabric data agent and Foundry project | Same Microsoft Entra tenant, same signed-in account | [Foundry page](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric) |
| Fabric data agent and Copilot Studio agent | Same tenant, same account | [Fabric Copilot Studio page](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-microsoft-copilot-studio) |
| Azure AI Search and the Foundry agent | Same tenant | [AI Search tool page](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search) |
| Foundry OAuth identity passthrough users | User's Entra tenant must match the project's tenant. Cross-tenant token exchange is not supported. | [MCP authentication page](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication) |
| Copilot Studio guests | Guests of a tenant cannot access Copilot Studio | [Licensing page](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing) |

How to check: the Fabric URL ends with `ctid=<tenant id>`. The Foundry portal URL ends with `tid=<tenant id>`. They must match. In the JB build both showed the same tenant ID, which is why the connection could work.

A related trap: the `ctid` value is the **tenant ID, not the workspace ID**. The workspace ID is the GUID between `/groups/` and `/aiskills/` in the Fabric URL. Pasting the tenant ID into the Foundry tool's Workspace ID field produces a valid-looking GUID that points nowhere.

## Fabric tenant settings (Fabric admin)

Path: Fabric portal, OneLake catalog, **Govern**, **Configurations**, **Tenant settings**. Needs a Fabric administrator. Changes can take up to one hour ([source](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-tenant-settings)).

| Setting | Why |
| --- | --- |
| **Users can use Copilot and other features powered by Azure OpenAI** | Required for the data agent. Can be set at tenant and capacity level. |
| **Capacities can be designated as Fabric Copilot capacities** | Lets capacity admins designate capacities for Copilot, including the data agent. |
| **Data sent to Azure OpenAI can be processed outside your capacity's geographic region, compliance boundary, or national cloud instance** | Required when the capacity's region is outside the EU data boundary and the US. |
| **Data sent to Azure OpenAI can be stored outside your capacity's geographic region, compliance boundary, or national cloud instance** | Same condition. The agent keeps conversation history across sessions for up to 28 days unless cleared; users can clear it any time. |

Scope each setting to a security group if you do not want it tenant-wide.

Compliance warning (Fabric docs): when a data agent is consumed from Foundry, Copilot Studio, M365 Copilot or as an MCP server, responses may leave Fabric's compliance boundary or region and fall under the other service's terms.

## Capacity and items

1. Paid capacity **F2 or higher**, or Power BI Premium **P1 or higher** with Fabric enabled. Trial capacity is not listed as supported.
2. The data agent and its data sources on capacities in the **same region**; otherwise queries fail.
3. At least one supported source with data: warehouse, lakehouse, Power BI semantic model, KQL database, mirrored database, ontology.
4. The data agent is **tested, then published**, with a rich description. An unpublished item is unreachable (404 or not found). When published it also becomes an MCP server with one tool, and its description becomes the tool description that clients read.

## Permissions per user

| Where | Minimum |
| --- | --- |
| Data agent | Read |
| Warehouse | `SELECT` on the tables |
| Lakehouse | Read on the item (and table access if enforced) |
| Power BI semantic model | Read; row-level and column-level security still apply (a community reply says Build is also needed; the Foundry page says Read) |
| KQL database | Reader role |
| Mirrored database | Read |
| Foundry project | **Foundry User** (formerly Azure AI User), or **Foundry Agent Consumer** for OAuth passthrough end users |

The query runs as the end user. Anything the user can read, the agent can surface. Review what the data agent exposes before sharing the agent (see the privacy lesson in [12](12_JB_NEWSLETTER_FIELD_LOG.md)).

## Authentication facts that explain most errors

| Route | Identity | Notes |
| --- | --- | --- |
| Foundry **Fabric data agent tool** (preview) | End user (on-behalf-of) | Simplest. Service principals not supported here. |
| Foundry MCP tool pointed at the data agent URL | Whatever the connection supplies | With no authentication configured: `401 TokenIsMissing`. Needs a Fabric IQ connection or a `user-entra-token` connection. |
| Direct MCP client (your own code) | User or service principal bearer token | Scope `https://api.fabric.microsoft.com/.default`. No dynamic client registration. |
| Copilot Studio connected agent | User authentication or agent author authentication | Teams validated; not supported in Microsoft 365 Copilot. |

Foundry connection audience for the data agent URL: `https://analysis.windows.net/powerbi/api`. Bring-your-own Entra app scope: `https://analysis.windows.net/powerbi/api/DataAgent.Execute.All` plus `offline_access`, with admin consent.

## Why region matters (Fabric side)

1. Data agent queries fail if a source sits on a capacity in a different region from the data agent.
2. Outside the EU data boundary and the US, the two cross-geo tenant settings are mandatory.
3. Every downstream consumer (Foundry, Copilot Studio) may process the response in its own region or terms.
4. Private networking: data agent supports tenant-level and workspace-level private link; a workspace-level link needs the workspace-specific host in the MCP URL.

## One-page pre-flight

- [ ] Tenant IDs match (Fabric `ctid` and Foundry `tid`).
- [ ] Four Fabric tenant settings reviewed; hour passed since enabling.
- [ ] F2+ capacity; sources co-located with the data agent.
- [ ] Data agent tested, described, **published**.
- [ ] Workspace ID taken from after `/groups/`, not from `ctid`.
- [ ] Users have Fabric read plus Foundry User.
- [ ] Decision made on sensitive tables and PII before sharing.
