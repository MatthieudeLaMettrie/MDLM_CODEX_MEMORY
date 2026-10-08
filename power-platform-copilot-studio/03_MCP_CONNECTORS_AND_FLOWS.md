# MCP servers, connectors and flows

Checked against Microsoft Learn on 2026-10-08. Part of the [Power Platform / Copilot Studio guide](README.md). No server was connected and no flow was run.

## How tools reach an agent

```text
Agent ─► Tool ─┬─► MCP server (URL, tools discovered)
               ├─► Power Platform connector (fixed actions)
               ├─► Flow (agent flow or Power Automate cloud flow)
               └─► Connected agent (another agent)
```

MCP access in Copilot Studio runs on Power Platform connectors, so **data policies apply to MCP too** ([source](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)). Only **Streamable HTTP** transport is supported; SSE support ended in August 2025.

## Add an MCP server (wizard)

Tools → **Add a tool** → **New tool** → **Model Context Protocol**. Fill in:

- **Server name**
- **Server description**: the orchestrator reads it to decide when to call the server, so say what it does and when to use it.
- **Server URL**
- **Authentication** and **configuration type**

### Authentication

| Option | Behaviour | Fields |
| --- | --- | --- |
| None | No credentials. | None. |
| API key | The agent's user supplies the key when creating the connection; the agent sends it on each call. | **Type**: Header or Query. Name of the header or query parameter. |
| OAuth 2.0 | Each user signs in and grants permission; no password sharing. | Configuration type below. |

### OAuth 2.0 configuration types

| Type | Use when | You enter |
| --- | --- | --- |
| **Dynamic discovery** | The server supports dynamic client registration (DCR) **and** publishes discovery metadata. Simplest. | Nothing beyond the URL. |
| **Dynamic** | Server supports DCR but not discovery. | **Authorization URL**; **Token URL template**. A callback URL may appear. |
| **Manual** | Server needs a pre-registered app. | **Client ID**, **Client secret**, **Authorization URL**, **Token URL template**, **Refresh URL**, optional **Scopes**. A callback URL appears; register it with the identity provider. |

Then: **Next** → on *Add tool* choose **Create a new connection** (or reuse one) → **Add to agent**.

Worked example (Manual, Entra-protected company server): register an app in Entra, copy the **callback URL** from Copilot Studio into its redirect URIs, create a client secret, then paste client ID, secret, the tenant's `/oauth2/v2.0/authorize` and `/token` URLs and the API scope. Keep the secret in a vault, not in notes.

### Custom connector alternative

Tools → Add a tool → New tool → **Custom connector**, then import an OpenAPI (Swagger 2.0) file. For a Streamable MCP server the path carries `x-ms-agentic-protocol: mcp-streamable-1.0`:

```yaml
swagger: '2.0'
info: {title: Contoso, description: MCP spec, version: 1.0.0}
host: contoso.com
basePath: /
schemes: [https]
paths:
  /mcp:
    post:
      summary: Contoso Lead Management Server
      x-ms-agentic-protocol: mcp-streamable-1.0
      operationId: InvokeMCP
      responses: {'200': {description: Success}}
```

Edit a connection later in Power Apps or Power Automate → Custom connectors. You can also register a bring-your-own MCP server in Agents 365 so it appears for approved use.

## Connectors (Add a tool → Connectors)

A connector wraps an API as a set of actions. A **connection** holds the credentials. The three highlighted in the 2026-10-08 screenshot:

| Connector | What it does | Typical auth | Example |
| --- | --- | --- | --- |
| Azure AI Foundry Agent Service | Calls a Foundry agent (thread, message, run). | Entra sign-in; same tenant as the project. | Pass "top 10 stores by sales last month" to a Foundry agent that holds the Fabric tool. |
| Azure AI Foundry Inference | Calls a deployed model directly (chat, embeddings). No agent logic. | Endpoint plus key, or Entra. | Classify an email as complaint, query or order and return JSON. |
| Azure AI Search | Queries a search index (keyword or vector). | Endpoint plus query key, or Entra. | Return the best policy passages for "damaged goods returns". |

I described the exact authentication choices from product knowledge, not from a connector reference page; confirm each in its connector documentation before relying on it.

### MCP versus connector

| | MCP server | Connector |
| --- | --- | --- |
| Tool list | Discovered from the server | Fixed in the connector |
| Updates | New tools appear without editing the agent | Version changes need maintenance |
| Governance | DLP via connector | DLP via connector |
| Choose when | The vendor provides an MCP server | A certified connector already exists |

## Flows ("Workflows")

The Workflows item in the navigation holds **agent flows**; Power Automate cloud flows can also be called from agents. Copilot Studio's licensing page lists flows (automated, instant, scheduled) as a standalone-plan capability, while the Teams plan only uses cloud flows inside topics ([comparison](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions)).

| Use a flow when | Use agent reasoning when |
| --- | --- |
| Steps must run in a fixed order | The path depends on the question |
| You write to a system, approve, or schedule | You answer from knowledge or data |
| You need an audit trail of each step | You need flexible language handling |

Scheduled flow runs count as environment activity, which helps keep a developer environment from being disabled ([activity rules](https://learn.microsoft.com/en-us/power-platform/admin/automatic-environment-cleanup)). Do not rely on a dummy flow as a design; it can hide a dead environment.

Premium connectors inside flows need premium licensing. Details of agent-flow design and limits were not verified in this guide.

## Apps

Power Apps live at make.powerapps.com in the same environment. They are not a Copilot Studio tool type in the screenshots seen. See the Apps note in [01](01_ADMIN_AND_ENVIRONMENTS.md).
