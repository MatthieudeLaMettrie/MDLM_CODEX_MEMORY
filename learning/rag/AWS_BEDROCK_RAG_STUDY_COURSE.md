# AWS Bedrock Knowledge Bases, AgentCore, and RAG: study course

Checked against official AWS documentation on 2026-09-28. Companion to the [Azure](AZURE_FOUNDRY_RAG_STUDY_COURSE.md) and [GCP](GCP_AGENT_SEARCH_RAG_STUDY_COURSE.md) courses. Code is a documented starting point; no AWS resources or paid model calls were made.

## Outcome

Explain Bedrock's indexing and retrieval path, create and query a knowledge base, distinguish managed from customer-managed options, expose retrieval as an AgentCore tool, call an agent using that tool, and evaluate evidence, permissions, latency, and cost.

## 1. Name the components

| Component | Job | Key boundary |
|---|---|---|
| Amazon Bedrock Knowledge Bases | Connects data sources and retrieves evidence for RAG. | A knowledge base is not the agent. |
| Managed Knowledge Base | AWS manages storage, indexing, and retrieval infrastructure. | Native AgentCore Gateway connector and document ACL support. |
| Customer-managed Knowledge Base | You manage the vector store and more ingestion choices. | Supports `RetrieveAndGenerate`; different capabilities from managed KB. |
| Bedrock AgentCore Gateway | Exposes tools to agents through MCP, including managed KB retrieval. | Gateway authenticates and routes tool calls. |
| Strands Agents SDK | Defines and runs a Python agent with tools. | It can discover KB tools through Gateway. |
| Bedrock Agents Classic | Older service with `InvokeAgent`. | Closed to new customers; existing customers can continue using it. |

AWS documents the two knowledge-base types and the Agents Classic availability change. [Knowledge Bases overview](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), [InvokeAgent reference](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/invoke_agent.html).

## 2. Draw the RAG path

```text
INDEXING: S3 / connector -> parsing -> chunking -> embedding -> vector index
QUESTION: user -> KB retrieval -> relevant passages -> model or agent -> cited answer
AGENT: Strands agent -> AgentCore Gateway MCP tool -> managed KB -> evidence
```

For unstructured documents, ingestion parses, chunks, embeds, and indexes the data. A change to a source may require a sync before retrieval reflects it. Store source and access metadata and verify that deletions propagate. In a customer-managed KB, you choose the vector store; in a managed KB, AWS operates the retrieval infrastructure. [Ingestion](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-data.html), [sync](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-data-source-sync-ingest.html).

## 3. Choose a retrieval pattern

| Path | What it returns | Use it when |
|---|---|---|
| `Retrieve` | Evidence chunks. | You want to inspect retrieval or control generation yourself. |
| `RetrieveAndGenerate` | Answer plus citations. | You have a **customer-managed** KB and want one managed RAG call. |
| Managed KB `AgenticRetrieveStream` | Multi-step retrieval, trace events, and optional synthesized answer. | The question requires multiple retrieval steps. |
| AgentCore Gateway KB tool | MCP retrieval tool callable by your agent. | You want a current agent architecture over a **managed** KB. |

Do not apply the `RetrieveAndGenerate` code below to a managed KB: the API reference says it is unsupported there. AgentCore Gateway's native KB connector is supported for managed KBs, not customer-managed KBs. [KB retrieval APIs](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-retrieval.html), [Boto3 API note](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate.html), [Gateway connector](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html).

## 4. Lab A: create a tiny knowledge base

Use three authorized policy documents in an S3 bucket. In Bedrock, create a managed KB if available in your Region, attach S3 as a source, and start ingestion. Inspect the ingest job and test search with five questions before attaching an agent. Alternatively, create a customer-managed KB and record the embedding model, vector store, chunking policy, and sync process you chose.

Check how headings, tables, and page references survive chunking. AWS supports fixed-size, hierarchical, and semantic strategies, each with trade-offs. Include a question with no answer in the corpus and a document that should be restricted. [Create managed KB](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-create.html), [chunking](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html).

## 5. Lab B: direct Boto3 RAG call for a customer-managed KB

Use this path only after a customer-managed KB has completed ingestion and your IAM identity has the necessary Bedrock/model permissions. Put IDs in environment variables; do not hardcode credentials. `BEDROCK_MODEL_ARN` must refer to a model or inference profile supported for your Region and account. [RetrieveAndGenerate API](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate.html).

```powershell
pip install --upgrade boto3
aws configure sso
aws sso login

$env:AWS_REGION = "<region>"
$env:BEDROCK_KB_ID = "<customer-managed-kb-id>"
$env:BEDROCK_MODEL_ARN = "<model-or-inference-profile-arn>"
```

```python
import os
import boto3

client = boto3.client(
    "bedrock-agent-runtime", region_name=os.environ["AWS_REGION"]
)
response = client.retrieve_and_generate(
    input={"text": "What equipment does our remote-work policy cover?"},
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": os.environ["BEDROCK_KB_ID"],
            "modelArn": os.environ["BEDROCK_MODEL_ARN"],
        },
    },
)

print(response["output"]["text"])
for citation in response.get("citations", []):
    for source in citation.get("retrievedReferences", []):
        print(source.get("location"), source.get("content", {}).get("text"))
```

The returned citation references identify evidence used for answer spans. Keep the `sessionId` returned by the first call if you continue the same conversation; the service creates it on the initial request. [Boto3 response and session reference](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate.html).

## 6. Lab C: call an agent using a managed KB through AgentCore

Create a **managed** KB and an AgentCore Gateway with a managed-KB target. Bind its `Retrieve` tool to the KB ID and give the Gateway service role scoped `bedrock:Retrieve` permission. The caller needs permission to invoke Gateway. You can also expose `AgenticRetrieveStream` for multi-step retrieval. The target setup and IAM policies are in AWS's [connector guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html).

Install the Strands and SigV4 MCP client packages, then call the agent locally:

```powershell
pip install --upgrade strands-agents mcp-proxy-for-aws
$env:AGENTCORE_GATEWAY_URL = "https://<gateway-id>.gateway.bedrock-agentcore.<region>.amazonaws.com/mcp"
$env:AWS_REGION = "<region>"
```

```python
# ask_agent.py
import os

from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient

gateway = MCPClient(
    lambda: aws_iam_streamablehttp_client(
        endpoint=os.environ["AGENTCORE_GATEWAY_URL"],
        aws_region=os.environ["AWS_REGION"],
        aws_service="bedrock-agentcore",
    )
)

with gateway:
    tools = gateway.list_tools_sync()
    agent = Agent(
        tools=tools,
        system_prompt=(
            "Use the knowledge-base retrieval tool for policy questions. "
            "Cite supporting sources and acknowledge missing evidence."
        ),
    )
    print(agent("What equipment does the remote-work policy reimburse?"))
```

The Gateway provides the MCP tool; the agent calls it when answering. The exact tool name is configured by the Gateway target and is discoverable through `tools/list`. The SigV4 client pattern comes from AWS's [Strands integration guide](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-gateway-target.html). Verify the Strands model provider and Region support in your account before running the lab.

### Existing Bedrock Agents Classic users

An existing Classic agent that already has a KB attached can still be called with `boto3.client("bedrock-agent-runtime").invoke_agent(agentId=..., agentAliasId=..., sessionId=..., inputText=...)`; consume `response["completion"]` events and their citation attribution. This is a migration/maintenance path, since AWS says Classic is closed to new customers. [InvokeAgent reference](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/invoke_agent.html).

## 7. Evaluate and explain the result

Use the same ten questions as in the Azure and GCP modules. Log retrieved passages, source locations, answer support, abstention, retrieval permissions, latency, and cost. Compare single-step retrieval with agentic retrieval on the two-document question. Inspect tool calls and traces before adjusting the prompt. A cited answer still needs checking: a citation can point to a source that does not support the precise claim.

**Ready to progress:** you can explain managed versus customer-managed KBs, run one direct RAG call, invoke a current agent with KB retrieval through Gateway, diagnose one missing passage, and demonstrate access control on a restricted document.

## Official references

- [Knowledge Bases overview](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Retrieval APIs](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-retrieval.html)
- [AgentCore managed-KB Gateway connector](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html)
- [Connect Strands agent through Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-gateway-target.html)
- [Boto3 RetrieveAndGenerate](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate.html)
