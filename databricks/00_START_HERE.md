# 00 — Start here

[Learning path](README.md) · Next: [01 — Core study guide](01_CORE_STUDY_GUIDE.md)

## 1. Your outcome

You should be able to take a new operational source, explain its contract, ingest it without losing evidence, build trustworthy Silver and Gold datasets, deploy the code reproducibly and recover when a run fails. A successful job is only one part of that outcome: stale data, inflated totals and missing deletes can survive a green run.

The course assumes you already know basic SQL and Python. Your existing Databricks Data Engineer Associate background provides a starting point; it does not establish current debugging readiness. This course is focused on delivery and operations, with optional later mapping to a live certification blueprint. It adds no exam booking or deadline.

One running example follows order changes from a point-of-sale application. Orders can change, arrive late or be deleted. Revenue is calculated from the latest non-deleted order state, and unknown stores remain visible. This is a teaching model, not a claim about your employer's architecture or actual business measures.

## 2. Choose a route

| Route | Suggested effort, adjustable | Sequence |
|---|---|---|
| Refresher | 8–12 hours | Diagnostic → 01 → lab → cases covering gaps |
| Full practical course | 24–36 hours | 01–02 with lab; 04–06 as assigned; workbook and capstone |
| Incident-focused | 2–4 hours per topic | Find the matching workbook incident → investigate → read related deep dive → reproduce in development |
| Azure integration focus | 10–16 hours | Core contracts → 05 → bundle/job lessons → integration capstone |

These are planning estimates, not measured course durations. Progress depends on access and prior knowledge. If you have no workspace, complete the source contract, offline oracle, architecture and diagnostic exercises; record cloud execution as pending rather than claiming lab completion.

## 3. Prepare your learning environment

For the cloud lab, use a development workspace with Unity Catalog enabled and an existing **catalog whose name ends in `_dev`**, such as `training_dev`. The administrator must configure managed storage, give you appropriate object privileges, and provide compute supporting the lab's SQL functions and volumes. The exact SKU, region, runtime and compute policy are yours to record; none is inferred here.

Use supported compute with volume access. Databricks Runtime 15.4 LTS or a later supported runtime is the intended classic-compute baseline; record the exact version, because merge semantics differ in 16.0+. Serverless can be used interactively if supported, but the supplied bundle uses an existing classic cluster and must be adapted before choosing serverless. Do not copy a classic cluster configuration into a serverless task. [Volume requirements](https://learn.microsoft.com/en-us/azure/databricks/volumes/)

For local bundle work, install the current Databricks CLI through the official instructions, then pin the version your team validates. The sample explicitly selects the direct deployment engine. Authenticate interactively using OAuth; CI/CD uses a configured workload identity/service principal. Keep credentials outside the repository. This course does not install a CLI, create credentials or modify grants on your behalf. [CLI authentication](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/authentication) · [Deployment engine](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/direct)

Start a lab evidence sheet with:

```text
Workspace alias / cloud / region:
Catalog and schemas:
Compute type / access mode / runtime:
CLI version / bundle engine:
Interactive identity / deployment identity / run_as identity:
Source path / checkpoint path, if streaming:
Git commit / input batch / target table versions:
Observed row counts / totals / rejected records:
```

Use aliases instead of publishing private workspace URLs or identifiable data. No passwords, tokens or source credentials belong in the sheet.

## 4. Initial diagnostic: attempt before reading explanations

Allow about 15 minutes. Answer **diagnosis → evidence → smallest appropriate fix → verification → confidence**. These are original exercises; detailed answers are intentionally absent.

**A. Merge ambiguity.** Target has one row for order 101. Today's source contains two updates for 101 at sequence 7 and 8. `MERGE ON order_id` with an unconditional update fails. A colleague proposes `dropDuplicates(["order_id"])`. What evidence do you inspect and what correctness rule must the fix express?

**B. Green ingestion, wrong totals.** Bronze received 10,000 rows, Silver has 9,700 valid records and 300 rejects. Joining Silver orders to a store dimension yields 11,200 rows. Gold revenue increased unexpectedly. Which two independent reconciliations help locate the error, and why does a successful write prove little?

**C. Deployment versus runtime.** `databricks bundle validate` and `bundle deploy` succeed. The job fails reading a volume, while the same notebook works interactively. Name the identities, permissions and resolved paths you would compare before changing code.

Continue with the matching cases in [07](07_TROUBLESHOOTING_PRACTICE.md), then return after completing the lab. Request a hint or solution after an attempt, or explicitly ask for answers.

## 5. Learn in an evidence loop

1. Predict the result before executing: grain, counts, totals and expected exceptions.
2. Run the smallest controlled example and capture its parameters and environment.
3. Explain any mismatch with evidence from data, plan or run history.
4. Apply a bounded repair and verify business correctness as well as job status.
5. Rerun the same input and introduce a stale update or failure.
6. Explain what prevents recurrence and who owns the control.

Use [progress.csv](progress.csv) for confidence and links to evidence. Confidence without a reproduced result remains a hypothesis. Move to [08](08_READINESS_AND_CAPSTONE.md) when you can demonstrate replay, deletion and recovery behavior without following a script line by line.
