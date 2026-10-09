# Field log: JB newsletter agent (Foundry plus Fabric data agent)

Observed 2026-10-09 in the user's own Foundry project and Fabric workspace. Part of the [Power Platform / Copilot Studio guide](README.md). Results are from screenshots the user shared; nothing was executed by the assistant. **No tenant, subscription, workspace or item IDs are recorded here**, and business table names are deliberately omitted.

## Timeline

| Step | What happened | Lesson |
| --- | --- | --- |
| 1 | Fabric data agent over a warehouse was already published; its Model Context Protocol tab showed an MCP server URL and tool | Publishing creates an MCP server automatically |
| 2 | Foundry project and a prompt agent (version 1, Running) existed | New Foundry portal, prompt agent type |
| 3 | The Fabric tool was added with the **tenant ID in the Workspace ID field** | `ctid` in the URL is the tenant, not the workspace. Workspace ID is between `/groups/` and `/aiskills/`. |
| 4 | The data agent was then added as an **MCP tool** with the URL and no authentication | Playground returned `401 TokenIsMissing`. MCP needs a token supplied by a Fabric IQ connection or `user-entra-token` connection. |
| 5 | MCP tool removed; **Microsoft Fabric data agent** tool added with corrected IDs; agent reached version 7 | The agent answered, and its trace showed `fabric_dataagent_preview_call` |
| 6 | The model was `claude-opus-5-5` (Global Standard) | Fabric tool worked with a Claude model even though the docs' model table lists none |
| 7 | Memory panel: "not available in this project region" and "supported only for Azure OpenAI models" | See [10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md): region claim unresolved, model claim matches docs |

## What the working agent revealed

1. **It answered a "what data do you have" question from the data agent's own documentation**, not a live schema read ("the tool couldn't pull a live list of tables and columns"). The data agent's instructions and descriptions are therefore visible to anyone who can ask. Keep secrets and internal commentary out of them.
2. **The agent can see a broad set of tables**, including a combined contact table with personal details and contact-preference flags, CRM extracts and a clearly labelled test table. Restrict the sources the data agent selects, or add PII guardrails, before sharing the agent.
3. **Web search was enabled.** The reply mixed warehouse facts with an offer to search the web. For a data-grounded newsletter, remove web search or tell the agent to use it only when asked.
4. **Instructions were empty** during early tests. Add explicit tool guidance and a "no rows means say so" rule.
5. Answers carried numbered citation markers and a "Fabric Response for" line, which is useful for checking sources.

## Mistakes to avoid next time

- Using the data agent URL as a plain MCP tool without a connection that carries a token.
- Confusing `ctid` (tenant) with the workspace GUID.
- Treating a missing tool in the docs' model table as proof it will not work. Test, then record.
- Sharing the agent before checking what data it can surface.
- Assuming a project is in a given region from a resource-name suffix; confirm in the Azure portal.

## Open items

- Confirm the Foundry resource region (memory, tool and model availability).
- Decide model for memory (Azure OpenAI) versus Claude for reasoning; they cannot be combined in one agent for memory today per the portal message.
- Run an evaluation set against known warehouse answers ([11](11_FOUNDRY_GUARDRAILS_EVALUATION_FINETUNING.md)).
- Create a guardrail with tool call and tool response points and PII control.
- Narrow the data agent's sources.
- Resolve whether an unattended (scheduled) newsletter run can use the Fabric tool: service principals are not supported for the tool, while direct MCP clients may use them.
- Decide on publishing channels (Teams and Microsoft 365 Copilot appeared as an unpublished option; per-user Fabric access through that channel is unverified).
