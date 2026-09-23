# Readiness and a flexible preparation window

Your baseline is not yet assessed. Course completion and prior project work are useful experience, but neither is a measured readiness result. Start with workbook Cases 1–3 and record time, confidence and hints.

## Mark the reasoning, not only the fix

Score each dimension 0–2. This is a coaching rubric, not an exam scoring model.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Diagnosis | Incorrect or unsupported | Plausible but incomplete | Correct mechanism and relevant assumptions |
| Evidence | No meaningful evidence | Useful observation or check | Explains how evidence distinguishes competing causes |
| Repair | Incorrect or unrelated | Works narrowly with gaps | Appropriate, scoped repair addressing the cause |
| Verification | Only says “rerun” | Checks execution or a value | Checks intended output plus an important edge case/regression |

Record whether help was used. An 8/8 after seeing the solution is valuable learning but not evidence of independent readiness. A high-confidence wrong answer should be prioritized because it reveals a misconception you may otherwise overlook.

## How diagnostic results change the plan

| Observation | Next practice |
|---|---|
| Confuses resource identity and warehouse names | Sources/ref/alias variations, then a new compilation case |
| Recognizes bad data but not why a run succeeded | Small incremental fixtures and selection/matching/application reasoning |
| Assumes refs build every parent | Predict selection on several DAGs before running `dbt ls` |
| Offers broad rebuilds without evidence | Require a hypothesis and a smaller investigative command first |
| Finds the cause but cannot verify correctness | Design positive, negative and boundary fixtures |
| Performs well on all three | Move directly to mixed tests, governance, dependencies and state |

## Suggested 7–10 day sequence

Use the sequence rather than treating the dates as a deadline. A session might be 45–90 minutes, but your available time is still unknown. Shorten or extend the sequence based on the evidence.

| Day | Focus | Observable outcome |
|---|---|---|
| 1 | Diagnostic; inspect failed reasoning steps | Baseline scored without answers or documentation |
| 2 | Naming, config, parse/compile and Jinja | Explain two unfamiliar failures and propose confirming evidence |
| 3 | Materializations and incremental correctness | Predict results for first run, rerun, updates, late data and empty targets |
| 4 | Data tests, unit tests, freshness, snapshots | Choose the correct assertion and make a bad fixture fail it |
| 5 | Selection, state, deferral and CI | Predict both selected nodes and resolved relations |
| 6 | Governance, packages and job evidence | Diagnose interface/dependency failures and preserve reproducible settings |
| 7 | Fresh mixed readiness set; review reasoning | Identify remaining gaps across all seven official domains |
| 8–9 | Targeted repair of gaps and delayed retests | Solve variations independently, without remembering an answer |
| 10 | Second fresh timed set and decision | Decide whether to book, continue or narrow specific gaps |

Do not wait for day 7 to review a misconception from day 2. Revisit it after a delay, while spending most time on still-weak topics. Do not extend study merely to fill ten days if you demonstrate readiness earlier.

## Proposed readiness gate

Use two fresh mixed sets generated after the practice phase. They should include all official domains and contain questions you have not already studied. Aim for at least 80% on each, with no repeatedly weak domain and no reliance on hints. This gives a buffer above the official passing threshold, but it is not a validated probability of passing.

In addition, independently diagnose and verify fixes for at least one new problem in each area that was weak in the diagnostic. You should be able to explain why a tempting alternative is wrong, recognize version/adapter assumptions, and identify what evidence is missing in an ambiguous scenario.

Use [official sample questions and the current exam guide](https://www.getdbt.com/certifications/analytics-engineer-certification-exam) to calibrate format. The twenty workbook cases are deeper troubleshooting exercises, not a timed mock exam. Repeating them from memory does not count as an unseen set.

The official page currently lists 65 questions in 120 minutes: about 1 minute 51 seconds per question on average. Use that as a pacing reference for exam-style questions, not as a time limit for a hands-on debugging lab.

## What to send back to this task

For now, send answers to Cases 1–3, plus your warehouse/adapter, dbt Core or platform experience, and available study time per day. We will score the attempt, choose the next fault, and keep answers withheld until you attempt it or ask for help.

For later sessions, send the case number, your reasoning, elapsed time, confidence, and any error/query output. Keep the progress CSV as a record of attempts; leave scores blank until reviewed rather than giving yourself credit for merely reading a chapter.
