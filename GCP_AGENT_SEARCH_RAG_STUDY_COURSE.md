# GCP Agent Search, Gemini, ADK, and RAG: study course

Checked against official Google documentation on 2026-09-28. Companion to the [Azure RAG course](AZURE_FOUNDRY_RAG_STUDY_COURSE.md). The code is a documented template and has not been run in your Google Cloud project.

## Outcome

Explain GCP's RAG components, create a searchable data store, ground Gemini on it, call an ADK agent using that data, and test citations, retrieval quality, permissions, latency, and cost.

## 1. Name the components

| Component | Job | Naming point |
|---|---|---|
| Agent Search | Managed enterprise search over website and document data. | Formerly Vertex AI Search. The console and APIs may still use older labels. |
| Discovery Engine API | API behind Agent Search data stores and search apps. | `discoveryengine.googleapis.com` remains in API paths. |
| Gemini on Google Cloud | Generates grounded answers. | A model is not itself the document index. |
| Google Gen AI SDK (`google-genai`) | Calls Gemini with a retrieval grounding tool. | Good for a direct grounded model call. |
| Agent Development Kit (`google-adk`) | Defines and runs agents with tools and sessions. | `VertexAiSearchTool` retains the old product name. |
| Vertex AI RAG Engine | A separate corpus-based RAG approach with more do-it-yourself control. | Do not confuse its corpus with an Agent Search data store. |

Google explicitly documents the Agent Search rebrand and says Discovery Engine API paths remain. [Agent Search overview](https://docs.cloud.google.com/generative-ai-app-builder/docs), [grounding choices](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search).

## 2. The two pipelines

```text
INDEXING: Cloud Storage / website / source -> parse -> chunks -> Agent Search data store
QUESTION: user -> ADK agent or Gemini -> data-store retrieval -> evidence -> cited answer
```

For the lab, use three small authorized policy documents with titles and source URLs. Include one document whose access should be restricted and one question that the corpus cannot answer. Confirm that each document is indexed before adding a model. Record how updates and deletions propagate. Agent Search provides managed parsing and search; for custom retrieval and corpus management, compare RAG Engine. [Agent Search overview](https://docs.cloud.google.com/generative-ai-app-builder/docs), [grounding with Agent Search](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search).

## 3. Choose the API path

| Path | Use it for | Core call |
|---|---|---|
| Gemini grounding with Agent Search | A single grounded model call. | `client.models.generate_content(..., tools=[retrieval_tool])` |
| ADK agent + Agent Search | An agent with instructions, tool use, sessions, and future workflow expansion. | `VertexAiSearchTool(...)` plus `InMemoryRunner.run_async(...)` |
| Direct Discovery Engine search | Retrieval debugging or custom RAG orchestration. | Search API against a serving configuration. |

Google Search grounding is for public web information. Use Agent Search grounding for your indexed enterprise documents. [Grounding with Google Search](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/ground-with-google-search), [Agent Search overview](https://docs.cloud.google.com/generative-ai-app-builder/docs).

## 4. Lab A: build and inspect the data store

1. In the Google Cloud console, enable the relevant APIs and create an **Agent Search** data store under AI Applications. Import the sample documents from Cloud Storage or another supported source.
2. Save its full path: `projects/<project>/locations/<location>/collections/default_collection/dataStores/<id>`.
3. Search for five known facts and two paraphrases. Inspect which document and passage appears before calling Gemini.
4. Add a new version of one document, refresh ingestion, and confirm the old statement is no longer retrieved.
5. If testing restricted content, set up the identity provider and create an access-controlled data store with ACL metadata from the start; the setting cannot be added to an existing data store. This capability is currently preview. Test with an identity that lacks access. Treat a returned restricted passage as a failure even if the final answer hides it.

Use [Create a search data store](https://docs.cloud.google.com/generative-ai-app-builder/docs/create-data-store-es) and [data source access control](https://docs.cloud.google.com/generative-ai-app-builder/docs/data-source-access-control) for the current console and permission steps.

## 5. Lab B: direct grounded Gemini call

Use Google Cloud credentials and a data store that has finished indexing. Follow the current [grounding Python example](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search); verify a supported model and location in your project.

```powershell
pip install --upgrade google-genai
gcloud auth application-default login

$env:GOOGLE_CLOUD_PROJECT = "<project-id>"
$env:GOOGLE_CLOUD_LOCATION = "global"
$env:GOOGLE_GENAI_USE_ENTERPRISE = "TRUE"
$env:AGENT_SEARCH_DATASTORE = "projects/<project-id>/locations/global/collections/default_collection/dataStores/<data-store-id>"
```

```python
import os

from google import genai
from google.genai.types import (
    GenerateContentConfig,
    HttpOptions,
    Retrieval,
    Tool,
    VertexAISearch,
)

client = genai.Client(http_options=HttpOptions(api_version="v1"))
search_tool = Tool(
    retrieval=Retrieval(
        vertex_ai_search=VertexAISearch(
            datastore=os.environ["AGENT_SEARCH_DATASTORE"]
        )
    )
)

response = client.models.generate_content(
    model="gemini-2.5-flash",  # Check current support in your region.
    contents="What equipment does our remote-work policy cover? Cite sources.",
    config=GenerateContentConfig(tools=[search_tool]),
)
print(response.text)
for candidate in response.candidates or []:
    print(candidate.grounding_metadata)
```

The grounding metadata holds supporting chunks and claim-to-source information when returned. Display and verify those references in an application; `response.text` alone is insufficient evidence. [Grounding with Agent Search](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search).

## 6. Lab C: call an ADK agent using RAG

ADK requires Google Cloud project authentication for this tool; a Google AI Studio API key alone is insufficient. Install `google-adk`, set the environment variables above, and run the code locally. The tool class deliberately retains `VertexAiSearchTool` as its Python name. [ADK grounding guide](https://adk.dev/grounding/grounding_with_search/).

```powershell
pip install --upgrade google-adk
```

```python
# ask_agent.py
import asyncio
import os

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import VertexAiSearchTool
from google.genai import types

root_agent = Agent(
    name="policy_rag_agent",
    model="gemini-flash-latest",  # Check model availability in your location.
    instruction=(
        "Answer policy questions using Agent Search. Cite supporting sources. "
        "If the documents do not support an answer, say so."
    ),
    tools=[
        VertexAiSearchTool(data_store_id=os.environ["AGENT_SEARCH_DATASTORE"])
    ],
)

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="policy_rag_lab")
    session = await runner.session_service.create_session(
        app_name="policy_rag_lab", user_id="learner"
    )
    async for event in runner.run_async(
        user_id="learner",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text="What equipment is reimbursed?")],
        ),
    ):
        if event.is_final_response() and event.content:
            print("".join(part.text or "" for part in event.content.parts))

if __name__ == "__main__":
    asyncio.run(main())
```

The runner calls the agent, which can invoke the retrieval tool. An in-memory session is suitable for learning; choose a persistent session store for a deployed application. Inspect full events and grounding metadata when validating citations. [ADK grounding guide](https://adk.dev/grounding/grounding_with_search/), [ADK runner pattern](https://adk.dev/plugins/).

## 7. Evaluation and mastery

Reuse one ten-question set from the Azure course: direct facts, paraphrases, a two-document question, a stale-document question, and an unanswerable question. For each question record the retrieved source, citation, factual support, response time, and whether permissions were enforced. Compare the direct Gemini call with the ADK agent. If the right document never appeared, diagnose ingestion or retrieval before changing instructions.

**Ready to progress:** you can identify the correct data store, call a grounded model and an ADK agent, trace an answer to its document, demonstrate one abstention, and show that a restricted document is not retrieved by an unauthorized identity.

## Official references

- [Agent Search overview and naming](https://docs.cloud.google.com/generative-ai-app-builder/docs)
- [Ground Gemini with Agent Search](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search)
- [ADK grounding with Search](https://adk.dev/grounding/grounding_with_search/)
- [ADK runner](https://adk.dev/plugins/)
