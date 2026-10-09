# Microsoft Foundry: platform map, services and why region matters

Checked against Microsoft Learn on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Based on the architecture, agent limits and Fabric tool pages plus screenshots of the user's own project (no IDs recorded). Nothing was deployed.

## The portal and what it contains

The project used here runs in the **new Foundry portal** (the "New Foundry" toggle). Left navigation, grouped as the portal shows it:

| Group | Item | Purpose |
| --- | --- | --- |
| Create | **Agents** | Build and version agents (prompt agents, hosted agents), with Playground, Details, Traces, Insights (preview), Monitor, Evaluation, Optimize tabs. Also Routines and Workflows (preview). |
| Create | **Models** | Model catalogue and deployments. |
| Create | **Services** | Foundry tools such as Speech, Language, Vision, Content Understanding (I did not open this page; contents are inferred from the architecture page). |
| Create | **Tools** | Reusable tool definitions: Fabric data agent, MCP servers, toolboxes. See [10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md). |
| Create | **Knowledge** | Foundry IQ knowledge bases and indexes (Azure AI Search). |
| Create | **Memory** | Memory stores. |
| Create | **Guardrails** | Content safety controls. See [11](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md). |
| Create | **Data** | Datasets and files. |
| Optimize | **Evaluations**, **Fine-tune** | Quality testing and model customisation. |

Top bar: Home, Discover, **Build**, Operate, Manage, Docs.

## Resource model

Source: [Foundry architecture](https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture).

```text
Azure subscription
  Resource group
    Foundry resource  (Microsoft.CognitiveServices/accounts, kind AIServices)   <- governance: networking, security, model deployments, connections
      Project         (subresource)                                              <- development boundary: agents, files, evaluations, tools
    Connected resources, separate governance: Azure AI Search, Storage, Cosmos DB, Key Vault
```

- The Foundry resource shares the `Microsoft.CognitiveServices` provider with Azure OpenAI, Speech, Language and Vision, so existing policies and RBAC carry over.
- Azure AI Search lives under `Microsoft.Search`.
- Control-plane actions (create deployments, projects) are separate from data-plane actions (build agents, run evaluations).

## Services you can use alongside agents

| Service | What it does | Typical use |
| --- | --- | --- |
| Azure OpenAI and other Foundry Models | Reasoning and generation models, plus partner models | Agent brain, judge model for evaluations |
| Agent Service | Hosts prompt agents and hosted agents, tools, threads | The core of this guide |
| Azure AI Search | Index and retrieval, agentic retrieval | Knowledge over documents. See [10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md). |
| Content Understanding, Document Intelligence | Extract structure from documents, images, audio | Invoice or form ingestion before indexing |
| Speech (and Voice Live) | Speech to text, text to speech, voice agents | Voice agents (preview; 60 minute session limit) |
| Language, Vision | Classification, entity extraction, image analysis | Pre- and post-processing |
| Content Safety (via Guardrails) | Harm and attack detection | See [11](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md) |
| Fabric (data agent, Fabric IQ) | Governed analytics data | See [02](02_FABRIC_AND_DATA_AGENTS.md) and [08](08_FABRIC_ADMIN_AND_TENANT_CHECKLIST.md) |
| Application Insights, Azure Monitor | Tracing and metrics | Traces tab, Monitor tab, trace evaluation |

## Why region matters

A Foundry **project region** decides four things:

1. **Which agent features exist.** The Agent Service is regional; tools and models vary by region. Example from the docs: file search is unavailable in Italy North and Brazil South, voice agents are unavailable in Poland Central and Spain Central. The documented tool-by-region table shows the Fabric data agent as available in every listed region.
2. **Which models you can deploy.** A model must also exist in the same region as the project ([model region availability](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability)).
3. **Data residency.** Agent endpoints are regional and data is stored in the same region as the endpoint. Foundry does not do automatic cross-region failover; multi-region means separate resources and your own routing.
4. **Memory and preview features** are only offered in a subset of regions (see [10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md)).

Deployment type decides where the *inference* is processed:

| Type | Processing |
| --- | --- |
| Global Standard / Provisioned / Batch | Any Azure region, Azure-managed |
| Data Zone Standard / Provisioned / Batch | Within the US or EU data zone |
| Standard / Regional Provisioned | The deployment's own region |
| Developer | Any region, no residency guarantee, fine-tuned model evaluation only, 24 hour life |

The JB agent's model showed **Global Standard**, so prompts and completions may be processed outside the project's region. That is acceptable only if JB's data policy allows it.

Other region rules:
- With private networking the Foundry resource must be in the same region as its virtual network; AI Search, Storage and Cosmos DB can be elsewhere (with cost implications).
- Azure AI Search region fixes data residency and which features are available (semantic ranker, integrated vectorisation). Putting Search, Foundry and Storage in the same region avoids bandwidth charges.
- Customer-managed keys need Key Vault in the same region as the Foundry resource.
- Fabric: data agent and its sources must share a capacity region; see [08](08_FABRIC_ADMIN_AND_TENANT_CHECKLIST.md).

## Basic versus standard agent setup

| | Basic | Standard |
| --- | --- | --- |
| Threads, files, vector stores | Microsoft-managed storage, logically separated | Your Cosmos DB, Blob Storage, Azure AI Search in your subscription |
| Data residency control | Limited | Full |
| Use when | Prototypes | Production, compliance, private networking |

## Roles

| Role (formerly) | Typical holder |
| --- | --- |
| Foundry User (Azure AI User) | Developers and end users of agents |
| Foundry Agent Consumer | End users in OAuth passthrough (least privilege) |
| Foundry Project Manager | Creates connections for some Fabric IQ flows |
| Foundry Account Owner / Owner | Creates the resource, configures guardrails |

The agent's own **agent identity** also needs Foundry User on the project when it calls tools at runtime (prompt agents).

## Limits worth knowing

128 tools per agent; 1,000 versions per agent; 100,000 messages per thread; 512 MB per file for prompt agents; hosted-agent concurrent sessions 1,000 or 2,000 per region by default. Exceeding the version cap returns a terminal error: delete old versions.
