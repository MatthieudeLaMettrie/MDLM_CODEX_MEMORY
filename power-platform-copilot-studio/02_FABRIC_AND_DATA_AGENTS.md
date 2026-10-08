# Agents on Fabric, Power BI semantic models and other databases

Checked against Microsoft Learn on 2026-10-08. Part of the [Power Platform / Copilot Studio guide](README.md). No Fabric, Foundry or Copilot Studio resource was created or tested. For authoring the semantic model and data agent itself, see the existing [Power BI semantic model agents guide](../guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md); this file covers the Copilot Studio and Foundry connection.

## Fabric is not a knowledge source

The "Add knowledge" dialog in Copilot Studio lists documents, websites, Dataverse, Azure DevOps, Confluence and other Copilot connectors ("Microsoft Graph only"). Fabric is absent by design. Fabric data is reached through a **Fabric data agent**, which Copilot Studio calls as a **connected agent** and Foundry calls as a **tool** (shown as *Knowledge* in the Foundry portal).

```text
User → Copilot Studio agent ──(connected agent)──► Fabric data agent ──► warehouse / lakehouse /
                                                                         semantic model / KQL / mirrored DB
User → Foundry agent ─────────(Fabric tool)───────► Fabric data agent ──► same sources
```

Supported sources for a data agent: warehouse, lakehouse, Power BI semantic model, KQL database, mirrored database, ontology. You need read access to the source.

## Decision table

| Need | Route | Why |
| --- | --- | --- |
| Natural-language questions over warehouse tables | Fabric data agent | It writes the query. Governed by the user's access. |
| Questions over a Power BI semantic model | Fabric data agent over the model | Semantic models are a supported source. Measures and relationships are reused. |
| Documents and wikis | Knowledge sources (SharePoint, OneDrive, uploads) | Cheapest and simplest. |
| Large unstructured corpus from OneLake | Azure AI Search index, then connector or knowledge | Search and RAG rather than SQL. |
| One fixed lookup or write | SQL connector or flow as a tool | Deterministic, but premium licensing. |
| Vendor system with an MCP server | MCP tool | Tools discovered automatically. See [03](03_MCP_CONNECTORS_AND_FLOWS.md). |
| No Copilot Studio licence | Foundry agent with the Fabric tool | Avoids Copilot Studio licensing. |

## Prerequisites (both routes)

From the [Foundry page](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-foundry) and the [Copilot Studio page](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-microsoft-copilot-studio):

1. Paid Fabric capacity **F2 or higher**, or Power BI Premium **P1 or higher** with Fabric enabled.
2. Fabric data agent tenant settings enabled, including **cross-geo processing and storing for AI** where your regions require it.
3. At least one supported data source with data, and read access to it.
4. The data agent is **tested, then published, with a rich description**.
5. Fabric and the consuming product are in the **same tenant**, signed in with the **same account**.
6. The user has at least read access to the data agent, and access to every underlying source.

Both pages warn that responses may leave Fabric's compliance boundary or region and fall under the other product's terms. Both features are in **preview**.

## Route A: Copilot Studio

Steps from the Fabric documentation:

1. Copilot Studio → select the **environment** → Create → **New agent**. Name and describe it.
2. Top pane **Agents** → **+ Add** → **Microsoft Fabric**.
3. Create or reuse the Fabric connection, then pick the published data agent and write a clear description of when to use it.
4. Select the connected agent and choose its authentication:
   - **User authentication:** each user's own identity reaches Fabric, so each user needs access to the data agent and the data.
   - **Agent author authentication:** the author's identity is used for everyone. Treat this as a permission-sharing decision.
5. Settings → Orchestration → turn on **generative AI orchestration**.
6. Test in the chat pane, then publish and add a channel.

Limits stated in the docs:

- A custom agent with a connected Fabric data agent is **not supported in Microsoft 365 Copilot** and is formally validated only for **Teams**.
- Shared users need read access to the data agent and its sources.
- Builders: the Fabric page says a Microsoft 365 Copilot licence plus a user licence; the Copilot Studio admin page lists tenant plus user licences. See the conflict note in [01](01_ADMIN_AND_ENVIRONMENTS.md).
- Community reports say the picker lists only agents in the same environment, and that connection failures return silently to "Not connected". Both are unofficial.

If the data agent is missing from the list: confirm it is published and running, you used the right account, same tenant, and workspace access.

## Route B: Foundry Agent Service

1. In Fabric, publish the data agent. Copy the URL `https://fabric.microsoft.com/groups/<workspace_id>/aiskills/<artifact_id>`.
2. In the Foundry portal → Agents → create or open an agent → **Add** knowledge → **Microsoft Fabric**.
3. **New connection.** Add `workspace-id` and `artifact-id` as custom keys and tick **Is Secret**. Name it and choose project or all-projects scope.
4. Write instructions saying when to use the Fabric tool. Test in the playground.
5. Roles: developers and end users need at least **AI Developer** RBAC in Foundry.

Behaviour: the agent uses the **end user's identity** (on-behalf-of) to query only data that user may access. The model you pick in Foundry orchestrates and writes the answer; it does not change the model Fabric uses. **Only one Fabric data agent per Foundry agent.** The page shows the Python SDK path (`azure-ai-projects` preview, `FabricTool(connection_id=...)`) and says to use the latest preview release. The page does not state model restrictions; verify the deployed model in the portal.

Never put workspace or artifact IDs into shared code or notes beyond what is needed; the connection stores them as secret keys.

## Working across two tenants (the JB case)

| Situation | Result |
| --- | --- |
| Fabric in JB's tenant, Copilot Studio in your tenant | Not supported. Connected agents and the Foundry Fabric tool require the same tenant and account. |
| Everything in JB's tenant | Supported. |
| Guest account for you in JB's tenant | Does **not** work for Copilot Studio (guests cannot access it). |

Practical choice for JB with no Copilot Studio licences: build a **Foundry agent with the Fabric tool** in JB's tenant, using their paid Fabric capacity and Foundry project. Add Copilot Studio only if Teams delivery justifies the licences. JB admin tasks: enable the data agent and cross-geo tenant settings, publish the data agent, grant users Fabric access and Foundry AI Developer, create you a member account.

## Other databases and sources

| Source | How | Notes |
| --- | --- | --- |
| Azure SQL, SQL Server | SQL connector as a tool, or mirror into Fabric | Premium connector licensing; user or shared connection. |
| Dataverse | Knowledge source | Honours Dataverse security roles. |
| Snowflake, Databricks, BigQuery | Mirror into Fabric, or use a connector or MCP server | Check connector availability and DLP first. |
| SharePoint, OneDrive, files | Knowledge | Not a database route. |
| Azure AI Search | Connector or index-backed knowledge | Needs an indexing pipeline. |

Do not describe a mirrored database as live. Mirroring has its own latency and cost; check the Fabric mirroring documentation for the specific source.

## Writing a good data agent description

The orchestrator chooses tools from descriptions. State the domain, tables or model, grain, time range and exclusions. Example for the JB case: "Answers questions about Birrell & Co weekly store sales from the MyTurn warehouse. Use for sales, units and store comparisons. Do not use for HR or finance questions."
