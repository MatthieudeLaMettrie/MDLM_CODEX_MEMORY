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

## Changes

- Added `power-platform-copilot-studio/` (README plus files 01–06: admin and environments, Fabric and data agents, MCP/connectors/flows, AI engineer playbook, 14 practice checks with a lab, official doc index).
- Added the folder to README.md and MEMORY.md.

## Validation and limits

Pages were fetched and read; no tenant, Fabric, Foundry or Copilot Studio resource was created or tested, and the lab was not run. Connector authentication details, ALM and Evaluate/Monitor requirements are marked unverified. No environment IDs, tenant IDs or credentials were stored.

## Next steps

- User to re-enable the environment before about 2026-10-18 and confirm which tenant hosts it.
- Resolve the licensing conflict against Microsoft's current licensing guide.
- Decide with JB whether to use Foundry only or add Copilot Studio licences.
