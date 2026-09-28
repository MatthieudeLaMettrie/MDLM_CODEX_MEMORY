# GCP and AWS RAG study courses

Date: 2026-09-28 (Australia/Sydney)

## Request and work

The user asked to add GCP and AWS equivalents of the Azure Foundry RAG study course. Reviewed repository instructions, memory, recent notes, and the Azure guide. Checked current official Google and AWS documentation. Added two standalone modules, linked them from README and MEMORY, and reused the Azure course's ten-question evaluation approach.

GCP course: documents Agent Search's rename from Vertex AI Search, the Discovery Engine API, Gemini grounding with `google-genai`, and a RAG-enabled ADK agent using `VertexAiSearchTool` and `InMemoryRunner`.

AWS course: distinguishes managed and customer-managed Bedrock Knowledge Bases, documents direct `RetrieveAndGenerate` for the customer-managed path, and explains a current Strands agent using an AgentCore Gateway managed-KB target. Bedrock Agents Classic is identified as unavailable to new customers.

## Validation and limits

Code shapes and product boundaries were checked against official documentation. The examples are templates with placeholders and have not been executed against cloud resources or real credentials. Before a live lab, verify model/region availability and IAM in the user's accounts. Check Markdown structure, links, and diff; commit and push the task files under standing repository authorization.
