# Azure Foundry SDK, Azure AI Search, and RAG: study course

Checked against Microsoft documentation on 2026-09-28. This module supports the Azure stage of the [continuous AI curriculum](AI_STUDY_CURRICULUM.md). Work through the labs with a small collection of documents you are permitted to index. Code is a documented starting point; it has not been run against your Azure subscription.

## Outcome

By the end, you should be able to explain the indexing and question-answering pipelines, create and inspect a Search index, connect it to a Foundry agent, call that agent with the current Python SDK, and test whether answers are grounded and permission-safe.

## 1. Name the components correctly

| Component | Job | Remember |
|---|---|---|
| Azure AI Search | Indexes content and retrieves relevant passages using keyword, vector, hybrid, and semantic techniques. | It remains a distinct Azure service. |
| Microsoft Foundry | Hosts project-level access to models, agents, connections, and tools. | The project endpoint is the central SDK entry point. |
| Foundry Agent Service | Stores and runs agent definitions that can invoke tools. | An agent is the orchestration layer, not the document index. |
| Foundry IQ | Managed knowledge layer using Azure AI Search agentic retrieval and knowledge bases. | It builds on Azure AI Search. |
| Fabric IQ | Business analytics workload in Microsoft Fabric. | It is not a rename of Azure AI Search or Foundry IQ. |

Source: [Foundry IQ FAQ](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq).

## 2. Draw the two RAG pipelines

```text
INDEXING (offline or scheduled)
Files/records -> extraction/OCR -> cleaning -> chunking -> embeddings -> Search index
                                                        + metadata, source URL, permissions

QUESTION TIME (per request)
User question -> retrieval/filtering -> relevant chunks -> model/agent -> cited answer
```

**Indexing** makes content searchable. A chunk is a passage small enough to retrieve precisely but large enough to preserve meaning. Keep a stable document ID, chunk ID, title, source URL, timestamps, and access-control metadata. The vector is a numerical representation of the chunk used for similarity search. Indexers and skillsets can automate extraction, chunking, and vectorization; a push pipeline can prepare and upload the content yourself.

**Question time** starts with retrieval, not generation. Keyword search finds exact terminology; vector search finds semantic similarity; hybrid search combines both. Semantic ranking can reorder candidates. Only then should the model write an answer from the retrieved evidence. Citations should point to a real source, and the agent should say when evidence is insufficient. [RAG overview](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

### Design decisions to record

1. **Corpus and freshness:** Which source is authoritative? How often does it change? What deletes or updates old chunks?
2. **Chunking:** Do headings, tables, and document boundaries survive? Can a retrieved chunk answer a question alone or with limited neighbours?
3. **Search mode:** Compare keyword, vector, hybrid, and semantic ranking on the *same* questions.
4. **Permissions:** Filter by the caller's effective access before handing any passage to the model. Do not rely on prompt instructions for access control.
5. **Evidence:** Preserve source URLs and citation annotations. Verify citations refer to passages that support each claim.
6. **Operations:** Measure retrieval quality, answer quality, latency, token usage, and cost. Re-evaluate after content or model changes.

## 3. Classic RAG versus agentic retrieval

| Pattern | Retrieval path | Choose it when |
|---|---|---|
| Classic RAG | Your code sends a single Search query, selects passages, and calls the model. | You need a simple, fast, controlled pipeline or generally available features only. |
| Foundry agent + Search tool | The agent can query a connected index as a tool. | You want an agent over an existing Search index. |
| Foundry IQ / agentic retrieval | Knowledge sources feed a knowledge base; an LLM plans subqueries and returns structured grounding/citations. | Queries are complex, multi-source, or conversational, and preview constraints are acceptable. |

Agentic retrieval needs **knowledge sources**, a **knowledge base**, and a **retrieve action**. The knowledge base is the queryable layer; the underlying Search service still performs retrieval. Microsoft recommends considering agentic retrieval for new RAG implementations, while classic RAG remains suitable where its simplicity or generally available features matter. Check current feature status before production use. [RAG overview](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview), [agentic retrieval quickstart](https://learn.microsoft.com/en-us/azure/search/search-get-started-agentic-retrieval)

## 4. Learn the SDK boundaries

The current Python Foundry SDK is `azure-ai-projects` **2.x**. A project endpoint typically looks like:

```text
https://<resource>.services.ai.azure.com/api/projects/<project>
```

`AIProjectClient` manages project resources such as connections and agents. `project.get_openai_client()` supplies an OpenAI-compatible client for Responses calls. `azure-search-documents` is the separate SDK for managing and querying Azure AI Search directly. Microsoft Agent Framework is a higher-level option for agents defined in application code. [Foundry SDK overview](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview), [Search Python samples](https://learn.microsoft.com/en-us/azure/search/samples-python)

**Version trap:** older Foundry classic articles use `azure.ai.agents`, threads, messages, and runs. Do not mix that shape with the 2.x `create_version` and Responses example below.

## 5. Lab A: prepare a tiny evidence corpus

Create three short documents with overlapping vocabulary, for example remote work policy, equipment reimbursement, and office security. Give each a distinct title and URL. Add one question whose answer is **absent** from all three. If using private material, use only content you are authorized to upload.

In Azure AI Search, create an index or use a supported ingestion wizard. Verify that it includes:

- A stable key for each chunk.
- A retrievable text field holding the passage.
- Retrievable title and source URL fields for citations.
- A searchable vector field if using vector or hybrid retrieval.
- Filterable permission and version/date fields if your application requires them.

Run a Search query before involving the agent. For each test question, inspect the actual returned chunks and their source URLs. If the right passage is missing here, prompt changes alone will not fix the retrieval problem. The Foundry Search tool documentation lists the index and connection requirements. [Connect Search to agents](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search)

## 6. Lab B: connect Search to a Foundry agent

Prerequisites: a Foundry project and model deployment, an Azure AI Search service/index, a Foundry project connection to that Search service, suitable role assignments, Python 3.10+, and an Azure CLI login. Configure the connection and identity according to your environment. For keyless authentication, follow the role and managed-identity requirements in the [Search tool setup](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search).

```powershell
pip install "azure-ai-projects>=2.3.0" azure-identity
az login

$env:FOUNDRY_PROJECT_ENDPOINT = "https://<resource>.services.ai.azure.com/api/projects/<project>"
$env:FOUNDRY_MODEL = "<deployed-model-name>"
$env:SEARCH_CONNECTION = "<foundry-connection-name>"
$env:SEARCH_INDEX = "<index-name>"
```

Create the agent **once** as project configuration:

```python
# create_agent.py
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AISearchIndexResource,
    AzureAISearchQueryType,
    AzureAISearchTool,
    AzureAISearchToolResource,
    PromptAgentDefinition,
)

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
connection = project.connections.get(os.environ["SEARCH_CONNECTION"])

agent = project.agents.create_version(
    agent_name="policy-rag-agent",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL"],
        instructions=(
            "Use the connected Search index to answer. Cite the supporting sources. "
            "If the retrieved evidence does not support an answer, say so."
        ),
        tools=[
            AzureAISearchTool(
                azure_ai_search=AzureAISearchToolResource(
                    indexes=[
                        AISearchIndexResource(
                            project_connection_id=connection.id,
                            index_name=os.environ["SEARCH_INDEX"],
                            query_type=AzureAISearchQueryType.SIMPLE,
                        )
                    ]
                )
            )
        ],
    ),
    description="Answers questions using the policy index.",
)
print(agent.name, agent.version)
```

The documented `SIMPLE` query type is a useful first connection test. Once it works, compare the supported `vector_semantic_hybrid` mode on your evaluation questions; that mode requires the index's vector/semantic configuration. Do not assume changing the enum alone creates an effective vector pipeline. The Search tool can target one index per tool configuration. [Search tool parameters and example](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search)

Call the persisted agent from your application:

```python
# ask_agent.py
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

response = openai.responses.create(
    input="What equipment does the remote-work policy reimburse?",
    tool_choice="required",
    extra_body={
        "agent_reference": {
            "name": "policy-rag-agent",
            "type": "agent_reference",
        }
    },
)

print(response.output_text)
for item in response.output:
    if getattr(item, "type", None) == "message":
        for content in item.content:
            for annotation in getattr(content, "annotations", []) or []:
                if getattr(annotation, "type", None) == "url_citation":
                    print("Source:", annotation.url)
```

`agent_reference` selects the saved agent. `tool_choice="required"` forces tool use for the call. The response text is the answer; citation annotations are separate data worth preserving in your UI. In a production application, manage agent versions deliberately instead of creating a version for every question. This follows Microsoft's current [Python prompt-agent example](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search).

## 7. Lab C: test the whole RAG system

Make a ten-question set before tuning: five direct facts, two paraphrases, one question requiring two passages, one outdated-policy question, and one unanswerable question. Record the expected supporting source for each answer.

| Check | What to inspect | Failure tells you |
|---|---|---|
| Retrieval recall | Is the necessary passage among retrieved results? | Indexing, chunking, query, or permissions may be wrong. |
| Grounded answer | Does every factual claim follow from the returned passage? | Model may be extrapolating. |
| Citation accuracy | Does the cited URL open the specific supporting source? | Metadata or citation handling may be broken. |
| Abstention | Does the agent acknowledge the absent answer? | Instructions/evidence handling need work. |
| Access control | Can a restricted user retrieve a forbidden passage? | Stop and fix filtering/identity before rollout. |
| Latency and cost | How long and how many model/retrieval calls per answer? | Complexity may exceed the value of agentic retrieval. |

Change one variable at a time: chunk size, retrieval mode, ranking, top-k, then instructions. Keep the question set fixed so improvements are measurable. Never judge RAG quality from answer prose alone.

## 8. Exercises and mastery check

1. Explain why a perfectly written prompt cannot recover a document chunk that retrieval never returned.
2. Show which fields in your index are used for search, citation, freshness, and permissions.
3. Run the same five questions with simple and hybrid retrieval. Record retrieved chunks, answer accuracy, latency, and citations.
4. Ask an unanswerable question. Capture both the retrieval result and the agent's answer.
5. Explain when you would use a knowledge base/Foundry IQ instead of a direct Search tool.
6. Revoke a test user's access to one document and verify that it no longer appears in retrieval for that user.

**Ready to progress:** you can create a small index, call the agent from code, trace a cited answer back to source text, explain one failed retrieval, and demonstrate that permissions are enforced in retrieval.

## Official references

- [Microsoft Foundry SDKs and endpoints](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview)
- [Connect Azure AI Search to Foundry agents](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search)
- [RAG in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Agentic retrieval quickstart](https://learn.microsoft.com/en-us/azure/search/search-get-started-agentic-retrieval)
- [Foundry IQ FAQ](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/foundry-iq-faq)
- [Azure AI Search Python samples](https://learn.microsoft.com/en-us/azure/search/samples-python)
