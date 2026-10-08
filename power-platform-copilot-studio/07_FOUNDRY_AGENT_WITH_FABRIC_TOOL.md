# Foundry agent with the Fabric data agent tool

Checked against Microsoft Learn on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md); extends [02](02_FABRIC_AND_DATA_AGENTS.md) Route B with the new Foundry portal. The Fabric tool is **preview**. Nothing here was executed: the steps come from the cited pages and from four screenshots of the user's own project (no IDs recorded).

## Starting state (from the screenshots)

| Item | Seen |
| --- | --- |
| Portal | New Foundry (toggle on), project `jb-newsletter` |
| Agent | `jbnewsletteragentv1`: type **Prompt**, **Running**, version 1, text interaction, created 2026-10-09 |
| Agent identity | An Entra agent identity and blueprint exist; endpoint access is "People with Azure RBAC permissions" |
| Channels | Teams & Microsoft 365 Copilot (not yet published), preview web app (active) |
| Left nav **Knowledge** | Foundry IQ: connects an **Azure AI Search** resource. **Not** the place for Fabric. |
| Fabric item | A published data agent over a warehouse. Its Settings → **Model Context Protocol** tab is populated, so it is published and exposes an MCP server. |
| Region | Foundry endpoint is in East US 2. Check the Fabric capacity region against the data agent's source regions. |

## Pre-flight checklist

1. Same **tenant** for Fabric and the Foundry project, same signed-in account.
2. Fabric capacity **F2 or higher** (or P1+), cross-geo AI tenant settings enabled if needed.
3. Data agent **tested and published** with a clear description.
4. Data agent and its data sources on capacities in the **same region** (a query fails otherwise).
5. You and every end user: Azure RBAC **Foundry User** (or higher) on the project (formerly Azure AI User).
6. You and every end user: at least **Read** on the data agent plus minimum rights on each source (warehouse: `SELECT`; semantic model: Read, with RLS/CLS still applied; lakehouse: Read; KQL: Reader).
7. **User identity** authentication. Service principals are not supported for the Fabric data agent.

## Steps

### 1. Copy the two GUIDs from Fabric

Open the data agent in Fabric. The browser URL looks like `.../groups/<workspace_id>/aiskills/<artifact_id>...`. Copy both GUIDs exactly. A wrong or edited value gives *Invalid workspace ID format* or *Artifact Id should not be empty and needs to be a valid GUID*.

### 2. Add the tool to the agent

1. Foundry portal → project **jb-newsletter** → **Build** → **Agents** → open `jbnewsletteragentv1`.
2. In the agent's **Playground**, add a tool and choose **Microsoft Fabric data agent** (the docs say "add the Microsoft Fabric data agent tool"; the exact menu labels in the new portal may differ, so use the **Tools** catalog if it is not in the agent's tool list).
3. Enter `workspace_id` and `artifact_id`. Complete setup. Foundry **creates the project connection** for you; you do not need the management center.
4. Copy the connection **ID** from the tool configuration (needed only for code).
5. Do **not** use left-nav Knowledge for this.

### 3. Give the agent tool guidance

Add to the instructions, then save (this creates a new agent version):

```text
For questions about newsletter articles, publishing cadence, article counts or
trends, use the Fabric tool. Always answer from its result. If it returns no
rows, say so; do not guess. State the date range the data covers.
```

Adapt the wording to the real data agent. The docs recommend explicit guidance such as "For customer and product sales data, use the Fabric tool", and you can force use with `tool_choice`. The model you pick only orchestrates and writes the reply; it does not change the model Fabric uses.

### 4. Test

1. In the Playground, ask a question with a known answer (compute it first in the warehouse).
2. Open **Traces** and confirm the Fabric tool was called.
3. Repeat as a second user who has Fabric access, and as one who does not. Expected: the second gets an `unauthorized` style failure.

### 5. Optional: call it from code

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition, MicrosoftFabricPreviewTool,
    FabricDataAgentToolParameters, ToolProjectConnection,
)

project = AIProjectClient(
    endpoint="<project endpoint>",            # https://<resource>.ai.azure.com/api/projects/<project>
    credential=DefaultAzureCredential(),
)
conn = project.connections.get("<fabric connection name>")

agent = project.agents.create_version(
    agent_name="jbnewsletteragentv1",
    definition=PromptAgentDefinition(
        model="<deployment name>",
        instructions="<instructions from step 3>",
        tools=[MicrosoftFabricPreviewTool(
            fabric_dataagent_preview=FabricDataAgentToolParameters(
                project_connections=[ToolProjectConnection(project_connection_id=conn.id)]
            )
        )],
    ),
)
openai = project.get_openai_client(agent_name=agent.name)
print(openai.responses.create(tool_choice="required", input="<question>").output_text)
```

Based on the docs' sample (SDK is preview; use the latest). The call runs as the signed-in user, so `DefaultAzureCredential` must resolve to a user, for example after `az login`.

REST alternative: a connection can be created by ARM `PUT .../connections/<name>?api-version=2025-04-01-preview` with `category` and `authType` `CustomKeys` and keys `workspace_id` and `artifact_id`.

## Alternative: the data agent as an MCP server

A published data agent is itself an MCP server exposing **one tool**. The URL is shown on the data agent's Settings → Model Context Protocol tab, or built as `https://api.fabric.microsoft.com/v1/mcp/workspaces/{WorkspaceId}/dataagents/{DataAgentId}/agent` ([Fabric page](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-mcp-server)). Facts:

- It supports MCP over streamable HTTP and **long-running tasks** (tasks extension).
- It does **not** support dynamic client registration, so the Foundry or Copilot "OAuth dynamic discovery" style will not work; the client must supply its own Fabric bearer token (scope `https://api.fabric.microsoft.com/.default`).
- Foundry's MCP page shows a project connection with `--auth-type user-entra-token` for a Fabric MCP endpoint using audience `https://analysis.windows.net/powerbi/api`. That example targets a different Fabric endpoint, so **the correct audience for the data agent URL is unverified**; test it.
- Use this route if you need tasks or want one tool surface shared across clients. Use the Fabric tool above first: it is simpler and documented for this exact case.

## What this means for unattended use

The Foundry page says service principals are not supported for the Fabric data agent, and the agent's own Entra identity is not a user. The Fabric MCP page says the token "can represent either a user identity or a service principal". These conflict. Until resolved, assume a **scheduled or unattended** newsletter run cannot rely on the Fabric tool; it needs a signed-in user, or a different route (for example querying the warehouse with an approved service principal).

## Publishing and channels

The Details page offered **Teams & Microsoft 365 Copilot → Publish**. Whether the Fabric tool's per-user pass-through works through that channel was **not verified**. Every end user would need Foundry User and Fabric access either way. Test with a non-author before announcing it.

## Troubleshooting

| Error or symptom | Cause | Fix |
| --- | --- | --- |
| `Artifact Id should not be empty and needs to be a valid GUID` | Bad connection values | Recreate the connection from the URL path. |
| `Invalid workspace ID format` | Edited GUID | Copy exactly. |
| `unauthorized` | User lacks data agent or source access, or wrong identity type | Grant access; use user identity. |
| `Cannot find the requested item` / `configuration not found` | Data agent not published or changed | Publish it; check sources. |
| Data agent missing or query fails | Different tenant, capacity or region mismatch | Same tenant; same-region capacities. |
| `Can't add messages to thread ... while a run is active` | Active run | Wait or start a new conversation. |
| Empty results | Question does not match data | Test in Fabric first. |
| Tool never called | Weak instructions | Add explicit guidance; use `tool_choice`. |
| Timeouts | Latency | Raise client timeout; retry with backoff; consider the MCP route's tasks. |

## Sources

- [Use the Microsoft Fabric data agent with Foundry agents](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric)
- [Data agent as Model Context Protocol server](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-mcp-server)
- [Connect agents to MCP server endpoints (Foundry)](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Consume a data agent in Foundry (Fabric docs)](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-foundry)
