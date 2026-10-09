# Foundry tools, knowledge (AI Search) and memory

Checked against Microsoft Learn on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Nothing was built except as recorded in [12](12_JB_NEWSLETTER_FIELD_LOG.md).

## Tools: what each is for

A **tool** gives the agent an action or data source. Add tools directly to an agent, or bundle them in a **toolbox**. Sources: [toolbox](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/toolbox), [limits and tool support](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/limits-quotas-regions).

| Tool | Use it when | Example |
| --- | --- | --- |
| **Fabric data agent** (preview) | Natural-language questions over warehouse, lakehouse, semantic model | "How many articles were published last month?" |
| **Fabric IQ** | Ontology, semantic model or data agent through a shared semantic layer; background mode for slow queries | Business entity questions across Fabric |
| **Azure AI Search** | Ground answers in your indexed documents with citations | Policy and procedure Q&A |
| **File search** | Search files uploaded to the agent (vector store) | A one-off PDF pack |
| **Web search** / Grounding with Bing | Current public information | News and market commentary |
| **Code interpreter** | Run Python in a sandbox, make charts, process files | Chart a CSV |
| **MCP** | Any remote MCP server; tools discovered automatically | GitHub, internal systems, Fabric data agent URL |
| **OpenAPI** | Call a REST API from its spec | Internal pricing API |
| **Function / Azure Functions** | Your own code | Custom business rule |
| **Agent-to-agent (A2A)** | Delegate to another agent | Specialist sub-agent |
| **Browser automation / Computer use** | Operate web UIs (limited regions and models) | Form-filling tasks |
| **SharePoint** | Search SharePoint content | Team documents |
| **Work IQ** (preview) | Microsoft 365 collaboration context | Meetings, chats |
| **Image generation** | Create images (needs `gpt-image-1` plus an orchestrator model) | Illustrations |
| **Tool search, Skills** | Toolbox-only: route by intent; reusable instructions | Large tool sets |

Practical rules from the docs:
- Add a clear **description** to every tool; the model uses it to choose.
- Tell the agent in its instructions when to use each tool; force with `tool_choice` while testing.
- Only one tool *without a name* of each type (web search, AI Search, code interpreter, file search) per toolbox.
- Tool availability depends on region **and** model. The documented tool-by-model table does not list Anthropic models, yet the Fabric tool worked with `claude-opus-5-5` in the JB project (see [12](12_JB_NEWSLETTER_FIELD_LOG.md)). Treat the table as incomplete for Claude, not as a ban, and test.
- Non-Foundry tools can incur cost and send data outside Foundry's compliance boundary.
- Each instruction or tool change creates a new agent **version**.

## Toolbox

A named bundle of tools exposed as one managed MCP endpoint: `{project_endpoint}/toolboxes/{name}/mcp?api-version=v1`.

- Versioned: first version becomes default; consumers always get the default; test a new version at the version-specific endpoint, then promote.
- Benefits: configure once, reuse across agents and any MCP client (Agent Framework, LangGraph and others), change tools without redeploying agents.
- Optional **guardrail** applies to the whole toolbox; **Tool search** lets the model find tools by intent instead of loading every definition.
- Prompt agents: the **agent identity** needs Foundry User; end users need it only for OAuth or user-token tools.
- Not needed for a single agent with a single tool. The Fabric data agent tool is not in the toolbox supported list (Fabric IQ is), and the portal's "Use in a toolbox" button looked disabled for it. Treat that as an inference.

## Knowledge

Knowledge is data an agent retrieves. Three ways in Foundry:

| Option | What it is | Best for |
| --- | --- | --- |
| **Foundry IQ knowledge base** | Managed, permission-aware, multi-source layer on Azure AI Search with agentic retrieval; sources include Blob, SharePoint, OneLake, web | Several agents sharing curated content, ACL enforcement |
| **Azure AI Search tool on an index** | Direct connection to one existing index | A single known index |
| **File search** | Per-agent vector store from uploaded files | Small, ad hoc document sets |

The portal's **Knowledge** page (screenshot) offers a **Foundry IQ resource**: pick an Azure AI Search resource, authentication type (API key shown), then Connect, or *Create new resource*. It is the AI Search route, **not** Fabric.

Memory is not knowledge: use memory for user-specific learned context, Foundry IQ for curated organisational content, file search for user-provided documents ([source](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory)).

### Set up Azure AI Search (step by step)

Sources: [create a search service](https://learn.microsoft.com/en-us/azure/search/search-create-service-portal), [AI Search tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search), [Foundry IQ](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq).

1. **Decide fixed properties first** (cannot change later): name (2-60 chars, lowercase letters, digits, dashes; endpoint `https://<name>.search.windows.net`), **region**, **tier**, compute type.
2. **Region:** choose one that supports the features you need (semantic ranker, integrated vectorisation, agentic retrieval) and ideally the same region as Foundry and your storage to avoid egress charges. Check the Search region and tier tables.
3. **Tier:** Free (one per subscription, no scaling, may be deleted if inactive, fine for a proof of concept and the Foundry portal quick start), Basic or Standard for production, Storage Optimized, Serverless Developer. Replicas: 2 for read SLA, 3 for read/write SLA.
4. **Create:** Azure portal, Create a resource, **Azure AI Search**, subscription, resource group, name, region, tier, Review and create (minutes).
5. **Authentication:** default is API keys. Switch to roles: Settings, Keys, choose *Both* until roles are assigned, then *Role-based access control*.
6. **Roles for keyless Foundry access:** give the Foundry account's system-assigned managed identity **Search Index Data Contributor** and **Search Service Contributor** on the search service.
7. **Create an index** that supports vector search: searchable retrievable `Edm.String` text fields, a searchable `Collection(Edm.Single)` vector field, and retrievable source URL and title fields for citations. Or let a knowledge source or the portal import wizard build it.
8. **Connect to Foundry:** either Knowledge, Foundry IQ resource, pick the search resource and auth type (portal flow), or create a project connection and note its ID (Management center, Connected resources). If public network access is off, the connection must use managed identity.
9. **Add to the agent:** add the Azure AI Search tool (or connect the knowledge base) and set `index_name` and, in code, `project_connection_id`. Default query type is `vector_semantic_hybrid`; others: `simple`, `vector`, `semantic`, `vector_simple_hybrid`.
10. **Test** with a question that has a known passage; check citations and Traces.

Limits: the AI Search tool targets **one index** per tool; the search resource and agent must share a tenant. For several indexes use multiple tools or connected agents, or a Foundry IQ knowledge base.

## Memory

Source: [What is Memory?](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory) (preview).

- A managed **long-term memory store**: extracts facts from conversations, consolidates them with an LLM, retrieves them in later sessions and devices.
- Three types, all on by default: **user profile** (stable preferences, retrieve at the start), **chat summary** (topics and threads, retrieve per turn), **procedural** (recurring routines).
- Management: item-level create, read, update, delete; store-level default TTL; direct remember or forget commands.
- Use via the **memory search tool** on a prompt agent (scope `{{$userId}}` resolves to the caller automatically) or the low-level Memory Store APIs (you set `scope` yourself).
- Limits: 100 scopes per store, 10,000 memories per scope, 1,000 search and 1,000 update requests per minute; **no VNet integration**.
- Security: memory can be poisoned by prompt injection; use content safety and adversarial testing. Use TTL and deletion for privacy.
- Cost: you pay for the chat and embedding models the store uses.

### Why memory is region- and model-dependent

1. It needs compatible **Azure OpenAI** chat and embedding deployments (examples use `gpt-5.2` and `text-embedding-3-small`).
2. It is available only in listed regions: Australia East, Brazil South, Canada East, East US 2, France Central, Italy North, Japan East, Korea Central, North Central US, Norway East, South Africa North, South India, Sweden Central, Switzerland North, UAE North, UK South, West US, West US 2, West US 3.
3. Both the chat and embedding models must be deployable in the project's region.

**Observed in the JB project (2026-10-09):** the Memory section showed two messages: *Memory is not available in this project region* and *Memory is currently supported only for Azure OpenAI models* (the agent used a Claude model). The second matches the docs. The first conflicts with the docs if the project is in East US 2, which the resource name suggests. The actual region was not verified. Check the Foundry resource's region in the Azure portal; if it is not on the list, memory needs a project in a supported region, and the agent needs an Azure OpenAI model.

## Use-case guide

| Goal | Combine |
| --- | --- |
| Newsletter agent over a Fabric warehouse | Fabric data agent tool, instructions, guardrail, evaluation set |
| Policy assistant over documents | Foundry IQ or AI Search tool, citations, guardrail |
| Support agent that remembers users | Memory (Azure OpenAI model, supported region) plus knowledge |
| Analyst agent that charts data | Fabric data agent plus code interpreter |
| Agent that acts in other systems | MCP or OpenAPI tools with approvals (`require_approval`) |
| Multi-agent workflow | A2A or toolbox plus connected agents |
