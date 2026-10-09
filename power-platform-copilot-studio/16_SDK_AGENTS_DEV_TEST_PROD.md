# Code-first agents: dev, test, prod and publishing by SDK

Checked against vendor docs on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Companion to [15](15_DEV_TEST_PROD_AND_PUBLISHING.md) (portal-first process); this file covers the SDKs. Code was taken from the vendor pages and **not run**. Anything marked *(general practice)* is my engineering advice, not stated by the vendor page I read. Sources: [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart), [hosting](https://code.claude.com/docs/en/agent-sdk/hosting), [permissions](https://code.claude.com/docs/en/agent-sdk/permissions), [Foundry SDK quickstart](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code), [A2A tutorial](https://a2a-protocol.org/latest/tutorials/python/1-introduction/) and [specification](https://a2a-protocol.org/latest/specification/), [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents), [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), [persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [deploy](https://docs.langchain.com/oss/python/langgraph/deploy).

## 1. Which tool for which job

| Framework | What it is | Who runs the loop | Good for | Watch out |
| --- | --- | --- | --- | --- |
| **OpenAI Agents SDK** (`openai-agents`) | Lightweight Python agent runtime: agents, tools, handoffs, guardrails, sessions, tracing, MCP | Your process | Multi-agent handoffs with OpenAI models | Tracing defaults to OpenAI's platform; docs page has no deployment guidance |
| **Claude Agent SDK** (`claude-agent-sdk`, `@anthropic-ai/claude-agent-sdk`) | Claude Code's agent loop as a library (built-in file, shell and web tools, hooks, subagents, MCP, sessions) | A spawned `claude` CLI subprocess in your container | Coding, file and research agents that need a shell | Subprocess per session, local disk state, strong permissions needed |
| **Anthropic Client SDK** (`anthropic`) | Direct Claude API calls; you write the tool loop (or use the beta tool runner) | Your code | Small, controlled agents; custom loops | You build everything else |
| **Claude Managed Agents** | Anthropic-hosted agent loop and sandbox | Anthropic | No infrastructure to run | Hosted by a third party; check data policy |
| **Foundry SDK** (`azure-ai-projects` 2.x) | Create, version and call Foundry agents; OpenAI-compatible Responses and Conversations | Foundry service | Azure governed agents, Fabric data agent tool, Entra RBAC | Preview features; 2.x is incompatible with 1.x |
| **A2A** (`a2a` Python SDK) | Open protocol so agents from any framework call each other (agent card, tasks) | Each agent's own server | Cross-framework and cross-team agent calls | Auth and discovery are yours to secure |
| **LangChain** (`create_agent`) | Prebuilt agent loop with middleware (retry, PII, human approval) and structured output | Your process | Fast agents with many model providers | Version-pinning, API churn |
| **LangGraph** (`langgraph`) | Low-level graph orchestration with checkpointed state, long-running workflows, human-in-the-loop | Your process or LangSmith Deployment | Stateful, branching workflows that must resume | More code than create_agent |

Rule of thumb: Foundry when the client lives in Azure and needs Entra and Fabric; Claude Agent SDK for tool-using coding or document agents; LangGraph when state, branching and resumption matter; A2A to connect them; OpenAI Agents SDK when OpenAI models and handoffs are the centre.

## 2. The common lifecycle for every SDK

The same stages as [15](15_DEV_TEST_PROD_AND_PUBLISHING.md), with code-first specifics.

1. **Repo layout** *(general practice)*: `agent/` (code, prompts as files), `tests/` (unit tests for tools, evaluation dataset), `infra/` (Bicep or Terraform), `.github/workflows/`, `pyproject.toml` with pinned versions and a lockfile.
2. **Configuration by environment variables**, never code: model name, endpoints, tool URLs, data IDs. One `.env.example`, no secrets committed. Secrets live in Key Vault (or the platform's secret store) and are injected at deploy time.
3. **Dev**: run locally with a dev key or `az login`; sample data; tracing on.
4. **Unit tests**: tools are plain functions, so test them without a model. Mock the model for loop tests.
5. **Evaluation gate**: a fixed set of prompts with expected facts or rubrics; run it on every PR and before each release; keep results as artefacts. Use an LLM judge plus a few exact-match cases. Track cost and latency too.
6. **Test environment**: separate keys, separate data, separate quota. Run the evaluation again plus red-team prompts, a PII probe and an access test as a non-admin.
7. **Prod**: image built once, promoted by tag; manual approval; canary or a small group first *(general practice)*; rollback = redeploy the previous image tag.
8. **Operate**: tracing, cost per task, error rate, alert on spend and on repeated tool errors, prompt and model change log.

Cross-cutting rules: pin SDK versions (all of these move quickly); put a hard cap on turns and cost per task; log tool calls but not secrets; separate the identity that runs the agent from the identity of the user whenever possible; treat tool output and web content as untrusted input (prompt injection).

## 3. OpenAI Agents SDK

**Install and first agent** (from the docs):

```bash
pip install openai-agents
export OPENAI_API_KEY=sk-...
```

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

**Primitives:** Agent, Runner, function tools (schema from type hints, Pydantic validation), handoffs or agents-as-tools, guardrails (input and output checks that run in parallel and fail fast), sessions (memory), tracing, MCP tools. The SDK uses the Responses API for OpenAI models; use the Responses API directly if you want to own the loop.

**Dev to prod**
- Dev: local run with a dev key; inspect traces in the OpenAI dashboard (built in).
- Test: put guardrails on input (off-topic, PII) and output; evaluate with a fixed prompt set; trace review.
- Prod: the docs do not describe deployment. *(general practice)* Wrap `Runner.run` in an HTTP service (FastAPI), containerise it, run on Azure Container Apps, App Service or Kubernetes, keep the key in Key Vault, set a per-request turn limit, add auth in front.
- Data note: tracing sends run data to OpenAI by default; for Metcash and client work confirm the data policy or disable or redirect tracing before using client data. *(verify in the SDK tracing docs; not read here)*
- Channels: Teams, Slack and web all go through your own service; there is no built-in channel publisher.

## 4. Claude: Client SDK, Agent SDK and Managed Agents

Pick one of three:

| You want | Use |
| --- | --- |
| Call Claude from your own code and write the loop | Client SDK (`anthropic`), optionally the beta tool runner |
| Claude Code's agent loop and built-in tools inside your app | Agent SDK |
| Anthropic to host the agent loop and sandbox | Managed Agents |

**Agent SDK install and first run** (from the quickstart):

```bash
pip install claude-agent-sdk          # or: uv add claude-agent-sdk
npm install @anthropic-ai/claude-agent-sdk
export ANTHROPIC_API_KEY=your-api-key   # SDK does not read .env files itself
```

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

**Providers:** Anthropic API key, Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Google Vertex (`CLAUDE_CODE_USE_VERTEX=1`), **Microsoft Foundry (`CLAUDE_CODE_USE_FOUNDRY=1`** plus Azure credentials), Claude Platform on AWS. Anthropic does not allow third parties to offer claude.ai login for their products; use API-key methods.

**Dev**
- Start with read-only tools and `plan` mode; add tools one at a time.
- Use hooks (`PreToolUse`) to block or log tool calls; subagents for focused work; MCP for external systems; sessions to resume.

**Permissions for test and prod (important)**
- Evaluation order: hooks, deny rules, ask rules, permission mode, allow rules, then `canUseTool`.
- For an unattended agent use a fixed tool surface: `allowed_tools=["Read","Glob","Grep"]` with `permission_mode="dontAsk"` (anything else is denied), and remove dangerous tools with `disallowed_tools=["Bash"]`.
- `bypassPermissions` approves everything not denied, and `allowed_tools` does **not** restrict it. Never use it outside a sandbox. Subagents inherit it.
- Pass `permission_mode` explicitly; the default may now be auto mode, which changes behaviour for broad allow rules.
- Auto-approved tools skip `canUseTool`, so put must-run checks in a `PreToolUse` hook.

**Hosting (verified on the hosting page)**
- The SDK spawns one `claude` CLI subprocess per session; it owns a shell, working directory and transcripts on local disk. Starting size about 1 GiB RAM, 1 CPU, 5 GiB disk per agent.
- Session patterns: **ephemeral** (container per task, exits when done; `TASK_PROMPT` env, `max_turns`), **long-running** (HTTP or WebSocket service; `ClaudeSDKClient` in Python, `streamInput()` in TypeScript), **hybrid** (container hydrates from a `SessionStore` and persists back; required for any session that must survive restarts), **multi-agent container**.
- Transcripts are lost on restart unless you configure a `SessionStore`; `CLAUDE.md` memory and working files need a volume or sync.
- Tenants: set `setting_sources=[]`, disable auto memory, per-tenant `CLAUDE_CONFIG_DIR` and `cwd`, per-tenant egress rules.
- Network: outbound HTTPS to the provider and to your MCP endpoints; use an egress proxy with domain allow-list that also injects credentials; authenticate inbound at a gateway, not in the agent.
- Observability: OpenTelemetry via `CLAUDE_CODE_ENABLE_TELEMETRY=1` and the standard `OTEL_*` variables; prompts and tool inputs are not exported by default.
- Limits: no overall session timeout (use `max_turns`), memory grows over long sessions (recycle), cap subagent turns.
- Tokens cost far more than the container; track cost per session.

**Test:** evaluation set of tasks with checkable outcomes (file diffs, tests passing); run in a throwaway container with a copy of the data; assert no writes outside the working directory.

**Publish:** Agent SDK has no channel publisher. Put an HTTP service in front (Teams or Slack bot, web backend) and call `query()`/the client. Per-user identity and tool credentials stay outside the agent via a proxy. For Azure customers, Claude can also run through Foundry model deployments (see 5).

## 5. Azure Foundry SDK

**Install** (Python; 2.x uses the new Foundry projects API, incompatible with 1.x):

```bash
pip install "azure-ai-projects>=2.3.0" azure-identity
az login
```

Also available for C# (`Azure.AI.Projects`, `Azure.AI.Projects.Agents`, `Azure.AI.Extensions.OpenAI`), TypeScript (`@azure/ai-projects`), Java (`azure-ai-agents`) and REST (token scope `https://ai.azure.com/.default`).

**Chat with a model, create a versioned agent, converse** (from the quickstart):

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

project = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential(),
)

agent = project.agents.create_version(
    agent_name="your-agent-name",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that answers general questions",
    ),
)
print(agent.id, agent.name, agent.version)

openai = project.get_openai_client(agent_name="your-agent-name")
conversation = openai.conversations.create()
r = openai.responses.create(conversation=conversation.id, input="What is the size of France in square miles?")
print(r.output_text)
```

Fabric tool in code: see [07](07_FOUNDRY_AGENT_WITH_FABRIC_TOOL.md).

**Dev to prod with the SDK**
1. `create_version` is the build step: every call creates an immutable version. Script it from the repo, not from the portal.
2. Parameterise `endpoint`, `model` deployment name and tool IDs per stage ([15](15_DEV_TEST_PROD_AND_PUBLISHING.md) section 2).
3. Authenticate with `DefaultAzureCredential`: `az login` locally, a managed identity or OIDC federated credential in CI and prod. No keys.
4. Evaluate with the Foundry evaluators in CI against the test project.
5. Pin a version through the endpoint `version_selector` (REST PATCH) and publish an Agent Application: ARM `PUT` application then agent deployment ([15](15_DEV_TEST_PROD_AND_PUBLISHING.md) section 4.2). Callers need Foundry User on the application and use the `.../applications/{app}/protocols/openai` Responses endpoint; stateless, keep history yourself.
6. Teams and Microsoft 365 use the Activity protocol and Azure Bot Service, set by the publish flow.
7. Roll back by re-pointing to the previous version.

**Claude through Foundry:** Claude models can be deployed in a Foundry resource (as in the JB project). The Claude Agent SDK can use them with `CLAUDE_CODE_USE_FOUNDRY=1`. Region, quota and Global Standard processing rules still apply ([09](09_FOUNDRY_PLATFORM_AND_SERVICES.md)).

## 6. A2A (Agent2Agent) examples

**What it is:** an open protocol so agents built with different frameworks can discover and call each other. Key ideas from the spec:
- **Agent Card**: JSON document describing identity, skills, capabilities (`streaming`, `pushNotifications`, `extendedAgentCard`), endpoint(s) and security. Served at `/.well-known/agent-card.json`.
- **Task lifecycle**: active `SUBMITTED`, `WORKING`; interrupted `INPUT_REQUIRED`, `AUTH_REQUIRED`; terminal `COMPLETED`, `FAILED`, `CANCELED`, `REJECTED`.
- **Operations**: Send Message, Send Streaming Message, Get Task, List Tasks, Cancel Task, Subscribe, push-notification config, Get Extended Agent Card. Bindings: JSON-RPC, gRPC, HTTP+JSON.
- **Security schemes**: API key, HTTP auth, OAuth 2.0 (authorization code, client credentials, device code), OpenID Connect, mutual TLS.
- Spec version 1.0.0; clients send an `A2A-Version` header. Method names differ from older drafts, so pin the SDK version.

**Python SDK** (`a2a`, Python 3.10+; samples at `github.com/a2aproject/a2a-samples`). The exact pip package name was not shown on the page I read; check the repo README. Minimal server from the tutorial (the `HelloWorldAgentExecutor` is the tutorial's echo agent; your own executor calls your OpenAI, Claude, Foundry or LangGraph agent):

```python
import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from agent_executor import HelloWorldAgentExecutor
from starlette.applications import Starlette

skill = AgentSkill(id='echo_bot', name='Echo Bot', description='Acknowledges the request.',
                   input_modes=['text/plain'], output_modes=['text/plain'],
                   tags=['a2a'], examples=['hi'])

card = AgentCard(
    name='Hello World Agent', description='Just a hello world agent', version='0.0.1',
    default_input_modes=['text/plain'], default_output_modes=['text/plain'],
    capabilities=AgentCapabilities(streaming=True, extended_agent_card=True),
    supported_interfaces=[AgentInterface(protocol_binding='JSONRPC',
                                         url='http://127.0.0.1:9999', protocol_version='1.0')],
    skills=[skill],
)

handler = DefaultRequestHandler(agent_executor=HelloWorldAgentExecutor(),
                                task_store=InMemoryTaskStore(), agent_card=card)
routes = []
routes.extend(create_agent_card_routes(card))
routes.extend(create_jsonrpc_routes(handler, '/'))
app = Starlette(routes=routes)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=9999)
```

Client (reassembled from the tutorial steps):

```python
import asyncio, httpx
from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

async def main():
    async with httpx.AsyncClient() as http:
        card = await A2ACardResolver(httpx_client=http, base_url='http://127.0.0.1:9999').get_agent_card()
    client = await create_client(agent=card, client_config=ClientConfig(streaming=False))
    request = SendMessageRequest(message=new_text_message('Say hello.', role=Role.ROLE_USER))
    async for chunk in client.send_message(request):
        print(chunk)

asyncio.run(main())
```

**A2A dev to prod**
- Dev: run two agents locally, one as server (for example a Fabric/Foundry "data agent" wrapper, or a Claude research agent) and one as client; fetch the card, send a task.
- Test: replace `InMemoryTaskStore` with a durable store *(general practice, tutorial uses in-memory)*; test streaming, cancel, `INPUT_REQUIRED` handling, timeouts, auth failure; contract-test the card.
- Prod: HTTPS only; the card's `url` must be the public URL; declare `securitySchemes` and enforce them (OAuth 2.0 client credentials with Entra is the usual enterprise choice *(general practice)*); version the card; rate limit; log task IDs; treat remote agent output as untrusted input.
- Publish: register the card URL in your internal catalogue; consumers need only the URL and credentials. Foundry agents can also act as A2A tools ([10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md)); Copilot Studio connects through connected agents or MCP.
- Choose A2A when the other agent is owned by another team or runs on another framework; choose plain tool calls or MCP for simple functions.

## 7. LangChain

**Minimal agent** (docs; tools and middleware are supplied by you):

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import PIIMiddleware, HumanInTheLoopMiddleware

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(
    model="openai:gpt-5.5",            # provider:model; also e.g. "anthropic:claude-sonnet-5"
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
```

Features shown on the page: middleware (`ModelRetryMiddleware`, `ToolRetryMiddleware`, `PIIMiddleware`, `HumanInTheLoopMiddleware(interrupt_on={...})`), structured output via `response_format=` (Pydantic, read `structured_response`), model strings across providers, streaming with `stream_events`. The package install command was not shown on that page; use `pip install langchain` plus the provider package, and pin versions.

**Dev to prod**
- Dev: local runs; set `LANGSMITH_TRACING=true` and a LangSmith key for traces *(or send traces to your own OpenTelemetry backend if client data must stay in your tenant)*.
- Test: LangSmith datasets and evaluators or your own harness; add `HumanInTheLoopMiddleware` on write-type tools; PII middleware; retry middleware.
- Prod: wrap in FastAPI or deploy with LangGraph/LangSmith Deployment (section 8). Use a checkpointer if you need threads.
- Publishing: your service fronts Teams, Slack, web.

## 8. LangGraph

**Install and shape** (docs): `pip install -U langgraph`. A graph is a `StateGraph` over a state type (for example `MessagesState`) with nodes and edges `START -> node -> END`, then `compile()`. Benefits: durable execution (resume after failure), human-in-the-loop (inspect and edit state), memory, LangSmith tracing.

**Persistence (checkpointers)** (docs):

```python
from langgraph.checkpoint.memory import InMemorySaver
graph = builder.compile(checkpointer=InMemorySaver())
graph.invoke({"messages": [{"role": "user", "content": "Hi, my name is Bob."}]},
             {"configurable": {"thread_id": "thread-1"}})

# production
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string("postgresql://...")
checkpointer.setup()
```

- `InMemorySaver`: tests only. `SqliteSaver`: development. `PostgresSaver` / `AsyncPostgresSaver`: production. Same `thread_id` shares state; keep it under 255 characters for Postgres. In Azure use Azure Database for PostgreSQL with Entra auth or a vault-held secret.

**Dev to prod**
1. Dev: `InMemorySaver`, run locally, inspect traces.
2. Test: Postgres checkpointer in test, replay failed runs from a checkpoint, interrupt and resume tests, evaluation set, concurrency test with many `thread_id`s.
3. Prod options (from the deploy page):
   - **LangSmith Deployment** (cloud): repo on GitHub (public or private), LangSmith, Deployments, New Deployment, pick repo, Submit; build takes about 15 minutes; Studio to inspect; API URL from Deployment details; call with `langgraph-sdk` or `POST <URL>/runs/stream` with `X-Api-Key`; the assistant ID is the graph name defined in `langgraph.json`. Other modes named: hybrid, standalone server, self-hosted with control plane (details not read).
   - **Self-host**: containerise your own FastAPI around the compiled graph with a Postgres checkpointer on Azure Container Apps or AKS *(general practice)*. The `langgraph dev/build/up` CLI commands were not covered by the pages I read; check the LangGraph CLI docs before relying on them.
4. Roll out: new graph version behind the same URL; checkpoints saved by an older graph shape can break resumption, so version your state schema and migrate or drain open threads *(general practice)*.
5. Publish: Teams and Slack bots call the graph API with the user's thread ID; a website backend does the same; the graph can also be exposed over A2A or MCP.

## 9. Publishing patterns for code-first agents

| Target | Pattern |
| --- | --- |
| **Teams** | Teams SDK / Microsoft 365 Agents SDK bot in front of your agent, registered through Azure Bot Service; or publish a Foundry agent with the portal flow ([15](15_DEV_TEST_PROD_AND_PUBLISHING.md) 4.3). Bot handles auth, history, adaptive cards. |
| **Slack** | Slack app (Events API or Bolt) calling your service; approve scopes in the workspace; verify Slack signing secret; respond within Slack time limits and post asynchronously. |
| **Website** | Backend-for-frontend with session auth, rate limits and abuse controls; server-sent events for streaming; never expose model keys in the browser. |
| **Other third parties** | Webhook or REST gateway (API Management) with API keys or OAuth, usage metering, versioned contracts. |
| **Other agents** | A2A server or MCP server. |
| **Scheduled jobs** | Container job or function with a managed identity; hard turn and cost limits; alert on failure. |

Common hardening: central gateway for authentication; per-tenant isolation of state and files; secret manager and egress proxy; rate limits; content filters; audit log of tool calls; data retention; kill switch (feature flag) per channel.

## 10. Choosing for the JB newsletter agent

- Already working: Foundry prompt agent plus Fabric data agent tool. Keep it in Foundry, move creation into a script (`create_version`) and manage stages as in [15](15_DEV_TEST_PROD_AND_PUBLISHING.md).
- If the newsletter must run on a schedule with no user, put a small Python job (Foundry SDK or LangGraph for a multi-step draft, review, approve flow) under a managed identity; LangGraph fits because of checkpointed human approval before sending.
- Use A2A only if another team's agent (for example a CRM agent) must be called.
- Claude Agent SDK is not needed unless the agent has to read and write files or run code.
- OpenAI Agents SDK is not a fit unless JB wants OpenAI models; the Foundry resource has no GPT deployment today.

## 11. Unverified or not read

- OpenAI Agents SDK deployment, tracing data controls, guardrail code; OpenAI Python client details.
- Anthropic Client SDK tool runner code and Managed Agents setup.
- Pip package name of the A2A SDK, A2A Entra integration, durable task stores.
- LangGraph CLI and `langgraph.json` structure; LangChain install command; self-hosted LangSmith options.
- Microsoft 365 Agents SDK / Teams SDK specifics for custom bots.
- Pricing and rate limits of any service.
