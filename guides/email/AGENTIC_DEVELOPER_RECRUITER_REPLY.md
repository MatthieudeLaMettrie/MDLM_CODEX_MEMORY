# AI Agentic Developer recruiter reply — draft

Prepared 2026-10-07. Replace the PDP and NSW rollout placeholders with the actual stage, audience and personal contribution before sending. The technical summary describes the documented implementation pattern; it does not establish that every step was implemented at each employer. The willingness statement is proposed first-person wording for the user's review.

---

Hi [Name],

Thanks for reviewing my profile. Happy to clarify both points and provide some technical detail.

**1. Agent delivery and my personal contribution**

At **Precision Data Partners**, I personally created the data agent for the newsletter workflow. The wider solution covered Fabric data preparation, semantic modelling and generating newsletter content for CRM use. My involvement included building the agent, alongside the solution design. **[Add the actual rollout stage and users; confirm which wider components you personally implemented.]**

At **NSW Government**, I developed copilots using Copilot Studio and Azure AI Foundry with Fabric and external data sources. **[Add the actual rollout stage, enterprise users and the specific components you personally built.]**

At **Metcash**, the Copilot Studio and Fabric Data Agent work was evaluation rather than a production deployment. Separately, I developed Python reporting automation using Synapse, including automated testing.

**2. Comfort with a hands-on developer role**

Yes, I'm comfortable with that. Although my background includes architecture and co-founder responsibilities, I've continued to build solutions myself, and I enjoy development, configuration, integration, testing and debugging.

I understand this role focuses on assigned development work within established patterns and under senior developers or architects. I'm comfortable with that structure, following the team's standards and incorporating feedback through code reviews. I'm applying with a clear understanding that the focus is hands-on delivery.

**Technical context**

For context, the reporting-agent implementation pattern is:

- **Data and semantic model:** prepare curated data and a Power BI semantic model with relationships, explicit DAX measures, date logic and business definitions. The model can be created in Fabric or authored in Power BI Desktop and published to the cloud. The report and agent query the hosted model; the report does not need to be rebuilt in Fabric.
- **Model preparation:** use descriptions and Prep for AI to clarify metrics and terminology. For semantic-model sources, calculation guidance belongs in the model because DAX generation uses that context rather than agent-level instructions. Verified answers can help guide common questions.
- **Fabric data agent:** attach the hosted model, select the relevant tables, configure source routing and answer presentation, test it directly, then publish it. This is separate from the outer agent built in Foundry or Copilot Studio.
- **Instructions and tool use:** define the domain, such as marketing and sales, and tell the outer agent to call the reporting tool for actual business figures, preserve the returned period/filters/units, clarify ambiguous questions and identify unavailable data. A persona prompt alone does not define a KPI calculation or provide data access.
- **Integration:** connect the published Fabric data agent through the applicable Fabric IQ catalog/MCP tool in Foundry or Copilot Studio. Fabric IQ provides broader business context across data, semantic models and optional ontologies; an ontology is not required for a semantic-model reporting agent.
- **Testing:** inspect generated DAX and tool traces, reconcile answers against existing reports using identical measures and filters, and test ambiguous questions, missing data, zero comparison values and restricted users. Measured changes should be distinguished from unsupported causal explanations.
- **Security and prerequisites:** configure consumer identity, model access and row-level security, and check capacity, region, tenant AI settings and licensing. For data-agent semantic-model queries, consumers need model Read permission. Test as ordinary consumers, since workspace administrator/member/contributor access can bypass Power BI RLS.
- **Production delivery:** publish/share the Fabric agent in the production workspace. Users can consume it in Fabric or, through the documented direct integration, in the Microsoft 365 Copilot Agent Store. A Copilot Studio outer agent is published through supported channels such as Teams. A Foundry agent can serve a custom application through its stable endpoint or be published to Teams/Microsoft 365 Copilot. The current Foundry endpoint model differs from legacy Agent Application publishing.
- **Release and operation:** separate development/test/production configurations, verify production source bindings, refresh credentials and consumer permissions, version configurations through Git and use supported deployment pipelines. Pin tested Foundry versions for controlled releases; monitor failures, collect feedback and keep a recoverable release. Channel availability and preview limitations must be checked for the selected integration.

The guide also compares this pattern with **Looker LookML and Conversational Analytics in GCP**, **Snowflake semantic views with Cortex Analyst/Cortex Agents**, and **Databricks Unity Catalog semantics/metric views with Genie Agents**. These are functional comparisons, rather than claims of identical features or production experience across all platforms.

The architecture diagrams, step-by-step setup, instruction examples, testing and deployment options are documented in this [technical guide](https://github.com/MatthieudeLaMettrie/MDLM_CODEX_MEMORY/blob/main/guides/data-engineering/POWER_BI_SEMANTIC_MODEL_AGENTS_GUIDE.md).

Kind regards,
Matthieu
