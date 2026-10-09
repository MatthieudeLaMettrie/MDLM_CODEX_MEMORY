# Power Platform and Copilot Studio guide

Date: 2026-10-08 (Australia/Sydney)

## Requests

1. Why Fabric is not visible as a knowledge source in Copilot Studio; what JB's tenant needs; whether a Fabric data agent is required.
2. Explain MCP authentication methods, configuration types and the Connectors tools (Foundry Agent Service, Foundry Inference, AI Search), with examples; verify against current Microsoft docs.
3. A screenshot of a disabled developer environment: enable it or create a new one, plus a full guide on Power Platform admin and Microsoft 365 admin for Copilot Studio (agents, workflows, apps), agents on Fabric, Power BI semantic models and other databases, MCP, flows and AI-engineer knowledge.
4. Save the result in this repository in the SnowPro Gen AI format, using Microsoft Learn as needed.

## Findings (all from Microsoft Learn read 2026-10-08)

- Fabric is reached through a published Fabric data agent: connected agent in Copilot Studio, Fabric tool in Foundry. Same tenant and same account required. Preview. Copilot Studio route validated for Teams only and not supported in Microsoft 365 Copilot. Foundry route: one data agent per agent, end-user identity, `workspace-id` and `artifact-id` custom keys.
- MCP: None, API key (header or query), OAuth 2.0 (Dynamic discovery, Dynamic, Manual). Earlier chat answers were corrected: API keys are supplied per connection, and the "Dynamic" type needs Authorization URL and Token URL template.
- Correction to an earlier chat answer: Copilot Studio guests cannot access the product, so a B2B guest account in JB's tenant would not work; a member account is needed.
- The user's environment was disabled by the inactivity cleanup on 2026-10-03; developer environments are deleted 15 days after disabling.
- Unresolved licensing conflict between the Fabric page and the Copilot Studio page about builder licences.

5. (2026-10-09) Screenshot of the Agents list: what is the difference between the *GitHub Copilot* and *Standard* values in the Powered by column? Answered from the Microsoft Learn harness pages; added a Harnesses section to file 01 and the doc index. It is a runtime choice, not the GitHub Copilot coding product. The Fabric/MCP/licensing pages cited earlier describe the standard harness; behaviour on the GitHub Copilot harness is unverified. User's agents: FEI_AGENT and Power BI Support Assistant show GitHub Copilot, Test_Agent_PDP shows Standard.
6. (2026-10-09) Four screenshots of the user's Foundry project (`jb-newsletter`, prompt agent `jbnewsletteragentv1`, Foundry IQ Knowledge page, Fabric data agent MCP tab) and a request for step-by-step creation of a Foundry agent with the Fabric tool. Added file 07 from the current Foundry and Fabric docs. Findings: Fabric belongs in the agent's tools, not left-nav Knowledge (Foundry IQ is AI Search); the data agent is already published and exposes an MCP server; docs conflict on whether service principals work (Foundry page says no, Fabric MCP page says yes), so unattended runs are unverified; correct MCP audience for the data agent URL unverified; Teams/M365 publishing of the Fabric tool unverified. Nothing executed; no IDs recorded.
7. (2026-10-09) Corrected the user's Foundry tool (workspace ID field held the tenant ID from `ctid`); explained Foundry toolboxes; diagnosed a 401 TokenIsMissing from the Fabric data agent MCP URL added without authentication. Added a field note to file 07 with the three fixes and the resolved audience and service-principal question. No IDs recorded. Nothing executed.
8. (2026-10-09) Screenshot of the working Foundry agent plus the Foundry docs URL; request to capture every insight in the repo (same tenant, Fabric admin settings, services, use cases, tools with examples, knowledge and AI Search setup, memory and region, guardrails, evaluations, fine-tuning). Researched current Foundry, Fabric and AI Search docs and wrote files 08–12, updated README, doc index and MEMORY. Key observation: Fabric tool worked with a Claude model; memory panel said region not available and Azure OpenAI only. Fine-tuning detail is search-summary level. Nothing executed; no IDs or business table names stored.

## Changes

- Added `power-platform-copilot-studio/` (README plus files 01–06: admin and environments, Fabric and data agents, MCP/connectors/flows, AI engineer playbook, 14 practice checks with a lab, official doc index).
- Added the folder to README.md and MEMORY.md.

## Validation and limits

Pages were fetched and read; no tenant, Fabric, Foundry or Copilot Studio resource was created or tested, and the lab was not run. Connector authentication details, ALM and Evaluate/Monitor requirements are marked unverified. No environment IDs, tenant IDs or credentials were stored.

## Next steps

- User to re-enable the environment before about 2026-10-18 and confirm which tenant hosts it.
- Resolve the licensing conflict against Microsoft's current licensing guide.
- Decide with JB whether to use Foundry only or add Copilot Studio licences.
