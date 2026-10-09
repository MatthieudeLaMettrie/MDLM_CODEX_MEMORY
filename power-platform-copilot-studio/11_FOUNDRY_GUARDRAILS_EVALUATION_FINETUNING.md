# Foundry guardrails, evaluations and fine-tuning

Checked against Microsoft Learn on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Fine-tuning detail comes from search summaries only (pages not opened); it is flagged. Nothing was configured.

## Guardrails

Source: [Guardrails and controls overview](https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview). Agent guardrails are in **preview**.

A **guardrail** is a named collection of **controls**. Each control names a **risk**, the **intervention points** that scan for it, and a **response action**. Detection uses Azure AI Content Safety classification models.

### Intervention points

| Point | Models | Agents |
| --- | --- | --- |
| User input | Yes | Yes |
| Tool call (preview) | No | Yes |
| Tool response (preview) | No | Yes |
| Output | Yes | Yes |

Tool call and tool response matter for the JB build: what the Fabric tool returns to the agent can be scanned before the model uses it.

### Risks

| Risk | Models | Agents (preview) |
| --- | --- | --- |
| Hate, Sexual, Self-harm, Violence (severity Low, Medium, High) | Yes | Yes |
| User prompt attacks, Indirect attacks (prompt injection) | Yes | Yes |
| Protected material (text, code) | Yes | Yes |
| **Personally identifiable information** (preview) | Yes | Yes |
| Task Adherence (preview) | Yes | Yes |
| Spotlighting (preview), Groundedness (preview) | Yes | **No** |

### Actions, defaults and precedence

- Actions: **Annotate** (models only) or **Annotate and block** (models and agents).
- Models get **Microsoft.DefaultV2** by default. An agent uses its own assigned guardrail; if none, it inherits its model deployment's guardrail.
- **The agent's guardrail fully overrides the model's.** If it omits a control, that risk is not scanned for the agent.
- Turning severity to Off needs an approved Limited Access request.
- Applies to Foundry Models sold by Azure and agents built in Foundry Agent Service, not to other agents registered in the control plane. Hosted agents also support network egress controls (preview).
- Creating guardrails needs the **Foundry Account Owner** (or Owner) role.

### Where to use them

1. Create a guardrail in **Guardrails**, include tool call and tool response points, and assign it to the agent (Playground has a Guardrail section; a toolbox can also carry one, shown only if a filter covers tool points).
2. Add PII detection where tables hold personal data. The JB data agent can reach a contact table with names, emails, phones and do-not-contact flags; a PII control and a narrower data agent source list both reduce exposure.
3. Test blocked and borderline prompts. If valid content is blocked, lower severity or switch the control to annotate for models.
4. Combine with Microsoft Purview and Defender for Cloud for audit and threat detection (recommended by the architecture page).

## Evaluations

Source: [Run evaluations from the portal](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluate-generative-ai-app), [agent evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators).

Purpose: test quality, behaviour and safety **before** deployment and monitor after. Start from Evaluation, Create, or an agent's Evaluation tab, or Playground, Metrics, Run full evaluation.

**Prerequisites:** a project; an agent, model or dataset (CSV or JSONL) to test; an Azure OpenAI connection with a deployed judge model such as `gpt-4.1-mini` for AI-assisted evaluators; **Foundry User**.

### Choose the approach

| Target | Scope | Data | Use for |
| --- | --- | --- | --- |
| Agent | Full conversations (preview) | Simulated | Pre-deployment behaviour tests (recommended start) |
| Agent | Full conversations | Existing conversations | Production monitoring |
| Agent | Individual turns | Dataset, synthetic or traces | Debugging tool use |
| Model | Individual turns | Synthetic or dataset | Benchmark models |
| Dataset | Individual turns | Pre-computed outputs | Cheap bulk scoring |

### Evaluators

- **Agent:** Intent Resolution, Task Adherence, Tool Call Success, Tool Selection, Tool Output Utilization, Tool Input Accuracy, Tool Call Accuracy.
- **Quality:** Customer Satisfaction, Task Completion, Coherence, Groundedness, Response Completeness, Fluency, Relevance.
- **Safety:** Violence, Sexual, Self-harm, Hate and Unfairness.

Needed fields: turn level `query` and `response` (plus optional `context`, `ground_truth`, `tool_calls`, `tool_definitions`); conversation level `messages` and `tool_definitions`. Groundedness works without `context` when the response contains tool results.

**Continuous evaluation** scores live traffic: evaluation rules with sampling rates for prompt agents, scheduled runs for hosted agents. It shows "No runs" until traffic exists. Community reports say tool evaluators can fail when tool definitions are missing from traces.

### A starter set for the JB agent (not run)

1. Build 10 to 20 questions whose answers you computed directly in the warehouse (counts per month, latest-version rules, date ranges).
2. Add negative cases: questions outside the data, requests for contact details, prompt-injection attempts.
3. Run individual-turn evaluation with Tool Call Accuracy, Groundedness, Relevance, Task Adherence and the safety evaluators; compare to the known answers by hand.
4. Re-run after every instruction, tool or model change. Use the cheaper judge model to control cost; judge quota counts against Azure OpenAI quota.
5. Once live, schedule evaluation of existing conversations.

## Fine-tuning

Sources: [fine-tuning considerations](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/fine-tuning-considerations), [customize a model](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning). **Summary-level; verify models and regions on the current pages.**

| Method | Learns from | Best for |
| --- | --- | --- |
| **Supervised (SFT)** | Input and output examples | Style, format, domain specialisation. Start here. |
| **Direct preference optimisation (DPO)** | Preferred versus rejected response pairs | Quality, safety, alignment when you already have preference data |
| **Reinforcement (RFT)** | Reward signals | Objective domains with clear right answers and reasoning models |

- Typically hundreds to thousands of labelled examples; iterate and evaluate after each run.
- Support is per model (DPO listed for `gpt-4o`, `gpt-4.1`, `gpt-4.1-mini`; Llama 3.3 70B listed SFT only). I did not see Anthropic models in the fine-tuning results; the JB agent's Claude model is therefore probably not fine-tunable in Foundry (unverified).
- Regions: availability differs per model and deployment type (standard, data zone, global). Fine-tuned models can be evaluated on the Developer deployment type (24 hour life, no SLA, any region).
- **Order of effort:** prompt and instructions, then tools and knowledge, then evaluation, then fine-tune only if a measurable gap remains. For a data-grounded newsletter agent, fine-tuning is rarely the first lever.

## Observability pieces to use together

Traces tab (tool calls per answer), Monitor tab (usage and errors), Insights (preview), Optimize tab and the left-nav Optimize group, Application Insights for trace evaluation, plus resource and project metrics in Azure Monitor.
