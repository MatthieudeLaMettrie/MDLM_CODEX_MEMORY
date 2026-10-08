# Practice checks

Part of the [Power Platform / Copilot Studio guide](README.md). Fourteen original closed-book checks based on files 01–04. Answer first, then open the key.

## Questions

1. A developer environment shows State *Disabled* and History shows "Disable, initiated by SYSTEM". After how many days of inactivity does this happen, and how long do you have to re-enable it?
2. The *Trigger environment activity* button is missing on a disabled environment. Why, and what is the only option?
3. Name two actions that do not count as environment activity.
4. A user can build in Copilot Studio but cannot publish. What licence state explains this?
5. Can a B2B guest user of your tenant use Copilot Studio?
6. Why is Fabric absent from the Add knowledge dialog, and how is Fabric data reached instead?
7. List four prerequisites for a Fabric data agent used from Copilot Studio.
8. Which two authentication options can a connected Fabric data agent use in Copilot Studio, and what changes for permissions?
9. A Foundry agent uses the Fabric tool. Whose identity runs the query, and how many Fabric data agents can one Foundry agent hold?
10. Which values do you add as custom keys in the Foundry Fabric connection, and what do you tick?
11. Choose the OAuth 2.0 type: the server supports DCR but publishes no discovery metadata.
12. A data policy blocks a connector. What else is blocked?
13. The external-model toggle is visible but cannot be selected. What is missing?
14. Fabric is in tenant A and your Copilot Studio is in tenant B. Does a connected agent work? What is the practical fix?

## Answer key

1. 30 days of inactivity (60 for a managed developer environment). 15 days after disabling it is deleted; re-enable within that time.
2. The button only shows for active environments that are about to be cleaned up. For a disabled one, re-enabling is the only option.
3. Visiting the home page and opening the designer (also solution explorer).
4. A trial licence: trial users can build and test but cannot publish.
5. No. Guests cannot access Copilot Studio; use a member account.
6. Fabric is not a Copilot connector source. Use a Fabric data agent as a connected agent (Copilot Studio) or a Fabric tool (Foundry).
7. Any four of: F2+ or P1+ capacity; cross-geo AI settings; a supported data source with read access; published, described data agent; same tenant and account; read access to the data agent and sources; generative orchestration on.
8. User authentication (each user needs access to the data agent and data) and Agent author authentication (the author's identity is used for everyone).
9. The end user's identity (on-behalf-of). One Fabric data agent per Foundry agent.
10. `workspace-id` and `artifact-id`; tick **Is Secret**.
11. **Dynamic**: enter the Authorization URL and Token URL template.
12. MCP servers and tools that use that connector.
13. Anthropic access has not been allowed in the Microsoft 365 admin center (AI providers operating as Microsoft subprocessors).
14. No: same tenant and account are required. Build the agent in tenant A with a member account, or use a Foundry agent in tenant A.

## Hands-on lab (not run)

Needs a tenant with Fabric capacity and Copilot Studio or Foundry access.

1. Create a lakehouse with a three-row sales table (store A 100, store B 250, store C 50; total 400).
2. Create and publish a Fabric data agent over it, with a description naming the table and grain.
3. Add it to a Foundry agent (Route B in [02](02_FABRIC_AND_DATA_AGENTS.md)) and ask "What is total sales and which store is highest?". Expected: 400, store B.
4. Repeat as a user with no lakehouse access. Expected: no data returned.
5. Repeat in Copilot Studio with each authentication mode and record the difference.
