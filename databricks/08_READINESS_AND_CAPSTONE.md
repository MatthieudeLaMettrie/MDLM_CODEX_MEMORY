# 08 — Readiness, capstone and operating runbooks

[Learning path](README.md) · [Course](02_COURSE_COMPANION.md) · [Practice](07_TROUBLESHOOTING_PRACTICE.md)

Readiness here means you can build, explain, verify and recover a bounded data product. It is an authored practical rubric, not a certification passing score or employer acceptance policy. Reading completion, elapsed study days and prior credentials do not automatically establish current delivery readiness.

## 1. Score reasoning and evidence separately

For each workbook attempt, score six items 0–2:

| Item | 0 | 1 | 2 |
|---|---|---|---|
| Diagnosis | Guess unrelated to evidence | Plausible cause | Specific failing boundary and competing hypothesis |
| Investigation | No useful check | Broad log/schema check | Small check distinguishing explanations |
| Repair | Unsafe/arbitrary | Plausible but scope unclear | Minimal justified fix with bounded replay |
| Verification | Green status only | One data check | Keys, business values and retry behavior where relevant |
| Prevention | “Be careful” | Generic test/alert | Specific control and named owner |
| Uncertainty | Invented assumptions | Some unknowns | Exact missing contract/evidence with next action |

Maximum 12 per attempt. Use the result to target practice, not to declare a pass. A strong written answer still needs execution evidence for hands-on claims. Record initial/retest scores and remaining gaps in [progress.csv](progress.csv).

Practical progression: attempt the three diagnostics, implement the lab, then retest data/state/identity cases. If a failure category remains weak, reproduce one small development example and explain it to another engineer before broadening scope.

## 2. Capstone brief

**Deliver an operational-order data product into an Azure Databricks medallion architecture, with a reviewed plan for integrating an existing Synapse estate.** Use synthetic or approved masked data. The baseline lab is your starting point; extend it under a versioned contract rather than silently changing its expected results.

Choose one ingestion route: immutable ADLS files, a development operational database or a synthetic API. A real external source is optional; if you have no access, implement synthetic immutable deliveries and provide the source/network/identity design as a separately unexecuted proposal.

Required behavior:

- Bronze preserves source values, event/delivery identity and durable provenance.
- Silver applies explicit parsing/quality rules, quarantine, event deduplication, authoritative ordering and deletes.
- Gold has a declared grain and measure definition; late corrections, unknown references and deleted groups reconcile.
- Versioned bundle/configuration defines a task graph with intended environment/run identity and controlled concurrency.
- Required output checks gate publication. Monitoring includes source freshness/completeness, not only run success.
- A failed run can be recovered from retained input with stable business effects.
- A Synapse integration proposal names the actual engine, transfer direction, reader compatibility and publication boundary.

Do not promote the fixture notebook to production by removing `_dev` checks. Build generalized code/configuration with explicit allowed destinations and a reviewed release plan. The supplied full Gold overwrite is a deliberate simplification; explain or implement your chosen incremental/publication design.

## 3. Required evidence pack

| Deliverable | Acceptance evidence |
|---|---|
| Architecture | Data/control diagrams; named services, identities and owners |
| Source contract | Grain, keys, operation, sequence, timestamps, scope and retention |
| Schema/quality policy | Types, requiredness, domain rules, rejection reasons and schema evolution |
| Implementation | Versioned code, parameters, task graph and dependencies |
| Baseline result | Raw classification, unique candidates, state and Gold reconciliations |
| Changes/deletes | Before/after values and tombstone/history policy |
| Replay | Same input and stale replay preserve latest business state |
| Failure/recovery | Captured failure boundary, durable state, repair scope and verified result |
| Deployment | CLI/runtime/engine, resolved target, principal, resource ID and executed artifact version |
| Performance | Representative baseline/experiment, metrics, correctness parity and usage interpretation |
| Integration | Consumer engine, export/load contract and compatibility checks |
| Operating handoff | Runnable runbook, freshness/quality alerts, rollback limits and owners |

If a row has no actual execution, label it **designed / not executed**. If a check failed, retain the failure and repair evidence. A screenshot of a green job without its source scope and reconciled output is not sufficient.

## 4. Capstone failure and data test matrix

Run these in isolated development state:

| Input / failure | Expected contract behavior |
|---|---|
| Identical event re-delivery in same and different files | One business effect; raw delivery evidence retained according to policy |
| Two valid changes for one key in one batch | Correct ordered state; intermediate changes preserved if history required |
| Contradictory equal sequence | Explicit conflict outcome; no invented winner |
| Older upsert after a newer delete | Deleted state remains authoritative |
| Unknown dimension key | Agreed unknown/quarantine behavior, no accidental revenue loss |
| Invalid numeric/date/key | Rejection reason and raw evidence retained; valid+reject reconciles |
| Optional field and incompatible type change | Agreed evolution/review behavior; consumer contract maintained |
| Late correction moving date/store | Old and new Gold groups correct; empty old group removed |
| Failure after Bronze, after Silver, before publication | Retry completes required effects without duplicate/lost records |
| Source page/file missing | Completeness gate prevents false publication success |
| Permission denial under run identity | Correct failing boundary identified; repaired under intended principal |
| Source retention shorter than outage | Explicit re-bootstrap/reconciliation rather than silent offset skip |

For each drill, retain input, commit/config, run ID, before/after versions and reconciliation. Check logical results rather than expecting retries to preserve Delta version numbers: an idempotent business effect can still involve a new transaction/version.

## 5. Performance experiment at a meaningful scale

The baseline lab has 16 lines and cannot prove production speedups. Generate a larger deterministic synthetic dataset in a separate namespace. Set the scale to fit an agreed development cost budget and reveal the bottleneck; do not prescribe a universal million-row target.

Pick one problem: skewed joins, excessive small files, repeated expensive computation, source extraction concurrency or inefficient scans. Before changing anything, collect the input/compute/runtime, elapsed time, scan bytes, shuffle, spill, stage task spread, output file count/size and attributable usage where available. Record startup separately.

Form one hypothesis, change one factor and compare against equivalent conditions. Afterward verify key uniqueness, rejected records, active order count, day/store totals and deletion/correction behavior. Discuss why a speedup may not generalize and whether the change affects downstream table-feature compatibility or source-system load.

Submit a measured result or a clearly unexecuted experiment design. Do not claim Photon/clustering/broadcast “improves performance” for your workload without observation. Total operating cost can include source load, storage/network and publication beyond Databricks usage units.

## 6. Incident runbook template

```text
Incident / pipeline / impact / owner:
Current published release and source data-as-of:
First failing service/task and exact error:
Run/batch/correlation IDs and code/config/runtime:
Source scope/offset/file set and completeness:
Bronze/Silver/Gold versions or durable publication state:
Identity/path/network boundaries crossed:
Hypotheses and discriminating evidence:
Containment and affected business keys/periods:
Smallest repair and replay start/end:
Checks before publishing repaired output:
Checks after retry and stale replay:
Consumer notification/publication outcome:
Prevention control, owner and follow-up:
Remaining uncertainty:
```

Containment can mean stopping an overlapping trigger, withholding an unvalidated release or preserving the last complete consumer snapshot. It should not erase the evidence needed to recover. Share sanitized failures with the right owner rather than broadcasting credentials or raw sensitive records.

### Runbook A: failed merge

Capture source candidates and target version; classify duplicate/schema/constraint/concurrency/access failure. Check business key/sequence, target uniqueness and competing writer history. Apply a contract-based repair in bounded scope, rerun with required checks, then verify a retry has one logical effect. Assign recurrence prevention to source contract, candidate validation or writer coordination as appropriate.

### Runbook B: failed ingestion

Capture source delivery/manifest, last durable offset, landing state, query/checkpoint/schema paths and first error. Distinguish missing delivery, file discovery, parsing, state access and sink failure. Recover from retained complete input, preserve offsets/checkpoint unless a reviewed migration is required, and verify source completeness as well as current state.

### Runbook C: failed DAB/runtime deployment

Capture CLI/version/engine, invocation/target/host/root, included artifacts and planned resource changes. Separate deployer identity from job run identity. Confirm actual deployed asset and execution parameters. Repair the denied/incorrect boundary, run a bounded data check and verify the intended resource ID/consumer release.

### Runbook D: failed Synapse publication

Name serverless/dedicated/Spark/pipeline component. Capture pinned source version, export file set/manifest, storage/SQL identities, staging/load status and publication marker. Check Delta reader compatibility or Parquet export completeness. If a load already committed before acknowledgement failure, reuse/reconcile it rather than blindly appending. Publish only a validated complete release.

These runbook outlines guide investigation; they do not replace service-specific commands and your organization's ownership controls.

## 7. Collaboration and handoff review

Review the evidence pack with four roles:

| Role | Question they must answer |
|---|---|
| Source owner | Does extraction represent all required changes/deletes within retained scope? |
| Platform/security owner | Are identities, networks, storage and environment boundaries configured as intended? |
| Data engineer/reviewer | Does code preserve grain, ordering, replay and data correctness? |
| Consumer/BI owner | Are measures, attribution and publication/data-as-of fit for use? |

Do a recovery handoff: give another engineer your runbook and a simulated failed batch. They should determine what committed, which scope to rerun and how to verify the published result without guessing from conversation history.

## 8. Readiness gates and next exercises

You have demonstrated the course's practical baseline when you can independently:

1. Explain the platform and identity boundaries.
2. Implement the source contract and layer grain.
3. Reconcile the baseline, changes, deletes and unknown references.
4. Prove retries and stale replays preserve authoritative state.
5. Diagnose one incident in each requested family with evidence.
6. Deploy/run under the intended configuration and distinguish each validation stage.
7. Design or execute a compatible Synapse publication with explicit limits.
8. Present a measured optimization and a usable recovery handoff.

Any missing gate becomes the next small exercise. Maintain the distinction between written reasoning, offline fixture checks and real cloud execution. If later using this course for Data Engineer Professional exam preparation, map it to the current official blueprint and add uncovered objectives; do not assume this role-focused curriculum fully covers that exam.
