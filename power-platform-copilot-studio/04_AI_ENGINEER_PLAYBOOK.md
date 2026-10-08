# AI engineer playbook

Checked against Microsoft Learn on 2026-10-08. Part of the [Power Platform / Copilot Studio guide](README.md). Items marked **Unverified** come from product knowledge, not a fetched page.

## 1. Pick the platform

| Platform | Best for | Trade-off |
| --- | --- | --- |
| Copilot Studio | Low-code agents, Teams and Microsoft 365 channels, flows, connectors | Needs Copilot Studio licensing; Fabric data agent route validated only for Teams. |
| Foundry Agent Service | Code-first agents, model choice, evaluation and tracing | Azure consumption; you build the user channel. |
| Fabric data agent | Governed natural-language access to analytics data | Preview; it is a tool for the two above, not a chat product by itself. |

The three combine: Fabric data agent as the data layer, Foundry or Copilot Studio as the orchestrator.

## 2. Identity: who is the call made as?

This is the main security question. For every tool, write down the identity used.

| Tool | Identity |
| --- | --- |
| Fabric data agent from Foundry | End user (on-behalf-of). |
| Fabric data agent from Copilot Studio | Choice: **User authentication** or **Agent author authentication**. |
| API-key MCP server | The key the connection owner supplied. |
| OAuth MCP server | Each signed-in user. |
| Connector connection | Whoever created the connection, unless set per user. |

Agent author authentication lets users reach data they could not open themselves. Use it only when that is the intent.

## 3. Environment strategy (ALM)

1. **Dev** (developer or sandbox) → **Test** (sandbox) → **Prod** (production), each with its own connections.
2. Move agents and flows between environments as **solutions** (**Unverified** for current Copilot Studio export behaviour; check the solutions documentation).
3. Use environment groups and rules to apply the same DLP, external-model and Generative AI settings to a set of environments.
4. Use service principals for pipelines rather than personal accounts (**Unverified**: confirm per connector).
5. Keep a developer environment alive or accept that it will be disabled after 30 days of inactivity; do not build anything you cannot rebuild there.

## 4. Data governance

- DLP: which connectors and MCP servers are allowed.
- Cross-geo AI: Fabric tenant settings and the environment's **Move data across regions** setting. Neither is reversible for data already moved.
- External models: Anthropic is outside EU Data Boundary commitments (see [01](01_ADMIN_AND_ENVIRONMENTS.md)).
- Data access: Fabric workspace roles, warehouse permissions, row-level security, Dataverse security roles.
- Sharing: anyone given a shared agent needs access to the data agent and underlying sources.

## 5. Cost

Copilot Studio is capacity-based (Copilot Credits; the licensing page also mentions billed sessions). Use the [usage estimator](https://microsoft.github.io/copilot-studio-estimator/) with agent type, traffic, orchestration, knowledge and tools before agreeing a budget. Foundry is Azure consumption. Fabric needs a paid capacity (F2 or higher). Per-credit prices were not verified.

## 6. Quality

1. **Descriptions drive routing.** Rewrite tool, MCP server and connected-agent descriptions until the right tool is chosen in test.
2. Write a fixed question set with known answers (for example from a semantic model: "total net sales for week 40") and rerun after every change.
3. Test as a normal user, not as the author, to catch permission gaps.
4. Use Copilot Studio's **Evaluate** and **Monitor** tabs (they appeared greyed in the 2026-10-08 screenshots; requirements **unverified**) and Foundry evaluations and tracing.
5. Plan for model retirement: pin a tested model and track the [model lifecycle guidance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/plan-agent-model-lifecycle).

## 7. Failure modes seen in the docs or community

| Symptom | Likely cause |
| --- | --- |
| Data agent not in the picker | Unpublished, wrong account, different tenant or environment, no workspace access. |
| Connection returns to "Not connected" | Authentication or tenant mismatch (community report). |
| Answers differ per user | Row-level security or user authentication. |
| Tool never called | Weak description or generative orchestration off. |
| Environment vanished | Inactivity cleanup; recover within 7 days of deletion. |

## 8. JB readiness checklist

JB = Birrell & Co tenant with a paid Fabric capacity and a Foundry environment, no Copilot Studio licences.

- [ ] Confirm the target tenant for the agent (Fabric, Foundry and agent in one tenant).
- [ ] Fabric admin: data agent and cross-geo AI tenant settings on.
- [ ] Capacity F2 or higher assigned to the workspace.
- [ ] Data agent over the warehouse or semantic model: tested, described, published.
- [ ] Member account (not guest) for the builder in JB's tenant.
- [ ] Foundry: connection with workspace and artifact IDs; AI Developer role for users.
- [ ] Fabric: users have data agent and data access.
- [ ] Fixed test questions with known answers recorded.
- [ ] Decision on Copilot Studio licences only if Teams delivery is required.
- [ ] Written approval for a Metcash employee to build against JB data from a work laptop.
